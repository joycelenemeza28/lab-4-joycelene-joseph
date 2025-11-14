import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)
from bst import * 


@dataclass
class Point2:
    x: float
    y: float

def dist_comes_before(p1: Point2, p2: Point2) -> bool:
    dist_sq_1 = p1.x**2 + p1.y**2
    dist_sq_2 = p2.x**2 + p2.y**2
    return dist_sq_1 < dist_sq_2

class BSTTests(unittest.TestCase):
    
    def setUp(self):
        self.cb_int = lambda a, b: a < b
        self.bst_int = BST(self.cb_int, None)
        
        self.cb_str = lambda a, b: a < b
        self.bst_str = BST(self.cb_str, None)
         
        self.cb_point = dist_comes_before
        self.bst_point = BST(self.cb_point, None)

    def test_is_empty(self):
        self.assertTrue(is_empty(self.bst_int))
        self.assertTrue(is_empty(self.bst_str))
        self.assertTrue(is_empty(self.bst_point))
        
        self.assertFalse(is_empty(insert(self.bst_int, 10)))
        self.assertFalse(is_empty(insert(self.bst_str, "hello")))
        p = Point2(3, 4) 
        self.assertFalse(is_empty(insert(self.bst_point, p)))

    def test_insert_and_lookup_int(self):
        bst = self.bst_int
        values = [10, 5, 15, 3, 7, 12, 18]
        for v in values:
            bst = insert(bst, v)
            
        for v in values:
            self.assertTrue(lookup(bst, v))
            
        self.assertFalse(lookup(bst, 0))
        self.assertFalse(lookup(bst, 8))
        self.assertFalse(lookup(bst, 20))

    def test_insert_and_lookup_str(self):
        bst = self.bst_str
        values = ["mango", "apple", "orange", "banana", "plum"]
        for v in values:
            bst = insert(bst, v)
            
        for v in values:
            self.assertTrue(lookup(bst, v))
            
        self.assertFalse(lookup(bst, "grape"))

    def test_insert_and_lookup_point(self):
        bst = self.bst_point
        p1 = Point2(3, 4)  
        p2 = Point2(1, 1)  
        p3 = Point2(10, 0) 
        p4 = Point2(0, 0)  
        p5 = Point2(6, 8)  
        values = [p1, p2, p3, p4, p5]
        
        for v in values:
            bst = insert(bst, v)
            
        for v in values:
            self.assertTrue(lookup(bst, v))
            
        self.assertTrue(lookup(bst, Point2(10, 0)))
        self.assertTrue(lookup(bst, Point2(6, 8)))
        
        self.assertFalse(lookup(bst, Point2(100, 100)))
        self.assertFalse(lookup(bst, Point2(1, 0)))

    def test_delete_int(self):
        bst = self.bst_int
        values = [10, 5, 15, 3, 7, 12, 18]
        for v in values:
            bst = insert(bst, v)
        
        bst = delete(bst, 3)
        self.assertFalse(lookup(bst, 3))
        bst = delete(bst, 15)
        self.assertFalse(lookup(bst, 15))
        self.assertTrue(lookup(bst, 12))
        self.assertTrue(lookup(bst, 18))
        
        bst = delete(bst, 5)
        self.assertFalse(lookup(bst, 5))
        self.assertTrue(lookup(bst, 7)) 
        
        bst = delete(bst, 10)
        self.assertFalse(lookup(bst, 10))
        self.assertTrue(lookup(bst, 12))
        
        bst_before_root_val = bst.root.value
        bst = delete(bst, 999)
        self.assertEqual(bst.root.value, bst_before_root_val)


if __name__ == '__main__':
    unittest.main()