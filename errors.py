class GenericError(Exception):
    def __init__(self, column: int, message: str):
        self.message = message
        self.column = column

    def __str__(self):
        return f"Error: {self.message} at column {self.column}"
