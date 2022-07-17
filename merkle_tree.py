import os
import hashlib


class Node:
    def __init__(self, left, right, value,content):
        self.left = left
        self.right = right
        self.value = value
        self.content = content
    def hash(val):
        return hashlib.sha256(val.encode("utf-8")).hexdigest()
    def __str__(self):
        return(str(self.value))


class MerkleTree:
    def __init__(self, values):
        self.buildTree(values)
    
    def buildTree(self, leaves):
        leaves = [Node(None, None, Node.hash(e),e) for e in leaves]
        while len(leaves) > 1:
            length = len(leaves)
            for i in range(length//2):
                left = leaves.pop(0)
                right = leaves.pop(0)
                value: str = Node.hash(left.value + right.value)
                print('value:  ',value)
                content: str = left.content + '+'+ right.content
                leaves.append(Node(left, right, Node.hash(value),content))
            if length%2 == 1:
                leaves.append(leaves.pop(0))
            print('leaves')
            print(leaves)
            print()
        self.root = leaves[0]
        
    def showTree(self, node)-> None:
        if node != None:
            if node.left != None:
                print("Left: "+str(node.left))
                print("Right: "+str(node.right))
            else:
                print("Input")
            print("Value: "+str(node.value))
            print("Content: "+str(node.content))
            print("")
            self.showTree(node.left)
            self.showTree(node.right)
    def getRootHash(self)-> str:
         return self.root.value


elems = ['1', '2', '3', '4']
mtree = MerkleTree(elems)
print("Root Hash: "+mtree.getRootHash()+"\n")
mtree.showTree(mtree.root)


elems = ['1', '2', '3', '4', '5', '6', '7','8', '9']
mtree = MerkleTree(elems)
print("Root Hash: "+mtree.getRootHash()+"\n")
mtree.showTree(mtree.root)