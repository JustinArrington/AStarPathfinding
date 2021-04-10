# A Python program to demonstrate common binary heap operations

# Import the heap functions from python library
from heapq import heappush, heappop


# heappop - pop and return the smallest element from heap
# heappush - push the value item onto the heap, maintaining
#             heap invarient
# heapify - transform list into heap, in place, in linear time

# A class for Min Heap
class PriorityQueue:

    # Constructor to initialize a heap
    def __init__(self):
        self.heap = []

    @staticmethod
    def parent(i):
        return (i - 1) / 2

    # Inserts a new key 'k'
    def put(self, k):
        heappush(self.heap, k)

    def size(self):
        return len(self.heap)

    # Remove minimum element from min heap
    def get(self):
        return heappop(self.heap)
    # Get the minimum element from the heap
    def peek(self):
        try:
            return self.heap[0]
        except IndexError:
            return None
