# LeetCode 28 — Find the Index of the First Occurrence
# Return the index of the first occurrence of `needle` in `haystack`,
# or -1 if `needle` is not a substring. If needle is empty, return 0.
#
# Approach: naive sliding window. For each starting position i in
# haystack where needle could fit, check character-by-character
# whether needle matches haystack[i : i + m]. We can't use slicing
# in this interpreter, so we compare manually with a helper.
# O((n - m + 1) * m) time, O(1) extra space. For tiny inputs this
# is more than fast enough.

def starts_at(haystack, i, needle, m):
    """Return True iff haystack[i : i + m] == needle."""
    for k in range(m):
        if haystack[i + k] != needle[k]:
            return False
    return True


def str_str(haystack, needle):
    n = len(haystack)
    m = len(needle)
    if m == 0:
        return 0
    if m > n:
        return -1
    last = n - m  # last starting position to try
    for i in range(last + 1):
        if starts_at(haystack, i, needle, m):
            return i
    return -1


# ---- Tests ----
print(str_str("sadbutsad", "sad"))                 # 0
print(str_str("leetcode", "leeto"))                # -1
print(str_str("hello", "ll"))                      # 2
print(str_str("aaaaa", "bba"))                     # -1
print(str_str("abc", ""))                          # 0
print(str_str("", "a"))                            # -1
print(str_str("a", "a"))                           # 0
print(str_str("mississippi", "issip"))             # 4
print(str_str("mississippi", "pi"))                # 9
print(str_str("ababababab", "ababab"))             # 0
print(str_str("ababababab", "babab"))              # 1
print(str_str("abcdef", "abcdef"))                 # 0
print(str_str("abcdef", "abcdefg"))                # -1
