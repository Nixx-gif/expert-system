from node import Node, Leaf

SYMBOLS = {
    "+": "AND",
    "|": "OR",
    "^": "XOR",
    "!": "NOT",
    "(": "LPAREN",
    ")": "RPAREN",
}

def tokenize(rule):
    tokens = []
    i = 0
    while i < len(rule):
        c = rule[i]
        if c == " ":
            i += 1
        elif c.isalpha():
            tokens.append(("FACT", c))
            i += 1
        elif c == "=" and rule[i+1] == ">":
            tokens.append(("IMPLIES", "=>"))
            i += 2
        elif c == "<" and rule[i+1:i+3] == "=>":
            tokens.append(("IFF", "<=>"))
            i += 3
        elif c in SYMBOLS:
            tokens.append((SYMBOLS[c], c))
            i += 1
        else:
            raise ValueError(f"Caractère inconnu : '{c}'")
    return tokens