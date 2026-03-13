from node import Node, Leaf

def parse_atom(tokens, i):
        if tokens[i][0] == "FACT":
            return Leaf(tokens[i][1]), i + 1
        if tokens[i][0] == "LPAREN":
            node, i = parse_implies(tokens, i + 1)
            return node, i + 1
        
def parse_not(tokens, i):
    if i < len(tokens) and tokens[i][0] == "NOT":
        operand, i = parse_atom(tokens, i + 1)
        return (Node("NOT", operand), i)
    return parse_atom(tokens, i)

def parse_binary(tokens, i, operator, parse_operand):
    left, i = parse_operand(tokens, i)
    if i < len(tokens) and tokens[i][0] == operator:
        right, i = parse_operand(tokens, i + 1)
        left = Node(operator, left, right)
    return (left, i)


def parse_and(tokens, i):
    return parse_binary(tokens, i, "AND", parse_not)

def parse_or(tokens, i):
    return parse_binary(tokens, i, "OR", parse_and)

def parse_xor(tokens, i):
    return parse_binary(tokens, i, "XOR", parse_or)

def parse_implies(tokens, i):
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