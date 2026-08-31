# LeetCode 125 — Valid Palindrome
# Determine whether a string is a palindrome, considering only
# alphanumeric characters and ignoring case. Everything else
# (spaces, punctuation) is stripped.
#
# Approach: build a filtered, lowercased string of just alphanumerics,
# then two-pointer scan from both ends comparing characters. O(n) time.
#
# Note: this interpreter doesn't yet expose str.isalnum() / .lower(),
# so we provide a small is_alnum helper and lowercase by ASCII
# arithmetic.

def is_digit(c):
    return c >= "0" and c <= "9"


def is_lower(c):
    return c >= "a" and c <= "z"


def is_upper(c):
    return c >= "A" and c <= "Z"


def to_lower(c):
    if is_upper(c):
        # ASCII trick: ord('A')=65, ord('a')=97, diff = 32
        return chr(ord(c) + 32)
    return c


def is_alnum(c):
    return is_digit(c) or is_lower(c) or is_upper(c)


def filter_chars(s):
    """Strip non-alphanumerics and lowercase what remains."""
    out = ""
    for i in range(len(s)):
        ch = s[i]
        if is_alnum(ch):
            out = out + to_lower(ch)
    return out


def is_palindrome(s):
    cleaned = filter_chars(s)
    n = len(cleaned)
    left = 0
    right = n - 1
    while left < right:
        if cleaned[left] != cleaned[right]:
            return False
        left = left + 1
        right = right - 1
    return True


# ---- Tests ----
print("'A man, a plan, a canal: Panama' :", is_palindrome("A man, a plan, a canal: Panama"))  # True
print("'race a car'                     :", is_palindrome("race a car"))                       # False
print("' '                              :", is_palindrome(" "))                                # True
print("'a'                              :", is_palindrome("a"))                                # True
print("'ab'                             :", is_palindrome("ab"))                               # False
print("'aba'                            :", is_palindrome("aba"))                              # True
print("'abba'                           :", is_palindrome("abba"))                             # True
print("'Was it a car or a cat I saw?'   :", is_palindrome("Was it a car or a cat I saw?"))     # True
print("'tab a cat'                      :", is_palindrome("tab a cat"))                        # False
print("'No lemon, no melon'             :", is_palindrome("No lemon, no melon"))               # True
print("'0P'                             :", is_palindrome("0P"))                               # False
