from MaxHeap import MaxHeap  # import the MaxHeap class (assumed defined in MaxHeap.py)
from MinHeap import MinHeap  # import the MinHeap class (assumed defined in MinHeap.py)

class Heap:
    # A small wrapper class intended to create either a MinHeap or a MaxHeap
    # based on the string argument passed to the constructor.
    def __init__(self, max_or_min):
        # `max_or_min` is expected to be a string like "min" or "max".
        # `.lower()` allows inputs like "Min", "MIN", etc.
        if max_or_min.lower() == "min":
            # If the user requests a min-heap, create/store a MinHeap instance.
            # (Note: this line assumes MinHeap is available as self.MinHeap, which
            # typically would be just MinHeap() since it was imported above.)
            self.Heap = self.MinHeap()
        elif max_or_min.lower() == "max":
            # If the user requests a max-heap, create/store a MaxHeap instance.
            # (Note: this line assumes MaxHeap is available as self.MaxHeap, which
            # typically would be just MaxHeap() since it was imported above.)
            self.Heap = self.MaxHeap()
