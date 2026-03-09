# Task 2 — Self-Study: Heap & Heap Sort

A self-study report and implementation of the **Heap** data structure and **Heap Sort** algorithm in Python, as part of the COMP2090SEF Course Project (2026 Spring).

---

## Files

| File | Description |
|---|---|
| `MinHeap.py` | Min-Heap ADT implementation |
| `MaxHeap.py` | Max-Heap ADT implementation |
| `Heap.py` | Unified wrapper class for both Min-Heap and Max-Heap |
| `HeapSort.py` | Heap Sort algorithm implementation with demo |

---

## Data Structure: Heap

A **Heap** is an array-based complete binary tree that satisfies the **heap property**:
- **Max-Heap:** Every node is ≥ its children → the root is always the **maximum**.
- **Min-Heap:** Every node is ≤ its children → the root is always the **minimum**.

Both variants are implemented and accessible through a unified `Heap` wrapper class.

### Abstract Data Type (ADT)

#### Min-Heap (`MinHeap.py`)

| Method | Description | Time Complexity |
|---|---|---|
| `insert(value)` | Add a new element and restore heap property upward | O(log n) |
| `extract_min()` | Remove and return the minimum (root) element | O(log n) |
| `build_heap(array)` | Build a heap from a list using Floyd's algorithm | O(n) |
| `_heapify_up(index)` | Sift a node up to restore the heap property | O(log n) |
| `_heapify_down(index)` | Sift a node down to restore the heap property | O(log n) |

#### Max-Heap (`MaxHeap.py`)

| Method | Description | Time Complexity |
|---|---|---|
| `insert(value)` | Add a new element and restore heap property upward | O(log n) |
| `extract_max()` | Remove and return the maximum (root) element | O(log n) |
| `build_heap(array)` | Build a heap from a list using Floyd's algorithm | O(n) |
| `_heapify_up(index)` | Sift a node up to restore the heap property | O(log n) |
| `_heapify_down(index)` | Sift a node down to restore the heap property | O(log n) |

### Key Operations Explained

Both heap variants are built on two core operations: **heapify up** (used after insertion) and **heapify down** (used after extraction or during build).

**`_heapify_up` — used in `insert()`**

After appending a new element at the end of the array, it is compared with its parent and swapped upward until the heap property is restored.

```python
# MinHeap version
def _heapify_up(self, index):
    parent = (index - 1) // 2
    if index > 0 and self.heap[parent] > self.heap[index]:
        self.heap[parent], self.heap[index] = \
        self.heap[index], self.heap[parent]
        self._heapify_up(parent)
```

**`_heapify_down` — used in `extract_min/max()` and `build_heap()`**

After swapping the root with the last element (or during build), the new root is compared with its children and sifted downward until the heap property is restored.

```python
# MinHeap version
def _heapify_down(self, index):
    size = len(self.heap)
    smallest = index
    left = 2 * index + 1
    right = 2 * index + 2

    if left < size and self.heap[left] < self.heap[smallest]:
        smallest = left
    if right < size and self.heap[right] < self.heap[smallest]:
        smallest = right

    if smallest != index:
        self.heap[smallest], self.heap[index] = \
        self.heap[index], self.heap[smallest]
        self._heapify_down(smallest)
```

### Unified Wrapper: `Heap.py`

The `Heap` class provides a single entry point to instantiate either a Min-Heap or Max-Heap by passing a string argument:

```python
from Heap import Heap

min_heap = Heap("min")   # Creates a MinHeap
max_heap = Heap("max")   # Creates a MaxHeap
```

### Possible Applications

- **Priority Queues** — Always access the highest or lowest priority element in O(log n).
- **Graph Algorithms** — Used in Dijkstra's shortest path and Prim's MST algorithms.
- **Scheduling Systems** — Task schedulers that always process the most urgent job first.
- **Median Maintenance** — A combination of Min-Heap and Max-Heap can track the running median of a data stream.

---

## Algorithm: Heap Sort

Heap Sort is a **comparison-based, in-place** sorting algorithm that uses a Max-Heap to sort an array in ascending order.

### How It Works

**Step 1 — Build a Max-Heap** from the unsorted array using Floyd's bottom-up algorithm, starting from the last non-leaf node. This takes **O(n)** time.

**Step 2 — Repeatedly extract the maximum** by swapping the root (the maximum element) with the last element of the current heap, shrinking the heap size by 1, and restoring the heap property with `_heapify`. Repeat until the heap is empty. This takes **O(n log n)** time.

```
Initial array:  [4, 10, 3, 5, 1]

After Step 1 (Max-Heap):  [10, 5, 3, 4, 1]

Iteration 1: swap root↔last → [1, 5, 3, 4, | 10] → heapify → [5, 4, 3, 1, | 10]
Iteration 2: swap root↔last → [1, 4, 3, | 5, 10] → heapify → [4, 1, 3, | 5, 10]
Iteration 3: swap root↔last → [3, 1, | 4, 5, 10] → heapify → [3, 1, | 4, 5, 10]
Iteration 4: swap root↔last → [1, | 3, 4, 5, 10] → heapify → [1, | 3, 4, 5, 10]

Sorted array: [1, 3, 4, 5, 10]  ✓
```

### Implementation

```python
def HeapSort(array):
    n = len(array)

    # Step 1: Build Max-Heap (start from last non-leaf node)
    for i in range(n // 2 - 1, -1, -1):
        _heapify(array, n, i)

    # Step 2: Extract max repeatedly and place at end
    for i in range(n - 1, 0, -1):
        array[0], array[i] = array[i], array[0]  # move max to end
        _heapify(array, i, 0)                     # restore heap on reduced array

def _heapify(array, length, index):
    largest = index
    left = 2 * index + 1
    right = 2 * index + 2

    if left < length and array[left] > array[largest]:
        largest = left
    if right < length and array[right] > array[largest]:
        largest = right

    if largest != index:
        array[largest], array[index] = array[index], array[largest]
        _heapify(array, length, largest)  # continue sifting down
```

### Complexity Analysis

| Case | Time Complexity | Space Complexity | Stable? |
|---|---|---|---|
| Best | O(n log n) | O(1) | No |
| Average | O(n log n) | O(1) | No |
| Worst | O(n log n) | O(1) | No |

- **Time:** Building the Max-Heap takes O(n); extracting the maximum n times takes O(log n) each → **O(n log n) overall in all cases**.
- **Space:** Sorting is done **in-place** with no extra array required → **O(1)**.
- **Stability:** Heap Sort is **not stable** — equal elements may be reordered due to non-adjacent swaps during heapification.

---

## How to Run

```bash
python3 HeapSort.py
```

**Example output:**
```
Before sorting: [42, 17, 65, 3, 89, 28, 54, 11, 76, 36]
After sorting:  [3, 11, 17, 28, 36, 42, 54, 65, 76, 89]
```

---

## References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009). *Introduction to Algorithms* (3rd ed.). MIT Press.
- GeeksforGeeks. (n.d.). *Heap Sort*. https://www.geeksforgeeks.org/heap-sort/
- Python Documentation. https://docs.python.org/3/
