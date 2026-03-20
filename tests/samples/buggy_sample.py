# Sample buggy Python file for testing PyDebugAI
# This file intentionally has multiple errors for demonstration

# Error 1: NameError — undefined variable
result = myundefinedvar + 10

# Error 2: TypeError — wrong types
total = "100" + 50

# Error 3: ZeroDivisionError
x = 10 / 0

# Error 4: IndexError
my_list = [1, 2, 3]
print(my_list[99])

# Error 5: AttributeError on NoneType
val = None
val.strip()

# Error 6: KeyError
my_dict = {"name": "Alice"}
print(my_dict["age"])

# Error 7: Typo in function name (pritn instead of print)
pritn("hello world")

# Error 8: Wrong number of arguments
def greet(name, age):
    return f"Hello {name}, you are {age}"

greet("Alice")  # missing 'age' argument
