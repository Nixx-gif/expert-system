# proplogic

A lightweight **propositional logic inference engine** written in Python. Feed it a rule file, and it resolves queries using backward chaining — returning `True`, `False`, or `Undetermined` for each fact.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Supported Syntax](#supported-syntax)
- [Getting Started](#getting-started)
- [Input File Format](#input-file-format)
- [Example](#example)
- [Project Structure](#project-structure)

---

## Overview

**proplogic** takes a plain-text file describing:

- **Rules** — propositional implications between named facts
- **Initial facts** — facts known to be true at startup
- **Queries** — facts to resolve

The engine uses **backward chaining**: to prove a goal, it recursively searches for rules whose conclusion contains that goal, then evaluates their premises. It handles three-valued logic — if a conclusion is inherently ambiguous (OR or XOR on the right-hand side), the result is `Undetermined` rather than forced to a definite value.

---

## Architecture

Five focused modules, each with a single responsibility:

```
src/
├── node.py          # AST data structures: Node (operator) and Leaf (fact)
├── tokenizer.py     # Lexer: rule string → token list
├── tree_parser.py   # Recursive descent parser: token list → AST
├── utils.py         # Rule matching, ambiguity detection, tree pretty-print
└── motor.py         # Entry point: file I/O, tree construction, query resolution
```

### Data flow

```
file.txt
   │
   ▼
read_files()        reads and strips comments / blank lines
   │
   ▼
parse()             splits into rules, initial facts, and queries
   │
   ├─► tokenize()         rule string → token list
   │
   ├─► parse_implies()    token list → AST (recursive descent)
   │
   └─► resolve()          backward chaining over all queries
            │
            └─► find_rules() → solve() / evaluate()
```

---

## Supported Syntax

| Symbol | Meaning        |
|--------|----------------|
| `+`    | AND            |
| `\|`   | OR             |
| `^`    | XOR            |
| `!`    | NOT            |
| `=>`   | Implies        |
| `<=>`  | If and only if |
| `(`    | Open group     |
| `)`    | Close group    |
| `=`    | Initial facts  |
| `?`    | Queries        |
| `#`    | Comment        |

**Operator precedence** (highest → lowest): `!` → `+` → `^` → `|` → `=>` / `<=>`

Facts are single uppercase letters (`A`–`Z`). Whitespace is ignored. Comments can appear inline.

---

## Getting Started

### Requirements

- Python 3.8+
- No external dependencies

### Run

```bash
cd src
python motor.py
```

The engine reads `../file.txt` by default. To use a different input file, update the `path` variable in `main()`.

---

## Input File Format

```
# Rules
A + B => C          # A and B implies C
C | D => E          # C or D implies E
A ^ B => F          # A xor B implies F
A <=> B             # A if and only if B

# Initial facts (true at start)
=AB

# Queries
?CEF
```

- One rule per line
- Facts are single uppercase letters
- `=` followed by letters sets the initial facts — bare `=` means no facts are initially true
- `?` followed by letters defines the queries
- `#` starts a comment, can appear inline

---

## Example

**Input:**

```
C => E
A + B + C => D
A | B => C
A + !B => F
V ^ W => X
A + B => Y + Z
=ABG
?GVX
```

**Output:**

```
G : True
V : Undetermined
X : False
```

---

## Project Structure

```
proplogic/
├── src/
│   ├── motor.py          # Entry point and inference engine
│   ├── node.py           # AST node types
│   ├── tokenizer.py      # Lexer
│   ├── tree_parser.py    # Recursive descent parser
│   └── utils.py          # Rule matching and tree utilities
├── file.txt              # Sample input file
├── .gitignore
└── README.md
```