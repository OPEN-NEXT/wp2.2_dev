# Python code guidelines

This document will summarise best practices for Python code and styling.

**TODO:** We need to identify and adopt good practices for exception handling.

## Style guidelines

* [Clean Code](https://github.com/zedr/clean-code-python) principles for Python
* Collection of Python [anti-patterns and worst practices](https://github.com/quantifiedcode/python-anti-patterns)

## Useful features

### exception handling

* The ["definitive" guide](https://julien.danjou.info/python-exceptions-guide/) to Python exceptions

### Static types

Python is a dynamically-typed language where you don't specify a variable's type when you create it. For example `myString = "Hello world"` creates a variable `myString` that is a string, but it is *implied* and not explicit.

* How to use [static type checking](https://medium.com/@ageitgey/learn-how-to-use-static-type-checking-in-python-3-6-in-10-minutes-12c86d72677b) in Python
* RealPython's guide to [Python type checking](https://realpython.com/python-type-checking/)
* [Pyright](https://github.com/Microsoft/pyright) is a type checker for Python code
* 