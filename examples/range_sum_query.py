# LeetCode 303 — Range Sum Query - Immutable
# Given an integer array, support range sum queries:
#   sumRange(i, j) returns the sum of nums[i..j] inclusive.
# Preprocess once with prefix sums so each query is O(1).
#
# Note: the original LeetCode API uses a method on a class instance
# (obj.sumRange(i, j)). This interpreter's class support is minimal
# (no `self`, no real instantiation), so we expose the query
# function as a plain closure and call it directly.

def make_range_sum(nums):
    """Return a function `f(i, j)` that answers range sum queries."""
    # prefix[k] = sum of nums[0..k-1], with prefix[0] = 0.
    prefix = [0]
    for n in nums:
        prefix.append(prefix[len(prefix) - 1] + n)

    def f(i, j):
        # Guard: if nums was empty, prefix has only one entry [0],
        # and there are no valid i/j pairs. Return 0 as a safe
        # degenerate value. (The LeetCode spec guarantees i/j are
        # in range for non-empty inputs.)
        if len(nums) == 0:
            return 0
        return prefix[j + 1] - prefix[i]

    return f


# ---- Tests ----
arr = make_range_sum([-2, 0, 3, -5, 2, -1])
print("sumRange(0, 2) =", arr(0, 2))   # 1  (-2+0+3)
print("sumRange(2, 5) =", arr(2, 5))   # -1 (3-5+2-1)
print("sumRange(0, 5) =", arr(0, 5))   # -3
print("sumRange(1, 1) =", arr(1, 1))   # 0

a2 = make_range_sum([1, 2, 3, 4, 5])
print("sumRange(0, 4) =", a2(0, 4))   # 15
print("sumRange(2, 3) =", a2(2, 3))   # 7
print("sumRange(4, 4) =", a2(4, 4))   # 5

a3 = make_range_sum([])
print("sumRange(0, 0) on empty =", a3(0, 0))  # 0

a4 = make_range_sum([0, 0, 0, 0])
print("sumRange(0, 3) =", a4(0, 3))   # 0

a5 = make_range_sum([10])
print("sumRange(0, 0) =", a5(0, 0))   # 10

