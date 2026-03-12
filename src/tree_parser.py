from node import Node, Leaf

def parse_atom(tokens, i):
        if tokens[i][0] == "FACT":
            node = Leaf(tokens[i][1])
            i += 1
            return(node, i)
        if tokens[i][0] == "LPAREN":
            i += 1
            node, i = parse_implies(tokens, i)
            i += 1
            return(node, i)
        
def parse_not(tokens, i):
    if i < len(tokens) and tokens[i][0] == "NOT":
        i += 1
        operand, i = parse_atom(tokens, i)
        return (Node("NOT", operand), i)
    return parse_atom(tokens, i)

def parse_and(tokens, i):
    left, i = parse_not(tokens, i)
    if i < len(tokens) and tokens[i][0] == "AND":
        i += 1
        right, i = parse_not(tokens, i)
        left = Node("AND", left, right)
    return (left, i)

def parse_or(tokens, i):
    left, i = parse_and(tokens, i)
    if i < len(tokens) and tokens[i][0] == "OR":
        i += 1
        right, i = parse_and(tokens, i)
        left = Node("OR", left, right)
    return (left, i)

def parse_xor(tokens, i):
    left, i = parse_or(tokens, i)
    if i < len(tokens) and tokens[i][0] == "XOR":
        i += 1
        right, i = parse_or(tokens, i)
        left = Node("XOR", left, right)
    return (left, i)

def parse_implies(tokens, i):
    left, i = parse_xor(tokens, i)
    if i < len(tokens) and tokens[i][0] == "IMPLIES":
        i += 1
        right, i = parse_xor(tokens, i)
        left = Node("IMPLIES", left, right)
    elif i < len(tokens) and tokens[i][0] == "IFF":
        i += 1
        right, i = parse_xor(tokens, i)
        left = Node("IFF", left, right)
    return (left, i)