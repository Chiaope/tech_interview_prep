"""
Two pointer problem is used to solve problems that involve searching for pairs in a sorted array or linked list. 
The two pointer technique involves using two pointers to traverse the data structure, one starting from the beginning and the other from the end, and moving them towards each other based on certain conditions. 
This approach can help reduce the time complexity of certain problems from O(n^2) to O(n).
"""

"""
Given a sorted array of integers, find two numbers such that they add up to a specific target number.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
Example:
Input: numbers = [1, 2, 3, 4, 6, 8, 8, 11], target = 16
Output: [5, 6]
"""

if __name__ == '__main__':
    numbers = [1, 2, 3, 4, 6, 8, 8, 11]
    target = 16
    
    left = 0
    right = len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            print(f"Output: [{left}, {right}]")
            break
        elif current_sum < target:
            left += 1
        else:
            right -= 1