# LeetCode 242 — Valid Anagram
# Determine if two strings are anagrams of each other (same letters
# in any order). Approach: count letter frequencies in both strings
# and compare the histograms. O(n) time, O(1) space (alphabet size).

def is_anagram(s, t):
    if len(s) != len(t):
        return False
    counts = {}
    for ch in s:
        if ch in counts:
            counts[ch] = counts[ch] + 1
        else:
            counts[ch] = 1
    for ch in t:
        if ch not in counts:
            return False
        counts[ch] = counts[ch] - 1
        if counts[ch] < 0:
            return False
    return True


# ---- Tests ----
print("listen / silent:", is_anagram("listen", "silent"))  # True
print("anagram / nagaram:", is_anagram("anagram", "nagaram"))  # True
print("rat / car:", is_anagram("rat", "car"))  # False
print("aabbcc / abcabc:", is_anagram("aabbcc", "abcabc"))  # True
print("a / b:", is_anagram("a", "b"))  # False
print("ab / ba:", is_anagram("ab", "ba"))  # True
print("abc / abcd:", is_anagram("abc", "abcd"))  # False
print("hello / world:", is_anagram("hello", "world"))  # False
print("Race / care:", is_anagram("Race", "care"))  # False (case matters in this version)
