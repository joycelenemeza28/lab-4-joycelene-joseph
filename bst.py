import sys 
import unittest 
from typing import *
from dataclasses import dataclass 
sys.setrecursionlimit(10**6) 

BinTree = Optional['Node']

@dataclass(frozen=True)
class Node:
    value: Any
    left: BinTree
    right: BinTree

@dataclass(frozen=True)
class BinarySearchTree:
    comes_before: Callable[[Any, Any], bool]
    root: BinTree

def is_empty(bst: BinarySearchTree) -> bool:
    #Takes a BST and returns True if tree is empty, otherwise false
    return bst.root is None

def insert(bst: BinarySearchTree, value: Any) -> BinarySearchTree:
    #Inserts a value into the BST and returns a new BST
    new_root = _insert_helper(bst.comes_before, bst.root, value)
    return BinarySearchTree(bst.comes_before, new_root)

def _insert_helper(comes_before: Callable[[Any, Any], bool], node: BinTree, value: Any) -> Node:
    #Recursive helper for insert, returns a new subtree as a node with the inserted value
    if node is None:
        return Node(value, None, None)
    
    if comes_before(value, node.value):
        new_left = _insert_helper(comes_before, node.left, value)
        return Node(node.value, new_left, node.right)
    
    else:
        new_right = _insert_helper(comes_before, node.right, value)
        return Node(node.value, node.left, new_right)
    
def lookup(bst: BinarySearchTree, value: Any) -> bool:
    #Returns True if the value is in the tree, False otherwise
    return _lookup_helper(bst.comes_before, bst.root, value)

def _lookup_helper(comes_before: Callable[[Any, Any], bool], node: BinTree, value: Any) -> bool:
    #Recursive helper for lookup
    if node is None:
        return False
    if not comes_before(value, node.value) and not comes_before(node.value, value):
        return True
    
    if comes_before(value, node.value):
        return _lookup_helper(comes_before, node.left, value)
    
    else: 
        return _lookup_helper(comes_before, node.right, value)
    
def delete(bst: BinarySearchTree, value: Any) -> BinarySearchTree:
    #Removes one instance of the value from the tree, returning a new BST
    new_root = _delete_helper(bst.comes_before, bst.root, value)
    return BinarySearchTree(bst.comes_before, new_root)

def _find_min(node: Node) -> Any:
    #Helper to find the minimum value in a non-empty subtree
    current = node
    while current.left is not None:
        current = current.left
    return current.value

def _delete_helper(comes_before: Callable[[Any, Any], bool], node: BinTree, value: Any) -> BinTree:
    #Recursive helper for delete, returns the new modified subtree
    if node is None:
        return None
    
    if comes_before(value, node.value):
        new_left = _delete_helper(comes_before, node.left, value)
        return Node(node.value, new_left, node.right)
    
    elif comes_before(node.value, value):
        new_right = _delete_helper(comes_before, node.right, value)
        return Node(node.value, node.left, new_right)
    
    else:
        if node.left is None and node.right is None:
            return None
        elif node.left is None:
            return node.right
        elif node.right is None:
            return node.left
        else:
            successor_val = _find_min(node.right)
            new_right_subtree = _delete_helper(comes_before, node.right, successor_val)
            return Node(successor_val, node.left, new_right_subtree)
        

def height(bst: BinarySearchTree) -> int:
    #Calculates the height of the tree
    return _height_helper(bst.root)

def _height_helper(node: BinTree) -> int:
    #Recursive helper for height
    if node is None:
        return -1
    
    return 1 + max(_height_helper(node.left), _height_helper(node.right))