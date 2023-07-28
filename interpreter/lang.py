from interpreter.errors import GenericError, IllegalCharacterError
from interpreter.token import Token, TokenType


class Position:
    def __init__(
        self, file_name: str, file_text: str, index: int, line: int, column: int
    ):
        self.file_name = file_name
        self.file_text = file_text
        self.index = index
        self.line = line
        self.column = column

    def advance(self, current_char: str | None = None):
        self.index += 1
        self.column += 1

        if current_char == "\n":
            self.line += 1
            self.column = 0

        return self

    def copy(self):
        return Position(
            self.file_name, self.file_text, self.index, self.line, self.column
        )


class Lexer:
    def __init__(self, file_name: str, text: str):
        self.text = text
        self.file_name = file_name
        self.position = Position(
            file_name=self.file_name, file_text=self.text, index=-1, line=0, column=-1
        )
        self.curr_char = None
        self.advance()

    def advance(self):
        self.position.advance(self.curr_char)
        self.curr_char = (
            self.text[self.position.column]
            if self.position.column < len(self.text)
            else None
        )

    def tokenize(self) -> tuple[list[Token], GenericError | None]:
        tokens: list[Token] = []
        skip_chars = {" ", "\t", "\n"}

        while self.curr_char is not None:
            if self.curr_char in skip_chars:
                self.advance()

            if self.curr_char.isdigit():
                num = self.generate_number()

                if isinstance(num, GenericError):
                    return [], num

                tokens.append(num)
            else:
                match self.curr_char:
                    case "+":
                        tokens.append(Token(TokenType.PLUS, self.curr_char))
                        self.advance()
                    case "-":
                        tokens.append(Token(TokenType.MINUS, self.curr_char))
                        self.advance()
                    case "*":
                        tokens.append(Token(TokenType.MUL, self.curr_char))
                        self.advance()
                    case "/":
                        tokens.append(Token(TokenType.DIV, self.curr_char))
                        self.advance()
                    case "(":
                        tokens.append(Token(TokenType.LPAREN, self.curr_char))
                        self.advance()
                    case ")":
                        tokens.append(Token(TokenType.RPAREN, self.curr_char))
                        self.advance()
                    case _:
                        pos_start = self.position.copy()
                        char = self.curr_char
                        self.advance()
                        return [], IllegalCharacterError(
                            self.file_name,
                            pos_start,
                            self.position,
                            char,
                        )

        return tokens, None

    def generate_number(self) -> Token | GenericError:
        decimals = 0
        start_col = self.position.column

        for char in self.text[start_col:]:
            is_last: bool = self.position.column == len(self.text) - 1

            if char == ".":
                pos_start = self.position.copy()
                decimals += 1
                self.advance()
                if decimals > 1:
                    return GenericError(
                        self.file_name,
                        pos_start,
                        self.position,
                        "Invalid number: too many decimals",
                    )
            elif not char.isdigit() or is_last:
                token = None

                if char.isdigit():
                    self.advance()

                if decimals > 0:
                    token = Token(
                        TokenType.FLOAT,
                        float(self.text[start_col : self.position.column]),
                    )
                else:
                    token = Token(
                        TokenType.INT, int(self.text[start_col : self.position.column])
                    )

                return token

            else:
                self.advance()

        return GenericError(
            self.file_name,
            self.position,
            self.position,
            "Invalid number",
        )


def run(file_name: str, text: str):
    lexer = Lexer(file_name=file_name, text=text)
    return lexer.tokenize()
