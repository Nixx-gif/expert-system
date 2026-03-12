class Node:
    def __init__(self, type, left=None, right=None):
        self.type = type
        self.left = left
        self.right = right
            
class Leaf:
    def __init__(self, value):
        self.value = value