class GenericError:
    def __init__(
        self,
        file_name: str,
        pos_start,
        pos_end,
        message: str,
    ):
        self.file_name = file_name
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.message = message

    def __str__(self):
        message = f"\nError: {self.message} at line {self.pos_start.line+1}, column {self.pos_start.column}"
        message += f'\nFile "{self.file_name}", line {self.pos_start.line+1}'
        return message


class IllegalCharacterError(GenericError):
    def __init__(
        self,
        file_name: str,
        pos_start,
        pos_end,
        char: str,
    ):
        super().__init__(
            file_name,
            pos_start,
            pos_end,
            f"Illegal character '{char}'",
        )
