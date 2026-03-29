from node import Node, Leaf


def parse_atom(tokens, i):
    """
    Parse an atomic expression: a single fact or a parenthesized sub-expression.

    Args:
        tokens (list[tuple]): The full token list.
        i (int): Current position in the token list.

    Returns:
        tuple[Node | Leaf, int]: The parsed node and the updated position.
    """
    if tokens[i][0] == "FACT":
        return Leaf(tokens[i][1]), i + 1
    if tokens[i][0] == "LPAREN":
        node, i = parse_implies(tokens, i + 1)
        return node, i + 1


def parse_not(tokens, i):
    """
    Parse a NOT expression or delegate to parse_atom.

    If the current token is NOT, consumes it and parses the following atom
    as its operand. Otherwise falls through to parse_atom.

    Args:
        tokens (list[tuple]): The full token list.
        i (int): Current position in the token list.

    Returns:
        tuple[Node | Leaf, int]: The parsed node and the updated position.
    """
    if i < len(tokens) and tokens[i][0] == "NOT":
        operand, i = parse_atom(tokens, i + 1)
        return (Node("NOT", operand), i)
    return parse_atom(tokens, i)


def parse_binary(tokens, i, operator, parse_operand):
    """
    Parse a binary expression for a given operator type.

    Parses the left operand using parse_operand, then checks if the current
    token matches the expected operator. If so, parses the right operand and
    builds a binary Node. Otherwise returns the left operand unchanged.

    This function handles single binary operations only (no chaining).
    Chaining is handled by the caller's precedence hierarchy.

    Args:
        tokens (list[tuple]): The full token list.
        i (int): Current position in the token list.
        operator (str): The token type to match (e.g. "AND", "OR", "XOR").
        parse_operand (callable): Parser function for the sub-expressions.

    Returns:
        tuple[Node | Leaf, int]: The parsed node and the updated position.
    """
    left, i = parse_operand(tokens, i)
    if i < len(tokens) and tokens[i][0] == operator:
        right, i = parse_operand(tokens, i + 1)
        left = Node(operator, left, right)
    return (left, i)


def parse_and(tokens, i):
    """
    Parse an AND expression (operator: +).

    Precedence: higher than XOR, OR. Operands are parsed by parse_not.

    Args:
        tokens (list[tuple]): The full token list.
        i (int): Current position in the token list.

    Returns:
        tuple[Node | Leaf, int]: The parsed node and the updated position.
    """
    return parse_binary(tokens, i, "AND", parse_not)


def parse_or(tokens, i):
    """
    Parse an OR expression (operator: |).

    Precedence: lower than AND, higher than XOR. Operands are parsed by parse_and.

    Args:
        tokens (list[tuple]): The full token list.
        i (int): Current position in the token list.

    Returns:
        tuple[Node | Leaf, int]: The parsed node and the updated position.
    """
    return parse_binary(tokens, i, "OR", parse_and)


def parse_xor(tokens, i):
    """
    Parse a XOR expression (operator: ^).

    Precedence: lower than OR. Operands are parsed by parse_or.

    Args:
        tokens (list[tuple]): The full token list.
        i (int): Current position in the token list.

    Returns:
        tuple[Node | Leaf, int]: The parsed node and the updated position.
    """
    return parse_binary(tokens, i, "XOR", parse_or)


def parse_implies(tokens, i):
    """
    Parse an implication (=>) or biconditional (<=>) expression.

    This is the top-level parser function, with the lowest precedence.
    It first parses the left-hand side via parse_xor, then checks for
    an IMPLIES or IFF token to build the corresponding binary node.

    If no implication token is found, returns the left-hand side as-is.

    Args:
        tokens (list[tuple]): The full token list.
        i (int): Current position in the token list.

    Returns:
        tuple[Node | Leaf, int]: The parsed node and the updated position.
    """
    left, i = parse_xor(tokens, i)
    if i >= len(tokens):
        return left, i
    if tokens[i][0] == "IMPLIES":
        right, i = parse_xor(tokens, i + 1)
        return Node("IMPLIES", left, right), i
    if tokens[i][0] == "IFF":
        right, i = parse_xor(tokens, i + 1)
        return Node("IFF", left, right), i
    return left, i