# LeetCode 27 — Remove Element
# Given an array and a value, remove all occurrences of the value
# in-place. Return the new length k. The order of the remaining
# elements can be changed; only the first k elements matter.
#
# Approach: two pointers. `write` tracks where the next kept element
# goes. `read` scans the array. If nums[read] != val, copy it to
# nums[write] and advance write. O(n) time, O(1) extra space.

def remove_element(nums, val):
    write = 0
    n = len(nums)
    for read in range(n):
        if nums[read] != val:
            nums[write] = nums[read]
            write = write + 1
    return write


def show(nums):
    return str(nums)


# ---- Tests ----
a1 = [3, 2, 2, 3]
k1 = remove_element(a1, 3)
print("Test 1: k =", k1, " arr =", show(a1))  # 2, [2, 2]

a2 = [0, 1, 2, 2, 3, 0, 4, 2]
k2 = remove_element(a2, 2)
print("Test 2: k =", k2, " arr =", show(a2))  # 5, [0, 1, 3, 0, 4, ...]

a3 = [1]
k3 = remove_element(a3, 1)
print("Test 3: k =", k3, " arr =", show(a3))  # 0, []

a4 = [1, 2, 3, 4]
k4 = remove_element(a4, 5)
print("Test 4: k =", k4, " arr =", show(a4))  # 4, [1, 2, 3, 4]

a5 = [4, 4, 4, 4]
k5 = remove_element(a5, 4)
print("Test 5: k =", k5, " arr =", show(a5))  # 0, [...]

a6 = [1, 1, 1, 1]
k6 = remove_element(a6, 1)
print("Test 6: k =", k6, " arr =", show(a6))  # 0, [...]
