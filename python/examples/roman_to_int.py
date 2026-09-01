# LeetCode 13 — Roman to Integer
# Convert a Roman numeral string to its integer value.
# Roman numerals use these symbols:
#   I=1, V=5, X=10, L=50, C=100, D=500, M=1000
# Subtractive pairs (e.g. IV = 4) count as a single value where
# a smaller numeral precedes a larger one.
# Approach: scan left-to-right. If the current value is less than
# the next, subtract it; otherwise add it.
# O(n) time, O(1) space.

def roman_to_int(s):
    # Build a lookup dict
    values = {
        "I": 1, "V": 5, "X": 10, "L": 50,
        "C": 100, "D": 500, "M": 1000,
    }
    total = 0
    n = len(s)
    for i in range(n):
        v = values[s[i]]
        if i + 1 < n and v < values[s[i + 1]]:
            total = total - v
        else:
            total = total + v
    return total


# ---- Tests ----
print("III     ->", roman_to_int("III"))      # 3
print("IV      ->", roman_to_int("IV"))       # 4
print("IX      ->", roman_to_int("IX"))       # 9
print("LVIII   ->", roman_to_int("LVIII"))    # 58   (50 + 5 + 3)
print("MCMXCIV ->", roman_to_int("MCMXCIV"))  # 1994 (1000 + 900 + 90 + 4)
print("MMXX    ->", roman_to_int("MMXX"))     # 2020
print("XL      ->", roman_to_int("XL"))       # 40
print("XC      ->", roman_to_int("XC"))       # 90
print("CD      ->", roman_to_int("CD"))       # 400
print("CM      ->", roman_to_int("CM"))       # 900
print("M       ->", roman_to_int("M"))        # 1000
print("I       ->", roman_to_int("I"))        # 1
