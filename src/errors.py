from dataclasses import dataclass

@dataclass
class Location:
    line: int
    column: int

class JSONError(Exception):
    def __init__(self, message: str, location: Location):
        self.message = message
        self.location = location
        super().__init__(f"{message} at line {location.line}, column {location.column}")

class TokenizerError(JSONError):
    pass

class ParserError(JSONError):
    pass

def format_error(source: str, error: JSONError) -> str:
    lines = source.splitlines()
    if error.location.line <= len(lines):
        line = lines[error.location.line - 1]
        pointer = " " * (error.location.column - 1) + "^"
        return f"{error.message}\n{line}\n{pointer}"
    return str(error)