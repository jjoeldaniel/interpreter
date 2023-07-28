from __future__ import annotations
from interpreter.token import TokenType


class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{self.value}"


class BinaryOperationNode:
    def __init__(
        self,
        left_node: NumberNode | BinaryOperationNode,
        operation: TokenType,
        right_node: NumberNode | BinaryOperationNode,
    ):
        self.left_node = left_node
        self.operation = operation
        self.right_node = right_node

    def __repr__(self):
        return f"({self.left_node}, {self.operation}, {self.right_node})"


def evaluate(node: BinaryOperationNode | NumberNode):
    if isinstance(node, NumberNode):
        return node.value

    left = evaluate(node.left_node)
    right = evaluate(node.right_node)

    if node.operation.type == TokenType.PLUS:
        return left + right
    elif node.operation.type == TokenType.MINUS:
        return left - right
    elif node.operation.type == TokenType.MUL:
        return left * right
    elif node.operation.type == TokenType.DIV:
        return left / right
