# LeetCode 1920 — Build Array from Permutation
# Given a zero-based permutation nums, build an array of the same
# length where ans[i] = nums[nums[i]].

def build_array(nums):
    n = len(nums)
    ans = []
    for i in range(n):
        ans.append(nums[nums[i]])
    return ans


def show(arr):
    return str(arr)


# ---- Tests ----
print("Test 1:", show(build_array([0, 2, 1, 5, 3, 4])))  # [0,1,2,4,5,3]
print("Test 2:", show(build_array([5, 0, 1, 2, 3, 4])))  # [4,5,0,1,2,3]
print("Test 3:", show(build_array([0])))                 # [0]
print("Test 4:", show(build_array([1, 0]))               )# [0, 1]
print("Test 5:", show(build_array([2, 1, 0])))           # [0, 1, 2]
