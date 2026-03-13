from node import Node, Leaf
from dataclasses import dataclass

@dataclass
class Match:
    premise: object
    conclusion: object
    ambiguous: bool

def find_rules(trees, query):
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
    if isinstance(node, Leaf):
        return node.value == query
    if isinstance(node, Node):
        return contains(node.left, query) or contains(node.right, query)
    return False

def is_ambiguous(node):
    if isinstance(node, Node):
        if node.kind in ("XOR", "OR"):
            return True
        return is_ambiguous(node.left) or is_ambiguous(node.right)
    return False

def print_tree(node, prefix="", is_last=True, is_root=True):
    if node is None:
        return

    connector = "" if is_root else ("└── " if is_last else "├── ")
    child_prefix = prefix + ("" if is_root else ("    " if is_last else "│   "))

    if isinstance(node, Leaf):
        print(prefix + connector + f"\033[92m{node.value}\033[0m")  # vert
    elif isinstance(node, Node):
        print(prefix + connector + f"\033[94m[{node.kind}]\033[0m")  # bleu
        children = [c for c in [node.left, node.right] if c is not None]
        for idx, child in enumerate(children):
            print_tree(child, child_prefix, idx == len(children) - 1, False)
        
        
