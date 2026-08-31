# LeetCode 268 — Missing Number
# Given an array of n distinct integers in the range [0, n], return
# the only number in the range that is missing from the array.
# Approach: the sum of 0..n is n*(n+1)/2. Subtract every number in
# the array; the remainder is the missing one.
# O(n) time, O(1) space.

def missing_number(nums):
    n = len(nums)
    expected = n * (n + 1) // 2
    actual = 0
    for x in nums:
        actual = actual + x
    return expected - actual


# ---- Tests ----
print("Test 1:", missing_number([3, 0, 1]))     # 2
print("Test 2:", missing_number([0, 1]))        # 2
print("Test 3:", missing_number([9, 6, 4, 2, 3, 5, 7, 0, 1]))  # 8
print("Test 4:", missing_number([0]))           # 1
print("Test 5:", missing_number([1]))           # 0
print("Test 6:", missing_number([4, 2, 1, 0]))  # 3
