# LeetCode 118 — Pascal's Triangle
# Generate the first n rows of Pascal's Triangle.
# Each element is the sum of the two numbers above it.
# Uses a list of lists (no multi-dimensional literal needed).

def generate(num_rows):
    triangle = []
    for row_num in range(num_rows):
        if row_num == 0:
            triangle.append([1])
            continue
        # Each row starts with a 1
        row = [1]
        # Fill in the interior elements: sum of two above
        prev_row = triangle[row_num - 1]
        for j in range(1, row_num):
            val = prev_row[j - 1] + prev_row[j]
            row.append(val)
        # Each row ends with a 1
        row.append(1)
        triangle.append(row)
    return triangle


def show(triangle):
    for row in triangle:
        print(str(row))


# ---- Tests ----
show(generate(5))
#  [1]
#  [1, 1]
#  [1, 2, 1]
#  [1, 3, 3, 1]
#  [1, 4, 6, 4, 1]

print("---")
show(generate(1))
print("---")
show(generate(0))
print("---")
show(generate(7))
