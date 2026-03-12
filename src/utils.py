from node import Node, Leaf

def print_tree(node, prefix="", is_last=True, is_root=True):
    if node is None:
        return

    connector = "" if is_root else ("└── " if is_last else "├── ")
    child_prefix = prefix + ("" if is_root else ("    " if is_last else "│   "))

    if isinstance(node, Leaf):
        print(prefix + connector + f"\033[92m{node.value}\033[0m")  # vert
    elif isinstance(node, Node):
        print(prefix + connector + f"\033[94m[{node.type}]\033[0m")  # bleu
        children = [c for c in [node.left, node.right] if c is not None]
        for idx, child in enumerate(children):
            print_tree(child, child_prefix, idx == len(children) - 1, False)
        
        
def find_rules(rules_tree, query):
    found = []
    for tree in rules_tree:
        
        if tree.type == "IMPLIES":
            if contains(tree.right, query):
                found.append((tree.left, tree.right, is_ambiguous(tree.right)))
                #print("query :", query , found)

        if tree.type == "IFF":
            if contains(tree.right, query):
                found.append((tree.left, tree.right, is_ambiguous(tree.right)))
            if contains(tree.left, query):
                found.append((tree.right, tree.left, is_ambiguous(tree.left)))

    return found

def contains(node, query):
    if isinstance(node, Leaf):
        if node.value == query:
            return True
    if isinstance(node, Node):
        return contains(node.left, query) or contains(node.right, query)
    return False

def is_ambiguous(node):
    if isinstance(node, Node):
        if node.type == "XOR" or node.type == "OR":
            return True
        return is_ambiguous(node.left) or is_ambiguous(node.right)
    return False