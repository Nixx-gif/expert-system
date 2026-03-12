from node import Node, Leaf

def tokenize(rule):
    tokens = []
    i = 0
    while i < len(rule):
        c = rule[i]
        if c == ' ':
            i += 1
            continue
        if c.isalpha():
            tokens.append(("FACT", c))
            i += 1
            continue
        if c == "+":
            tokens.append(("AND", c))
            i += 1
            continue
        if c == "|":
            tokens.append(("OR", c))
            i += 1
            continue
        if c == "^":
            tokens.append(("XOR", c))
            i += 1
            continue
        if c == "!":
            tokens.append(("NOT", c))
            i += 1
            continue
        if c == "(":
            tokens.append(("LPAREN", c))
            i += 1
            continue
        if c == ")":
            tokens.append(("RPAREN", c))
            i += 1
            continue
        if c == "=":
            if rule[i+1] == ">":
                tokens.append(("IMPLIES", rule[i:i+2]))
                i += 2
                continue
        if c == "<":
            if rule[i+1] == "=":
                if rule[i+2] == ">":
                    tokens.append(("IFF", rule[i:i+3]))
                    i += 3
                    continue
        else:
            tokens.append(("ERROR", c))
            i += 1
            continue
    return tokens