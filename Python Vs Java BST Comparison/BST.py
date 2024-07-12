import time
from random import randint

startTime = (time.time()) * 1000


class BSTNode:
    def __init__(self, num):
        self.left = None
        self.right = None
        self.key = num


def insert(root, bstNode):
    if root is None:
        root = bstNode

    else:
        if root.key < bstNode.key:
            if root.right is None:
                root.right = bstNode

            else:
                insert(root.right, bstNode)

        else:
            if root.left is None:
                root.left = bstNode

            else:
                insert(root.left, bstNode)


def displayInOrder(root):
    if root:
        displayInOrder(root.left)
        print(root.key)
        displayInOrder(root.right)


root = BSTNode(10)
i = 0

while i < 9:
    number = randint(0, 1000)
    insert(root, BSTNode(number))
    i += 1

displayInOrder(root)

endTime = (time.time()) * 1000
deltaTime = endTime - startTime
print(deltaTime)
