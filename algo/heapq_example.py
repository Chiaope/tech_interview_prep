"""
Heapq module provides an implementation of the heap queue algorithm, also known as the priority queue algorithm.
This is useful for implementing efficient priority queues, where the smallest element is always at the front of the queue.
If you want to implement a max heap, you can invert the values by multiplying them by -1 before pushing them onto the heap.
"""

import heapq

if __name__ == "__main__":
    numbers = [21, 1, 45, 78, 3, 5]

    # This will create a min heap from the list of numbers inplace
    heapq.heapify(numbers)

    print(f"Min heap: {numbers}")

    heapq.heappush(numbers, 8)
    print(f"Min heap after pushing 8: {numbers}")
    
    smallest = heapq.heappop(numbers)
    print(f"Smallest element popped from the heap: {smallest}")
    print(f"Min heap after popping the smallest element: {numbers}")
    
    top_3_smallest = heapq.nsmallest(3, numbers)
    print(f"Top 3 smallest elements: {top_3_smallest}")
    
    top_3_largest = heapq.nlargest(3, numbers)
    print(f"Top 3 largest elements: {top_3_largest}")