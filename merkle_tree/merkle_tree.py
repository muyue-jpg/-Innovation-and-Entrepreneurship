
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 16:06:34 2022

@author: lenovo
"""

import hashlib
import random


#叶节点
class Node:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.parent = None
        self.value = value
        self.hash = hashlib.sha256(('0x00'+value).encode('utf-8')).hexdigest()
#MerkleTree:
class MerkleTree:
    def __init__(self,value):
        self.leaves = value
        self.root = None
    #创建merkle树
    def buildTree(self): 
        allnodes = []
        for i in self.leaves:
            allnodes.append(i)
        while len(allnodes) != 1:
            temp = []
            for i in range(0, len(allnodes), 2):
                leftnode = allnodes[i]
                if i+1 < len(allnodes):
                    rightnode = allnodes[i+1]
                else:
                    temp.append(allnodes[i])
                    break

                parentValue = leftnode.hash + rightnode.hash
                parent = Node(parentValue)
                parent.hash = hashlib.sha256(('0x01'+parentValue).encode('utf-8')).hexdigest()
                leftnode.parent = parent
                rightnode.parent = parent
                parent.left = leftnode
                parent.right = rightnode
                temp.append(parent)
            allnodes = temp
        self.root = allnodes[0]
    #获取根节点的哈希值
    def getRoot(self)-> str:
         return self.root.hash
     
    #为指定元素建立包含证明
    def check_inclusion(self, value, Hash):
        arr = Hash.split()
        hash_node = hashlib.sha256(('0x00'+value).encode('utf-8')).hexdigest()
        if arr[1][0] == '0':
            tmp = hashlib.sha256((arr[1][1:] + hash_node).encode('utf-8')).hexdigest()
        elif arr[1][0] == '1':
            tmp = hashlib.sha256((hash_node + arr[1][1:]).encode('utf-8')).hexdigest()
        for i in range(2, len(arr)):
            hash_node = tmp
            if arr[i][0] == '0':
                tmp = hashlib.sha256((arr[i][1:] + hash_node).encode('utf-8')).hexdigest()
            elif arr[i][0] == '1':
                tmp = hashlib.sha256((hash_node + arr[i][1:]).encode('utf-8')).hexdigest()
        if tmp == arr[0]:
            return True
        else:
            return False

#构建具有10w叶节点的Merkle树
ls = []
for i in range(100000):
    ls.append(Node(''.join(random.sample('0123456789abcdefghijklmnopqrstuvwxyz',5))))
merkleTree=MerkleTree(ls)
merkleTree.buildTree()
print("Root: ",merkleTree.getRoot())
#检查是否包含
value = 'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
Hash= "9ca619dd4a13d02391aeb48fa9dd0a56f6fcf7ed0bc7311c45e64c052eca7133 1ba915e042e9aafcd4348b060345025ef2eb8f93d4fc7fe1719b9a7e1c1034be 451f7cb426ffa960fdad0301d4f4ccf4107751dfbe878cc5a71824f72b4d67bc"
print("#检查是否包含")
print("value=",value)
print("结果为",merkleTree.check_inclusion(value, Hash))


          
