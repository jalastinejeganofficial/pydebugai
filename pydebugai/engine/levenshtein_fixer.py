"""
Levenshtein Fixer — Detects name/attribute typos and suggests the closest match.
Handles NameError and AttributeError using edit distance algorithms.
"""
from __future__ import annotations
import ast
import builtins
from typing import List, Optional, Set
from ..models import ErrorCategory, Suggestion

try:
    from Levenshtein import distance as _lev_distance
    _LEV_AVAILABLE = True
except ImportError:
    _LEV_AVAILABLE = False


def _simple_edit_distance(s1: str, s2: str) -> int:
    """Pure-Python Levenshtein distance fallback."""
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if s1[i - 1] == s2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp
    return dp[n]


def edit_distance(s1: str, s2: str) -> int:
    if _LEV_AVAILABLE:
        return _lev_distance(s1, s2)
    return _simple_edit_distance(s1, s2)


def _find_closest(target: str, candidates: Set[str],
                  max_dist: int = 3) -> List[tuple]:
    """
    Find candidates within edit distance `max_dist` of target.
    Returns list of (name, distance) sorted by distance.
    """
    if not target or not candidates:
        return []
    results = []
    for c in candidates:
        d = edit_distance(target.lower(), c.lower())
        if d <= max_dist:
            results.append((c, d))
    results.sort(key=lambda x: x[1])
    return results[:5]


_BUILTINS_SET: Set[str] = set(dir(builtins))

# Common library attribute misspellings
_COMMON_ATTRS: dict[str, list[str]] = {
    "list": ["append", "extend", "pop", "remove", "insert", "sort", "reverse",
             "clear", "copy", "count", "index"],
    "dict": ["get", "keys", "values", "items", "update", "pop", "setdefault",
             "clear", "copy", "fromkeys"],
    "str": ["join", "split", "strip", "replace", "find", "index", "format",
            "upper", "lower", "startswith", "endswith", "encode", "decode",
            "lstrip", "rstrip", "count", "center", "zfill", "removeprefix",
            "removesuffix"],
    "set": ["add", "remove", "discard", "union", "intersection",
            "difference", "issubset", "issuperset", "symmetric_difference"],
}


class LevenshteinFixer:
    """
    Suggests corrections for NameError and AttributeError using
    Levenshtein edit distance — detecting typos in variable/function names.
    """

    def suggest_for_name_error(self, wrong_name: str,
                               source_code: str,
                               line: Optional[int] = None) -> List[Suggestion]:
        """
        Given a NameError on `wrong_name`, extract all defined names from
        the source code + builtins and find close matches.
        """
        candidates = self._collect_source_names(source_code)
        candidates.update(_BUILTINS_SET)

        close = _find_closest(wrong_name, candidates)
        if not close:
            return []

        suggestions = []
        for candidate, dist in close:
            confidence = max(0.5, 1.0 - (dist * 0.2))
            suggestions.append(Suggestion(
                title=f"Did you mean '{candidate}'?",
                explanation=(
                    f"'{wrong_name}' is not defined, but '{candidate}' is a close match "
                    f"(edit distance: {dist}). You may have a typo."
                ),
                fix_code=f"# Replace '{wrong_name}' with '{candidate}'\n"
                         f"# {wrong_name} → {candidate}",
                line=line,
                confidence=confidence,
                source="levenshtein",
                category=ErrorCategory.NAME,
            ))
        return suggestions

    def suggest_for_attribute_error(self, obj_type: str, wrong_attr: str,
                                    line: Optional[int] = None) -> List[Suggestion]:
        """
        Given an AttributeError on `wrong_attr` for `obj_type`,
        find closest valid attributes for that type.
        """
        candidates: Set[str] = set()

        # Add known attributes for common types
        type_lower = obj_type.lower()
        for key, attrs in _COMMON_ATTRS.items():
            if key in type_lower:
                candidates.update(attrs)

        # Also try to get attrs from the actual type via eval (safe for builtins)
        try:
            real_type = __builtins__[obj_type] if isinstance(__builtins__, dict) else getattr(builtins, obj_type, None)
            if real_type:
                candidates.update(a for a in dir(real_type) if not a.startswith("__"))
        except Exception:
            pass

        close = _find_closest(wrong_attr, candidates)
        if not close:
            return []

        suggestions = []
        for candidate, dist in close:
            confidence = max(0.45, 1.0 - (dist * 0.22))
            suggestions.append(Suggestion(
                title=f"Did you mean '{obj_type}.{candidate}'?",
                explanation=(
                    f"'{obj_type}' has no attribute '{wrong_attr}', "
                    f"but '{candidate}' is a close match (edit distance: {dist})."
                ),
                fix_code=f"my_obj.{candidate}()  # '{wrong_attr}' → '{candidate}'",
                line=line,
                confidence=confidence,
                source="levenshtein",
                category=ErrorCategory.ATTRIBUTE,
            ))
        return suggestions

    def _collect_source_names(self, source_code: str) -> Set[str]:
        """Extract all defined names from source code via AST."""
        names: Set[str] = set()
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return names

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                names.add(node.id)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.add(node.name)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in node.names:
                    name = alias.asname or alias.name.split(".")[0]
                    names.add(name)
            elif isinstance(node, ast.arg):
                names.add(node.arg)
        return names
