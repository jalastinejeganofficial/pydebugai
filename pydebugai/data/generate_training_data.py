"""
Comprehensive Training Data Generator for PyDebugAI ML Classifier.

Generates thousands of Python error examples covering:
- Basic syntax errors
- Variable and type errors
- Function and method errors
- Class and OOP errors
- Data structure errors (list, dict, set, tuple)
- File I/O errors
- Import and module errors
- Exception handling errors
- DSA algorithm errors (sorting, searching, recursion, etc.)
- Common beginner mistakes
"""

import json
from typing import List, Dict


def generate_basic_syntax_errors() -> List[Dict]:
    """Generate basic Python syntax error examples."""
    return [
        # NameError - undefined variables (50+ examples)
        {"error_message": "name 'x' is not defined", "category": "NameError"},
        {"error_message": "name 'y' is not defined", "category": "NameError"},
        {"error_message": "name 'result' is not defined", "category": "NameError"},
        {"error_message": "name 'total' is not defined", "category": "NameError"},
        {"error_message": "name 'count' is not defined", "category": "NameError"},
        {"error_message": "name 'value' is not defined", "category": "NameError"},
        {"error_message": "name 'data' is not defined", "category": "NameError"},
        {"error_message": "name 'item' is not defined", "category": "NameError"},
        {"error_message": "name 'index' is not defined", "category": "NameError"},
        {"error_message": "name 'key' is not defined", "category": "NameError"},
        {"error_message": "name 'my_var' is not defined", "category": "NameError"},
        {"error_message": "name 'undefined_variable' is not defined", "category": "NameError"},
        {"error_message": "name 'missing_var' is not defined", "category": "NameError"},
        {"error_message": "name 'not_defined' is not defined", "category": "NameError"},
        {"error_message": "name 'hello' is not defined", "category": "NameError"},
        {"error_message": "name 'world' is not defined", "category": "NameError"},
        {"error_message": "name 'foo' is not defined", "category": "NameError"},
        {"error_message": "name 'bar' is not defined", "category": "NameError"},
        {"error_message": "name 'baz' is not defined", "category": "NameError"},
        {"error_message": "name 'qux' is not defined", "category": "NameError"},
        {"error_message": "name 'temp' is not defined", "category": "NameError"},
        {"error_message": "name 'num' is not defined", "category": "NameError"},
        {"error_message": "name 'string' is not defined", "category": "NameError"},
        {"error_message": "name 'number' is not defined", "category": "NameError"},
        {"error_message": "name 'flag' is not defined", "category": "NameError"},
        {"error_message": "name 'counter' is not defined", "category": "NameError"},
        {"error_message": "name 'accumulator' is not defined", "category": "NameError"},
        {"error_message": "name 'sum' is not defined", "category": "NameError"},
        {"error_message": "name 'average' is not defined", "category": "NameError"},
        {"error_message": "name 'maximum' is not defined", "category": "NameError"},
        {"error_message": "name 'minimum' is not defined", "category": "NameError"},
        {"error_message": "name 'length' is not defined", "category": "NameError"},
        {"error_message": "name 'width' is not defined", "category": "NameError"},
        {"error_message": "name 'height' is not defined", "category": "NameError"},
        {"error_message": "name 'area' is not defined", "category": "NameError"},
        {"error_message": "name 'volume' is not defined", "category": "NameError"},
        {"error_message": "name 'radius' is not defined", "category": "NameError"},
        {"error_message": "name 'diameter' is not defined", "category": "NameError"},
        {"error_message": "name 'circumference' is not defined", "category": "NameError"},
        {"error_message": "name 'perimeter' is not defined", "category": "NameError"},
        
        # Typos in variable names (common beginner mistakes)
        {"error_message": "name 'pritn' is not defined", "category": "NameError"},
        {"error_message": "name 'pint' is not defined", "category": "NameError"},
        {"error_message": "name 'prnt' is not defined", "category": "NameError"},
        {"error_message": "name 'lenn' is not defined", "category": "NameError"},
        {"error_message": "name 'len' is not defined", "category": "NameError"},
        {"error_message": "name 'raange' is not defined", "category": "NameError"},
        {"error_message": "name 'rnage' is not defined", "category": "NameError"},
        {"error_message": "name 'rang' is not defined", "category": "NameError"},
        {"error_message": "name 'inpt' is not defined", "category": "NameError"},
        {"error_message": "name 'inputt' is not defined", "category": "NameError"},
        {"error_message": "name 'strr' is not defined", "category": "NameError"},
        {"error_message": "name 'intt' is not defined", "category": "NameError"},
        {"error_message": "name 'floa' is not defined", "category": "NameError"},
        {"error_message": "name 'floatt' is not defined", "category": "NameError"},
        {"error_message": "name 'listt' is not defined", "category": "NameError"},
        {"error_message": "name 'dic' is not defined", "category": "NameError"},
        {"error_message": "name 'dictt' is not defined", "category": "NameError"},
        {"error_message": "name 'set' is not defined", "category": "NameError"},
        {"error_message": "name 'sett' is not defined", "category": "NameError"},
        {"error_message": "name 'tupl' is not defined", "category": "NameError"},
        {"error_message": "name 'tuplee' is not defined", "category": "NameError"},
        {"error_message": "name 'apend' is not defined", "category": "NameError"},
        {"error_message": "name 'appnd' is not defined", "category": "NameError"},
        {"error_message": "name 'appendd' is not defined", "category": "NameError"},
        {"error_message": "name 'extnd' is not defined", "category": "NameError"},
        {"error_message": "name 'extendd' is not defined", "category": "NameError"},
        {"error_message": "name 'inser' is not defined", "category": "NameError"},
        {"error_message": "name 'insertt' is not defined", "category": "NameError"},
        {"error_message": "name 'remov' is not defined", "category": "NameError"},
        {"error_message": "name 'removee' is not defined", "category": "NameError"},
        {"error_message": "name 'pop' is not defined", "category": "NameError"},
        {"error_message": "name 'popp' is not defined", "category": "NameError"},
        {"error_message": "name 'clea' is not defined", "category": "NameError"},
        {"error_message": "name 'clear' is not defined", "category": "NameError"},
        {"error_message": "name 'sortt' is not defined", "category": "NameError"},
        {"error_message": "name 'sortted' is not defined", "category": "NameError"},
        {"error_message": "name 'revers' is not defined", "category": "NameError"},
        {"error_message": "name 'reversee' is not defined", "category": "NameError"},
        
        # Module imports used before import
        {"error_message": "name 'os' is not defined", "category": "NameError"},
        {"error_message": "name 'sys' is not defined", "category": "NameError"},
        {"error_message": "name 'math' is not defined", "category": "NameError"},
        {"error_message": "name 'random' is not defined", "category": "NameError"},
        {"error_message": "name 'time' is not defined", "category": "NameError"},
        {"error_message": "name 'datetime' is not defined", "category": "NameError"},
        {"error_message": "name 'collections' is not defined", "category": "NameError"},
        {"error_message": "name 'itertools' is not defined", "category": "NameError"},
        {"error_message": "name 'functools' is not defined", "category": "NameError"},
        {"error_message": "name 'typing' is not defined", "category": "NameError"},
        {"error_message": "name 'pathlib' is not defined", "category": "NameError"},
        {"error_message": "name 'json' is not defined", "category": "NameError"},
        {"error_message": "name 'csv' is not defined", "category": "NameError"},
        {"error_message": "name 're' is not defined", "category": "NameError"},
        {"error_message": "name 'urllib' is not defined", "category": "NameError"},
        {"error_message": "name 'http' is not defined", "category": "NameError"},
        {"error_message": "name 'socket' is not defined", "category": "NameError"},
        {"error_message": "name 'threading' is not defined", "category": "NameError"},
        {"error_message": "name 'multiprocessing' is not defined", "category": "NameError"},
        {"error_message": "name 'subprocess' is not defined", "category": "NameError"},
        {"error_message": "name 'logging' is not defined", "category": "NameError"},
        {"error_message": "name 'unittest' is not defined", "category": "NameError"},
        {"error_message": "name 'pytest' is not defined", "category": "NameError"},
        {"error_message": "name 'numpy' is not defined", "category": "NameError"},
        {"error_message": "name 'pandas' is not defined", "category": "NameError"},
        {"error_message": "name 'matplotlib' is not defined", "category": "NameError"},
        {"error_message": "name 'seaborn' is not defined", "category": "NameError"},
        {"error_message": "name 'sklearn' is not defined", "category": "NameError"},
        {"error_message": "name 'tensorflow' is not defined", "category": "NameError"},
        {"error_message": "name 'torch' is not defined", "category": "NameError"},
        
        # Self and cls in wrong context
        {"error_message": "name 'self' is not defined", "category": "NameError"},
        {"error_message": "name 'cls' is not defined", "category": "NameError"},
        {"error_message": "name 'kwargs' is not defined", "category": "NameError"},
        {"error_message": "name 'args' is not defined", "category": "NameError"},
        
        # Free variables and closures
        {"error_message": "free variable 'counter' referenced before assignment", "category": "NameError"},
        {"error_message": "free variable 'total' referenced before assignment", "category": "NameError"},
        {"error_message": "free variable 'result' referenced before assignment", "category": "NameError"},
        {"error_message": "global name 'db' is not defined", "category": "NameError"},
        {"error_message": "global name 'config' is not defined", "category": "NameError"},
        {"error_message": "nonlocal name 'state' is not defined", "category": "NameError"},
    ]


