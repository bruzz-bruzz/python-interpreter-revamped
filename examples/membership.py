# Show off the `in` and `not in` membership operators.
# Demonstrates: list literals, `in`, `not in`, and the `for ... in ...` loop.

vowels = ["a", "e", "i", "o", "u"]
word = "hello"

print("Letter checks for:", word)
for ch in word:
    if ch in vowels:
        print("  ", ch, "is a vowel")
    else:
        print("  ", ch, "is a consonant")

# Substring check
phrases = ["hello world", "goodbye", "help me", "oh no"]
print("\nSubstring 'help' in:")
for p in phrases:
    if "help" in p:
        print("  yes:", p)
    else:
        print("  no: ", p)

# `not in` - guard against unsafe input
allowed = ["yes", "y", "ok"]
user_input = "nope"
if user_input not in allowed:
    print("\nSorry,", user_input, "is not a valid answer.")
