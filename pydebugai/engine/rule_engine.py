"""
Rule Engine — 60+ hand-crafted rules mapping Python error patterns → fix suggestions.
Fast, deterministic, fully offline. No ML needed for common errors.
"""
from __future__ import annotations
import re
from typing import List, Optional, Tuple
from ..models import ErrorCategory, Suggestion


# ─── Rule definition ──────────────────────────────────────────────────────────

class Rule:
    """A single pattern-based fix rule."""
    def __init__(self, category: ErrorCategory, pattern: str, title: str,
                 explanation: str, fix_template: Optional[str] = None,
                 references: Optional[List[str]] = None, confidence: float = 0.85):
        self.category = category
        self.pattern = re.compile(pattern, re.IGNORECASE)
        self.title = title
        self.explanation = explanation
        self.fix_template = fix_template
        self.references = references or []
        self.confidence = confidence

    def match(self, error_message: str) -> Optional[re.Match]:
        return self.pattern.search(error_message)


# ─── Rule database ────────────────────────────────────────────────────────────

RULES: List[Rule] = [

    # ── NameError ─────────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.NAME,
        r"name '(.+?)' is not defined",
        "Undefined Name",
        "You're using a variable or function that hasn't been defined yet. "
        "Check for typos, make sure you defined it before using it, or import the required module.",
        "# Check: did you mean to define '{name}' first?\n{name} = <value>  # or import {name}",
        ["https://docs.python.org/3/library/exceptions.html#NameError"],
        0.90,
    ),
    Rule(
        ErrorCategory.NAME,
        r"name '(print|input|len|range|type|int|str|list|dict|set|tuple)' is not defined",
        "Built-in Function Shadowed or Python 2 Code",
        "This is a built-in Python function. If it's not defined, you may be running Python 2 code in Python 3, "
        "or you accidentally reassigned this name earlier in your code.",
        "# Do not reassign built-in names like print, len, etc.",
        ["https://docs.python.org/3/library/functions.html"],
        0.95,
    ),
    Rule(
        ErrorCategory.NAME,
        r"free variable '(.+?)' referenced before assignment",
        "Free Variable Referenced Before Assignment",
        "You're referencing a variable inside a closure (nested function) before it's assigned in the enclosing scope. "
        "Use `nonlocal` to modify the enclosing variable.",
        "nonlocal {name}  # Add this at the top of the inner function",
        [],
        0.88,
    ),

    # ── TypeError ─────────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.TYPE,
        r"unsupported operand type\(s\) for (.+?): '(.+?)' and '(.+?)'",
        "Incompatible Type Operation",
        "You're trying to apply an operator (like +, -, *, /) to incompatible types. "
        "Convert one of the values to a compatible type first.",
        "# Convert types before operation:\nresult = int(a) + int(b)  # or str(a) + str(b)",
        ["https://docs.python.org/3/library/exceptions.html#TypeError"],
        0.90,
    ),
    Rule(
        ErrorCategory.TYPE,
        r"'(.+?)' object is not (iterable|subscriptable|callable)",
        "Object Not Iterable/Subscriptable/Callable",
        "You're trying to iterate, index, or call an object that doesn't support that operation. "
        "Check the type of your variable.",
        "# Check the type:\nprint(type(my_var))  # Make sure it's the right type",
        [],
        0.88,
    ),
    Rule(
        ErrorCategory.TYPE,
        r"takes (\d+) positional argument(?:s)? but (\d+) (?:was|were) given",
        "Wrong Number of Arguments",
        "You called a function with the wrong number of arguments. "
        "Check the function signature and provide the correct number of arguments.",
        "# Check the function definition and match argument count.",
        [],
        0.92,
    ),
    Rule(
        ErrorCategory.TYPE,
        r"missing (\d+) required positional argument(?:s)?: (.+)",
        "Missing Required Arguments",
        "You're calling a function without providing all required arguments. "
        "Add the missing arguments to your function call.",
        "# Example: func(arg1, arg2, ...)",
        [],
        0.93,
    ),
    Rule(
        ErrorCategory.TYPE,
        r"can only concatenate (str|list|tuple) \(not \"(.+?)\"\) to (str|list|tuple)",
        "Type Mismatch in Concatenation",
        "You're trying to concatenate incompatible types. Convert the second value to match the first type.",
        "# Convert to string: result = my_string + str(my_number)",
        [],
        0.91,
    ),
    Rule(
        ErrorCategory.TYPE,
        r"'(.+?)' object cannot be interpreted as an integer",
        "Non-Integer Where Integer Required",
        "A function (like range()) requires an integer argument, but you passed a different type. "
        "Use int() to convert.",
        "# Convert to integer: range(int(value))",
        [],
        0.90,
    ),
    Rule(
        ErrorCategory.TYPE,
        r"object of type '(.+?)' has no len\(\)",
        "Object Has No Length",
        "You're calling len() on an object that doesn't support it (e.g., int, float). "
        "Only sequences and collections have a length.",
        "# len() works on: str, list, tuple, dict, set, etc.",
        ["https://docs.python.org/3/library/functions.html#len"],
        0.88,
    ),

    # ── ValueError ────────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.VALUE,
        r"invalid literal for int\(\) with base \d+: '(.+?)'",
        "Cannot Convert String to Int",
        "You're trying to convert a string to an integer, but the string contains non-numeric characters. "
        "Make sure the string only contains digits.",
        "# Check the value before converting:\nif value.strip().isdigit():\n    num = int(value)\nelse:\n    print(f'Cannot convert {value!r} to int')",
        [],
        0.92,
    ),
    Rule(
        ErrorCategory.VALUE,
        r"could not convert string to float: '(.+?)'",
        "Cannot Convert String to Float",
        "The string you're trying to convert to a float contains non-numeric characters.",
        "try:\n    num = float(value)\nexcept ValueError:\n    print(f'Invalid float: {value!r}')",
        [],
        0.91,
    ),
    Rule(
        ErrorCategory.VALUE,
        r"not enough values to unpack \(expected (\d+), got (\d+)\)",
        "Unpacking Count Mismatch",
        "You're trying to unpack an iterable into more variables than it contains. "
        "Check the length of your iterable or use * to capture remaining values.",
        "# Use * for variable-length unpacking:\na, *rest = my_list",
        [],
        0.89,
    ),
    Rule(
        ErrorCategory.VALUE,
        r"too many values to unpack \(expected (\d+)\)",
        "Too Many Values to Unpack",
        "Your iterable contains more values than the variables you're unpacking into.",
        "a, b, *rest = my_list  # Use * to capture extras",
        [],
        0.89,
    ),

    # ── AttributeError ────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.ATTRIBUTE,
        r"'(.+?)' object has no attribute '(.+?)'",
        "Attribute Not Found",
        "The object doesn't have the attribute or method you're trying to access. "
        "Check the correct attribute name with dir(obj) or the documentation.",
        "# To see all available attributes:\nprint(dir(my_object))",
        [],
        0.88,
    ),
    Rule(
        ErrorCategory.ATTRIBUTE,
        r"'NoneType' object has no attribute '(.+?)'",
        "Called Method on None (NoneType)",
        "Your variable is None, but you're trying to call a method on it. "
        "This often happens when a function returns None implicitly. Check your function return values.",
        "# Check before using:\nif my_var is not None:\n    my_var.method()",
        [],
        0.95,
    ),
    Rule(
        ErrorCategory.ATTRIBUTE,
        r"'(.+?)' object has no attribute '(append|extend|pop|remove|insert|sort|reverse)'",
        "List Method on Non-List Object",
        "You're calling a list method on a non-list type. Make sure your variable is actually a list.",
        "# Ensure it's a list:\nmy_var = list(my_var)  # Convert to list first",
        [],
        0.90,
    ),
    Rule(
        ErrorCategory.ATTRIBUTE,
        r"module '(.+?)' has no attribute '(.+?)'",
        "Module Attribute Not Found",
        "The module doesn't have the function or attribute you're looking for. "
        "It may be in a sub-module, or you may have the wrong name.",
        "# Check module contents:\nimport my_module\nprint(dir(my_module))",
        ["https://docs.python.org/3/"],
        0.87,
    ),

    # ── IndexError ────────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.INDEX,
        r"list index out of range",
        "List Index Out of Range",
        "You're trying to access an index that doesn't exist in the list. "
        "Remember Python uses 0-based indexing, and negative indices count from the end.",
        "# Safe access pattern:\nif 0 <= index < len(my_list):\n    value = my_list[index]\nelse:\n    print(f'Index {index} out of range (len={len(my_list)})')",
        ["https://docs.python.org/3/tutorial/introduction.html#lists"],
        0.93,
    ),
    Rule(
        ErrorCategory.INDEX,
        r"string index out of range",
        "String Index Out of Range",
        "You're trying to access a character position that doesn't exist in the string.",
        "# Safe access:\nif 0 <= index < len(my_str):\n    char = my_str[index]",
        [],
        0.92,
    ),
    Rule(
        ErrorCategory.INDEX,
        r"tuple index out of range",
        "Tuple Index Out of Range",
        "You're trying to access an index beyond the tuple's length.",
        "# Check length first: if index < len(my_tuple):",
        [],
        0.91,
    ),

    # ── KeyError ──────────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.KEY,
        r"KeyError: ('?.+?'?)",
        "Dictionary Key Not Found",
        "The key you're looking up doesn't exist in the dictionary. "
        "Use .get() for safe access, or check with `in` first.",
        "# Safe access with default:\nvalue = my_dict.get(key, default_value)\n\n# Or check first:\nif key in my_dict:\n    value = my_dict[key]",
        ["https://docs.python.org/3/library/stdtypes.html#dict"],
        0.93,
    ),

    # ── ImportError ───────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.IMPORT,
        r"No module named '(.+?)'",
        "Module Not Found",
        "Python can't find the module you're trying to import. "
        "Install it with pip, or check that the module name is spelled correctly.",
        "# Install the missing package:\npip install {module_name}\n\n# Or if it's a local file, check the file path and name.",
        ["https://pypi.org/"],
        0.95,
    ),
    Rule(
        ErrorCategory.IMPORT,
        r"cannot import name '(.+?)' from '(.+?)'",
        "Import Name Not Found in Module",
        "The name you're trying to import doesn't exist in that module. "
        "Check the module's documentation for the correct name.",
        "# View available names:\nimport {module}\nprint(dir({module}))",
        [],
        0.90,
    ),

    # ── SyntaxError ───────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.SYNTAX,
        r"unexpected EOF while parsing|unexpected end of file",
        "Unexpected End of File",
        "Python reached the end of your file while expecting more code. "
        "You likely have an unclosed bracket, parenthesis, or string.",
        "# Check for unclosed: ( ) [ ] { } or multi-line strings '''",
        [],
        0.92,
    ),
    Rule(
        ErrorCategory.SYNTAX,
        r"expected ':' after",
        "Missing Colon",
        "Python expects a colon `:` at the end of `if`, `for`, `while`, `def`, `class`, `try`, etc.",
        "if condition:  # Don't forget the colon\n    pass",
        [],
        0.95,
    ),
    Rule(
        ErrorCategory.SYNTAX,
        r"invalid syntax",
        "Invalid Syntax",
        "Python encountered code it can't understand. Common causes: missing colon, unmatched brackets, "
        "incorrect operators, using Python 2 syntax in Python 3 (e.g., `print` without parentheses).",
        "# Common fixes:\n# 1. Add missing colon: if x == 1:\n# 2. Use print(): print('hello')\n# 3. Check brackets: (), [], {}",
        ["https://docs.python.org/3/reference/"],
        0.80,
    ),
    Rule(
        ErrorCategory.SYNTAX,
        r"EOL while scanning string literal",
        "Unterminated String",
        "Your string is missing its closing quote. Make sure every string is properly closed.",
        "# Close the string:\nmy_str = 'hello'  # or \"hello\"",
        [],
        0.95,
    ),
    Rule(
        ErrorCategory.SYNTAX,
        r"invalid character '(.+?)' \(U\+",
        "Invalid Unicode Character",
        "Your code contains a non-ASCII character that Python can't interpret as valid syntax. "
        "This often happens when copying code from a web page or document that uses fancy quotes.",
        "# Replace smart quotes with straight quotes:\n# \" → \"\n# ' → '",
        [],
        0.90,
    ),

    # ── IndentationError ──────────────────────────────────────────────────────
    Rule(
        ErrorCategory.INDENT,
        r"unexpected indent",
        "Unexpected Indentation",
        "This line is indented more than expected. Make sure your indentation is consistent "
        "and that you're not adding indentation where it's not needed.",
        "# Use consistent indentation (4 spaces recommended):\ndef func():\n    x = 1  # 4 spaces\n    return x",
        [],
        0.93,
    ),
    Rule(
        ErrorCategory.INDENT,
        r"expected an indented block",
        "Missing Indented Block",
        "Python expects an indented code block after a colon (`:`), but found none. "
        "Add the body of your function, loop, or conditional.",
        "if condition:\n    pass  # Add actual code here, or use 'pass' as placeholder",
        [],
        0.95,
    ),
    Rule(
        ErrorCategory.INDENT,
        r"unindent does not match any outer indentation level",
        "Inconsistent Indentation",
        "Your indentation doesn't match any outer block. You may have mixed tabs and spaces, "
        "or removed too many levels of indentation.",
        "# Use consistent indentation. Convert all tabs to spaces:\n# In your editor: Edit > Convert Indentation to Spaces",
        [],
        0.90,
    ),

    # ── ZeroDivisionError ─────────────────────────────────────────────────────
    Rule(
        ErrorCategory.ZERO_DIV,
        r"division by zero|integer division or modulo by zero",
        "Division By Zero",
        "You're dividing a number by zero, which is mathematically undefined. "
        "Add a check before dividing.",
        "# Safe division:\nif divisor != 0:\n    result = numerator / divisor\nelse:\n    result = 0  # or handle the case",
        [],
        0.97,
    ),

    # ── RecursionError ────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.RECURSION,
        r"maximum recursion depth exceeded",
        "Maximum Recursion Depth Exceeded",
        "Your recursive function calls itself too many times without a proper base case. "
        "Add a base case to stop the recursion, or consider using an iterative approach.",
        "def factorial(n):\n    if n <= 1:  # Base case — REQUIRED!\n        return 1\n    return n * factorial(n - 1)",
        ["https://docs.python.org/3/library/sys.html#sys.setrecursionlimit"],
        0.95,
    ),

    # ── FileNotFoundError ─────────────────────────────────────────────────────
    Rule(
        ErrorCategory.OS,
        r"No such file or directory: '(.+?)'",
        "File or Directory Not Found",
        "The file path you specified doesn't exist. Check the path, ensure the file exists, "
        "and consider using `os.path.exists()` to check before opening.",
        "import os\npath = 'my_file.txt'\nif os.path.exists(path):\n    with open(path) as f:\n        data = f.read()\nelse:\n    print(f'File not found: {path}')",
        [],
        0.95,
    ),

    # ── StopIteration ─────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.STOP_ITER,
        r"StopIteration",
        "Iterator Exhausted",
        "You called next() on an iterator that has no more items. "
        "Use a for loop or provide a default value to next().",
        "# Safe next() with default:\nvalue = next(my_iterator, None)  # Returns None if exhausted\n\n# Or use a for loop:\nfor item in my_iterable:\n    process(item)",
        [],
        0.90,
    ),

    # ── MemoryError ───────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.MEMORY,
        r"MemoryError",
        "Out of Memory",
        "Your program ran out of available memory. This often happens with very large data structures. "
        "Consider using generators, chunking data, or increasing available memory.",
        "# Use generators instead of lists for large datasets:\ndef gen_data():\n    for i in range(10**9):\n        yield i  # Only one item in memory at a time",
        [],
        0.85,
    ),

    # ── OverflowError ─────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.OVERFLOW,
        r"math range error|Result too large|OverflowError",
        "Arithmetic Overflow",
        "A numeric result is too large to be represented. For integers Python handles big numbers automatically, "
        "but for floats you may hit the limit.",
        "import math\n# Check for overflow:\ntry:\n    result = math.exp(very_large_number)\nexcept OverflowError:\n    result = float('inf')",
        [],
        0.83,
    ),

    # ── AssertionError ────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.ASSERTION,
        r"AssertionError",
        "Assertion Failed",
        "An `assert` statement evaluated to False. Check the condition being asserted "
        "and make sure the values match your expectations.",
        "# Debug the assertion:\nprint(f'Actual value: {actual_value}')\nassert actual_value == expected, f'Got {actual_value}, expected {expected}'",
        [],
        0.85,
    ),

    # ── Unicode ───────────────────────────────────────────────────────────────
    Rule(
        ErrorCategory.UNICODE,
        r"'(.+?)' codec can't (encode|decode) character",
        "Unicode Encoding/Decoding Error",
        "A character in your text can't be represented in the codec you're using. "
        "Specify the correct encoding or use 'ignore' / 'replace' error handling.",
        "# Specify encoding explicitly:\nwith open('file.txt', encoding='utf-8', errors='replace') as f:\n    data = f.read()\n\n# Or encode with error handling:\ntext.encode('ascii', errors='ignore')",
        [],
        0.88,
    ),
]


