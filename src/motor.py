from tree_parser import parse_atom, parse_not, parse_and, parse_or, parse_xor, parse_implies
from node import Node, Leaf
from tokenizer import tokenize
from utils import print_tree, find_rules, Match

def main():
    with open("../file.txt") as f:
        text = f.read()
    text = text.split('\n')
    new = []
    for i in text:
        line = i.split('#')[0].strip()
        if line:
            new.append(line)
    rules, facts, queries = parse(new)
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
        
def read_files(path):
    with open(path) as f:
        lines = f.read().split('\n')
        return [line.split('#')[0].strip() for line in lines if line.split('#')[0].strip()]
    
def parse(text):
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
    trees = []
    for rule in rules:
        tokens = tokenize(rule)
        tree, _ = parse_implies(tokens, 0)
        print_tree(tree)
        trees.append(tree)
    return trees

def resolve(trees, facts, queries):
    for query in queries:
        visited = set()
        result = solve(visited, facts, trees, query)
        if result is None:
            print(f"{query} : Undetermined")
        else:
            print(f"{query} : {result}")
            

def solve(visited, facts, trees, query):
    if query in facts:
        return True
    if query in visited:
        return False
    visited.add(query)
    for match in find_rules(trees, query):
        result = evaluate(visited, facts, trees, match.premise)
        if result and not match.ambiguous:
            return True
        if result and match.ambiguous:
            return None
        return False

    
def evaluate(visited, facts, trees, node):
    if isinstance(node, Leaf):
        return solve(visited, facts, trees, node.value)
    if node.kind == "NOT":
        val = evaluate(visited, facts, trees, node.left)
        return None if val is None else not val
    left = evaluate(visited, facts, trees, node.left)
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