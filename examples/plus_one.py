# LeetCode 66 — Plus One
# Given an array of digits representing a non-negative integer,
# add 1 to the integer and return the digits.
# Approach: iterate from the least significant digit (right end),
# add 1, propagate any carry. If we carry all the way past the most
# significant digit, prepend a 1.
# O(n) time, O(1) extra space (or O(n) for the rare prepend case).

def plus_one(digits):
    n = len(digits)
    i = n - 1
    while i >= 0 and digits[i] == 9:
        digits[i] = 0
        i = i - 1
    if i < 0:
        # All digits were 9s, e.g. 999 + 1 = 1000
        result = [1]
        for j in range(n):
            result.append(0)
        return result
    digits[i] = digits[i] + 1
    return digits


def show(arr):
    return str(arr)


# ---- Tests ----
print("Test 1:", show(plus_one([1, 2, 3])))        # [1, 2, 4]
print("Test 2:", show(plus_one([4, 3, 2, 1])))     # [4, 3, 2, 2]
print("Test 3:", show(plus_one([9])))              # [1, 0]
print("Test 4:", show(plus_one([9, 9, 9])))        # [1, 0, 0, 0]
print("Test 5:", show(plus_one([0])))              # [1]
print("Test 6:", show(plus_one([8, 9, 9, 9])))     # [9, 0, 0, 0]
print("Test 7:", show(plus_one([1, 9, 0])))        # [1, 9, 1]
