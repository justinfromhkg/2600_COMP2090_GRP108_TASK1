class MinHeap:
    def __init__(self):
        # Internal list representation of the heap.
        # In a min-heap, each parent node is <= its children.
        self.heap = []

    def _heapify_down(self, index):  # index: the node to be sifted down
        # Restore the min-heap property by moving the value at `index`
        # down the tree until it is <= both children (or it reaches a leaf).
        size = len(self.heap)

        smallest = index  # assume the current node is the smallest initially

        # Compute indices of left and right children in an array-based heap
        left = 2 * index + 1
        right = 2 * index + 2

        # If left child exists and is smaller than current smallest, update smallest
        if left < size and self.heap[left] < self.heap[smallest]:
            smallest = left

        # If right child exists and is smaller than current smallest, update smallest
        if right < size and self.heap[right] < self.heap[smallest]:
            smallest = right

        # If one of the children is smaller, swap and continue heapifying down
        if smallest != index:
            self.heap[smallest], self.heap[index] = \
            self.heap[index], self.heap[smallest]

            # Continue sifting down from the child position where the swap occurred
            self._heapify_down(smallest)

    def _heapify_up(self, index):
        # Restore the min-heap property by moving the value at `index`
        # up the tree while it is smaller than its parent.
        parent = (index - 1) // 2  # parent index in an array-based heap

        # If not at root and parent is larger, swap with parent
        if index > 0 and self.heap[parent] > self.heap[index]:
            self.heap[parent], self.heap[index] = \
            self.heap[index], self.heap[parent]

            # Continue sifting up from the parent's position
            self._heapify_up(parent)

    def insert(self, value):
        # Add a new value to the heap, then restore heap property by heapifying up.
        self.heap.append(value)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        # Remove and return the minimum element (root of the heap).
        # Steps:
        # 1) Swap root with last element
        # 2) Pop last element (former root)
        # 3) Heapify down from root to restore min-heap property
        if len(self.heap) == 0:
            # Return False to indicate the heap is empty (no min to extract)
            return False

        # Swap the root (min) with the last element
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]

        # Remove the last element (which is the min after the swap)
        min_val = self.heap.pop()

        # Restore the heap property starting from the root
        self._heapify_down(0)

        # Return the extracted minimum value
        return min_val

    def build_heap(self, array):
        # Build a min-heap from an arbitrary array in O(n) time using bottom-up heapify.
        # Copy to avoid modifying the original input array.
        self.heap = array[:]

        # Start from the last non-leaf node and heapify down each node to the root.
        # Last non-leaf node is at index (n // 2 - 1).
        start = len(self.heap) // 2 - 1
        for i in range(start, -1, -1):
            self._heapify_down(i)
