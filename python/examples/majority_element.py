# LeetCode 169 — Majority Element
# Given an array where one element appears more than n/2 times, find
# that element. It is guaranteed to exist.
# Approach: Boyer-Moore voting. We keep a candidate and a counter.
# On matching the candidate, the counter goes up. On a mismatch,
# it goes down. When the counter hits zero, we adopt the current
# element as the new candidate. At the end, the candidate is the
# majority element.
# O(n) time, O(1) space.

def majority_element(nums):
    candidate = nums[0]
    count = 1
    n = len(nums)
    for i in range(1, n):
        if count == 0:
            candidate = nums[i]
            count = 1
        elif nums[i] == candidate:
            count = count + 1
        else:
            count = count - 1
    return candidate


# ---- Tests ----
print("Test 1:", majority_element([3, 2, 3]))           # 3
print("Test 2:", majority_element([2, 2, 1, 1, 1, 2, 2]))  # 2
print("Test 3:", majority_element([1]))                 # 1
print("Test 4:", majority_element([6, 5, 5]))           # 5
print("Test 5:", majority_element([1, 2, 3, 1, 1, 1]))  # 1
print("Test 6:", majority_element([7, 7, 7, 7, 1, 2, 3]))  # 7
print("Test 7:", majority_element([4]))                 # 4 (single element)
