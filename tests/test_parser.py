import pytest
from src.tokenizer import Tokenizer
from src.parser import Parser
from src.errors import ParserError, TokenizerError

def parse_json(text: str):
    tokenizer = Tokenizer(text)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

def test_empty_object():
    result = parse_json("{}")
    assert result == {}

def test_simple_object():
    result = parse_json('{"name": "John", "age": 30}')
    assert result == {"name": "John", "age": 30}

def test_nested_object():
    result = parse_json('''
    {
        "person": {
            "name": "John",
            "age": 30,
            "address": {
                "street": "123 Main St",
                "city": "New York"
            }
        }
    }
    ''')
    assert result == {
        "person": {
            "name": "John",
            "age": 30,
            "address": {
                "street": "123 Main St",
                "city": "New York"
            }
        }
    }
def test_arrays():
    test_cases = [
        ("[]", []),
        ("[1, 2, 3]", [1, 2, 3]),
        ('["a", "b", "c"]', ["a", "b", "c"]),
        ("[[1, 2], [3, 4]]", [[1, 2], [3, 4]])
    ]
    
    for input_str, expected in test_cases:
        result = parse_json(input_str)
        assert result == expected

def test_complex_structure():
    json = '''
    {
        "name": "John Doe",
        "age": 30,
        "is_student": true,
        "courses": ["Math", "Physics"],
        "grades": {
            "Math": 95.5,
            "Physics": 89.0
        },
        "contact": {
            "email": "john@example.com",
            "phone": null
        }
    }
    '''
    result = parse_json(json)
    assert result["name"] == "John Doe"
    assert result["age"] == 30
    assert result["is_student"] is True
    assert result["courses"] == ["Math", "Physics"]
    assert result["grades"]["Math"] == 95.5
    assert result["contact"]["phone"] is None

def test_error_invalid_syntax():
    invalid_inputs = [
        ('{"key": }', "Expected value"),
        ('{"key": "value",}', "Expected string key"),
        ('[1, 2,]', "Expected value"),
        ('{"key": undefined}', "Expected value, got identifier: undefined"),
        ('{key: "value"}', "Expected string key")  # Added this case
    ]
    
    for input_str, error_msg in invalid_inputs:
        with pytest.raises((ParserError, TokenizerError)) as exc_info:
            parse_json(input_str)
        assert error_msg in str(exc_info.value)


def test_numbers():
    json = '''
    {
        "integer": 42,
        "negative": -17,
        "float": 3.14159,
        "scientific": 1.23e-4,
        "zero": 0
    }
    '''
    result = parse_json(json)
    assert result["integer"] == 42
    assert result["negative"] == -17
    assert isinstance(result["float"], float)
    assert isinstance(result["scientific"], float)
    assert result["zero"] == 0

def test_string_escapes():
    json = '''
    {
        "normal": "Hello, World!",
        "escaped": "Hello,\\n\\"World\\"!",
        "unicode": "Hello World"
    }
    '''
    result = parse_json(json)
    assert result["normal"] == "Hello, World!"
    assert result["escaped"] == 'Hello,\\n\\"World\\"!'
    assert result["unicode"] == "Hello World"
