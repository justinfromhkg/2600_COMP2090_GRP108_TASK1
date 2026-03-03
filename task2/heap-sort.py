# heap_sort.py
# Heap Sort Algorithm Implementation
# Uses Max-Heap property to sort an array in ascending order in-place

def heap_sort(arr):
    """
    Sort an array in ascending order using Heap Sort.
    
    Phase 1: Build Max-Heap from array - O(n)
    Phase 2: Extract elements one by one - O(n log n)
    
    Overall Time Complexity: O(n log n)
    Space Complexity: O(1) — in-place sorting
    """
    n = len(arr)

    # Phase 1: Build Max-Heap
    # Start from the last non-leaf node (index n//2 - 1) and sift down
    for i in range(n // 2 - 1, -1, -1):
        _sift_down_max(arr, n, i)
    # After this phase, arr[0] is the largest element

    # Phase 2: Extract elements from heap one by one
    for i in range(n - 1, 0, -1):
        # Move current root (max element) to end
        arr[0], arr[i] = arr[i], arr[0]
        # Sift down on the reduced heap (size = i)
        _sift_down_max(arr, i, 0)

    return arr


def _sift_down_max(arr, heap_size, i):
    """
    Sift down to maintain Max-Heap property within heap_size.
    The largest value among current node and its children moves up.
    
    Parameters:
        arr       : The array representing the heap
        heap_size : Current size of the heap portion
        i         : Index to sift down from
    """
    largest = i          # Assume current node is the largest
    left = 2 * i + 1     # Left child index
    right = 2 * i + 2    # Right child index

    # Check if left child exists and is larger than current largest
    if left < heap_size and arr[left] > arr[largest]:
        largest = left

    # Check if right child exists and is larger than current largest
    if right < heap_size and arr[right] > arr[largest]:
        largest = right

    # If largest is not the current node, swap and continue sifting down
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _sift_down_max(arr, heap_size, largest)