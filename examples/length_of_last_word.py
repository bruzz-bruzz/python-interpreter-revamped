# LeetCode 58 — Length of Last Word
# Given a string s consisting of words and spaces, return the length
# of the last word in the string. A word is a maximal substring of
# non-space characters.
#
# Approach: scan from the end. Skip trailing spaces, then count
# characters until the next space (or the start of the string).
# O(n) time, O(1) extra space.

def length_of_last_word(s):
    n = len(s)
    i = n - 1
    # Skip trailing spaces.
    while i >= 0 and s[i] == " ":
        i = i - 1
    # Count characters of the last word.
    count = 0
    while i >= 0 and s[i] != " ":
        count = count + 1
        i = i - 1
    return count


# ---- Tests ----
print(length_of_last_word("Hello World"))           # 5
print(length_of_last_word("   fly me   to   the moon  "))  # 4
print(length_of_last_word("luffy is still joyboy")) # 6
print(length_of_last_word("a"))                     # 1
print(length_of_last_word(" "))                     # 0
print(length_of_last_word(""))                      # 0
print(length_of_last_word("a "))                    # 1
print(length_of_last_word("day"))                   # 3
print(length_of_last_word("  day  "))               # 3
print(length_of_last_word("    "))                  # 0
print(length_of_last_word("Today is a nice day"))   # 3
