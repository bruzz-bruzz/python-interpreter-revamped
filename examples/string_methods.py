# Demonstrate string methods: case conversion, trimming, splitting,
# substring search, and replacement.
# Demonstrates: string methods, method chaining, `len()`, and `for ... in ...`.

text = "  Hello, World!  "
print("Original:", text)
print("Uppercase:", text.upper())
print("Lowercase:", text.lower())
print("Stripped:", text.strip())

sentence = "the quick brown fox"
words = sentence.split(" ")
print("Words:")
for w in words:
    print(" -", w)

print("Contains 'quick':", "quick" in sentence)
print("Starts with 'the':", sentence.startswith("the"))
print("Ends with 'fox':", sentence.endswith("fox"))

# Chaining
shouty = "  hello, world  ".strip().upper().replace("WORLD", "Python")
print("Chained:", shouty)
