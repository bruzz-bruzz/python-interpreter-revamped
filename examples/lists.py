# Demonstrate lists: literals, indexing, for-iteration, and length.
# Demonstrates: list literals, indexing, `len()`, and `for ... in ...`.

nums = [10, 20, 30, 40, 50]
print("first:", nums[0])
print("last:", nums[-1])
print("count:", len(nums))

print("all:")
for n in nums:
    print(" -", n)

# Sum the elements with a for loop.
total = 0
for n in nums:
    total += n
print("sum:", total)
