# app.py
from flask import Flask, json, request, jsonify, send_from_directory
from flask_cors import CORS
from src.tokenizer import Tokenizer
from src.parser import Parser
from src.errors import TokenizerError, ParserError

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://json-parser-ten.vercel.app",
            "http://localhost:5000",
            "http://localhost:3000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "Accept"]
    }
})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://json-parser-ten.vercel.app')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/parse', methods=['POST'])
def parse_json():
    try:
        data = request.json
        json_str = data.get('json', '')
        
        if not json_str.strip():
            return jsonify({'error': 'Please enter some JSON to parse'})
        
        # Create tokenizer and get tokens
        tokenizer = Tokenizer(json_str)
        tokens = tokenizer.tokenize()
        
        # Create parser and parse tokens
        parser = Parser(tokens)
        parsed_result = parser.parse()
        
        return jsonify({
            'tokens': [str(token) for token in tokens],
            'parsed': parsed_result
        })
        
    except (TokenizerError, ParserError) as e:
        return jsonify({'error': str(e)})
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'})
    
@app.route('/format', methods=['POST'])
def format_json():
    try:
        data = request.json
        json_str = data.get('json', '')
        
        if not json_str.strip():
            return jsonify({'error': 'Please enter some JSON to format'})
        
        # Try to parse and format using our parser
        tokenizer = Tokenizer(json_str)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        parsed_result = parser.parse()
        
        # Format with indentation
        formatted = json.dumps(parsed_result, indent=4)
        
        return jsonify({
            'formatted': formatted
        })
        
    except (TokenizerError, ParserError) as e:
        return jsonify({'error': str(e)})
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)