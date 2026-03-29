from node import Node, Leaf
from dataclasses import dataclass


@dataclass
class Match:
    premise: object
    conclusion: object
    ambiguous: bool


def find_rules(trees, query):
    """
    Search all rule trees for rules whose conclusion contains the given query.

    For IMPLIES rules (A => B): matches if the right-hand side contains the query.
    For IFF rules (A <=> B): matches both directions.

    Args:
        trees (list[Node]): All parsed rule trees.
        query (str): The fact identifier to search for in rule conclusions.

    Returns:
        list[Match]: All matches found, each containing the premise, conclusion,
                    and whether the conclusion is ambiguous (OR/XOR).
    """
    found = []
    for tree in trees:
        if tree.kind == "IMPLIES":
            if contains(tree.right, query):
                found.append(Match(tree.left, tree.right, is_ambiguous(tree.right)))
        elif tree.kind == "IFF":
            if contains(tree.right, query):
                found.append(Match(tree.left, tree.right, is_ambiguous(tree.right)))
            if contains(tree.left, query):
                found.append(Match(tree.right, tree.left, is_ambiguous(tree.left)))
    return found


def contains(node, query):
    """
    Recursively check whether an AST node contains a given fact identifier.

    NOT nodes are excluded: a rule concluding !V does not prove V.

    Args:
        node (Node | Leaf): The AST node to search.
        query (str): The fact identifier to look for.

    Returns:
        bool: True if the node contains the query as a positive fact, False otherwise.
    """
    if isinstance(node, Leaf):
        return node.value == query
    if isinstance(node, Node):
        if node.kind == "NOT":
            return False
        return contains(node.left, query) or contains(node.right, query)
    return False


def is_ambiguous(node):
    """
    Determine whether an AST node is ambiguous as a conclusion.

    A conclusion is ambiguous if it contains an OR or XOR operator,
    meaning the inference engine cannot assign a definite value to a
    specific fact within it.

    Args:
        node (Node | Leaf): The AST node to inspect.

    Returns:
        bool: True if the node contains OR or XOR, False otherwise.
    """
    if isinstance(node, Node):
        if node.kind in ("XOR", "OR"):
            return True
        return is_ambiguous(node.left) or is_ambiguous(node.right)
    return False


def print_tree(node, prefix="", is_last=True, is_root=True):
    """
    Recursively print an AST as a colored tree to stdout.

    Leaf nodes are printed in green, operator nodes in blue.
    Uses box-drawing characters to represent the tree structure.

    Args:
        node (Node | Leaf | None): The current node to print.
        prefix (str): The indentation prefix accumulated from parent nodes.
        is_last (bool): Whether this node is the last child of its parent.
        is_root (bool): Whether this node is the root of the tree.
    """
    if node is None:
        return

    connector = "" if is_root else ("└── " if is_last else "├── ")
    child_prefix = prefix + ("" if is_root else ("    " if is_last else "│   "))

    if isinstance(node, Leaf):
        print(prefix + connector + f"\033[92m{node.value}\033[0m")
    elif isinstance(node, Node):
        print(prefix + connector + f"\033[94m[{node.kind}]\033[0m")
        children = [c for c in [node.left, node.right] if c is not None]
        for idx, child in enumerate(children):
            print_tree(child, child_prefix, idx == len(children) - 1, False)