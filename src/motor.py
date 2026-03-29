from node import Node, Leaf
from tokenizer import tokenize
from tree_parser import parse_implies
from utils import find_rules, Match


def main():
    path = "../file.txt"
    lines = read_files(path)
    rules, facts, queries = parse(lines)
    trees = build_trees(rules)
    resolve(trees, facts, queries)


def read_files(path):
    with open(path) as f:
        lines = f.read().split('\n')
    return [line.split('#')[0].strip() for line in lines if line.split('#')[0].strip()]


def parse(text):
    """
    Parse the cleaned lines of an input file into rules, facts, and queries.

    Lines starting with '=' define initial facts (true propositions).
    Lines starting with '?' define queries to resolve.
    All other lines are treated as inference rules.

    Args:
        text (list[str]): Cleaned lines (comments and blank lines already removed).

    Returns:
        tuple:
            - rules (list[str]): Raw rule strings to be tokenized and parsed.
            - facts (set[str]): Set of initially true fact identifiers.
            - queries (set[str]): Set of fact identifiers to query.
    """
    queries = set()
    facts   = set()
    rules   = []
    for line in text:
        if line[0] == '=':
            facts.update(line[1:])
        elif line[0] == '?':
            queries.update(line[1:])
        else:
            rules.append(line)
    return rules, facts, queries


def build_trees(rules):
    """
    Tokenize and parse each rule string into an expression tree.

    Args:
        rules (list[str]): Raw rule strings (e.g. "A + B => C").

    Returns:
        list[Node]: List of AST root nodes, one per rule.
    """
    trees = []
    for rule in rules:
        tokens = tokenize(rule)
        tree, _ = parse_implies(tokens, 0)
        trees.append(tree)
    return trees


def resolve(trees, facts, queries):
    """
    Resolve each query against the rule trees and initial facts, and print results.

    For each query, a fresh visited set is used to avoid infinite loops.
    Results are printed as "<query> : True/False/Undetermined".

    Args:
        trees (list[Node]): Parsed expression trees for all rules.
        facts (set[str]): Set of initially known true facts.
        queries (set[str]): Set of facts to resolve.
    """
    for query in queries:
        visited = set()
        result = solve(visited, facts, trees, query)
        if result is None:
            print(f"{query} : Undetermined")
        else:
            print(f"{query} : {result}")


def solve(visited, facts, trees, query):
    """
    Recursively determine the truth value of a query using backward chaining.

    Returns True if the query can be proven, False if it cannot,
    or None if the result is indeterminate (ambiguous conclusion).

    Args:
        visited (set[str]): Facts currently being resolved (cycle detection).
        facts (set[str]): Set of initially known true facts.
        trees (list[Node]): All parsed rule trees.
        query (str): The fact to resolve.

    Returns:
        bool | None: True, False, or None (undetermined).
    """
    if query in facts:
        return True
    if query in visited:
        return False
    visited.add(query)
    undetermined = False
    for match in find_rules(trees, query):
        result = evaluate(visited, facts, trees, match.premise)
        if result is True and not match.ambiguous:
            return True
        if result is True and match.ambiguous:
            undetermined = True
        if result is None:
            undetermined = True
    return None if undetermined else False


def evaluate(visited, facts, trees, node):
    """
    Recursively evaluate an AST node to a truth value.

    Handles leaf nodes (facts), NOT, AND, OR, and XOR operators.
    Propagates None (undetermined) if any operand is undetermined.

    Args:
        visited (set[str]): Facts currently being resolved (cycle detection).
        facts (set[str]): Set of initially known true facts.
        trees (list[Node]): All parsed rule trees.
        node (Node | Leaf): The AST node to evaluate.

    Returns:
        bool | None: True, False, or None (undetermined).

    Raises:
        ValueError: If an unknown node kind is encountered.
    """
    if isinstance(node, Leaf):
        return solve(visited, facts, trees, node.value)
    if node.kind == "NOT":
        val = evaluate(visited, facts, trees, node.left)
        return None if val is None else not val
    left  = evaluate(visited, facts, trees, node.left)
    right = evaluate(visited, facts, trees, node.right)
    if left is None or right is None:
        return None
    if node.kind == "AND":
        return left and right
    if node.kind == "OR":
        return left or right
    if node.kind == "XOR":
        return left ^ right
    raise ValueError(f"Type de node inconnu : {node.kind}")


if __name__ == "__main__":
    main()