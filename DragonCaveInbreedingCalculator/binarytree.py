#Found on http://stackoverflow.com/questions/5448015/trees-in-python
#Possibly originally from http://cs.uni.edu/~fienup/cs052f10/lectures/lec19_questions.pdf

from collections import deque
class EmptyTree(object):
    """Represents an empty tree."""
    # Supported methods
    def isEmpty(self):
        return True
    def __str__(self):
        return ""
    def __iter__(self):
        """Iterator for the tree."""
        return iter([])
    def preorder(self, lyst):
        return
    def inorder(self, lyst):
        return
    def postorder(self, lyst):
        return

class BinaryTree(object):
    """Represents a nonempty binary tree."""
    # Singleton for all empty tree objects
    THE_EMPTY_TREE = EmptyTree()
    def __init__(self, item):
        """Creates a tree with
        the given item at the root."""
        self._root = item
        self._left = BinaryTree.THE_EMPTY_TREE
        self._right = BinaryTree.THE_EMPTY_TREE
        self._parent = BinaryTree.THE_EMPTY_TREE #added
    def isEmpty(self):
        return False
    def getRoot(self):
        return self._root
    def getLeft(self):
        return self._left
    def getRight(self):
        return self._right
    def getParent(self):
        return self._parent
    def setRoot(self, item):
        self._root = item
    def setParent(self, tree):
        self._parent = tree
    def setLeft(self, tree):
        self._left = tree
        self._left.setParent(self)
    def setRight(self, tree):
        self._right = tree
        self._right.setParent(self)
    def removeLeft(self):
        left = self._left
        left.setParent(BinaryTree.THE_EMPTY_TREE)
        self._left = BinaryTree.THE_EMPTY_TREE
        return left
    def removeRight(self):
        right = self._right
        right.setParent(BinaryTree.THE_EMPTY_TREE)
        self._right = BinaryTree.THE_EMPTY_TREE
        return right
    def __str__(self):
        """Returns a string representation of the tree
        rotated 90 degrees to the left."""
        def strHelper(tree, level):
            result = ""
            if not tree.isEmpty():
                result += strHelper(tree.getRight(), level + 1)
                result += "   " * level
                result += str(tree.getRoot()) + "\n"
                result += strHelper(tree.getLeft(), level + 1)
            return result
        return strHelper(self, 0)
    def __iter__(self):
        """Iterator for the tree."""
        lyst = []
        self.inorder(lyst)
        return iter(lyst)
    def preorder(self, lyst):
        """Adds items to lyst during
        a preorder traversal."""
        lyst.append(self)
        self.getLeft().preorder(lyst)
        self.getRight().preorder(lyst)
    def inorder(self, lyst):
        """Adds items to lyst during
        an inorder traversal."""
        self.getLeft().inorder(lyst)
        lyst.append(self)
        self.getRight().inorder(lyst)
    def postorder(self, lyst):
        """Adds items to lystduring
        a postorder traversal."""
        self.getLeft().postorder(lyst)
        self.getRight().postorder(lyst)
        lyst.append(self)
    def levelorder(self, lyst):
        """Adds items to lyst during
        a levelorder traversal."""
        # levelsQueue = LinkedQueue()
        levelsQueue = deque ([])
        levelsQueue.append(self)
        while levelsQueue != deque():
            node = levelsQueue.popleft()
            lyst.append(node.getRoot())
            left = node.getLeft()
            right = node.getRight()
            if not left.isEmpty():
                levelsQueue.append(left)
            if not right.isEmpty():
                levelsQueue.append(right)
    def find(self, string):
        for node in iter(self):
            if (node.getRoot() == string):
                return node
        return BinaryTree.THE_EMPTY_TREE