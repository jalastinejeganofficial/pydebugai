"""
Error Parser — extracts structured info from Python tracebacks.
Handles all standard Python exception types.
"""
from __future__ import annotations
import re
from typing import Optional, Tuple, List
from ..models import ErrorCategory, Severity, Diagnostic


# ─── Regex patterns for different traceback sections ──────────────────────────
_TRACEBACK_START = re.compile(r"^Traceback \(most recent call last\):", re.MULTILINE)
_FILE_LINE = re.compile(r'^\s+File "(.+?)", line (\d+), in (.+)$')
_EXCEPTION_LINE = re.compile(
    r'^([\w.]+(?:Error|Exception|Warning|Interrupt|Exit|Timeout|Overflow|'
    r'StopIteration|GeneratorExit|KeyboardInterrupt|SystemExit|Warning))\s*:\s*(.*)$'
)
_SYNTAX_CARET = re.compile(r'^\s*\^+\s*$')

# Map exception name strings → ErrorCategory
_CATEGORY_MAP: dict[str, ErrorCategory] = {
    "SyntaxError": ErrorCategory.SYNTAX,
    "IndentationError": ErrorCategory.INDENT,
    "TabError": ErrorCategory.INDENT,
    "NameError": ErrorCategory.NAME,
    "UnboundLocalError": ErrorCategory.NAME,
    "TypeError": ErrorCategory.TYPE,
    "ValueError": ErrorCategory.VALUE,
    "AttributeError": ErrorCategory.ATTRIBUTE,
    "IndexError": ErrorCategory.INDEX,
    "KeyError": ErrorCategory.KEY,
    "ImportError": ErrorCategory.IMPORT,
    "ModuleNotFoundError": ErrorCategory.IMPORT,
    "ZeroDivisionError": ErrorCategory.ZERO_DIV,
    "RecursionError": ErrorCategory.RECURSION,
    "MemoryError": ErrorCategory.MEMORY,
    "RuntimeError": ErrorCategory.RUNTIME,
    "OSError": ErrorCategory.OS,
    "FileNotFoundError": ErrorCategory.OS,
    "PermissionError": ErrorCategory.OS,
    "AssertionError": ErrorCategory.ASSERTION,
    "StopIteration": ErrorCategory.STOP_ITER,
    "UnicodeDecodeError": ErrorCategory.UNICODE,
    "UnicodeEncodeError": ErrorCategory.UNICODE,
    "UnicodeError": ErrorCategory.UNICODE,
    "OverflowError": ErrorCategory.OVERFLOW,
    "TimeoutError": ErrorCategory.TIMEOUT,
}


class ParsedError:
    """Structured representation of one Python exception."""

    def __init__(self):
        self.exception_type: str = "Unknown"
        self.message: str = ""
        self.file_path: str = ""
        self.line_number: int = 0
        self.col_offset: int = 0
        self.in_function: str = ""
        self.offending_line: str = ""
        self.category: ErrorCategory = ErrorCategory.UNKNOWN
        self.full_traceback: str = ""
        # For SyntaxError — python shows a caret (^) pointing to the column
        self.syntax_col: int = 0

    @property
    def severity(self) -> Severity:
        if self.category in (ErrorCategory.SYNTAX, ErrorCategory.INDENT):
            return Severity.ERROR
        return Severity.ERROR

    def to_diagnostic(self) -> Diagnostic:
        return Diagnostic(
            line=max(self.line_number, 1),
            col=max(self.col_offset, 0),
            end_line=max(self.line_number, 1),
            end_col=max(self.col_offset + 1, 1),
            severity=self.severity,
            category=self.category,
            message=f"{self.exception_type}: {self.message}",
            snippet=self.offending_line.strip(),
        )


def parse_traceback(traceback_text: str) -> Optional[ParsedError]:
    """
    Parse a Python traceback string and return a ParsedError.
    Returns None if no valid exception found.
    """
    if not traceback_text.strip():
        return None

    error = ParsedError()
    error.full_traceback = traceback_text

    lines = traceback_text.splitlines()

    # Collect all "File ..., line N, in func" frames
    frames: List[Tuple[str, int, str]] = []
    i = 0
    while i < len(lines):
        m = _FILE_LINE.match(lines[i])
        if m:
            file_path, lineno, func = m.group(1), int(m.group(2)), m.group(3)
            # The line after the File line is usually the offending code
            code_line = lines[i + 1].strip() if i + 1 < len(lines) else ""
            frames.append((file_path, lineno, func))
            if code_line and not _FILE_LINE.match(lines[i + 1] if i + 1 < len(lines) else ""):
                error.offending_line = code_line
        i += 1

    # Use the last (innermost) frame
    if frames:
        error.file_path, error.line_number, error.in_function = frames[-1]

    # Find the exception line (last non-empty line in format "ExceptionType: message")
    for line in reversed(lines):
        m = _EXCEPTION_LINE.match(line.strip())
        if m:
            error.exception_type = m.group(1)
            error.message = m.group(2).strip()
            error.category = _CATEGORY_MAP.get(error.exception_type, ErrorCategory.UNKNOWN)
            break

    # For SyntaxError — Python may print the file/line inside the message
    if error.category == ErrorCategory.SYNTAX and not error.line_number:
        syn_match = re.search(r'\("(.+?)", line (\d+)\)', traceback_text)
        if syn_match:
            error.file_path = syn_match.group(1)
            error.line_number = int(syn_match.group(2))

    # Try to find caret column for syntax errors
    for idx, line in enumerate(lines):
        if _SYNTAX_CARET.match(line):
            # Count leading spaces in the caret line to get col offset
            error.syntax_col = len(line) - len(line.lstrip())
            error.col_offset = error.syntax_col
            break

    if not error.exception_type or error.exception_type == "Unknown":
        return None

    return error


def parse_syntax_error(source_code: str) -> Optional[ParsedError]:
    """
    Try to compile source code and catch SyntaxError without executing it.
    Returns ParsedError if syntax error found, else None.
    """
    try:
        compile(source_code, "<string>", "exec")
        return None
    except SyntaxError as e:
        error = ParsedError()
        error.exception_type = "SyntaxError"
        error.message = str(e.msg)
        error.line_number = e.lineno or 0
        error.col_offset = e.offset or 0
        error.category = ErrorCategory.SYNTAX
        error.offending_line = e.text or ""
        return error
    except IndentationError as e:
        error = ParsedError()
        error.exception_type = "IndentationError"
        error.message = str(e.msg)
        error.line_number = e.lineno or 0
        error.col_offset = e.offset or 0
        error.category = ErrorCategory.INDENT
        error.offending_line = e.text or ""
        return error
