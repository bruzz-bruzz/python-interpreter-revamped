# LeetCode 67 — Add Binary
# Given two binary strings a and b, return their sum as a binary
# string. The inputs are non-empty and contain only '0' and '1'.
#
# Approach: walk both strings from the right end, like grade-school
# addition. At each position sum the two bits plus the carry, write
# the new least-significant bit to the output, and propagate the
# carry. We use a helper to convert a single character to an int.
#
# Since this interpreter doesn't expose int(ch), we hand-roll it.

def char_to_digit(c):
    if c == "0":
        return 0
    if c == "1":
        return 1
    return 0  # unreachable for valid input


def digit_to_char(d):
    if d == 0:
        return "0"
    return "1"


def add_binary(a, b):
    i = len(a) - 1
    j = len(b) - 1
    carry = 0
    # Build the answer right-to-left, then reverse.
    out = ""
    while i >= 0 or j >= 0 or carry != 0:
        da = 0
        db = 0
        if i >= 0:
            da = char_to_digit(a[i])
            i = i - 1
        if j >= 0:
            db = char_to_digit(b[j])
            j = j - 1
        total = da + db + carry
        carry = total // 2
        out = out + digit_to_char(total % 2)
    # Reverse the string.
    rev = ""
    for k in range(len(out) - 1, -1, -1):
        rev = rev + out[k]
    return rev


# ---- Tests ----
print(add_binary("11", "1"))          # "100"
print(add_binary("1010", "1011"))     # "10101"
print(add_binary("0", "0"))           # "0"
print(add_binary("1", "1"))           # "10"
print(add_binary("1111", "1111"))     # "11110"
print(add_binary("1010", "0"))        # "1010"
print(add_binary("0", "1010"))        # "1010"
print(add_binary("1", "1111"))        # "10000"
print(add_binary("100", "110010"))    # "110110"
print(add_binary("111111", "1"))      # "1000000"
