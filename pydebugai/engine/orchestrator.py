"""
Orchestrator — Master AI controller that combines all engines.
Pipeline: AST → Execute → TracebackParse → Rules → ML → Levenshtein → CodeBERT
Merges, deduplicates, and ranks all suggestions by confidence.
"""
from __future__ import annotations
import re
import logging
from typing import List, Optional
from ..models import (
    AnalysisResult, Diagnostic, Suggestion, ErrorCategory, Severity,
)
from .error_parser import parse_traceback, parse_syntax_error
from .ast_analyzer import ASTAnalyzer
from .rule_engine import RuleEngine
from .ml_classifier import MLClassifier
from .levenshtein_fixer import LevenshteinFixer
from .transformer_model import TransformerModel
from .self_learner import SelfLearner

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Master AI orchestration layer.
    Runs all sub-engines in sequence, then merges and ranks their outputs.
    """

    def __init__(self, enable_transformer: bool = False):
        """
        enable_transformer: if True, loads CodeBERT (requires torch/transformers).
        Disabled by default for fast startup; enable for deeper analysis.
        """
        self._ast = ASTAnalyzer()
        self._rules = RuleEngine()
        self._ml = MLClassifier()
        self._lev = LevenshteinFixer()
        self._transformer = TransformerModel(lazy=True) if enable_transformer else None
        self._learner = SelfLearner()

    # ─── Main entry points ────────────────────────────────────────────────────

    def analyze_file(self, file_path: str, execute: bool = True) -> AnalysisResult:
        """Full pipeline analysis of a Python file."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                source_code = f.read()
        except OSError as e:
            return AnalysisResult(
                file_path=file_path, source_code="",
                diagnostics=[Diagnostic(
                    line=0, col=0, end_line=0, end_col=0,
                    severity=Severity.ERROR, category=ErrorCategory.OS,
                    message=f"Cannot open file: {e}",
                )],
            )
        return self.analyze_code(source_code, file_path=file_path, execute=execute)

    def analyze_code(self, source_code: str, file_path: str = "<string>",
                     execute: bool = True) -> AnalysisResult:
        """Full pipeline analysis on source code string."""
        result = AnalysisResult(
            file_path=file_path, source_code=source_code,
        )

        # ── Step 1: AST static analysis (always) ──────────────────────────────
        static_diagnostics = self._ast.analyze(source_code, file_path)
        result.diagnostics.extend(static_diagnostics)

        # If syntax error → skip execution, generate suggestions from static
        has_syntax_error = any(
            d.category in (ErrorCategory.SYNTAX, ErrorCategory.INDENT)
            for d in static_diagnostics
            if d.severity == Severity.ERROR
        )

        # ── Step 2: Execute ────────────────────────────────────────────────────
        execution_result = None
        stderr_text = ""
        if execute and not has_syntax_error:
            from ..executor import execute_file
            execution_result = execute_file(file_path, source_code=source_code)
            result.execution_result = execution_result
            stderr_text = execution_result.stderr

        # ── Step 3: Parse runtime traceback ────────────────────────────────────
        parsed_error = None
        if stderr_text:
            parsed_error = parse_traceback(stderr_text)
            if parsed_error:
                result.diagnostics.append(parsed_error.to_diagnostic())

        # ── Step 4: Generate suggestions from all engines ─────────────────────
        suggestions: List[Suggestion] = []

        # 4a. For each diagnostic, run rule engine + Levenshtein
        targets: List[tuple] = []
        if parsed_error:
            targets.append((parsed_error.category, parsed_error.message,
                            parsed_error.line_number, parsed_error.exception_type))
        for d in static_diagnostics:
            targets.append((d.category, d.message, d.line, d.category.value))

        for category, msg, line, exc_type in targets:
            # Rule engine
            rule_sugg = self._rules.suggest(msg, category, line=line)
            suggestions.extend(rule_sugg)

            # ML classifier enrichment
            ml_preds = self._ml.predict(msg)
            ml_boost = {cat: conf for cat, conf in ml_preds}
            for s in rule_sugg:
                cat_name = s.category.value
                if cat_name in ml_boost:
                    s.confidence = min(1.0, s.confidence + ml_boost[cat_name] * 0.1)

            # Levenshtein for name/attribute errors
            if category == ErrorCategory.NAME:
                name_match = re.search(r"name '(.+?)' is not defined", msg)
                if name_match:
                    lev_sugg = self._lev.suggest_for_name_error(
                        name_match.group(1), source_code, line=line
                    )
                    suggestions.extend(lev_sugg)

            elif category == ErrorCategory.ATTRIBUTE:
                attr_match = re.search(r"'(.+?)' object has no attribute '(.+?)'", msg)
                if attr_match:
                    lev_sugg = self._lev.suggest_for_attribute_error(
                        attr_match.group(1), attr_match.group(2), line=line
                    )
                    suggestions.extend(lev_sugg)

        # 4b. CodeBERT (if enabled and available)
        if self._transformer and parsed_error:
            ctx = self._get_context_lines(source_code, parsed_error.line_number)
            transformer_sugg = self._transformer.suggest(
                parsed_error.message, code_context=ctx,
                line=parsed_error.line_number,
            )
            suggestions.extend(transformer_sugg)

        # ── Step 5: For unknown errors — run rule engine across all categories ─
        if not suggestions and stderr_text:
            suggestions = self._rules.suggest_all_categories(stderr_text)

        # ── Step 6: Merge, deduplicate, and rank ──────────────────────────────
        result.suggestions = self._rank_suggestions(suggestions)

        # ── Step 7: Record interaction for self-learning ──────────────────────
        try:
            error_type = parsed_error.exception_type if parsed_error else "Static"
            error_msg = parsed_error.message if parsed_error else (
                static_diagnostics[0].message if static_diagnostics else ""
            )
            if error_msg:
                self._learner.record_interaction(
                    error_type=error_type,
                    error_msg=error_msg,
                    suggestions=[s.to_dict() for s in result.suggestions[:5]],
                    source_code=source_code[:1000],
                    file_path=file_path,
                )
        except Exception:
            pass

        return result

    # ─── Helpers ──────────────────────────────────────────────────────────────

    def _rank_suggestions(self, suggestions: List[Suggestion]) -> List[Suggestion]:
        """Deduplicate by title and sort by confidence descending."""
        seen: dict = {}
        for s in suggestions:
            key = s.title.lower().strip()
            if key not in seen or s.confidence > seen[key].confidence:
                seen[key] = s
        ranked = sorted(seen.values(), key=lambda x: x.confidence, reverse=True)
        return ranked[:10]  # top 10

    def _get_context_lines(self, source_code: str, line: int, window: int = 3) -> str:
        """Return a few lines of code around the error line."""
        lines = source_code.splitlines()
        start = max(0, line - window - 1)
        end = min(len(lines), line + window)
        return "\n".join(lines[start:end])

    def record_feedback(self, interaction_id: int, selected_idx: int,
                        feedback: int, error_type: str = "",
                        error_msg: str = "", category: str = ""):
        """Pass feedback through to self-learner."""
        self._learner.record_feedback(
            interaction_id, selected_idx, feedback,
            error_type, error_msg, category,
        )

    def get_stats(self) -> dict:
        return self._learner.get_stats()
