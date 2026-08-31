# LeetCode 1 — Two Sum
# Given an array of integers and a target, return indices of the two
# numbers that add up to the target.
#
# Approach: for each number, check if its complement (target - num) has
# been seen before. If yes, return the stored index and the current index.
# If no, store the number and its index. O(n) time, O(n) space.

def two_sum(nums, target):
    seen = {}  # maps number -> most-recent index
    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in seen:
            return [seen[complement], i]
        seen[nums[i]] = i
    return []  # no solution (won't happen for valid LeetCode input)


# ---- Tests ----
print("Test 1:", two_sum([2, 7, 11, 15], 9))   # [0, 1]   2+7=9
print("Test 2:", two_sum([3, 2, 4], 6))         # [1, 2]   2+4=6
print("Test 3:", two_sum([3, 3], 6))            # [0, 1]   3+3=6
print("Test 4:", two_sum([1, 5, 3, 7], 10))     # [2, 3]   3+7=10
print("Test 5:", two_sum([-1, -2, -3, -4, -5], -8))  # [2, 4]  -3+-5=-8
