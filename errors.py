class GenericError:
    def __init__(
        self, file_name: str, file_text: str, line: int, column: int, message: str
    ):
        self.file_name = file_name
        self.file_text = file_text
        self.line = line
        self.column = column
        self.message = message

    def __str__(self):
        message = f'File "{self.file_name}"'
        message += (
            f"\nError: {self.message} at line {self.line+1}, column {self.column}"
        )
        return message


class IllegalCharacterError(GenericError):
    def __init__(
        self, file_name: str, file_text: str, line: int, column: int, char: str
    ):
        super().__init__(
            file_name, file_text, line, column, f"Illegal character '{char}'"
        )
