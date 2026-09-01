# LeetCode 283 — Move Zeroes
# Move all 0s to the end of the array while maintaining the relative
# order of the non-zero elements. Must be done in-place.
# Approach: use a write pointer that tracks where the next non-zero
# should go. Iterate through with a read pointer; whenever a non-zero
# is found, write it to the write position and advance write.
# After the loop, fill the rest with zeros.
# O(n) time, O(1) extra space.

def move_zeroes(nums):
    write = 0  # next position to write a non-zero
    n = len(nums)
    for i in range(n):
        if nums[i] != 0:
            nums[write] = nums[i]
            write = write + 1
    # Fill the rest with zeros
    for i in range(write, n):
        nums[i] = 0


def show(nums):
    return str(nums)


# ---- Tests ----
a1 = [0, 1, 0, 3, 12]
move_zeroes(a1)
print("Test 1:", show(a1))  # [1, 3, 12, 0, 0]

a2 = [0]
move_zeroes(a2)
print("Test 2:", show(a2))  # [0]

a3 = [1, 2, 3]
move_zeroes(a3)
print("Test 3:", show(a3))  # [1, 2, 3]  (no zeros)

a4 = [4, 2, 4, 0, 0, 0, 5, 1]
move_zeroes(a4)
print("Test 4:", show(a4))  # [4, 2, 4, 5, 1, 0, 0, 0]

a5 = [0, 0, 1]
move_zeroes(a5)
print("Test 5:", show(a5))  # [1, 0, 0]
