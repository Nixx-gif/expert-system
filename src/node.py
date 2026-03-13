from dataclasses import dataclass
@dataclass
class Leaf:
    value: str
            
@dataclass
class Node:
    kind: str
    left: object = None
    right: object = None