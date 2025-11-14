import sys 
import unittest 
from typing import * 
from dataclasses import dataclass 
import math 
import matplotlib.pyplot as plt 
import numpy as np 
import random 
import time
sys.setrecursionlimit(10**6) 
 
from bst import * 
 
TREES_PER_RUN : int = 10000 

def random_tree(n: int) -> BST:
    ComesBefore = lambda a, b: a < b
    bst = BST(ComesBefore, None)
    
    for _ in range(n):
        bst = insert(bst, random.random())
    return bst

def generate_height_graph():
    print("Generating height vs. N graph...")
    
    n_max = 300 

    x_coords = np.linspace(0, n_max, 50, dtype=int)
    y_coords = []
    
    for n in x_coords:
        if n == 0:
            avg_height = -1
        else:
            total_height = 0
            for _ in range(TREES_PER_RUN):
                t = random_tree(n)
                total_height += height(t)
            avg_height = total_height / TREES_PER_RUN
        
        y_coords.append(avg_height)
        
    print("Height data generated. Plotting...")
    
    x_numpy: np.ndarray = np.array(x_coords)
    y_numpy: np.ndarray = np.array(y_coords)
    
    plt.plot(x_numpy, y_numpy, label='Average Height')
    
    log_x = x_coords[1:] 
    log_y = [2.5 * math.log2(x) for x in log_x] 
    plt.plot(log_x, log_y, label='O(log N) reference (scaled)', linestyle='--')
    
    plt.xlabel("N (Number of Nodes)")
    plt.ylabel("Average Tree Height")
    plt.title("Average BST Height vs. Number of Nodes (N)")
    plt.grid(True)
    plt.legend()
    plt.show()

def generate_insert_time_graph():
    print("Generating insert time vs. N graph...")
    
    n_max = 300
    
    x_coords = np.linspace(0, n_max, 50, dtype=int)
    y_coords = []
    
    for n in x_coords:
        trees = [random_tree(n) for _ in range(TREES_PER_RUN)]
        values_to_insert = [random.random() for _ in range(TREES_PER_RUN)]
        
        start_time = time.perf_counter()
        
        for i in range(TREES_PER_RUN): 
            insert(trees[i], values_to_insert[i])
            
        end_time = time.perf_counter()
        
        total_time = end_time - start_time
        avg_time = total_time / TREES_PER_RUN
        y_coords.append(avg_time)
        
    print("Insert time data generated. Plotting...")
    
    x_numpy: np.ndarray = np.array(x_coords)
    y_numpy: np.ndarray = np.array(y_coords)
    
    plt.plot(x_numpy, y_numpy, label='Average Insert Time')
    
    plt.xlabel("N (Number of Nodes)")
    plt.ylabel("Average Time to Insert (seconds)")
    plt.title("Average Insert Time vs. Number of Nodes (N)")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    generate_height_graph()
    generate_insert_time_graph()
