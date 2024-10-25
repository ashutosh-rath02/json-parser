# JSON Parser from Scratch

A custom JSON parser built from scratch in Python that tokenizes and parses JSON strings into native Python objects. This project demonstrates the inner workings of JSON parsing without relying on built-in parsing libraries.

## Features

- **Custom Tokenizer**: Breaks down JSON strings into tokens with precise line and column tracking
- **Custom Parser**: Converts tokens into native Python objects (dictionaries, lists, etc.)
- **Detailed Error Handling**: Provides specific error messages with line and column information
- **Interactive UI**: Web interface for testing and visualizing the parsing process
- **Syntax Highlighting**: Color-coded output for better readability
- **Token Visualization**: See how your JSON is broken down into tokens
- **Formatting**: Pretty print your JSON with proper indentation

## Demo

## Installation

```bash
# Clone the repository
git clone https://github.com/ashutosh-rath02/json-parser.git
cd json-parser

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Run the Web Interface

```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

### Use as a Module

```python
from src.tokenizer import Tokenizer
from src.parser import Parser

# Parse JSON string
def parse_json(json_string):
    tokenizer = Tokenizer(json_string)
    tokens = tokenizer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

# Example usage
json_string = '{"name": "John", "age": 30}'
result = parse_json(json_string)
print(result)  # {'name': 'John', 'age': 30}
```

## Features in Detail

### Tokenizer

- Breaks down JSON into tokens like `STRING`, `NUMBER`, `BOOLEAN`, etc.
- Tracks line and column numbers for error reporting
- Handles escape sequences in strings
- Validates basic syntax

### Parser

- Converts token stream into Python objects
- Handles nested structures (objects and arrays)
- Type conversion (string, number, boolean, null)
- Error detection and reporting

### Error Handling

- Precise error locations
- Descriptive error messages
- Visual error highlighting
- Syntax validation

## Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_parser.py
```

## Error Examples

```python
# Invalid JSON
parse_json('{key: "value"}')
# Error: Expected string key at line 1, column 2

parse_json('{"key": undefined}')
# Error: Expected value, got identifier: undefined at line 1, column 9
```

## Supported JSON Features

- Objects (`{}`)
- Arrays (`[]`)
- Strings (`"..."`)
- Numbers (integer and floating-point)
- Booleans (`true`/`false`)
- Null (`null`)
- Nested structures
- Unicode strings
- Scientific notation numbers

## Limitations

- No support for comments
- No streaming for large files
- Single-threaded processing
- Memory-bound by input size

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Running in Production

### Using Render.com

1. Sign up at render.com
2. Connect your GitHub repository
3. Create a new Web Service
4. Use `gunicorn app:app` as the start command

### Using Local Network

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn app:app
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

- Inspired by the JSON specification [json.org](https://json.org)
- Built as a learning project for understanding parsers and compilers
- Thanks to the testing suite at [JSON Test Suite](https://github.com/nst/JSONTestSuite)

## Author

Your Name - [@yourtwitter](https://twitter.com/v_ashu_dev)

Project Link: [https://github.com/yourusername/json-parser](https://github.com/ashutosh-rath02/json-parser)
