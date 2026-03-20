"""
Code Executor — safe subprocess-based Python file runner.
Captures stdout, stderr, exit code, and execution time.
Supports timeout to prevent infinite loops.
"""
from __future__ import annotations
import sys
import os
import time
import subprocess
import tempfile
from pathlib import Path
from typing import Optional
from .models import ExecutionResult


def execute_file(file_path: str, source_code: Optional[str] = None,
                 timeout: float = 15.0) -> ExecutionResult:
    """
    Execute a Python file (or inline source_code) in a subprocess.
    Returns ExecutionResult with stdout, stderr, exit_code, timing.
    """
    tmp_file = None

    try:
        target_path = file_path

        # If source_code provided but file doesn't exist — write to a temp file
        if source_code and (not Path(file_path).exists() or file_path == "<string>"):
            tmp = tempfile.NamedTemporaryFile(
                suffix=".py", mode="w", encoding="utf-8",
                delete=False, prefix="pydebugai_"
            )
            tmp.write(source_code)
            tmp.flush()
            tmp.close()
            target_path = tmp.name
            tmp_file = target_path

        start = time.perf_counter()
        proc = subprocess.run(
            [sys.executable, target_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(Path(file_path).parent) if Path(file_path).exists() else None,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        return ExecutionResult(
            stdout=proc.stdout or "",
            stderr=proc.stderr or "",
            exit_code=proc.returncode,
            timed_out=False,
            execution_time_ms=round(elapsed_ms, 2),
            file_path=file_path,
        )

    except subprocess.TimeoutExpired:
        return ExecutionResult(
            stdout="",
            stderr=f"⏱ Execution timed out after {timeout:.0f} seconds. "
                   "Check for infinite loops or very slow operations.",
            exit_code=-1,
            timed_out=True,
            execution_time_ms=timeout * 1000,
            file_path=file_path,
        )
    except FileNotFoundError:
        return ExecutionResult(
            stdout="",
            stderr=f"❌ File not found: '{file_path}'",
            exit_code=-1,
            file_path=file_path,
        )
    except Exception as e:
        return ExecutionResult(
            stdout="",
            stderr=f"❌ Executor error: {e}",
            exit_code=-1,
            file_path=file_path,
        )
    finally:
        if tmp_file:
            try:
                os.unlink(tmp_file)
            except OSError:
                pass


def execute_snippet(code: str, timeout: float = 10.0) -> ExecutionResult:
    """Execute a Python code snippet string directly."""
    return execute_file("<string>", source_code=code, timeout=timeout)
