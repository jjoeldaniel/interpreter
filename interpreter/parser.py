from interpreter.token import Token
from interpreter.decisions import BinaryOperationNode, NumberNode


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
