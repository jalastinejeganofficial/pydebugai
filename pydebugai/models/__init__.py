"""
Data models for PyDebugAI — shared across all engine components.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    HINT = "hint"


class ErrorCategory(str, Enum):
    SYNTAX = "SyntaxError"
    NAME = "NameError"
    TYPE = "TypeError"
    VALUE = "ValueError"
    ATTRIBUTE = "AttributeError"
    INDEX = "IndexError"
    KEY = "KeyError"
    IMPORT = "ImportError"
    INDENT = "IndentationError"
    ZERO_DIV = "ZeroDivisionError"
    RECURSION = "RecursionError"
    MEMORY = "MemoryError"
    RUNTIME = "RuntimeError"
    OS = "OSError"
    ASSERTION = "AssertionError"
    STOP_ITER = "StopIteration"
    UNICODE = "UnicodeError"
    OVERFLOW = "OverflowError"
    TIMEOUT = "TimeoutError"
    UNKNOWN = "Unknown"


@dataclass
class Diagnostic:
    """Represents a single error/warning found in Python code."""
    line: int
    col: int
    end_line: int
    end_col: int
    severity: Severity
    category: ErrorCategory
    message: str
    source: str = "pydebugai"
    code: Optional[str] = None         # e.g. "E001"
    snippet: Optional[str] = None      # the offending source line


@dataclass
class Suggestion:
    """A fix suggestion for a diagnostic."""
    title: str
    explanation: str
    fix_code: Optional[str] = None       # exact fixed snippet
    fix_diff: Optional[str] = None       # unified diff string
    line: Optional[int] = None
    confidence: float = 0.0              # 0.0–1.0
    source: str = "rule_engine"          # which engine produced this
    category: ErrorCategory = ErrorCategory.UNKNOWN
    references: List[str] = field(default_factory=list)  # doc URLs

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "explanation": self.explanation,
            "fix_code": self.fix_code,
            "fix_diff": self.fix_diff,
            "line": self.line,
            "confidence": round(self.confidence, 3),
            "source": self.source,
            "category": self.category.value,
            "references": self.references,
        }


@dataclass
class ExecutionResult:
    """Result of running a Python file."""
    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool = False
    execution_time_ms: float = 0.0
    file_path: Optional[str] = None


@dataclass
class AnalysisResult:
    """Full analysis result returned to CLI and VSCode extension."""
    file_path: str
    source_code: str
    diagnostics: List[Diagnostic] = field(default_factory=list)
    suggestions: List[Suggestion] = field(default_factory=list)
    execution_result: Optional[ExecutionResult] = None
    static_only: bool = False           # True if no execution was done

    def top_suggestions(self, n: int = 5) -> List[Suggestion]:
        """Return top-N suggestions sorted by confidence."""
        return sorted(self.suggestions, key=lambda s: s.confidence, reverse=True)[:n]

    def has_errors(self) -> bool:
        return any(d.severity == Severity.ERROR for d in self.diagnostics)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "has_errors": self.has_errors(),
            "diagnostics": [
                {
                    "line": d.line,
                    "col": d.col,
                    "severity": d.severity.value,
                    "category": d.category.value,
                    "message": d.message,
                    "snippet": d.snippet,
                }
                for d in self.diagnostics
            ],
            "suggestions": [s.to_dict() for s in self.top_suggestions()],
            "execution": {
                "stdout": self.execution_result.stdout if self.execution_result else "",
                "stderr": self.execution_result.stderr if self.execution_result else "",
                "exit_code": self.execution_result.exit_code if self.execution_result else -1,
                "timed_out": self.execution_result.timed_out if self.execution_result else False,
                "execution_time_ms": self.execution_result.execution_time_ms if self.execution_result else 0,
            } if self.execution_result else None,
        }
