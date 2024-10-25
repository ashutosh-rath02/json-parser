# tokenizer.py
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
from .errors import TokenizerError, Location

class TokenType(Enum):
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"
    COMMA = ","
    COLON = ":"
    STRING = "STRING"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"
    IDENTIFIER = "IDENTIFIER"
    EOF = "EOF"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', line={self.line}, col={self.column})"

class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> List[Token]:
        while not self.is_at_end():
            self.start = self.current
            try:
                self.scan_token()
            except TokenizerError as e:
                raise TokenizerError(
                    f"{e.message} near '{self.source[max(0, self.current-10):min(len(self.source), self.current+10)]}'",
                    e.location
                )
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> str:
        char = self.source[self.current]
        self.current += 1
        self.column += 1
        return char

    def peek(self) -> Optional[str]:
        if self.is_at_end():
            return None
        return self.source[self.current]

    def peek_next(self) -> Optional[str]:
        if self.current + 1 >= len(self.source):
            return None
        return self.source[self.current + 1]

    def scan_token(self):
        char = self.advance()

        if char in [' ', '\r', '\t']:
            return
        elif char == '\n':
            self.line += 1
            self.column = 1
            return

        # Single-character tokens
        elif char == '{': self.add_token(TokenType.LEFT_BRACE)
        elif char == '}': self.add_token(TokenType.RIGHT_BRACE)
        elif char == '[': self.add_token(TokenType.LEFT_BRACKET)
        elif char == ']': self.add_token(TokenType.RIGHT_BRACKET)
        elif char == ',': self.add_token(TokenType.COMMA)
        elif char == ':': self.add_token(TokenType.COLON)

        # String
        elif char == '"': self.string()

        # Number
        elif char.isdigit() or char == '-': self.number()

        # Keywords (true, false, null) and identifiers
        elif char.isalpha():
            # Move back one character to read the full identifier
            self.current -= 1
            self.column -= 1
            self.identifier()
        else:
            raise TokenizerError(
                f"Unexpected character: {char}",
                Location(self.line, self.column - 1)
            )


    def string(self):
        string_content = []
        start_line = self.line
        start_column = self.column - 1

        while True:
            if self.is_at_end():
                raise TokenizerError(
                    "Unterminated string",
                    Location(start_line, start_column)
                )

            char = self.peek()
            if char == '"':
                break

            if char == '\\':
                self.advance()
                if self.is_at_end():
                    raise TokenizerError(
                        "Unterminated escape sequence",
                        Location(self.line, self.column)
                    )
                
                escape_char = self.advance()
                if escape_char in '"\\bfnrt':
                    string_content.append('\\' + escape_char)
                else:
                    raise TokenizerError(
                        f"Invalid escape sequence: \\{escape_char}",
                        Location(self.line, self.column - 1)
                    )
            else:
                if char == '\n':
                    raise TokenizerError(
                        "Unterminated string - newline found",
                        Location(self.line, self.column)
                    )
                string_content.append(char)
                self.advance()

        self.advance()
        value = ''.join(string_content)
        self.add_token(TokenType.STRING, value)

    def number(self):
        while (peek := self.peek()) is not None and peek.isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next() and self.peek_next().isdigit():
            self.advance()
            while (peek := self.peek()) is not None and peek.isdigit():
                self.advance()

        if (peek := self.peek()) is not None and peek.lower() == 'e':
            self.advance()
            if (peek := self.peek()) is not None and peek in '+-':
                self.advance()
            while (peek := self.peek()) is not None and peek.isdigit():
                self.advance()

        value = self.source[self.start:self.current]
        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        # Consume first character (already validated as alphabetic)
        start_line = self.line
        start_column = self.column
        
        # Consume first character
        self.advance()
        
        # Consume rest of identifier
        while (peek := self.peek()) and (peek.isalnum() or peek == '_'):
            self.advance()

        text = self.source[self.start:self.current]
        
        # Handle keywords
        if text == "true" or text == "false":
            self.add_token(TokenType.BOOLEAN, text)
        elif text == "null":
            self.add_token(TokenType.NULL, text)
        else:
            # Pass any other identifier to the parser for validation
            self.add_token(TokenType.IDENTIFIER, text)
            
    def add_token(self, type: TokenType, literal: str = None):
        text = self.source[self.start:self.current] if literal is None else literal
        self.tokens.append(Token(type, text, self.line, self.column - len(text)))
