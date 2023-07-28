class GenericError(Exception):
    def __init__(self, line: int, column: int, message: str):
        self.message = message
        self.line = line
        self.column = column

    def __str__(self):
        return f"Error: {self.message} at line {self.line}, column {self.column}"
