# LeetCode 14 — Longest Common Prefix
# Find the longest prefix shared by all strings in the list.
# If no common prefix exists, return "".
# Approach: scan character by character across the first string,
# checking that every other string has the same character at that
# position. Stop on the first mismatch.
# O(S) time, where S is the total number of characters across all strings.

def prefix(s, length):
    """Return the first `length` characters of s, manually built up
    since this interpreter does not yet support slice expressions."""
    out = ""
    for i in range(length):
        out = out + s[i]
    return out


def longest_common_prefix(strs):
    if len(strs) == 0:
        return ""
    first = strs[0]
    count = len(strs)
    for i in range(len(first)):
        ch = first[i]
        for j in range(1, count):
            s = strs[j]
            if i >= len(s) or s[i] != ch:
                return prefix(first, i)
    return first


# ---- Tests ----
print(longest_common_prefix(["flower", "flow", "flight"]))  # "fl"
print(longest_common_prefix(["dog", "racecar", "car"]))      # ""
print(longest_common_prefix(["interspecies", "interstellar", "interstate"]))  # "inters"
print(longest_common_prefix(["throne"]))                     # "throne"
print(longest_common_prefix([]))                             # ""
print(longest_common_prefix(["alone"]))                      # "alone"
print(longest_common_prefix(["a"]))                          # "a"
print(longest_common_prefix(["abc", "abc", "abc"]))          # "abc"
print(longest_common_prefix(["abc", "abd", "abe"]))          # "ab"
