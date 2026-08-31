# LeetCode 189 — Rotate Array
# Given an array, rotate it to the right by k steps in-place.
# k is non-negative. For example, with k=3:
#   [1, 2, 3, 4, 5, 6, 7]  ->  [5, 6, 7, 1, 2, 3, 4]
#
# Approach: triple-reversal. Reversing the entire array puts each
# element k positions away in the right direction. Then reverse the
# first k elements (to put them in the right order) and reverse the
# remaining n - k elements (to put them in the right order too).
#
# Normalize k with modulo n first so k > n still works.
#
# Since this interpreter does not support slicing, we use a helper
# to reverse nums[i : j] in-place.

def reverse_range(nums, i, j):
    """Reverse nums[i : j] in place using a two-pointer swap.
    The exclusive upper bound j matches Python slice semantics."""
    left = i
    right = j - 1
    while left < right:
        temp = nums[left]
        nums[left] = nums[right]
        nums[right] = temp
        left = left + 1
        right = right - 1


def rotate(nums, k):
    n = len(nums)
    if n == 0:
        return
    k = k % n
    if k == 0:
        return
    reverse_range(nums, 0, n)      # reverse the whole list
    reverse_range(nums, 0, k)      # reverse the first k
    reverse_range(nums, k, n)      # reverse the rest


def show(arr):
    return str(arr)


# ---- Tests ----
a1 = [1, 2, 3, 4, 5, 6, 7]
rotate(a1, 3)
print("Test 1:", show(a1))   # [5, 6, 7, 1, 2, 3, 4]

a2 = [-1, -100, 3, 99]
rotate(a2, 2)
print("Test 2:", show(a2))   # [3, 99, -1, -100]

a3 = [1, 2, 3, 4, 5, 6, 7]
rotate(a3, 0)
print("Test 3:", show(a3))   # [1, 2, 3, 4, 5, 6, 7]  (k=0 no-op)

a4 = [1, 2]
rotate(a4, 3)  # k % n == 1
print("Test 4:", show(a4))   # [2, 1]

a5 = [1]
rotate(a5, 5)
print("Test 5:", show(a5))   # [1]

a6 = []
rotate(a6, 4)
print("Test 6:", show(a6))   # []

a7 = [1, 2, 3, 4, 5]
rotate(a7, 5)  # full rotation
print("Test 7:", show(a7))   # [1, 2, 3, 4, 5]

a8 = [9, 8, 7, 6, 5, 4, 3, 2, 1]
rotate(a8, 4)
print("Test 8:", show(a8))   # [2, 1, 9, 8, 7, 6, 5, 4, 3]
