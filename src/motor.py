from tree_parser import parse_atom, parse_not, parse_and, parse_or, parse_xor, parse_implies
from node import Node, Leaf
from tokenizer import tokenize
from utils import print_tree, find_rules


def main():
    with open("../file.txt") as f:
        text = f.read()
    text = text.split('\n')
    new = []
    for i in text:
        line = i.split('#')[0].strip()
        if line:
            new.append(line)
    parse(new)
    
    
def parse(text):
    queries = set()
    facts   = set()
    rules   = []
    for i in text:
        if i[0] == '=':
            facts.update(i.strip('='))
        elif i[0] == '?':
            queries.update(i.strip('?'))
        else:
            rules.append(i)
    print(facts)
    print(queries)
    print(rules)
    tokens = []
    for r in rules:
        token = tokenize(r)
        print(token)
        tokens.append(token)
    trees = []
    for t in tokens:
        tree, _ = parse_implies(t, 0)
        trees.append(tree)
        print_tree(tree)
    visited = set()
    for s in queries:
        r = solve(visited, facts, trees, s)
        if r is None:
            print(f"{s} : Undetermined")
            continue
        print(f"{s} : {r}")

def solve(visited, facts, trees, query):
    if query in facts:
        return True
    if query in visited:
        return False
    visited.add(query)
    found_tree = find_rules(trees, query)
    for found in found_tree:
        result = evaluate(visited, facts, trees, found[0])
        if result and not found[2]:
            return True
        if result and found[2]:
            return None
    return False

def evaluate(visited, facts, trees, node):
    if isinstance(node, Leaf):
        return solve(visited, facts, trees, node.value)
    if node.type == "AND":
        return evaluate(visited, facts, trees, node.left) and evaluate(visited, facts, trees, node.right)
    if node.type == "NOT":
        return not evaluate(visited, facts, trees, node.left)
    if node.type == "OR": 
        return evaluate(visited, facts, trees, node.left) or evaluate(visited, facts, trees, node.right)
    if node.type == "XOR":
        return evaluate(visited, facts, trees, node.left) ^ evaluate(visited, facts, trees, node.right)
    
    
    
if __name__ == "__main__":
    main()