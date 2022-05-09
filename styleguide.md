# KlebLib Style Guide

 This is a comprehensive guide to styling Python files in KlebLib. The aim of this document is to make KlebLib more readable, and therefore easier to maintain. 

 ## Python Defaults
 
  Unless otherwise stated, the styling recommended in the Python documentation is to be followed here. 

 ## Indentation

  Blocks of code should be indented with four spaces, *not* tabs.

 ## Naming Conventions

  ### Variables

   Variable names should be written using camelCase.

  ### Constants

   Names of variables that will not change should be written in SCREAMING_SNAKE_CASE.

  ### Functions

   Names of functions should be written in snake_case. 

  ### Classes

   Names of classes should be written in TitleCamelCase. 

 ## Type Hints

  Type hints for arguments should always be written without spaces, e.g `def foo(bar:str):`, even when a default value is specified, such as in `def foo(bar:str=None):`. Type hints for function return values should be written with spaces around the arrow, e.g `def foo() -> None:`. Non-magic functions, along with `__init__`, should always have type hints, even when they are only intended for internal use. 

  ### Unions
   
   Unions should always be written with the shorthand `|` with no spaces, e.g `str|int`. The order should always be `memoryview`, `bytes`, `bytearray`, `bool`, `int`, `float`, `complex`, `str`, `list`, `tuple`, `set`, `range`, any other iterator, `dict`, `NoneType`, followed by aliases, and then any custom types. 

 ## Order

  Code should be ordered as follows:

  * Imports
  * Global constants
  * Classes
    * `__new__`
    * `__init__`
    * Comparison operators
    * Binary arithmetic operators
    * Unary arithmetic operators
    * `__repr__`
    * Type conversion methods, in the order laid out in [Unions](#user-content-unions)