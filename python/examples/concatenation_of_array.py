# LeetCode 1929 — Concatenation of Array
# Given an integer array nums, return an array of length 2n that
# consists of nums concatenated to itself.

def get_concatenation(nums):
    n = len(nums)
    result = []
    for i in range(n):
        result.append(nums[i])
    for i in range(n):
        result.append(nums[i])
    return result


def show(arr):
    return str(arr)


# ---- Tests ----
print("Test 1:", show(get_concatenation([1, 2, 1])))   # [1, 2, 1, 1, 2, 1]
print("Test 2:", show(get_concatenation([1, 3, 2, 1])))# [1, 3, 2, 1, 1, 3, 2, 1]
print("Test 3:", show(get_concatenation([])))           # []
print("Test 4:", show(get_concatenation([5])))          # [5, 5]
print("Test 5:", show(get_concatenation([0, 0, 0])))    # [0, 0, 0, 0, 0, 0]