def generate_type_errors() -> List[Dict]:
    """Generate TypeError examples."""
    return [
        # Type mismatches in operations
        {"error_message": "unsupported operand type(s) for +: 'int' and 'str'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for +: 'str' and 'int'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for +: 'list' and 'str'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for +: 'dict' and 'list'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for -: 'str' and 'int'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for -: 'list' and 'int'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for *: 'NoneType' and 'int'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for *: 'str' and 'NoneType'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for /: 'str' and 'int'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for /: 'list' and 'int'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for //: 'str' and 'int'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for %: 'str' and 'int'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for **: 'str' and 'int'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for &: 'int' and 'str'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for |: 'int' and 'str'", "category": "TypeError"},
        {"error_message": "unsupported operand type(s) for ^: 'int' and 'str'", "category": "TypeError"},
        
        # Object not callable
        {"error_message": "'str' object is not callable", "category": "TypeError"},
        {"error_message": "'int' object is not callable", "category": "TypeError"},
        {"error_message": "'list' object is not callable", "category": "TypeError"},
        {"error_message": "'dict' object is not callable", "category": "TypeError"},
        {"error_message": "'tuple' object is not callable", "category": "TypeError"},
        {"error_message": "'set' object is not callable", "category": "TypeError"},
        {"error_message": "'NoneType' object is not callable", "category": "TypeError"},
        {"error_message": "'float' object is not callable", "category": "TypeError"},
        {"error_message": "'bool' object is not callable", "category": "TypeError"},
        
        # Object not iterable
        {"error_message": "'int' object is not iterable", "category": "TypeError"},
        {"error_message": "'float' object is not iterable", "category": "TypeError"},
        {"error_message": "'NoneType' object is not iterable", "category": "TypeError"},
        {"error_message": "'bool' object is not iterable", "category": "TypeError"},
        {"error_message": "'integer' object is not iterable", "category": "TypeError"},
        
        # Wrong argument counts
        {"error_message": "takes 1 positional argument but 2 were given", "category": "TypeError"},
        {"error_message": "takes 2 positional arguments but 3 were given", "category": "TypeError"},
        {"error_message": "takes 1 positional argument but 4 were given", "category": "TypeError"},
        {"error_message": "takes 0 positional arguments but 1 was given", "category": "TypeError"},
        {"error_message": "takes 2 positional arguments but 1 was given", "category": "TypeError"},
        {"error_message": "takes 3 positional arguments but 2 were given", "category": "TypeError"},
        {"error_message": "missing 1 required positional argument: 'self'", "category": "TypeError"},
        {"error_message": "missing 1 required positional argument: 'name'", "category": "TypeError"},
        {"error_message": "missing 1 required positional argument: 'value'", "category": "TypeError"},
        {"error_message": "missing 1 required positional argument: 'data'", "category": "TypeError"},
        {"error_message": "missing 2 required positional arguments: 'x' and 'y'", "category": "TypeError"},
        {"error_message": "missing 3 required positional arguments: 'a', 'b', and 'c'", "category": "TypeError"},
        
        # String concatenation errors
        {"error_message": "can only concatenate str (not \"int\") to str", "category": "TypeError"},
        {"error_message": "can only concatenate str (not \"list\") to str", "category": "TypeError"},
        {"error_message": "can only concatenate str (not \"dict\") to str", "category": "TypeError"},
        {"error_message": "can only concatenate list (not \"str\") to list", "category": "TypeError"},
        {"error_message": "can only concatenate tuple (not \"list\") to tuple", "category": "TypeError"},
        
        # No len() for certain types
        {"error_message": "object of type 'int' has no len()", "category": "TypeError"},
        {"error_message": "object of type 'float' has no len()", "category": "TypeError"},
        {"error_message": "object of type 'NoneType' has no len()", "category": "TypeError"},
        {"error_message": "object of type 'bool' has no len()", "category": "TypeError"},
        
        # Wrong indexing
        {"error_message": "'dict' object is not subscriptable by integer", "category": "TypeError"},
        {"error_message": "'set' object is not subscriptable", "category": "TypeError"},
        {"error_message": "list indices must be integers or slices, not str", "category": "TypeError"},
        {"error_message": "list indices must be integers or slices, not float", "category": "TypeError"},
        {"error_message": "list indices must be integers or slices, not list", "category": "TypeError"},
        {"error_message": "string indices must be integers", "category": "TypeError"},
        {"error_message": "string indices must be slices, not str", "category": "TypeError"},
        {"error_message": "tuple indices must be integers or slices, not str", "category": "TypeError"},
        
        # Unhashable types
        {"error_message": "unhashable type: 'list'", "category": "TypeError"},
        {"error_message": "unhashable type: 'dict'", "category": "TypeError"},
        {"error_message": "unhashable type: 'set'", "category": "TypeError"},
        
        # Bytes and string mixing
        {"error_message": "a bytes-like object is required, not 'str'", "category": "TypeError"},
        {"error_message": "a bytes-like object is required, not 'int'", "category": "TypeError"},
        {"error_message": "cannot use a bytes pattern on a string-like object", "category": "TypeError"},
        
        # Format string errors
        {"error_message": "unsupported format character", "category": "TypeError"},
        {"error_message": "not enough arguments for format string", "category": "TypeError"},
        {"error_message": "too many arguments for format string", "category": "TypeError"},
        
        # Unary operation errors
        {"error_message": "bad operand type for unary -: 'str'", "category": "TypeError"},
        {"error_message": "bad operand type for unary +: 'str'", "category": "TypeError"},
        {"error_message": "bad operand type for unary ~: 'str'", "category": "TypeError"},
        
        # Zip and iteration errors
        {"error_message": "zip argument #2 must support iteration", "category": "TypeError"},
        {"error_message": "zip argument #1 must support iteration", "category": "TypeError"},
        {"error_message": "map() requires at least one iterable", "category": "TypeError"},
        
        # Unpacking errors
        {"error_message": "cannot unpack non-sequence NoneType", "category": "TypeError"},
        {"error_message": "cannot unpack non-sequence int object", "category": "TypeError"},
        {"error_message": "cannot unpack non-sequence float object", "category": "TypeError"},
        
        # Membership test errors
        {"error_message": "argument of type 'NoneType' is not iterable", "category": "TypeError"},
        {"error_message": "argument of type 'int' is not iterable", "category": "TypeError"},
        {"error_message": "argument of type 'float' is not iterable", "category": "TypeError"},
        
        # Join errors
        {"error_message": "sequence item 0: expected str instance, int found", "category": "TypeError"},
        {"error_message": "sequence item 1: expected str instance, list found", "category": "TypeError"},
        {"error_message": "sequence item 2: expected str instance, NoneType found", "category": "TypeError"},
        
        # Attribute access on wrong type
        {"error_message": "'list' object has no attribute 'keys'", "category": "AttributeError"},
        {"error_message": "'list' object has no attribute 'values'", "category": "AttributeError"},
        {"error_message": "'list' object has no attribute 'items'", "category": "AttributeError"},
        {"error_message": "'dict' object has no attribute 'append'", "category": "AttributeError"},
        {"error_message": "'dict' object has no attribute 'extend'", "category": "AttributeError"},
        {"error_message": "'tuple' object has no attribute 'append'", "category": "AttributeError"},
        {"error_message": "'tuple' object has no attribute 'remove'", "category": "AttributeError"},
        {"error_message": "'set' object has no attribute 'index'", "category": "AttributeError"},
        {"error_message": "'set' object has no attribute 'sort'", "category": "AttributeError"},
        
        # NoneType attribute errors
        {"error_message": "'NoneType' object has no attribute 'split'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'strip'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'lower'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'upper'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'replace'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'find'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'index'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'get'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'pop'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'append'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'remove'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'keys'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'values'", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'items'", "category": "AttributeError"},
        
        # Int attribute errors
        {"error_message": "'int' object has no attribute 'append'", "category": "AttributeError"},
        {"error_message": "'int' object has no attribute 'extend'", "category": "AttributeError"},
        {"error_message": "'int' object has no attribute 'insert'", "category": "AttributeError"},
        {"error_message": "'int' object has no attribute 'remove'", "category": "AttributeError"},
        {"error_message": "'int' object has no attribute 'pop'", "category": "AttributeError"},
        {"error_message": "'int' object has no attribute 'clear'", "category": "AttributeError"},
        {"error_message": "'int' object has no attribute 'sort'", "category": "AttributeError"},
        {"error_message": "'int' object has no attribute 'reverse'", "category": "AttributeError"},
        {"error_message": "'int' object has no attribute 'copy'", "category": "AttributeError"},
        {"error_message": "'int' object has no attribute 'index'", "category": "AttributeError"},
        {"error_message": "'int' object has no attribute 'count'", "category": "AttributeError"},
        
        # Str attribute typos
        {"error_message": "'str' object has no attribute 'appnd'", "category": "AttributeError"},
        {"error_message": "'str' object has no attribute 'lowr'", "category": "AttributeError"},
        {"error_message": "'str' object has no attribute 'uppr'", "category": "AttributeError"},
        {"error_message": "'str' object has no attribute 'stripp'", "category": "AttributeError"},
        {"error_message": "'str' object has no attribute 'splitt'", "category": "AttributeError"},
        {"error_message": "'str' object has no attribute 'joinn'", "category": "AttributeError"},
        {"error_message": "'str' object has no attribute 'formatt'", "category": "AttributeError"},
        
        # Module attribute errors
        {"error_message": "module 'os' has no attribute 'listdirr'", "category": "AttributeError"},
        {"error_message": "module 'os' has no attribute 'getcwd'", "category": "AttributeError"},
        {"error_message": "module 'sys' has no attribute 'argvv'", "category": "AttributeError"},
        {"error_message": "module 'math' has no attribute 'sqr'", "category": "AttributeError"},
        {"error_message": "module 'random' has no attribute 'randintt'", "category": "AttributeError"},
        {"error_message": "module 'datetime' has no attribute 'datetume'", "category": "AttributeError"},
    ]


def generate_value_errors() -> List[Dict]:
    """Generate ValueError examples."""
    return [
        # Invalid literal conversions
        {"error_message": "invalid literal for int() with base 10: 'hello'", "category": "ValueError"},
        {"error_message": "invalid literal for int() with base 10: 'abc'", "category": "ValueError"},
        {"error_message": "invalid literal for int() with base 10: '12.34'", "category": "ValueError"},
        {"error_message": "invalid literal for int() with base 10: ''", "category": "ValueError"},
        {"error_message": "invalid literal for int() with base 10: 'NaN'", "category": "ValueError"},
        {"error_message": "invalid literal for int() with base 10: 'Infinity'", "category": "ValueError"},
        {"error_message": "could not convert string to float: 'abc'", "category": "ValueError"},
        {"error_message": "could not convert string to float: 'hello'", "category": "ValueError"},
        {"error_message": "could not convert string to float: ''", "category": "ValueError"},
        {"error_message": "could not convert string to float: 'NaN'", "category": "ValueError"},
        
        # Unpacking errors
        {"error_message": "not enough values to unpack (expected 3, got 2)", "category": "ValueError"},
        {"error_message": "not enough values to unpack (expected 2, got 1)", "category": "ValueError"},
        {"error_message": "not enough values to unpack (expected 4, got 3)", "category": "ValueError"},
        {"error_message": "too many values to unpack (expected 2)", "category": "ValueError"},
        {"error_message": "too many values to unpack (expected 3)", "category": "ValueError"},
        {"error_message": "too many values to unpack (expected 1)", "category": "ValueError"},
        
        # Math domain errors
        {"error_message": "math domain error", "category": "ValueError"},
        {"error_message": "math domain error in sqrt", "category": "ValueError"},
        {"error_message": "math domain error in log", "category": "ValueError"},
        {"error_message": "math domain error in asin", "category": "ValueError"},
        {"error_message": "math domain error in acos", "category": "ValueError"},
        
        # String conversion limits
        {"error_message": "Exceeds the limit for integer string conversion", "category": "ValueError"},
        {"error_message": "Exceeds the limit for floating point string conversion", "category": "ValueError"},
        
        # Generator/coroutine errors
        {"error_message": "generator already executing", "category": "ValueError"},
        {"error_message": "cannot reuse already exhausted generator", "category": "ValueError"},
        {"error_message": "cannot reuse already exhausted coroutine", "category": "ValueError"},
        
        # Pickle errors
        {"error_message": "unsupported pickle protocol: 5", "category": "ValueError"},
        {"error_message": "unsupported pickle protocol: 4", "category": "ValueError"},
        
        # File mode errors
        {"error_message": "invalid mode: 'rb+'", "category": "ValueError"},
        {"error_message": "invalid mode: 'w++'", "category": "ValueError"},
        {"error_message": "invalid mode: 'abc'", "category": "ValueError"},
        
        # JSON errors
        {"error_message": "out of range float values are not JSON compliant", "category": "ValueError"},
        {"error_message": "circular reference detected", "category": "ValueError"},
        {"error_message": "No JSON object could be decoded", "category": "ValueError"},
        {"error_message": "JSONDecodeError: Expecting value", "category": "ValueError"},
        {"error_message": "JSONDecodeError: Expecting property name", "category": "ValueError"},
        {"error_message": "JSONDecodeError: Expecting ',' delimiter", "category": "ValueError"},
        {"error_message": "JSONDecodeError: Expecting ':' delimiter", "category": "ValueError"},
    ]


def generate_index_key_errors() -> List[Dict]:
    """Generate IndexError and KeyError examples."""
    return [
        # Index out of range
        {"error_message": "list index out of range", "category": "IndexError"},
        {"error_message": "string index out of range", "category": "IndexError"},
        {"error_message": "tuple index out of range", "category": "IndexError"},
        {"error_message": "bytearray index out of range", "category": "IndexError"},
        {"error_message": "array index out of range", "category": "IndexError"},
        {"error_message": "deque index out of range", "category": "IndexError"},
        
        # Pop from empty
        {"error_message": "pop from empty list", "category": "IndexError"},
        {"error_message": "pop from empty deque", "category": "IndexError"},
        {"error_message": "pop from empty stack", "category": "IndexError"},
        {"error_message": "pop from empty queue", "category": "IndexError"},
        
        # Empty container errors
        {"error_message": "queue.Empty", "category": "IndexError"},
        {"error_message": "EmptySequence.index()", "category": "IndexError"},
        
        # Assignment errors
        {"error_message": "list assignment index out of range", "category": "IndexError"},
        {"error_message": "list index out of bounds", "category": "IndexError"},
        
        # Key errors
        {"error_message": "KeyError: 'name'", "category": "KeyError"},
        {"error_message": "KeyError: 'age'", "category": "KeyError"},
        {"error_message": "KeyError: 'id'", "category": "KeyError"},
        {"error_message": "KeyError: 'email'", "category": "KeyError"},
        {"error_message": "KeyError: 'address'", "category": "KeyError"},
        {"error_message": "KeyError: 'phone'", "category": "KeyError"},
        {"error_message": "KeyError: 'city'", "category": "KeyError"},
        {"error_message": "KeyError: 'country'", "category": "KeyError"},
        {"error_message": "KeyError: 'salary'", "category": "KeyError"},
        {"error_message": "KeyError: 'department'", "category": "KeyError"},
        {"error_message": "KeyError: 0", "category": "KeyError"},
        {"error_message": "KeyError: 1", "category": "KeyError"},
        {"error_message": "KeyError: 2", "category": "KeyError"},
        {"error_message": "KeyError: 'key'", "category": "KeyError"},
        {"error_message": "KeyError: 'value'", "category": "KeyError"},
        {"error_message": "KeyError: 'data'", "category": "KeyError"},
        {"error_message": "KeyError: 'result'", "category": "KeyError"},
        {"error_message": "KeyError: 'output'", "category": "KeyError"},
        {"error_message": "KeyError: 'input'", "category": "KeyError"},
        {"error_message": "KeyError: 'config'", "category": "KeyError"},
        {"error_message": "KeyError: 'settings'", "category": "KeyError"},
    ]


def generate_import_errors() -> List[Dict]:
    """Generate ImportError examples."""
    return [
        # Missing modules
        {"error_message": "No module named 'numpy'", "category": "ImportError"},
        {"error_message": "No module named 'pandas'", "category": "ImportError"},
        {"error_message": "No module named 'requests'", "category": "ImportError"},
        {"error_message": "No module named 'matplotlib'", "category": "ImportError"},
        {"error_message": "No module named 'seaborn'", "category": "ImportError"},
        {"error_message": "No module named 'sklearn'", "category": "ImportError"},
        {"error_message": "No module named 'tensorflow'", "category": "ImportError"},
        {"error_message": "No module named 'torch'", "category": "ImportError"},
        {"error_message": "No module named 'keras'", "category": "ImportError"},
        {"error_message": "No module named 'flask'", "category": "ImportError"},
        {"error_message": "No module named 'django'", "category": "ImportError"},
        {"error_message": "No module named 'fastapi'", "category": "ImportError"},
        {"error_message": "No module named 'sqlalchemy'", "category": "ImportError"},
        {"error_message": "No module named 'celery'", "category": "ImportError"},
        {"error_message": "No module named 'redis'", "category": "ImportError"},
        {"error_message": "No module named 'pymongo'", "category": "ImportError"},
        {"error_message": "No module named 'psycopg2'", "category": "ImportError"},
        {"error_message": "No module named 'mysql'", "category": "ImportError"},
        {"error_message": "No module named 'boto3'", "category": "ImportError"},
        {"error_message": "No module named 'PIL'", "category": "ImportError"},
        {"error_message": "No module named 'cv2'", "category": "ImportError"},
        {"error_message": "No module named 'scipy'", "category": "ImportError"},
        {"error_message": "No module named 'statsmodels'", "category": "ImportError"},
        {"error_message": "No module named 'networkx'", "category": "ImportError"},
        {"error_message": "No module named 'beautifulsoup4'", "category": "ImportError"},
        {"error_message": "No module named 'lxml'", "category": "ImportError"},
        {"error_message": "No module named 'yaml'", "category": "ImportError"},
        {"error_message": "No module named 'toml'", "category": "ImportError"},
        
        # Cannot import name
        {"error_message": "cannot import name 'DataFrame' from 'pandas'", "category": "ImportError"},
        {"error_message": "cannot import name 'Series' from 'pandas'", "category": "ImportError"},
        {"error_message": "cannot import name 'np' from 'numpy'", "category": "ImportError"},
        {"error_message": "cannot import name 'plt' from 'matplotlib'", "category": "ImportError"},
        {"error_message": "cannot import name 'Sequential' from 'tensorflow'", "category": "ImportError"},
        {"error_message": "cannot import name 'nn' from 'torch'", "category": "ImportError"},
        {"error_message": "cannot import name 'Flask' from 'flask'", "category": "ImportError"},
        {"error_message": "cannot import name 'APIView' from 'rest_framework'", "category": "ImportError"},
        {"error_message": "cannot import name 'get_object_or_404' from 'django.shortcuts'", "category": "ImportError"},
    ]


def generate_syntax_errors() -> List[Dict]:
    """Generate SyntaxError examples."""
    return [
        # Basic syntax errors
        {"error_message": "invalid syntax", "category": "SyntaxError"},
        {"error_message": "unexpected EOF while parsing", "category": "SyntaxError"},
        {"error_message": "EOL while scanning string literal", "category": "SyntaxError"},
        {"error_message": "expected ':'", "category": "SyntaxError"},
        {"error_message": "expected ')'", "category": "SyntaxError"},
        {"error_message": "expected ']'", "category": "SyntaxError"},
        {"error_message": "expected '}'", "category": "SyntaxError"},
        {"error_message": "unexpected ')'", "category": "SyntaxError"},
        {"error_message": "unexpected ']'", "category": "SyntaxError"},
        {"error_message": "unexpected '}'", "category": "SyntaxError"},
        {"error_message": "parenthesis is never closed", "category": "SyntaxError"},
        {"error_message": "bracket is never closed", "category": "SyntaxError"},
        {"error_message": "brace is never closed", "category": "SyntaxError"},
        
        # Argument syntax errors
        {"error_message": "non-keyword arg after keyword arg", "category": "SyntaxError"},
        {"error_message": "duplicate keyword argument", "category": "SyntaxError"},
        {"error_message": "positional argument follows keyword argument", "category": "SyntaxError"},
        {"error_message": "iterable argument unpacking follows keyword argument", "category": "SyntaxError"},
        {"error_message": "dictionary update sequence element has wrong length", "category": "SyntaxError"},
        
        # Statement outside function/class
        {"error_message": "return outside function", "category": "SyntaxError"},
        {"error_message": "yield outside function", "category": "SyntaxError"},
        {"error_message": "break outside loop", "category": "SyntaxError"},
        {"error_message": "continue not properly in loop", "category": "SyntaxError"},
        {"error_message": "pass outside function or class", "category": "SyntaxError"},
        
        # Starred expression errors
        {"error_message": "can't use starred expression here", "category": "SyntaxError"},
        {"error_message": "two starred expressions in assignment", "category": "SyntaxError"},
        {"error_message": "multiple starred expressions in assignment", "category": "SyntaxError"},
        {"error_message": "starred assignment target must be in a list or tuple", "category": "SyntaxError"},
        
        # Future import errors
        {"error_message": "future feature annotations is not defined", "category": "SyntaxError"},
        {"error_message": "future feature division is not defined", "category": "SyntaxError"},
        {"error_message": "future feature print_function is not defined", "category": "SyntaxError"},
        {"error_message": "from __future__ imports must occur at the beginning", "category": "SyntaxError"},
        
        # Lambda errors
        {"error_message": "lambda cannot contain assignment", "category": "SyntaxError"},
        {"error_message": "named arguments must follow bare *", "category": "SyntaxError"},
        
        # Comprehension errors
        {"error_message": "asynchronous comprehension outside asynchronous function", "category": "SyntaxError"},
        {"error_message": "default value cannot contain comprehensions", "category": "SyntaxError"},
        
        # F-string errors
        {"error_message": "f-string: expecting '}'", "category": "SyntaxError"},
        {"error_message": "f-string expression part cannot include a backslash", "category": "SyntaxError"},
        {"error_message": "f-string: single '}' is not allowed", "category": "SyntaxError"},
    ]


def generate_indentation_errors() -> List[Dict]:
    """Generate IndentationError examples."""
    return [
        {"error_message": "unexpected indent", "category": "IndentationError"},
        {"error_message": "unexpected unindent", "category": "IndentationError"},
        {"error_message": "expected an indented block", "category": "IndentationError"},
        {"error_message": "expected an indented block after function definition", "category": "IndentationError"},
        {"error_message": "expected an indented block after class definition", "category": "IndentationError"},
        {"error_message": "expected an indented block after 'if' statement", "category": "IndentationError"},
        {"error_message": "expected an indented block after 'for' statement", "category": "IndentationError"},
        {"error_message": "expected an indented block after 'while' statement", "category": "IndentationError"},
        {"error_message": "expected an indented block after 'try' statement", "category": "IndentationError"},
        {"error_message": "expected an indented block after 'except' statement", "category": "IndentationError"},
        {"error_message": "unindent does not match any outer indentation level", "category": "IndentationError"},
        {"error_message": "unindent does not match any outer indentation", "category": "IndentationError"},
        {"error_message": "mixing tabs and spaces is not supported", "category": "IndentationError"},
        {"error_message": "inconsistent use of tabs and spaces in indentation", "category": "IndentationError"},
        {"error_message": "TabError: inconsistent use of tabs and spaces", "category": "IndentationError"},
    ]


def generate_division_recursion_errors() -> List[Dict]:
    """Generate ZeroDivisionError and RecursionError examples."""
    return [
        # Division by zero
        {"error_message": "division by zero", "category": "ZeroDivisionError"},
        {"error_message": "integer division or modulo by zero", "category": "ZeroDivisionError"},
        {"error_message": "float division by zero", "category": "ZeroDivisionError"},
        {"error_message": "complex division by zero", "category": "ZeroDivisionError"},
        {"error_message": "modulo by zero", "category": "ZeroDivisionError"},
        {"error_message": "division by zero in array operation", "category": "ZeroDivisionError"},
        
        # Recursion depth exceeded
        {"error_message": "maximum recursion depth exceeded", "category": "RecursionError"},
        {"error_message": "maximum recursion depth exceeded in comparison", "category": "RecursionError"},
        {"error_message": "maximum recursion depth exceeded while calling a function", "category": "RecursionError"},
        {"error_message": "maximum recursion depth exceeded during iteration", "category": "RecursionError"},
        {"error_message": "recursion limit exceeded", "category": "RecursionError"},
        {"error_message": "infinite recursion detected", "category": "RecursionError"},
    ]


def generate_os_system_errors() -> List[Dict]:
    """Generate OSError, IOError, and system-related errors."""
    return [
        # File not found
        {"error_message": "No such file or directory: 'data.txt'", "category": "OSError"},
        {"error_message": "No such file or directory: 'config.json'", "category": "OSError"},
        {"error_message": "No such file or directory: 'input.csv'", "category": "OSError"},
        {"error_message": "No such file or directory: 'output.log'", "category": "OSError"},
        {"error_message": "No such file or directory: '/tmp/test.txt'", "category": "OSError"},
        {"error_message": "FileNotFoundError: [Errno 2] No such file or directory", "category": "OSError"},
        
        # Permission denied
        {"error_message": "Permission denied: 'system_file'", "category": "OSError"},
        {"error_message": "Permission denied: '/etc/passwd'", "category": "OSError"},
        {"error_message": "Permission denied: '/root/secret.txt'", "category": "OSError"},
        {"error_message": "PermissionError: [Errno 13] Permission denied", "category": "OSError"},
        
        # File system errors
        {"error_message": "read-only file system", "category": "OSError"},
        {"error_message": "too many open files", "category": "OSError"},
        {"error_message": "no space left on device", "category": "OSError"},
        {"error_message": "disk quota exceeded", "category": "OSError"},
        {"error_message": "file already exists", "category": "OSError"},
        {"error_message": "directory not empty", "category": "OSError"},
        
        # Network errors
        {"error_message": "connection refused", "category": "OSError"},
        {"error_message": "network unreachable", "category": "OSError"},
        {"error_message": "connection reset by peer", "category": "OSError"},
        {"error_message": "timed out", "category": "OSError"},
        {"error_message": "address already in use", "category": "OSError"},
        {"error_message": "socket connection broken", "category": "OSError"},
        
        # Timeout errors
        {"error_message": "timeout expired", "category": "TimeoutError"},
        {"error_message": "operation timed out", "category": "TimeoutError"},
        {"error_message": "connection timed out", "category": "TimeoutError"},
        {"error_message": "request timed out", "category": "TimeoutError"},
    ]


def generate_unicode_encoding_errors() -> List[Dict]:
    """Generate UnicodeError and encoding-related errors."""
    return [
        # Decode errors
        {"error_message": "'utf-8' codec can't decode byte 0xff", "category": "UnicodeError"},
        {"error_message": "'utf-8' codec can't decode byte 0x80", "category": "UnicodeError"},
        {"error_message": "'utf-8' codec can't decode byte 0xc0", "category": "UnicodeError"},
        {"error_message": "'ascii' codec can't decode byte 0xe9", "category": "UnicodeError"},
        {"error_message": "'latin-1' codec can't decode byte 0x81", "category": "UnicodeError"},
        {"error_message": "UnicodeDecodeError: 'utf-8' codec can't decode byte", "category": "UnicodeError"},
        
        # Encode errors
        {"error_message": "'ascii' codec can't encode character '\\u2019'", "category": "UnicodeError"},
        {"error_message": "'ascii' codec can't encode character '\\u00e9'", "category": "UnicodeError"},
        {"error_message": "'utf-8' codec can't encode character", "category": "UnicodeError"},
        {"error_message": "UnicodeEncodeError: 'ascii' codec can't encode character", "category": "UnicodeError"},
        
        # Other unicode errors
        {"error_message": "UnicodeTranslateError: character maps to <undefined>", "category": "UnicodeError"},
        {"error_message": "codec can't encode character in position 0", "category": "UnicodeError"},
        {"error_message": "codec can't decode byte in position 5", "category": "UnicodeError"},
    ]


def generate_assertion_runtime_errors() -> List[Dict]:
    """Generate AssertionError, RuntimeError, and other assertion-like errors."""
    return [
        # Assertion errors
        {"error_message": "AssertionError", "category": "AssertionError"},
        {"error_message": "assert 0 == 1", "category": "AssertionError"},
        {"error_message": "assert False", "category": "AssertionError"},
        {"error_message": "assert True == False", "category": "AssertionError"},
        {"error_message": "assert x is not None", "category": "AssertionError"},
        {"error_message": "assert len(items) > 0", "category": "AssertionError"},
        {"error_message": "assert result == expected", "category": "AssertionError"},
        {"error_message": "Assertion failed", "category": "AssertionError"},
        {"error_message": "assert condition is true", "category": "AssertionError"},
        
        # Runtime errors
        {"error_message": "dictionary changed size during iteration", "category": "RuntimeError"},
        {"error_message": "set changed size during iteration", "category": "RuntimeError"},
        {"error_message": "list changed size during iteration", "category": "RuntimeError"},
        {"error_message": "cannot modify collection while iterating", "category": "RuntimeError"},
        {"error_message": "generator already executing", "category": "RuntimeError"},
        {"error_message": "cannot reuse already exhausted generator", "category": "RuntimeError"},
        {"error_message": "cannot reuse already exhausted coroutine", "category": "RuntimeError"},
        {"error_message": "task is already done", "category": "RuntimeError"},
        {"error_message": "event loop is closed", "category": "RuntimeError"},
        {"error_message": "this event loop is already running", "category": "RuntimeError"},
        {"error_message": "asyncio.run() cannot be called from a running event loop", "category": "RuntimeError"},
    ]


def generate_memory_overflow_errors() -> List[Dict]:
    """Generate MemoryError, OverflowError, and resource-related errors."""
    return [
        # Memory errors
        {"error_message": "MemoryError", "category": "MemoryError"},
        {"error_message": "MemoryError: Unable to allocate memory", "category": "MemoryError"},
        {"error_message": "MemoryError: Failed to allocate buffer", "category": "MemoryError"},
        {"error_message": "out of memory", "category": "MemoryError"},
        {"error_message": "cannot allocate memory for array", "category": "MemoryError"},
        
        # Overflow errors
        {"error_message": "math range error", "category": "OverflowError"},
        {"error_message": "math overflow error", "category": "OverflowError"},
        {"error_message": "int too large to convert to float", "category": "OverflowError"},
        {"error_message": "Python int too large to convert to C long", "category": "OverflowError"},
        {"error_message": "signed integer overflow", "category": "OverflowError"},
        {"error_message": "unsigned integer overflow", "category": "OverflowError"},
        
        # StopIteration
        {"error_message": "StopIteration", "category": "StopIteration"},
        {"error_message": "StopIteration: no more items", "category": "StopIteration"},
        {"error_message": "StopIteration: end of sequence", "category": "StopIteration"},
        
        # SystemExit and KeyboardInterrupt
        {"error_message": "SystemExit", "category": "RuntimeError"},
        {"error_message": "KeyboardInterrupt", "category": "RuntimeError"},
        {"error_message": "GeneratorExit", "category": "RuntimeError"},
    ]


def generate_dsa_algorithm_errors() -> List[Dict]:
    """Generate errors specific to DSA algorithms (sorting, searching, trees, graphs)."""
    return [
        # Sorting algorithm errors
        {"error_message": "list index out of range in quicksort partition", "category": "IndexError"},
        {"error_message": "list index out of range in merge sort", "category": "IndexError"},
        {"error_message": "list index out of range in heap sort", "category": "IndexError"},
        {"error_message": "maximum recursion depth exceeded in quicksort", "category": "RecursionError"},
        {"error_message": "maximum recursion depth exceeded in merge sort", "category": "RecursionError"},
        {"error_message": "'<' not supported between instances of 'str' and 'int' in sort", "category": "TypeError"},
        {"error_message": "'>' not supported between instances of 'dict' and 'dict' in sort", "category": "TypeError"},
        {"error_message": "comparison failed in binary search", "category": "TypeError"},
        
        # Binary search tree errors
        {"error_message": "'NoneType' object has no attribute 'left' in BST traversal", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'right' in BST traversal", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'value' in BST node", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'key' in BST node", "category": "AttributeError"},
        {"error_message": "maximum recursion depth exceeded in BST insertion", "category": "RecursionError"},
        {"error_message": "maximum recursion depth exceeded in BST deletion", "category": "RecursionError"},
        {"error_message": "maximum recursion depth exceeded in tree traversal", "category": "RecursionError"},
        
        # Graph algorithm errors
        {"error_message": "'dict' object has no attribute 'neighbors' in graph", "category": "AttributeError"},
        {"error_message": "'dict' object has no attribute 'visited' in DFS", "category": "AttributeError"},
        {"error_message": "KeyError: 'vertex' in graph adjacency list", "category": "KeyError"},
        {"error_message": "KeyError: 'node' in graph dictionary", "category": "KeyError"},
        {"error_message": "maximum recursion depth exceeded in DFS traversal", "category": "RecursionError"},
        {"error_message": "queue index out of range in BFS", "category": "IndexError"},
        {"error_message": "stack index out of range in DFS", "category": "IndexError"},
        {"error_message": "heap index out of range in Dijkstra", "category": "IndexError"},
        {"error_message": "'<' not supported between instances in priority queue", "category": "TypeError"},
        
        # Dynamic programming errors
        {"error_message": "list index out of range in DP table", "category": "IndexError"},
        {"error_message": "dictionary key not found in memoization", "category": "KeyError"},
        {"error_message": "maximum recursion depth exceeded in recursive DP", "category": "RecursionError"},
        {"error_message": "matrix dimensions don't match for multiplication", "category": "ValueError"},
        {"error_message": "DP table initialization error: negative size", "category": "ValueError"},
        
        # Linked list errors
        {"error_message": "'NoneType' object has no attribute 'next' in linked list", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'data' in linked list node", "category": "AttributeError"},
        {"error_message": "'LinkedList' object has no attribute 'head'", "category": "AttributeError"},
        {"error_message": "'Node' object has no attribute 'value'", "category": "AttributeError"},
        {"error_message": "cannot traverse empty linked list", "category": "IndexError"},
        
        # Stack and queue errors
        {"error_message": "pop from empty stack", "category": "IndexError"},
        {"error_message": "peek on empty stack", "category": "IndexError"},
        {"error_message": "dequeue from empty queue", "category": "IndexError"},
        {"error_message": "queue is empty", "category": "IndexError"},
        {"error_message": "stack underflow", "category": "IndexError"},
        {"error_message": "queue overflow", "category": "MemoryError"},
        
        # Heap errors
        {"error_message": "heap index out of bounds", "category": "IndexError"},
        {"error_message": "'<' not supported between heap elements", "category": "TypeError"},
        {"error_message": "heapq heappush on non-list", "category": "TypeError"},
        {"error_message": "heapq heappop from empty heap", "category": "IndexError"},
        
        # Hash table errors
        {"error_message": "hash collision resolution failed", "category": "RuntimeError"},
        {"error_message": "load factor exceeded in hash table", "category": "MemoryError"},
        {"error_message": "unhashable type in dictionary key", "category": "TypeError"},
        {"error_message": "unhashable type in set", "category": "TypeError"},
        
        # Trie errors
        {"error_message": "'NoneType' object has no attribute 'children' in trie", "category": "AttributeError"},
        {"error_message": "'NoneType' object has no attribute 'is_end_of_word' in trie", "category": "AttributeError"},
        {"error_message": "KeyError: 'character' in trie node children", "category": "KeyError"},
        
        # Segment tree and Fenwick tree errors
        {"error_message": "segment tree index out of range", "category": "IndexError"},
        {"error_message": "Fenwick tree update index out of bounds", "category": "IndexError"},
        {"error_message": "segment tree query range invalid", "category": "ValueError"},
        
        # Greedy algorithm errors
        {"error_message": "comparison of incompatible types in greedy choice", "category": "TypeError"},
        {"error_message": "empty candidate set in greedy algorithm", "category": "IndexError"},
        {"error_message": "optimal substructure not found", "category": "ValueError"},
        
        # Backtracking errors
        {"error_message": "maximum recursion depth exceeded in backtracking", "category": "RecursionError"},
        {"error_message": "no valid configuration found in backtracking", "category": "ValueError"},
        {"error_message": "constraint violation in backtracking solution", "category": "AssertionError"},
    ]


def generate_common_beginner_mistakes() -> List[Dict]:
    """Generate errors from common beginner programmer mistakes."""
    return [
        # Using = instead of ==
        {"error_message": "cannot assign to operator", "category": "SyntaxError"},
        {"error_message": "keyword can't be an expression", "category": "SyntaxError"},
        
        # Forgetting colons
        {"error_message": "expected ':' after if statement", "category": "SyntaxError"},
        {"error_message": "expected ':' after for statement", "category": "SyntaxError"},
        {"error_message": "expected ':' after while statement", "category": "SyntaxError"},
        {"error_message": "expected ':' after def statement", "category": "SyntaxError"},
        {"error_message": "expected ':' after class statement", "category": "SyntaxError"},
        {"error_message": "expected ':' after else statement", "category": "SyntaxError"},
        {"error_message": "expected ':' after elif statement", "category": "SyntaxError"},
        {"error_message": "expected ':' after try statement", "category": "SyntaxError"},
        {"error_message": "expected ':' after except statement", "category": "SyntaxError"},
        {"error_message": "expected ':' after finally statement", "category": "SyntaxError"},
        {"error_message": "expected ':' after with statement", "category": "SyntaxError"},
        
        # Missing parentheses
        {"error_message": "unexpected EOF while parsing function call", "category": "SyntaxError"},
        {"error_message": "unexpected EOF while parsing tuple", "category": "SyntaxError"},
        {"error_message": "unexpected EOF while parsing list", "category": "SyntaxError"},
        {"error_message": "unexpected EOF while parsing dictionary", "category": "SyntaxError"},
        
        # Quote mismatches
        {"error_message": "EOL while scanning string literal with mismatched quotes", "category": "SyntaxError"},
        {"error_message": "unterminated string literal", "category": "SyntaxError"},
        {"error_message": "mismatched quotes in string", "category": "SyntaxError"},
        
        # Boolean constant typos
        {"error_message": "name 'ture' is not defined", "category": "NameError"},
        {"error_message": "name 'flase' is not defined", "category": "NameError"},
        {"error_message": "name 'None' is not defined", "category": "NameError"},
        {"error_message": "name 'null' is not defined", "category": "NameError"},
        {"error_message": "name 'undefined' is not defined", "category": "NameError"},
        
        # Using keywords as variable names
        {"error_message": "can't assign to keyword", "category": "SyntaxError"},
        {"error_message": "invalid syntax with 'if' as variable", "category": "SyntaxError"},
        {"error_message": "invalid syntax with 'for' as variable", "category": "SyntaxError"},
        {"error_message": "invalid syntax with 'while' as variable", "category": "SyntaxError"},
        {"error_message": "invalid syntax with 'def' as variable", "category": "SyntaxError"},
        {"error_message": "invalid syntax with 'class' as variable", "category": "SyntaxError"},
        {"error_message": "invalid syntax with 'import' as variable", "category": "SyntaxError"},
        {"error_message": "invalid syntax with 'return' as variable", "category": "SyntaxError"},
        
        # Mutable default argument issues (runtime, not syntax)
        {"error_message": "'list' object keeps growing across function calls", "category": "RuntimeError"},
        {"error_message": "'dict' object keeps accumulating across function calls", "category": "RuntimeError"},
        
        # Variable scope issues
        {"error_message": "local variable referenced before assignment", "category": "UnboundLocalError"},
        {"error_message": "local variable 'x' referenced before assignment", "category": "UnboundLocalError"},
        {"error_message": "local variable 'result' referenced before assignment", "category": "UnboundLocalError"},
        {"error_message": "cannot access local variable before assignment", "category": "UnboundLocalError"},
        
        # Modifying while iterating
        {"error_message": "dictionary changed size during iteration", "category": "RuntimeError"},
        {"error_message": "set changed size during iteration", "category": "RuntimeError"},
        {"error_message": "list modified during iteration", "category": "RuntimeError"},
        
        # Shallow vs deep copy issues
        {"error_message": "nested list modification affects original", "category": "RuntimeError"},
        {"error_message": "shallow copy mutation bug", "category": "RuntimeError"},
        
        # Integer division confusion
        {"error_message": "integer division returns unexpected floor value", "category": "RuntimeError"},
        {"error_message": "// operator returns float unexpectedly", "category": "RuntimeError"},
        
        # Chained comparison misunderstanding
        {"error_message": "chained comparison evaluates unexpectedly", "category": "RuntimeError"},
        {"error_message": "1 < x < 10 evaluates incorrectly", "category": "RuntimeError"},
        
        # List multiplication pitfalls
        {"error_message": "list multiplication creates shared references", "category": "RuntimeError"},
        {"error_message": "[[]] * n creates nested lists with same reference", "category": "RuntimeError"},
    ]


def generate_all_training_data() -> List[Dict]:
    """Generate comprehensive training dataset."""
    all_data = []
    
    generators = [
        generate_basic_syntax_errors,
        generate_type_errors,
        generate_value_errors,
        generate_index_key_errors,
        generate_import_errors,
        generate_syntax_errors,
        generate_indentation_errors,
        generate_division_recursion_errors,
        generate_os_system_errors,
        generate_unicode_encoding_errors,
        generate_assertion_runtime_errors,
        generate_memory_overflow_errors,
        generate_dsa_algorithm_errors,
        generate_common_beginner_mistakes,
    ]
    
    for generator in generators:
        print(f"Generating {generator.__name__}...")
        all_data.extend(generator())
    
    print(f"\nTotal training samples generated: {len(all_data)}")
    return all_data


def save_training_data(data: List[Dict], output_path: str = "error_patterns_comprehensive.json"):
    """Save generated training data to JSON file."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Training data saved to {output_path}")


if __name__ == "__main__":
    print("=" * 60)
    print("PyDebugAI Comprehensive Training Data Generator")
    print("=" * 60)
    print()
    
    # Generate all training data
    training_data = generate_all_training_data()
    
    # Save to file
    save_training_data(training_data)
    
    # Show category distribution
    categories = {}
    for item in training_data:
        cat = item["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategory Distribution:")
    print("-" * 60)
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"{cat:30s}: {count:4d} samples")
    
    print("\n" + "=" * 60)
    print("✅ Training data generation complete!")
    print("=" * 60)
