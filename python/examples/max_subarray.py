# LeetCode 53 — Maximum Subarray
# Given an array of integers, find the contiguous subarray with the
# largest sum. Kadane's algorithm: at each step, either extend the
# current subarray (current + n) or start a new one (n). Track the
# best sum seen.
# O(n) time, O(1) space.

def max_subarray(nums):
    best = nums[0]
    current = nums[0]
    for i in range(1, len(nums)):
        n = nums[i]
        if current + n > n:
            current = current + n
        else:
            current = n
        if current > best:
            best = current
    return best


# ---- Tests ----
print("[-2,1,-3,4,-1,2,1,-5,4]:", max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # 6  (4,-1,2,1)
print("[1]:", max_subarray([1]))                                                       # 1
print("[5,4,-1,7,8]:", max_subarray([5, 4, -1, 7, 8]))                                # 23
print("[-1]:", max_subarray([-1]))                                                     # -1
print("[-1,-2,-3,-4]:", max_subarray([-1, -2, -3, -4]))                                # -1
print("[0,0,0,0]:", max_subarray([0, 0, 0, 0]))                                        # 0
print("[1,2,3,4,5]:", max_subarray([1, 2, 3, 4, 5]))                                   # 15
print("[-2,-1]:", max_subarray([-2, -1]))                                              # -1
