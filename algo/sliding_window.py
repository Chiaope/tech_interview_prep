"""
Sliding window problem is basically like a rolling window that move over the data set with a fixed window.
"""

"""
Given an array of integers, find the maximum sum of a subarray of size k.
Example:
Input: arr = [1, 2, 3, 4, 5], k = 2
Output: 9
"""


from collections import deque


if __name__ == "__main__":
    arr = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    dq = deque()
    results = []
    for i in range(len(arr)):
        if len(dq) > 0 and dq[0] < i - k + 1:
            dq.popleft()
        while len(dq) > 0 and arr[i] > arr[dq[-1]]:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            results.append(arr[dq[0]])
    print(results)
