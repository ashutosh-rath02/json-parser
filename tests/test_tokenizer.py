import pytest
from src.tokenizer import Tokenizer, TokenType, TokenizerError

def test_empty_object():
    tokenizer = Tokenizer("{}")
    tokens = tokenizer.tokenize()
    assert len(tokens) == 3  # {, }, EOF
    assert tokens[0].type == TokenType.LEFT_BRACE
    assert tokens[1].type == TokenType.RIGHT_BRACE

def test_simple_string():
    tokenizer = Tokenizer('{"key": "value"}')
    tokens = tokenizer.tokenize()
    assert tokens[1].type == TokenType.STRING
    assert tokens[1].value == "key"
    assert tokens[3].type == TokenType.STRING
    assert tokens[3].value == "value"

def test_numbers():
    test_cases = [
        ("123", 123),
        ("-456", -456),
        ("3.14", "3.14"),
        ("-2.718", "-2.718"),
        ("1e-10", "1e-10")
    ]
    
    for input_str, expected_value in test_cases:
        tokenizer = Tokenizer(input_str)
        tokens = tokenizer.tokenize()
        assert tokens[0].type == TokenType.NUMBER
        assert tokens[0].value == str(expected_value)

def test_boolean_and_null():
    tokenizer = Tokenizer('[true, false, null]')
    tokens = tokenizer.tokenize()
    assert tokens[1].type == TokenType.BOOLEAN
    assert tokens[1].value == "true"
    assert tokens[3].type == TokenType.BOOLEAN
    assert tokens[3].value == "false"
    assert tokens[5].type == TokenType.NULL

# def test_invalid_input():
#     with pytest.raises(TokenizerError) as exc_info:
#         Tokenizer('{invalid}').tokenize()
#     assert "Invalid token: invalid" in str(exc_info.value)

def test_string_escapes():
    tokenizer = Tokenizer(r'{"text": "Hello \"World\"!"}')
    tokens = tokenizer.tokenize()
    assert tokens[3].value == r'Hello \"World\"!'

def test_nested_structures():
    json = '''
    {
        "object": {"nested": "value"},
        "array": [1, 2, {"key": "value"}]
    }
    '''
    tokenizer = Tokenizer(json)
    tokens = tokenizer.tokenize()
    assert len([t for t in tokens if t.type == TokenType.LEFT_BRACE]) == 3