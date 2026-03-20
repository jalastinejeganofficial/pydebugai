"""
Self-Learner — SQLite-backed feedback learning system.
Records every (error, suggestion, user_feedback) interaction.
Periodically retrains ML classifier with accumulated positive/negative signals.
Implements an RLHF-lite reward loop.
"""
from __future__ import annotations
import sqlite3
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any

logger = logging.getLogger(__name__)

_PKG_DIR = Path(__file__).parent.parent
_DB_PATH = _PKG_DIR / "data" / "feedback.db"

# Retrain after this many new positive feedback entries
_RETRAIN_THRESHOLD = 25


class SelfLearner:
    """
    SQLite-backed self-learning system.
    Stores interactions, records feedback, and triggers ML retraining.
    """

    def __init__(self, db_path: Optional[Path] = None):
        self._db_path = db_path or _DB_PATH
        self._db_path.parent.mkdir(exist_ok=True, parents=True)
        self._conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        self._init_db()

    def _init_db(self):
        cur = self._conn.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS interactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ts          TEXT NOT NULL,
                error_type  TEXT NOT NULL,
                error_msg   TEXT NOT NULL,
                source_code TEXT,
                file_path   TEXT,
                suggestions TEXT NOT NULL,   -- JSON array
                selected_idx INTEGER,        -- which suggestion user picked
                feedback     INTEGER DEFAULT 0  -- +1 helpful / -1 not helpful / 0 neutral
            );

            CREATE TABLE IF NOT EXISTS positive_samples (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                ts          TEXT NOT NULL,
                error_message TEXT NOT NULL,
                category      TEXT NOT NULL,
                fix_code      TEXT,
                user_notes    TEXT
            );

            CREATE TABLE IF NOT EXISTS metrics (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                ts      TEXT NOT NULL,
                event   TEXT NOT NULL,   -- 'feedback', 'retrain', 'session'
                value   REAL DEFAULT 0.0,
                meta    TEXT            -- JSON
            );
        """)
        self._conn.commit()

    # ── Recording ─────────────────────────────────────────────────────────────

    def record_interaction(self, error_type: str, error_msg: str,
                           suggestions: List[Dict], source_code: str = "",
                           file_path: str = "") -> int:
        """Store an interaction. Returns the row ID."""
        cur = self._conn.cursor()
        cur.execute(
            """INSERT INTO interactions (ts, error_type, error_msg, source_code, file_path, suggestions)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (datetime.utcnow().isoformat(), error_type, error_msg,
             source_code[:2000], file_path, json.dumps(suggestions)),
        )
        self._conn.commit()
        return cur.lastrowid

    def record_feedback(self, interaction_id: int, selected_idx: int,
                        feedback: int, error_type: str = "",
                        error_msg: str = "", category: str = ""):
        """
        Record user feedback on a suggestion.
        feedback: +1 (helpful), -1 (not helpful), 0 (neutral)
        """
        cur = self._conn.cursor()
        cur.execute(
            """UPDATE interactions SET feedback=?, selected_idx=?
               WHERE id=?""",
            (feedback, selected_idx, interaction_id),
        )

        # Log metric
        cur.execute(
            """INSERT INTO metrics (ts, event, value, meta)
               VALUES (?, 'feedback', ?, ?)""",
            (datetime.utcnow().isoformat(), float(feedback),
             json.dumps({"interaction_id": interaction_id, "category": category})),
        )
        self._conn.commit()

        # If positive, add to training samples
        if feedback > 0 and error_msg and category:
            cur.execute(
                """INSERT INTO positive_samples (ts, error_message, category)
                   VALUES (?, ?, ?)""",
                (datetime.utcnow().isoformat(), error_msg, category),
            )
            self._conn.commit()
            self._maybe_retrain()

    def _maybe_retrain(self):
        """Trigger ML retraining if enough positive samples accumulated."""
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM positive_samples")
        count = cur.fetchone()[0]
        if count > 0 and count % _RETRAIN_THRESHOLD == 0:
            logger.info(f"Accumulated {count} positive samples — triggering ML retrain.")
            self._trigger_retrain()

    def _trigger_retrain(self):
        """Pull positive samples and kick off ML retrain."""
        try:
            from .ml_classifier import MLClassifier
            cur = self._conn.cursor()
            cur.execute("SELECT error_message, category FROM positive_samples")
            rows = cur.fetchall()
            extra = [{"error_message": r[0], "category": r[1]} for r in rows]
            clf = MLClassifier()
            clf.retrain(extra)
            # Log retrain event
            cur.execute(
                """INSERT INTO metrics (ts, event, value, meta) VALUES (?, 'retrain', ?, ?)""",
                (datetime.utcnow().isoformat(), float(len(extra)),
                 json.dumps({"sample_count": len(extra)})),
            )
            self._conn.commit()
        except Exception as e:
            logger.warning(f"Self-learner retrain error: {e}")

    # ── Analytics ─────────────────────────────────────────────────────────────

    def get_stats(self) -> Dict[str, Any]:
        cur = self._conn.cursor()
        cur.execute("SELECT COUNT(*) FROM interactions")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM interactions WHERE feedback=1")
        helpful = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM interactions WHERE feedback=-1")
        not_helpful = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM positive_samples")
        samples = cur.fetchone()[0]
        accuracy = (helpful / max(total, 1)) * 100
        return {
            "total_interactions": total,
            "helpful_feedback": helpful,
            "not_helpful_feedback": not_helpful,
            "positive_samples": samples,
            "estimated_accuracy": round(accuracy, 1),
        }

    def get_recent_errors(self, limit: int = 10) -> List[Dict]:
        cur = self._conn.cursor()
        cur.execute(
            """SELECT ts, error_type, error_msg, feedback
               FROM interactions ORDER BY id DESC LIMIT ?""",
            (limit,)
        )
        rows = cur.fetchall()
        return [{"ts": r[0], "error_type": r[1], "error_msg": r[2], "feedback": r[3]}
                for r in rows]

    def close(self):
        self._conn.close()
