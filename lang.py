from enum import Enum
from errors import GenericError


class TokenType(Enum):
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    INT = "INT"
    FLOAT = "FLOAT"


class Token:
    def __init__(self, type_: TokenType, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = -1
        self.curr_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.curr_char = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        tokens: list[Token] = []
        skip_chars = {" ", "\t", "\n"}

        while self.curr_char is not None:
            if self.curr_char in skip_chars:
                self.advance()

            if self.curr_char.isdigit():
                tokens.append(self.generate_number())

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
                case _:
                    self.advance()

        return tokens

    def generate_number(self) -> Token:
        decimals = 0
        start_pos = self.pos

        for char in self.text[start_pos:]:
            is_last: bool = self.pos == len(self.text) - 1

            if char == ".":
                decimals += 1
                self.advance()
                if decimals > 1:
                    raise GenericError(
                        self.pos, self.pos, "Invalid number: too many decimals"
                    )
            elif not char.isdigit() or is_last:
                token = None

                if char.isdigit():
                    self.advance()

                if decimals > 0:
                    token = Token(
                        TokenType.FLOAT, float(self.text[start_pos : self.pos])
                    )
                else:
                    token = Token(TokenType.INT, int(self.text[start_pos : self.pos]))

                if char.isdigit():
                    self.advance()

                return token

            else:
                self.advance()

        raise GenericError(self.pos, self.pos, "Invalid number")


def run(text: str):
    lexer = Lexer(text)
    return lexer.tokenize()
