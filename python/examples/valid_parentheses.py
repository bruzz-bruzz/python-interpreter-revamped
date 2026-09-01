# LeetCode 20 — Valid Parentheses
# Determine if a string of brackets is valid:
#   - Every open bracket has a matching close bracket.
#   - Brackets close in the correct order.
#   - The stack approach: push opens, pop on closes and verify match.
# O(n) time, O(n) space.

def is_valid(s):
    stack = []
    pairs = {
        ")": "(",
        "]": "[",
        "}": "{",
    }
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if len(stack) == 0:
                return False
            if stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return len(stack) == 0


# ---- Tests ----
print("()        :", is_valid("()"))           # True
print("()[]{}    :", is_valid("()[]{}"))         # True
print("(]        :", is_valid("(]"))           # False
print("([)]      :", is_valid("([)]"))         # False
print("{[]}      :", is_valid("{[]}"))         # True
print("empty     :", is_valid(""))              # True  (empty string is valid)
print("(         :", is_valid("("))            # False
print(")         :", is_valid(")"))            # False
print("(((())))  :", is_valid("(((())))"))      # True
print("([{}])    :", is_valid("([{}])"))        # True
print("((())     :", is_valid("((())"))         # False
