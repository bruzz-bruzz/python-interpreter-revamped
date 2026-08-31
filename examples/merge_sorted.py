# LeetCode 88 — Merge Sorted Array
# Merge two sorted arrays nums1 and nums2 into nums1, in sorted order.
# nums1 has enough trailing space (filled with 0s) to hold all elements.
# Approach: three pointers working from the back, so we never overwrite
# values we still need to read. O(m + n) time, O(1) extra space.

def merge(nums1, m, nums2, n):
    i = m - 1       # pointer into nums1 (the real elements)
    j = n - 1       # pointer into nums2
    k = m + n - 1   # write position in nums1 (from the back)

    while i >= 0 and j >= 0:
        if nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1

    # Any leftover elements in nums2 (if any) need to be copied in.
    # Leftovers in nums1 are already in place.
    while j >= 0:
        nums1[k] = nums2[j]
        j -= 1
        k -= 1


# ---- Tests ----
def show(nums):
    return str(nums)


a1 = [1, 2, 3, 0, 0, 0]
merge(a1, 3, [2, 5, 6], 3)
print("Test 1:", show(a1))  # [1, 2, 2, 3, 5, 6]

a2 = [1]
merge(a2, 1, [], 0)
print("Test 2:", show(a2))  # [1]

a3 = [0]
merge(a3, 0, [1], 1)
print("Test 3:", show(a3))  # [1]

a4 = [4, 5, 6, 0, 0, 0]
merge(a4, 3, [1, 2, 3], 3)
print("Test 4:", show(a4))  # [1, 2, 3, 4, 5, 6]

a5 = [-1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0]
merge(a5, 5, [-1, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7], 6)
print("Test 5:", show(a5))  # sorted merge
