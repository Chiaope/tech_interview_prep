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
    # iterate through the indexes of the array because we only want the index
    # using index will speed up the process because we can use the index to get the value from the array
    for i in range(len(arr)):
        # check if left most index is out of the window, if so pop it from the left
        if len(dq) > 0 and dq[0] < i - k + 1:
            dq.popleft()
        # the right most index is the smallest value in the window
        # if the current value is greater than the right most value
        # pop it from the right
        while len(dq) > 0 and arr[i] > arr[dq[-1]]:
            dq.pop()
        # once removed all the smaller values from the right
        # add the current index to the right
        dq.append(i)
        # check if we have at least k elements in the window
        if i >= k - 1:
            # the left most index is the largest value in the window
            results.append(arr[dq[0]])
    print(results)
