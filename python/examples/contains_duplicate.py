# LeetCode 217 — Contains Duplicate
# Return True if the array contains any duplicate.
# O(n) time using a set.

def contains_duplicate(nums):
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False


# ---- Tests ----
print("has dup [1,2,3,1]:", contains_duplicate([1, 2, 3, 1]))   # True
print("has dup [1,2,3,4]:", contains_duplicate([1, 2, 3, 4]))   # False
print("has dup [1,1,1,3,3,4,3,2,4,2]:", contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]))  # True
print("has dup []:", contains_duplicate([]))                    # False
print("has dup [42]:", contains_duplicate([42]))                # False
print("has dup [0,0]:", contains_duplicate([0, 0]))             # True
