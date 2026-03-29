SYMBOLS = {
    "+": "AND",
    "|": "OR",
    "^": "XOR",
    "!": "NOT",
    "(": "LPAREN",
    ")": "RPAREN",
}


def tokenize(rule):
    """
    Convert a raw rule string into a list of typed tokens.

    Recognized tokens:
        - Single uppercase letters       → ("FACT", "A")
        - Operator symbols (+, |, ^, !)  → ("AND"|"OR"|"XOR"|"NOT", symbol)
        - Parentheses                    → ("LPAREN"|"RPAREN", symbol)
        - Implication arrow =>           → ("IMPLIES", "=>")
        - Biconditional arrow <=>        → ("IFF", "<=>")

    Whitespace is silently ignored. Comments must be stripped before calling.

    Args:
        rule (str): A single rule string, e.g. "A + B => C".

    Returns:
        list[tuple[str, str]]: Ordered list of (token_type, token_value) pairs.

    Raises:
        ValueError: If an unrecognized character is encountered.
    """
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