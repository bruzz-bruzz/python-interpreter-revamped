# LeetCode 35 — Search Insert Position
# Given a sorted array of distinct ints and a target, return the
# index if the target is found. If not, return the index where it
# would be if it were inserted in order. The algorithm should run
# in O(log n) time.
#
# Approach: classic binary search. We maintain [lo, hi] as the
# candidate range. When the loop exits, lo is the insertion point.

def search_insert(nums, target):
    lo = 0
    hi = len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo


# ---- Tests ----
print(search_insert([1, 3, 5, 6], 5))    # 2
print(search_insert([1, 3, 5, 6], 2))    # 1
print(search_insert([1, 3, 5, 6], 7))    # 4
print(search_insert([1, 3, 5, 6], 0))    # 0
print(search_insert([1], 0))             # 0
print(search_insert([1], 1))             # 0
print(search_insert([1], 2))             # 1
print(search_insert([1, 3, 5], 4))       # 2
print(search_insert([], 5))               # 0
print(search_insert([1, 3, 5, 7, 9], 8)) # 4
print(search_insert([1, 3, 5, 7, 9], 10))# 5
print(search_insert([1, 3, 5, 7, 9], -1))# 0
