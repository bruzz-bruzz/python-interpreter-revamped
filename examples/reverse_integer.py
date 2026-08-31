# LeetCode 7 — Reverse Integer
# Given a 32-bit signed integer, reverse the digits.
# If the reversed value overflows a 32-bit signed int, return 0.
# Approach: peel off digits with x % 10 and build up the result.
# We use abs() and a sign flag to handle negatives uniformly.

INT_MAX = 2147483647
INT_MIN = -2147483648

def reverse_integer(x):
    sign = 1
    if x < 0:
        sign = -1
        n = -x
    else:
        n = x
    result = 0
    while n > 0:
        digit = n % 10
        result = result * 10 + digit
        n = n // 10
    result = result * sign
    if result < INT_MIN or result > INT_MAX:
        return 0
    return result


# ---- Tests ----
print("123   ->", reverse_integer(123))     # 321
print("-123  ->", reverse_integer(-123))    # -321
print("120   ->", reverse_integer(120))     # 21
print("0     ->", reverse_integer(0))       # 0
print("1534236469 ->", reverse_integer(1534236469))  # 0 (overflow)
print("-2147483412 ->", reverse_integer(-2147483412))# -2143847412
print("1     ->", reverse_integer(1))       # 1
print("10    ->", reverse_integer(10))      # 1
print("1000000 ->", reverse_integer(1000000))  # 1
