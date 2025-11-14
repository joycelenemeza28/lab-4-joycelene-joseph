import sys 
import unittest 
from typing import *
from dataclasses import dataclass 
sys.setrecursionlimit(10**6) 

ComesBefore= Callable[[Any,Any],bool]

@dataclass(frozen=True)
class Node:
    value: Any 
    left: 'BinTree'
    right: 'BinTree'

BinTree: TypeAlias= Optional[Node]

@dataclass(frozen=True)
class BST:
    comes_before: ComesBefore
    root: BinTree

#returns true if tree is empty and false otherwise
def is_empty(bst: BST)-> bool:
    return bst.root is None

#helper function for insert
def insert_helper(tree: BinTree, value: Any, comes_before: ComesBefore)-> BinTree:
    if tree is None:
        return Node(value, None, None)
    if comes_before(value, tree.value):
        new_left= insert_helper(tree.left, value, comes_before)
        return Node(tree.value,new_left, tree.right)
    else:
        new_right= insert_helper(tree.right, value, comes_before)
        return Node(tree.value,tree.left, new_right)
    
#adds the value to tree 
def insert(bst: BST,value: Any)-> BST:
    new_root= insert_helper(bst.root, value, bst.comes_before)
    return BST(bst.comes_before, new_root)

#determines if two values are considered equal based on the comes_before function
def is_equal(val_1: Any, val_2: Any, comes_before: ComesBefore)-> bool:
    return(not comes_before(val_1, val_2) and (not comes_before(val_2, val_1)))

#helper function for lookup
def lookup_helper(tree: BinTree, value: Any, comes_before: ComesBefore)-> bool:
    if tree is None:
        return False
    if is_equal(value, tree.value,comes_before):
       return True
    if comes_before(value, tree.value):
        return lookup_helper(tree.left, value, comes_before)
    else:
        return lookup_helper(tree.right, value, comes_before)

#returns true if the value is found, false otherwise 
def lookup(bst: BST, value: Any)-> bool:
    return lookup_helper(bst.root, value, bst.comes_before)
 
#finds the node with the minimum value in a non-empty BinTree
def find_min_node(tree: BinTree)-> Node:
    if tree is None:
        raise ValueError("Cannot find min on an empty tree/subtree")
    if tree.left is None:
        return tree
    return find_min_node(tree.left)

#deletes minimum value node from a non-empty BinTree and returns resulting tree
def delete_min_node(tree: BinTree)-> BinTree:
    if tree is None:
        raise ValueError("Cannot find min on an empty tree/subtree")
    if tree.left is None:
        return tree.right 
    new_left= delete_min_node(tree.left)
    return Node(tree.value, new_left, tree.right)

#helper function for delete
def delete_helper(tree: BinTree, value: Any, comes_before: ComesBefore)-> BinTree:
    if tree is None:
        return None
    if is_equal(value, tree.value, comes_before):
        if tree.left is None:
            return tree.right
        if tree.right is None:
            return tree.left
        successor_node = find_min_node(tree.right)
        successor_value = successor_node.value

        new_right = delete_min_node(tree.right)
        return Node(successor_value, tree.left, new_right)
    if comes_before(value, tree.value):
        new_left= delete_helper(tree.left, value, comes_before)
        return Node(tree.value, new_left, tree.right)
    else:
        new_right = delete_helper(tree.right, value, comes_before)
        return Node(tree.value, tree.left, new_right)
    
#returns a new BST instance 
def delete(bst:BST, value: Any)->BST:
    new_root = delete_helper(bst.root, value, bst.comes_before)
    return BST(comes_before= bst.comes_before, root=new_root)

#helper function for height 
def height_helper(node: BinTree) -> int:
    if node is None:
        return -1
    return 1 + max(height_helper(node.left), height_helper(node.right))

#Calculates the height of the tree
def height(bst: BST) -> int:
    return height_helper(bst.root)