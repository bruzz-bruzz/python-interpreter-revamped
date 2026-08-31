# LeetCode 202 — Happy Number
# A happy number is one where repeatedly replacing the number with
# the sum of the squares of its digits eventually reaches 1. Numbers
# that don't reach 1 enter a cycle.
#
# Approach: a Floyd-style cycle detector. Walk the sequence with a
# `slow` pointer (one step) and a `fast` pointer (two steps). If
# they ever meet, the sequence is in a cycle and the number is not
# happy. If `fast` reaches 1, the number is happy.
#
# Helper: sum of squares of digits, computed manually since we
# don't have a clean way to iterate digits otherwise.

def sum_sq_digits(n):
    total = 0
    while n > 0:
        d = n % 10
        total = total + d * d
        n = n // 10
    return total


def is_happy(n):
    slow = n
    fast = n
    while True:
        slow = sum_sq_digits(slow)
        fast = sum_sq_digits(sum_sq_digits(fast))
        if fast == 1:
            return True
        if slow == fast:
            return False


# ---- Tests ----
print(is_happy(19))     # True  (1^2+9^2=82, 8^2+2^2=68, ..., reaches 1)
print(is_happy(2))      # False (enters the 4, 16, 37, 58, 89, ... cycle)
print(is_happy(1))      # True
print(is_happy(7))      # True
print(is_happy(4))      # False
print(is_happy(10))     # True
print(is_happy(11))     # False
print(is_happy(100))    # True
print(is_happy(999))    # False
print(is_happy(130))    # False
print(is_happy(44))     # True
