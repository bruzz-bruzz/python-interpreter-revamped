# LeetCode 387 — First Unique Character in a String
# Given a string, find the index of the first non-repeating
# character. If none, return -1.
# Approach: build a frequency map of all chars, then walk the string
# again to find the first one whose count is 1.
# O(n) time, O(k) extra space where k is the alphabet size.

def first_unique_char(s):
    counts = {}
    for i in range(len(s)):
        ch = s[i]
        if ch in counts:
            counts[ch] = counts[ch] + 1
        else:
            counts[ch] = 1
    for i in range(len(s)):
        ch = s[i]
        if counts[ch] == 1:
            return i
    return -1


# ---- Tests ----
print("'leetcode'   :", first_unique_char("leetcode"))   # 0  (l)
print("'loveleetcode':", first_unique_char("loveleetcode"))  # 2  (v)
print("'aabb'       :", first_unique_char("aabb"))       # -1
print("'z'          :", first_unique_char("z"))          # 0
print("'aabbc'      :", first_unique_char("aabbc"))      # 4  (c)
print("'abcabc'     :", first_unique_char("abcabc"))     # -1
print("'stress'     :", first_unique_char("stress"))     # 1  (t)
