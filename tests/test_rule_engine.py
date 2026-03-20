"""
Tests for Rule Engine.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pydebugai.engine.rule_engine import RuleEngine
from pydebugai.models import ErrorCategory


def _engine():
    return RuleEngine()


def test_name_error_rule():
    e = _engine()
    results = e.suggest("name 'x' is not defined", ErrorCategory.NAME, line=5)
    assert len(results) > 0
    assert results[0].confidence > 0.7


def test_type_error_rule():
    e = _engine()
    results = e.suggest(
        "unsupported operand type(s) for +: 'int' and 'str'",
        ErrorCategory.TYPE, line=3,
    )
    assert len(results) > 0
    assert "type" in results[0].explanation.lower() or "convert" in results[0].explanation.lower()


def test_index_error_rule():
    e = _engine()
    results = e.suggest("list index out of range", ErrorCategory.INDEX, line=7)
    assert len(results) > 0
    assert results[0].fix_code is not None


def test_key_error_rule():
    e = _engine()
    results = e.suggest("KeyError: 'name'", ErrorCategory.KEY)
    assert len(results) > 0
    assert "get" in results[0].fix_code or "in" in results[0].fix_code


def test_import_error_rule():
    e = _engine()
    results = e.suggest("No module named 'numpy'", ErrorCategory.IMPORT)
    assert len(results) > 0
    assert "pip" in results[0].fix_code.lower()


def test_zero_div_rule():
    e = _engine()
    results = e.suggest("division by zero", ErrorCategory.ZERO_DIV)
    assert len(results) > 0
    assert results[0].confidence >= 0.90


def test_none_type_attribute():
    e = _engine()
    results = e.suggest("'NoneType' object has no attribute 'split'", ErrorCategory.ATTRIBUTE)
    assert len(results) > 0


def test_syntax_invalid():
    e = _engine()
    results = e.suggest("invalid syntax", ErrorCategory.SYNTAX)
    assert len(results) > 0


def test_recursion_error_rule():
    e = _engine()
    results = e.suggest("maximum recursion depth exceeded", ErrorCategory.RECURSION)
    assert len(results) > 0
    assert "base case" in results[0].explanation.lower() or "recursive" in results[0].explanation.lower()


def test_confidence_sorted():
    e = _engine()
    results = e.suggest("list index out of range", ErrorCategory.INDEX)
    if len(results) >= 2:
        assert results[0].confidence >= results[1].confidence


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {t.__name__}: {e}")
    print(f"\n{passed}/{len(tests)} tests passed")