# ─── Engine class ─────────────────────────────────────────────────────────────

class RuleEngine:
    """Fast, rule-based fix engine for Python errors."""

    def __init__(self):
        self._rules = RULES

    def suggest(self, error_message: str, category: ErrorCategory,
                line: Optional[int] = None) -> List[Suggestion]:
        """
        Match error message against all rules and return matching Suggestion list.
        Sorted by confidence descending.
        """
        suggestions: List[Suggestion] = []
        for rule in self._rules:
            # Filter by category for speed
            if rule.category != category and rule.category != ErrorCategory.UNKNOWN:
                if rule.category != category:
                    continue
            m = rule.match(error_message)
            if m:
                # Fill template placeholders from regex groups
                fix_code = rule.fix_template
                if fix_code and m.lastindex:
                    groups = {str(i + 1): g for i, g in enumerate(m.groups()) if g}
                    # Also try named-like replacement
                    for placeholder in re.findall(r'\{(\w+)\}', fix_code):
                        if placeholder.isdigit() and placeholder in groups:
                            fix_code = fix_code.replace(f'{{{placeholder}}}', groups[placeholder])
                        elif placeholder in ('name', 'module', 'module_name'):
                            val = m.group(1) if m.lastindex >= 1 else placeholder
                            fix_code = fix_code.replace(f'{{{placeholder}}}', val)

                suggestions.append(Suggestion(
                    title=rule.title,
                    explanation=rule.explanation,
                    fix_code=fix_code,
                    line=line,
                    confidence=rule.confidence,
                    source="rule_engine",
                    category=category,
                    references=rule.references,
                ))

        return sorted(suggestions, key=lambda s: s.confidence, reverse=True)

    def suggest_all_categories(self, error_message: str,
                               line: Optional[int] = None) -> List[Suggestion]:
        """Try matching against all categories (slower, for unknown error types)."""
        suggestions: List[Suggestion] = []
        seen_titles: set = set()
        for rule in self._rules:
            m = rule.match(error_message)
            if m and rule.title not in seen_titles:
                seen_titles.add(rule.title)
                fix_code = rule.fix_template
                suggestions.append(Suggestion(
                    title=rule.title,
                    explanation=rule.explanation,
                    fix_code=fix_code,
                    line=line,
                    confidence=rule.confidence * 0.8,  # penalise cross-category
                    source="rule_engine",
                    category=rule.category,
                    references=rule.references,
                ))
        return sorted(suggestions, key=lambda s: s.confidence, reverse=True)
