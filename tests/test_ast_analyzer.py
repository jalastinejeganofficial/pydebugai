"""
Tests for AST Analyzer.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pydebugai.engine.ast_analyzer import ASTAnalyzer
from pydebugai.models import ErrorCategory, Severity


def test_syntax_error_detected():
    code = "def foo(\n    pass"
    a = ASTAnalyzer()
    diags = a.analyze(code)
    assert any(d.category == ErrorCategory.SYNTAX for d in diags)


def test_undefined_name_warning():
    code = "print(undefined_variable)"
    a = ASTAnalyzer()
    diags = a.analyze(code)
    assert any("undefined_variable" in d.message for d in diags)


def test_division_by_zero():
    code = "x = 10 / 0"
    a = ASTAnalyzer()
    diags = a.analyze(code)
    assert any(d.category == ErrorCategory.ZERO_DIV for d in diags)


def test_is_vs_equals_warning():
    code = "x = 5\nif x is 5:\n    pass"
    a = ASTAnalyzer()
    diags = a.analyze(code)
    assert any("==" in d.message for d in diags)


def test_clean_code_no_errors():
    code = "x = 10\nprint(x)"
    a = ASTAnalyzer()
    diags = a.analyze(code)
    # Should be clean — only maybe warnings, no fatal errors
    assert not any(d.severity == Severity.ERROR for d in diags)


def test_indentation_error():
    code = "if True:\npass"
    a = ASTAnalyzer()
    diags = a.analyze(code)
    assert any(d.category in (ErrorCategory.SYNTAX, ErrorCategory.INDENT) for d in diags)


def test_defined_before_use_ok():
    code = "x = 5\ny = x + 1\nprint(y)"
    a = ASTAnalyzer()
    diags = a.analyze(code)
    assert not any("x" in d.message and "not defined" in d.message for d in diags)


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
