# min_heap.py
# Min-Heap Data Structure Implementation
# Supports insert, extract_min, peek, and heapify operations

class MinHeap:
    """
    A Min-Heap implemented using a Python list.
    The smallest element is always at index 0 (the root).
    """

    def __init__(self):
        """Initialize an empty heap."""
        self.heap = []

    def insert(self, val):
        """
        Insert a new value into the heap.
        Step 1: Append to the end of the list.
        Step 2: Sift-up to restore the heap property.
        Time Complexity: O(log n)
        """
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def _sift_up(self, i):
        """
        Move element at index i upward until heap property is satisfied.
        Compare with parent; swap if current < parent.
        """
        parent = (i - 1) // 2
        while i > 0 and self.heap[i] < self.heap[parent]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            i = parent
            parent = (i - 1) // 2

    def extract_min(self):
        """
        Remove and return the minimum element (root).
        Step 1: Swap root with last element.
        Step 2: Remove last element.
        Step 3: Sift-down from root to restore heap property.
        Time Complexity: O(log n)
        """
        if not self.heap:
            raise IndexError("Heap is empty.")
        # Swap root with the last element
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        min_val = self.heap.pop()  # Remove the original root
        self._sift_down(0)
        return min_val

    def _sift_down(self, i):
        """
        Move element at index i downward until heap property is satisfied.
        Compare with smaller child; swap if current > smaller child.
        """
        n = len(self.heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i

            # Find the smallest among current, left child, right child
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest == i:
                break  # Heap property satisfied

            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            i = smallest

    def peek(self):
        """Return the minimum value without removing it. O(1)"""
        if not self.heap:
            raise IndexError("Heap is empty.")
        return self.heap[0]

    def heapify(self, arr):
        """
        Build a Min-Heap from an existing list in O(n) time.
        Start from the last non-leaf node and sift-down each node.
        Last non-leaf node is at index (n//2 - 1).
        """
        self.heap = arr[:]  # Copy to avoid mutating original
        n = len(self.heap)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)

    def __str__(self):
        return f"MinHeap: {self.heap}"