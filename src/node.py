from dataclasses import dataclass


@dataclass
class Leaf:
    """
    A terminal node in the AST, representing a single propositional fact.

    Attributes:
        value (str): The fact identifier, a single uppercase letter (e.g. "A").
    """
    value: str


@dataclass
class Node:
    """
    An internal node in the AST, representing a logical operator.

    Attributes:
        kind (str): The operator type. One of:
                    "NOT", "AND", "OR", "XOR", "IMPLIES", "IFF".
        left (Node | Leaf | None): The left (or only) operand.
        right (Node | Leaf | None): The right operand. None for unary operators (NOT).
    """
    kind: str
    left: object = None
    right: object = None