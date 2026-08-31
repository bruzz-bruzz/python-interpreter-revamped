# LeetCode 344 — Reverse String
# Write a function that reverses a list of characters in-place.
# We represent a "string" as a list of single-char strings.
# Uses a two-pointer approach: swap elements at the left and right
# pointers, then move inward. O(n) time, O(1) space.

def reverse_string(s):
    left = 0
    right = len(s) - 1
    while left < right:
        temp = s[left]
        s[left] = s[right]
        s[right] = temp
        left = left + 1
        right = right - 1


def to_list(s):
    chars = []
    for i in range(len(s)):
        chars.append(s[i])
    return chars


def show(chars):
    out = ""
    for ch in chars:
        out = out + ch
    return out


# ---- Tests ----
a1 = to_list("hello")
reverse_string(a1)
print(show(a1))  # "olleh"

a2 = to_list("Hannah")
reverse_string(a2)
print(show(a2))  # "hannaH"

a3 = to_list("")
reverse_string(a3)
print(show(a3))  # ""

a4 = to_list("a")
reverse_string(a4)
print(show(a4))  # "a"

a5 = to_list("ab")
reverse_string(a5)
print(show(a5))  # "ba"
