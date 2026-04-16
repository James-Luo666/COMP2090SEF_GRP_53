from __future__ import print_function
import math

class MinHeap:
    def __init__(self):
        #Set an empty list for the heap
        self.arr = []

    # Get the index of the left child
    def left(self, i): return 2 * i + 1

    # Get the index of the right child
    def right(self, i): return 2 * i + 2

    # Get the index of the parent
    def parent(self, i): return (i - 1) // 2
    
    # Find the smallest index without deleting it
    def get_min(self):
        return self.arr[0] if self.arr else None
    
    # Insert a new key into the heap
    def insert(self, k):
        self.arr.append(k)
        i = len(self.arr) - 1
        
        # Fix the min heap property by bubbling up
        while i > 0 and self.arr[self.parent(i)] > self.arr[i]:
            p = self.parent(i)
            self.arr[i], self.arr[p] = self.arr[p], self.arr[i]
            i = p


    # Remove and return the root (minimum) element
    def extract_min(self):
        if len(self.arr) <= 0: return None
        if len(self.arr) == 1: return self.arr.pop()
        
        res = self.arr[0]
        # Replace root with the last element and heapify down
        self.arr[0] = self.arr.pop() 
        self.min_heapify(0)
        return res


    # Recursive method to fix the heap property downwards
    def min_heapify(self, i):
        l, r, n = self.left(i), self.right(i), len(self.arr)
        smallest = i
        
        # Find the smallest among root, left child, and right child
        if l < n and self.arr[l] < self.arr[smallest]: smallest = l
        if r < n and self.arr[r] < self.arr[smallest]: smallest = r
          
        # If the root is not the smallest, swap and continue heapifying
        if smallest != i:
            self.arr[i], self.arr[smallest] = self.arr[smallest], self.arr[i]
            self.min_heapify(smallest)

# --- Execution ---
h = MinHeap()

a = int(input("Enter a number. if you want to stop, enter -1:"))
while a != -1:
    h.insert(a)
    a = int(input("Enter a number. if you want to stop, enter -1:"))
else:
    print(h.extract_min(), end=" ") 
    print(h.get_min(), end=" ")
