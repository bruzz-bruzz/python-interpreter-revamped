# LeetCode 26 — Remove Duplicates from Sorted Array
# Given a sorted array, remove duplicates in-place so each element
# appears only once. Return the number of unique elements k. The
# first k elements of the array should hold the unique values in
# sorted order; the rest doesn't matter.
#
# Approach: two pointers. `write` is the position the next unique
# value should go. `read` scans forward. Whenever nums[read] differs
# from the previous value, we copy it to nums[write] and advance
# write. Because the input is sorted, identical values are adjacent.
# O(n) time, O(1) extra space.

def remove_duplicates(nums):
    if len(nums) == 0:
        return 0
    write = 1  # index 0 is always the first unique value
    n = len(nums)
    for read in range(1, n):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write = write + 1
    return write


def show(nums):
    return str(nums)


# ---- Tests ----
a1 = [1, 1, 2]
k1 = remove_duplicates(a1)
print("Test 1: k =", k1, " arr =", show(a1))  # 2, [1, 2]

a2 = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
k2 = remove_duplicates(a2)
print("Test 2: k =", k2, " arr =", show(a2))  # 5, [0, 1, 2, 3, 4, ...]

a3 = [1]
k3 = remove_duplicates(a3)
print("Test 3: k =", k3, " arr =", show(a3))  # 1, [1]

a4 = []
k4 = remove_duplicates(a4)
print("Test 4: k =", k4, " arr =", show(a4))  # 0, []

a5 = [1, 1, 1, 1]
k5 = remove_duplicates(a5)
print("Test 5: k =", k5, " arr =", show(a5))  # 1, [1, ...]

a6 = [1, 2, 3, 4, 5]
k6 = remove_duplicates(a6)
print("Test 6: k =", k6, " arr =", show(a6))  # 5, [1, 2, 3, 4, 5]

a7 = [-3, -3, -2, -1, -1, 0, 0, 0, 1]
k7 = remove_duplicates(a7)
print("Test 7: k =", k7, " arr =", show(a7))  # 5, [-3, -2, -1, 0, 1, ...]
