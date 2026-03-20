"""
AST Analyzer — static analysis of Python code using the `ast` module.
Catches errors BEFORE running: undefined names, bad imports, type hints, etc.
"""
from __future__ import annotations
import ast
import builtins
from typing import List, Set, Dict, Optional
from ..models import Diagnostic, Severity, ErrorCategory


_BUILTIN_NAMES: Set[str] = set(dir(builtins))

# Common stdlib module names (top 100 most used)
_STDLIB_MODULES = {
    "os", "sys", "re", "json", "math", "time", "datetime", "pathlib",
    "collections", "itertools", "functools", "typing", "io", "abc",
    "copy", "random", "string", "struct", "hashlib", "hmac", "base64",
    "urllib", "http", "socket", "ssl", "threading", "multiprocessing",
    "subprocess", "shutil", "glob", "fnmatch", "tempfile", "logging",
    "traceback", "inspect", "types", "gc", "weakref", "contextlib",
    "dataclasses", "enum", "warnings", "unittest", "pdb", "profile",
    "cProfile", "timeit", "pickle", "shelve", "sqlite3", "csv",
    "configparser", "argparse", "getopt", "optparse", "ast", "dis",
    "token", "tokenize", "keyword", "operator", "heapq", "bisect",
    "array", "queue", "asyncio", "concurrent", "signal", "platform",
    "uuid", "decimal", "fractions", "statistics", "textwrap", "pprint",
    "difflib", "filecmp", "zipfile", "tarfile", "gzip", "bz2", "lzma",
    "xml", "html", "email", "smtplib", "ftplib", "telnetlib",
}


