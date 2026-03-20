"""
Tests for error_parser module.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pydebugai.engine.error_parser import parse_traceback, parse_syntax_error


def test_name_error():
    tb = """Traceback (most recent call last):
  File "test.py", line 3, in <module>
    print(x)
NameError: name 'x' is not defined"""
    err = parse_traceback(tb)
    assert err is not None
    assert err.exception_type == "NameError"
    assert "x" in err.message
    assert err.line_number == 3


def test_type_error():
    tb = """Traceback (most recent call last):
  File "test.py", line 5, in <module>
    result = 1 + "hello"
TypeError: unsupported operand type(s) for +: 'int' and 'str'"""
    err = parse_traceback(tb)
    assert err is not None
    assert err.exception_type == "TypeError"
    assert err.line_number == 5


def test_index_error():
    tb = """Traceback (most recent call last):
  File "test.py", line 2, in <module>
    print(lst[10])
IndexError: list index out of range"""
    err = parse_traceback(tb)
    assert err is not None
    assert err.exception_type == "IndexError"


def test_import_error():
    tb = """Traceback (most recent call last):
  File "test.py", line 1, in <module>
    import nonexistent_module
ModuleNotFoundError: No module named 'nonexistent_module'"""
    err = parse_traceback(tb)
    assert err is not None
    assert err.exception_type == "ModuleNotFoundError"


def test_syntax_error():
    code = "def foo(\n    pass"
    err = parse_syntax_error(code)
    assert err is not None
    assert err.exception_type == "SyntaxError"
    assert err.line_number > 0


def test_zero_division():
    tb = """Traceback (most recent call last):
  File "test.py", line 1, in <module>
    x = 1 / 0
ZeroDivisionError: division by zero"""
    err = parse_traceback(tb)
    assert err is not None
    assert err.exception_type == "ZeroDivisionError"


def test_attribute_error():
    tb = """Traceback (most recent call last):
  File "test.py", line 3, in <module>
    x = None
    x.split()
AttributeError: 'NoneType' object has no attribute 'split'"""
    err = parse_traceback(tb)
    assert err is not None
    assert err.exception_type == "AttributeError"


def test_key_error():
    tb = """Traceback (most recent call last):
  File "test.py", line 2, in <module>
    d['missing']
KeyError: 'missing'"""
    err = parse_traceback(tb)
    assert err is not None
    assert err.exception_type == "KeyError"


def test_empty_traceback():
    err = parse_traceback("")
    assert err is None


def test_value_error():
    tb = """Traceback (most recent call last):
  File "test.py", line 1, in <module>
    int('abc')
ValueError: invalid literal for int() with base 10: 'abc'"""
    err = parse_traceback(tb)
    assert err is not None
    assert err.exception_type == "ValueError"


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
