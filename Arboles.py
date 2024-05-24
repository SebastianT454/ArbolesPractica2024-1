class BinaryNode:
    def __init__(self, index, value) -> None:
        self.value = value
        self.index = index
        self.left = None
        self.right = None

    def __repr__(self) -> str:
        return str(self.value)
    
class ExpressionAnalysisTree:
    def __init__(self) -> None:
        self.root = None
    
    def insert(self, Node, NodeIndex, NodeValue):
        if not self.root:
            self.root = BinaryNode(NodeIndex, NodeValue)
            return
        
        if NodeIndex < Node.index:
            if Node.left is None:
                Node.left = BinaryNode(NodeIndex, NodeValue)
                return
            else:
                return self.insert(Node.left, NodeIndex, NodeValue)
                        
        else:
            if Node.right is None:
                Node.right = BinaryNode(NodeIndex, NodeValue)
                return
            else:
                return self.insert(Node.right, NodeIndex, NodeValue)

    def evaluate(self, node):
        if node.left is None and node.right is None:
            return int(node.value)
        
        valor_izquierdo = self.evaluate(node.left)
        valor_derecho = self.evaluate(node.right)
        
        if node.value == '+':
            return valor_izquierdo + valor_derecho
        elif node.value == '-':
            return valor_izquierdo - valor_derecho
        elif node.value == '*':
            return valor_izquierdo * valor_derecho
        elif node.value == '/':
            return valor_izquierdo / valor_derecho

    def print(self, node, prefix="", is_left=True):
        if not node:
            print("Empty Tree")
            return
        if node.right:
            self.print(node.right, prefix + ("│   " if is_left else "    "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(node.value))
        if node.left:
            self.print(node.left, prefix + ("    " if is_left else "│   "), True)

"""
Bst = ExpressionAnalysisTree()
Bst.insert(Bst.root, 3, "-")
Bst.insert(Bst.root, 1, "+")
Bst.insert(Bst.root, 0, "5")
Bst.insert(Bst.root, 2, "6")
Bst.insert(Bst.root, 7, "/")
Bst.insert(Bst.root, 8, "5")
Bst.insert(Bst.root, 5, "*")
Bst.insert(Bst.root, 4, "3")
Bst.insert(Bst.root, 6, "3")
Bst.print(Bst.root)

print(Bst.evaluate(Bst.root))
"""