class _ScopeAnalyzer(ast.NodeVisitor):
    """Walks AST and collects defined names per scope, flags undefined ones."""

    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.diagnostics: List[Diagnostic] = []
        self._scopes: List[Set[str]] = [set(_BUILTIN_NAMES)]
        self._imported: Set[str] = set()

    # ── scope helpers ──────────────────────────────────────────────────────────
    def _push_scope(self):
        self._scopes.append(set())

    def _pop_scope(self):
        if len(self._scopes) > 1:
            self._scopes.pop()

    def _define(self, name: str):
        self._scopes[-1].add(name)

    def _is_defined(self, name: str) -> bool:
        return any(name in scope for scope in reversed(self._scopes))

    def _add_diagnostic(self, node: ast.AST, category: ErrorCategory,
                        message: str, severity: Severity = Severity.ERROR):
        line = getattr(node, "lineno", 0)
        col = getattr(node, "col_offset", 0)
        snippet = self.source_lines[line - 1] if 0 < line <= len(self.source_lines) else ""
        self.diagnostics.append(Diagnostic(
            line=line, col=col, end_line=line,
            end_col=col + 1, severity=severity,
            category=category, message=message, snippet=snippet.rstrip(),
        ))

    # ── visitor methods ────────────────────────────────────────────────────────
    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name.split(".")[0]
            self._define(name)
            self._imported.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self._define(name)
            self._imported.add(name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._define(node.name)
        self._push_scope()
        # define arguments
        for arg in node.args.args + node.args.posonlyargs + node.args.kwonlyargs:
            self._define(arg.arg)
        if node.args.vararg:
            self._define(node.args.vararg.arg)
        if node.args.kwarg:
            self._define(node.args.kwarg.arg)
        self.generic_visit(node)
        self._pop_scope()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node: ast.ClassDef):
        self._define(node.name)
        self._push_scope()
        self.generic_visit(node)
        self._pop_scope()

    def visit_Assign(self, node: ast.Assign):
        self.generic_visit(node)
        for target in node.targets:
            self._collect_targets(target)

    def visit_AnnAssign(self, node: ast.AnnAssign):
        self.generic_visit(node)
        if node.target:
            self._collect_targets(node.target)

    def visit_For(self, node: ast.For):
        self._collect_targets(node.target)
        self.generic_visit(node)

    def visit_With(self, node: ast.With):
        for item in node.items:
            if item.optional_vars:
                self._collect_targets(item.optional_vars)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler):
        if node.name:
            self._define(node.name)
        self.generic_visit(node)

    def visit_Global(self, node: ast.Global):
        for name in node.names:
            self._define(name)

    def visit_Nonlocal(self, node: ast.Nonlocal):
        for name in node.names:
            self._define(name)

    def visit_ListComp(self, node: ast.ListComp):
        self._push_scope()
        self.generic_visit(node)
        self._pop_scope()

    visit_SetComp = visit_ListComp
    visit_DictComp = visit_ListComp
    visit_GeneratorExp = visit_ListComp

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            if not self._is_defined(node.id):
                self._add_diagnostic(
                    node, ErrorCategory.NAME,
                    f"Name '{node.id}' is used before it is defined",
                    Severity.WARNING,  # soft — might be defined at runtime
                )
        elif isinstance(node.ctx, (ast.Store, ast.Del)):
            self._define(node.id)

    def _collect_targets(self, target):
        """Recursively define names from assignment targets."""
        if isinstance(target, ast.Name):
            self._define(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for elt in target.elts:
                self._collect_targets(elt)
        elif isinstance(target, ast.Starred):
            self._collect_targets(target.value)


class _ComparisonChecker(ast.NodeVisitor):
    """Checks for common comparison mistakes: `is` vs `==`, etc."""

    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.diagnostics: List[Diagnostic] = []

    def visit_Compare(self, node: ast.Compare):
        for op, comparator in zip(node.ops, node.comparators):
            if isinstance(op, (ast.Is, ast.IsNot)):
                if isinstance(comparator, ast.Constant):
                    val = comparator.value
                    if isinstance(val, (int, str, float, bytes)) and val is not None:
                        line = node.lineno
                        snippet = self.source_lines[line - 1] if 0 < line <= len(self.source_lines) else ""
                        op_str = "is not" if isinstance(op, ast.IsNot) else "is"
                        self.diagnostics.append(Diagnostic(
                            line=line, col=node.col_offset,
                            end_line=line, end_col=node.col_offset + 10,
                            severity=Severity.WARNING,
                            category=ErrorCategory.TYPE,
                            message=f"Use `== {repr(val)}` instead of `{op_str} {repr(val)}` for value comparison",
                            snippet=snippet.rstrip(),
                        ))
        self.generic_visit(node)


class _DivisionByZeroChecker(ast.NodeVisitor):
    """Detects literal division-by-zero."""

    def __init__(self, source_lines: List[str]):
        self.source_lines = source_lines
        self.diagnostics: List[Diagnostic] = []

    def visit_BinOp(self, node: ast.BinOp):
        if isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
            if isinstance(node.right, ast.Constant) and node.right.value == 0:
                line = node.lineno
                snippet = self.source_lines[line - 1] if 0 < line <= len(self.source_lines) else ""
                self.diagnostics.append(Diagnostic(
                    line=line, col=node.col_offset,
                    end_line=line, end_col=node.col_offset + 5,
                    severity=Severity.ERROR,
                    category=ErrorCategory.ZERO_DIV,
                    message="Division by zero: the right operand is 0",
                    snippet=snippet.rstrip(),
                ))
        self.generic_visit(node)


class ASTAnalyzer:
    """
    Static code analyzer using Python's `ast` module.
    Detects potential errors without executing the code.
    """

    def analyze(self, source_code: str, file_path: str = "<string>") -> List[Diagnostic]:
        """
        Analyze Python source code and return a list of Diagnostics.
        Returns [] if source parses cleanly with no static issues found.
        """
        diagnostics: List[Diagnostic] = []
        source_lines = source_code.splitlines()

        # 1. Parse AST — catch SyntaxError first
        try:
            tree = ast.parse(source_code, filename=file_path)
        except SyntaxError as e:
            diagnostics.append(Diagnostic(
                line=e.lineno or 0, col=e.offset or 0,
                end_line=e.lineno or 0, end_col=(e.offset or 0) + 1,
                severity=Severity.ERROR, category=ErrorCategory.SYNTAX,
                message=f"SyntaxError: {e.msg}",
                snippet=(e.text or "").rstrip(),
            ))
            return diagnostics
        except IndentationError as e:
            diagnostics.append(Diagnostic(
                line=e.lineno or 0, col=e.offset or 0,
                end_line=e.lineno or 0, end_col=(e.offset or 0) + 1,
                severity=Severity.ERROR, category=ErrorCategory.INDENT,
                message=f"IndentationError: {e.msg}",
                snippet=(e.text or "").rstrip(),
            ))
            return diagnostics

        # 2. Scope / undefined name analysis
        scope_checker = _ScopeAnalyzer(source_lines)
        scope_checker.visit(tree)
        diagnostics.extend(scope_checker.diagnostics)

        # 3. Comparison style checks
        cmp_checker = _ComparisonChecker(source_lines)
        cmp_checker.visit(tree)
        diagnostics.extend(cmp_checker.diagnostics)

        # 4. Division by zero
        div_checker = _DivisionByZeroChecker(source_lines)
        div_checker.visit(tree)
        diagnostics.extend(div_checker.diagnostics)

        # Sort by line
        diagnostics.sort(key=lambda d: (d.line, d.col))
        return diagnostics
