# Building a JSON Parser from Scratch - A Comprehensive Guide

## Table of Contents

1. Understanding JSON and Parsing Concepts
2. Lexical Analysis (Tokenization)
3. Syntax Analysis (Parsing)
4. Error Handling and Recovery
5. Implementation Details
6. Testing and Validation

## 1. Understanding JSON and Parsing Concepts

### What is JSON?

JSON (JavaScript Object Notation) is a lightweight data interchange format. The official specification can be found at [json.org](https://json.org/).

Basic JSON data types:

```json
{
  "string": "Hello, World!",
  "number": 42,
  "float": 3.14,
  "boolean": true,
  "null": null,
  "array": [1, 2, 3],
  "object": { "key": "value" }
}
```

### Parser Components

A parser typically consists of two main components:

1. **Lexical Analyzer (Lexer/Tokenizer)**: Converts raw input into tokens
2. **Syntax Analyzer (Parser)**: Converts tokens into a structured format

### Recommended Reading:

- [Crafting Interpreters - Scanning](https://craftinginterpreters.com/scanning.html)
- [Parsing Basics](https://en.wikipedia.org/wiki/Parsing#Computer_languages)
- [JSON Grammar Specification](https://www.json.org/json-en.html)

## 2. Lexical Analysis (Tokenization)

Let's break down the tokenizer implementation:

```python
from enum import Enum
from dataclasses import dataclass

# Define token types
class TokenType(Enum):
    LEFT_BRACE = "{"     # Marks start of object
    RIGHT_BRACE = "}"    # Marks end of object
    LEFT_BRACKET = "["   # Marks start of array
    RIGHT_BRACKET = "]"  # Marks end of array
    COMMA = ","          # Separates elements
    COLON = ":"          # Separates key-value pairs
    STRING = "STRING"    # String values
    NUMBER = "NUMBER"    # Numeric values
    BOOLEAN = "BOOLEAN"  # true/false
    NULL = "NULL"        # null value
    EOF = "EOF"          # End of input

# Token class to store token information
@dataclass
class Token:
    type: TokenType    # Type of token
    value: str        # Actual text value
    line: int         # Line number for error reporting
    column: int       # Column number for error reporting
```

### Key Concepts:

1. **Tokens**: The smallest meaningful units in the input

   - Example: `{"name": "John"}` becomes tokens: `{`, `"name"`, `:`, `"John"`, `}`

2. **Position Tracking**: Keep track of line and column numbers for error reporting

```python
def advance(self):
    char = self.peek()
    self.current += 1
    self.column += 1
    return char

def new_line(self):
    self.line += 1
    self.column = 1
```

3. **Lexical Patterns**: Recognizing different types of tokens

```python
def scan_token(self):
    char = self.advance()

    # Single-character tokens
    if char == '{': return self.make_token(TokenType.LEFT_BRACE)
    if char == '}': return self.make_token(TokenType.RIGHT_BRACE)

    # Multi-character tokens
    if char == '"': return self.string()
    if self.is_digit(char): return self.number()
```

### Resources for Lexical Analysis:

- [Lexical Analysis Tutorial](https://www.geeksforgeeks.org/lexical-analysis-in-compiler-design/)
- [Building a Lexer in Python](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html)
- [Regular Expressions in Lexical Analysis](https://www.cs.princeton.edu/~appel/modern/java/CUP/manual.html)

## 3. Syntax Analysis (Parsing)

The parser implements a recursive descent approach:

```python
class Parser:
    def parse_value(self):
        # Parse different types of values based on the current token
        if self.match(TokenType.LEFT_BRACE):
            return self.parse_object()
        if self.match(TokenType.LEFT_BRACKET):
            return self.parse_array()
        if self.match(TokenType.STRING):
            return self.parse_string()
        # ... other value types
```

### Key Concepts:

1. **Recursive Descent Parsing**: Top-down parsing technique

```python
def parse_object(self):
    obj = {}

    while not self.check(TokenType.RIGHT_BRACE):
        key = self.parse_string()
        self.consume(TokenType.COLON, "Expected ':'")
        value = self.parse_value()  # Recursive call
        obj[key] = value

        if not self.match(TokenType.COMMA):
            break

    self.consume(TokenType.RIGHT_BRACE, "Expected '}'")
    return obj
```

2. **Grammar Rules**: JSON grammar in BNF notation

```
object → '{' (string ':' value (',' string ':' value)*)? '}'
array  → '[' (value (',' value)*)? ']'
value  → string | number | object | array | 'true' | 'false' | 'null'
```

3. **Error Handling**: Synchronization and recovery

```python
def synchronize(self):
    self.advance()

    while not self.is_at_end():
        if self.previous.type == TokenType.RIGHT_BRACE:
            return

        self.advance()
```

### Resources for Parsing:

- [Recursive Descent Parsing](https://www.craftinginterpreters.com/parsing-expressions.html)
- [Parser Combinators](https://www.aosabook.org/en/500L/parsing.html)
- [Syntax Analysis Tutorial](https://www.tutorialspoint.com/compiler_design/compiler_design_syntax_analysis.htm)

## 4. Error Handling and Recovery

Implementing robust error handling:

```python
class JSONError(Exception):
    def __init__(self, message: str, line: int, column: int, source: str):
        self.message = message
        self.line = line
        self.column = column
        self.source = source

    def format_error(self):
        # Get the problematic line
        lines = self.source.splitlines()
        error_line = lines[self.line - 1]

        # Create error pointer
        pointer = ' ' * (self.column - 1) + '^'

        return f"""Error: {self.message}
Line {self.line}, Column {self.column}
{error_line}
{pointer}"""
```

### Error Handling Strategies:

1. **Panic Mode Recovery**: Skip tokens until a synchronization point
2. **Error Productions**: Grammar rules that handle common mistakes
3. **Error Messages**: Provide context and suggestions

### Resources for Error Handling:

- [Error Recovery in Parsing](https://www.cs.cornell.edu/courses/cs412/2008sp/lectures/lec12.pdf)
- [Compiler Error Recovery](https://www.semanticscholar.org/paper/Error-Recovery-in-a-Parser-Generator-Charles/1e1d9e7d0f4d3b5f5f8f5f8f5f8f5f8f5f8f5f8f)

## 5. Implementation Details

### Performance Optimizations:

1. **String Interning**: Reuse string objects

```python
def intern_string(self, string: str) -> str:
    if string in self.string_pool:
        return self.string_pool[string]
    self.string_pool[string] = string
    return string
```

2. **Buffer Management**: Efficient string handling

```python
def read_string(self):
    buffer = []
    while self.peek() != '"':
        buffer.append(self.advance())
    return ''.join(buffer)
```

### Resources for Optimization:

- [String Interning in Python](https://stackoverflow.com/questions/15541404/python-string-interning)
- [Performance Tips for Parsers](https://blog.gopheracademy.com/advent-2014/parsers-lexers/)

## 6. Testing and Validation

### Test Cases:

1. **Valid JSON**:

```python
def test_valid_json():
    parser = JSONParser()
    assert parser.parse('{"name": "John", "age": 30}') == {
        "name": "John",
        "age": 30
    }
```

2. **Invalid JSON**:

```python
def test_invalid_json():
    parser = JSONParser()
    with pytest.raises(JSONError) as e:
        parser.parse('{"name": }')
    assert "Expected value" in str(e.value)
```

### Test Resources:

- [JSON Test Suite](https://github.com/nst/JSONTestSuite)
- [Property-Based Testing](https://hypothesis.readthedocs.io/en/latest/)

## Advanced Topics

1. **Streaming Parser**: Parse large JSON files
2. **Schema Validation**: Validate against JSON Schema
3. **Pretty Printing**: Format JSON output
4. **Custom Extensions**: Add new features to JSON

### Advanced Resources:

- [JSON Schema](https://json-schema.org/)
- [Streaming Parsers](https://en.wikipedia.org/wiki/Streaming_parser)
- [JSON Lines Format](http://jsonlines.org/)

## Books and Further Reading:

1. "Crafting Interpreters" by Robert Nystrom
2. "Compilers: Principles, Techniques, and Tools" (Dragon Book)
3. "Engineering a Compiler" by Cooper and Torczon

## Online Courses:

1. [Coursera: Compilers](https://www.coursera.org/learn/build-a-computer)
2. [edX: Programming Languages](https://www.edx.org/course/programming-languages-part-a)

Would you like me to elaborate on any particular aspect or provide more specific examples for any section?
