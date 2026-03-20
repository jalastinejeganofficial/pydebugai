"""
FastAPI local HTTP server — bridges Python AI engine ↔ VSCode extension.
Runs on localhost:7432.
"""
from __future__ import annotations
import logging
from typing import Optional, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logger = logging.getLogger(__name__)

app = FastAPI(
    title="PyDebugAI Server",
    description="Local AI debugging server for Python — used by the VSCode extension",
    version="0.1.0",
)

# Allow requests from VSCode webview (localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lazy-loaded orchestrator (avoid slow startup)
_orchestrator = None

def get_orchestrator():
    global _orchestrator
    if _orchestrator is None:
        from .engine.orchestrator import Orchestrator
        _orchestrator = Orchestrator(enable_transformer=False)
    return _orchestrator


# ─── Request / Response models ────────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    code: Optional[str] = None           # inline code string
    file_path: Optional[str] = None      # path to .py file
    execute: bool = True                 # run the code?

class FeedbackRequest(BaseModel):
    interaction_id: int
    selected_idx: int
    feedback: int                        # +1, -1, or 0
    error_type: str = ""
    error_msg: str = ""
    category: str = ""


# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/status")
def status():
    """Health check endpoint."""
    return {"status": "ok", "version": "0.1.0", "engine": "PyDebugAI"}


@app.post("/analyze")
def analyze(req: AnalyzeRequest) -> Dict[str, Any]:
    """
    Analyze Python code or a file and return diagnostics + suggestions.
    """
    orc = get_orchestrator()

    if req.file_path:
        if not Path(req.file_path).exists():
            raise HTTPException(status_code=404, detail=f"File not found: {req.file_path}")
        result = orc.analyze_file(req.file_path, execute=req.execute)
    elif req.code:
        result = orc.analyze_code(req.code, file_path="<vscode>", execute=req.execute)
    else:
        raise HTTPException(status_code=400, detail="Provide 'code' or 'file_path'")

    return result.to_dict()


@app.post("/feedback")
def feedback(req: FeedbackRequest):
    """Record user feedback on a suggestion (thumbs up/down)."""
    orc = get_orchestrator()
    orc.record_feedback(
        interaction_id=req.interaction_id,
        selected_idx=req.selected_idx,
        feedback=req.feedback,
        error_type=req.error_type,
        error_msg=req.error_msg,
        category=req.category,
    )
    return {"status": "recorded"}


@app.get("/stats")
def stats():
    """Return self-learning statistics."""
    orc = get_orchestrator()
    return orc.get_stats()
