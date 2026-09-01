# LeetCode 119 — Pascal's Triangle II
# Given an integer rowIndex, return the rowIndex-th (0-indexed) row
# of Pascal's Triangle. Each interior element is the sum of the two
# elements directly above it; the edges are 1.
#
# Approach: iterative, only keeping the previous row. Compute the
# next row by pairing adjacent elements with a leading 0 and
# trailing 0, e.g.  [0, 1, 3, 3, 1, 0]  ->  [1, 4, 6, 4, 1].
# O(rowIndex^2) time, O(rowIndex) extra space.

def get_row(row_index):
    row = [1]
    for i in range(1, row_index + 1):
        # Build the next row from `row` paired with itself shifted by 1.
        # next[j] = row[j - 1] + row[j], with row[-1] treated as 0.
        next_row = [1]
        for j in range(1, i):
            next_row.append(row[j - 1] + row[j])
        next_row.append(1)
        row = next_row
    return row


def show(row):
    return str(row)


# ---- Tests ----
print(show(get_row(0)))   # [1]
print(show(get_row(1)))   # [1, 1]
print(show(get_row(2)))   # [1, 2, 1]
print(show(get_row(3)))   # [1, 3, 3, 1]
print(show(get_row(4)))   # [1, 4, 6, 4, 1]
print(show(get_row(5)))   # [1, 5, 10, 10, 5, 1]
print(show(get_row(6)))   # [1, 6, 15, 20, 15, 6, 1]
print(show(get_row(10)))  # [1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1]
