# LeetCode 9 — Palindrome Number
# Determine whether an integer is a palindrome (reads the same forwards
# and backwards). Negative numbers are not palindromes because of the
# leading '-'.
#
# Approach: reverse the second half of the digits and compare against
# the first half. Stops in the middle, so it runs in O(log n) time and
# O(1) space.

def is_palindrome(x):
    if x < 0:
        return False
    if x % 10 == 0 and x != 0:
        return False  # any number ending in 0 isn't a palindrome
    reversed_half = 0
    while x > reversed_half:
        reversed_half = reversed_half * 10 + x % 10
        x = x // 10  # integer division
    # x and reversed_half have the same number of digits, or
    # reversed_half has one extra (odd-digit case).
    return x == reversed_half or x == reversed_half // 10


# ---- Tests ----
print("121 is palindrome:", is_palindrome(121))           # True
print("-121 is palindrome:", is_palindrome(-121))         # False
print("10 is palindrome:", is_palindrome(10))             # False
print("0 is palindrome:", is_palindrome(0))               # True
print("12321 is palindrome:", is_palindrome(12321))       # True
print("1234 is palindrome:", is_palindrome(1234))         # False
print("1001 is palindrome:", is_palindrome(1001))         # True
print("1 is palindrome:", is_palindrome(1))               # True
print("1221 is palindrome:", is_palindrome(1221))         # True
