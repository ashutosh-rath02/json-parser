from typing import Any, List
from .tokenizer import Token, TokenType
from .errors import ParserError, Location

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Any:
        if not self.tokens:
            raise ParserError(
                "No tokens to parse",
                Location(1, 1)
            )
        return self.parse_value()

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def peek(self) -> Token:
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def check(self, type: TokenType) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == type

    def match(self, *types: TokenType) -> bool:
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type: TokenType, message: str) -> Token:
        if self.check(type):
            return self.advance()
        token = self.peek()
        raise ParserError(message, Location(token.line, token.column))

    def parse_value(self):
        if self.match(TokenType.STRING):
            return self.previous().value
        
        if self.match(TokenType.NUMBER):
            value = self.previous().value
            try:
                if '.' in value or 'e' in value.lower():
                    return float(value)
                return int(value)
            except ValueError:
                token = self.previous()
                raise ParserError(
                    f"Invalid number: {value}",
                    Location(token.line, token.column)
                )
        
        if self.match(TokenType.BOOLEAN):
            return self.previous().value == "true"
        
        if self.match(TokenType.NULL):
            return None
        
        if self.match(TokenType.LEFT_BRACE):
            return self.parse_object()
        
        if self.match(TokenType.LEFT_BRACKET):
            return self.parse_array()
        
        if self.match(TokenType.IDENTIFIER):
            token = self.previous()
            raise ParserError(
                f"Expected value, got identifier: {token.value}",
                Location(token.line, token.column)
            )
        
        token = self.peek()
        raise ParserError(
            "Expected value",
            Location(token.line, token.column)
        )

    def parse_object(self) -> dict:
        obj = {}
        
        if not self.check(TokenType.RIGHT_BRACE):
            while True:
                if not self.check(TokenType.STRING):
                    if self.check(TokenType.IDENTIFIER):
                        token = self.peek()
                        raise ParserError(
                            "Expected string key",
                            Location(token.line, token.column)
                        )
                    token = self.peek()
                    raise ParserError(
                        "Expected string key",
                        Location(token.line, token.column)
                    )
                
                key = self.advance().value
                self.consume(TokenType.COLON, "Expected ':' after key")
                value = self.parse_value()
                obj[key] = value
                
                if not self.match(TokenType.COMMA):
                    break

        self.consume(TokenType.RIGHT_BRACE, "Expected '}'")
        return obj

    def parse_array(self) -> list:
        array = []
        
        if not self.check(TokenType.RIGHT_BRACKET):
            while True:
                array.append(self.parse_value())
                if not self.match(TokenType.COMMA):
                    break

        self.consume(TokenType.RIGHT_BRACKET, "Expected ']'")
        return array