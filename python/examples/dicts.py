# Demonstrate dictionaries: literals, indexing, assignment, iteration, methods.
# Demonstrates: dict literals, `len()`, membership (`in`), `for ... in ...`,
# and the native dict methods exposed through attribute access.

# A dictionary literal maps string keys to values.
ages = {"alice": 30, "bob": 25, "carol": 40}
print("ages:", ages)
print("len:", len(ages))

# Index by key.
print("alice:", ages["alice"])
print("bob:", ages["bob"])

# `in` checks for key membership.
print("alice in ages:", "alice" in ages)
print("dave in ages:", "dave" in ages)

# Adding and overwriting entries via subscript assignment.
ages["dave"] = 35
ages["alice"] = 31
print("after updates:", ages)

# Iteration over a dict yields its keys.
print("keys:")
for name in ages:
    print(" -", name, "is", ages[name])

# Native dict methods: keys(), values(), items().
print("values:", list(ages.values()))
print("count:", len(ages.keys()))

# Nested dicts.
people = {
    "alice": {"age": 30, "city": "Paris"},
    "bob":   {"age": 25, "city": "Berlin"},
}
for name in people:
    info = people[name]
    print(name, "lives in", info["city"], "and is", info["age"])

# Building a dict incrementally.
counts = {}
words = ["the", "cat", "sat", "on", "the", "mat", "the"]
for word in words:
    if word in counts:
        counts[word] = counts[word] + 1
    else:
        counts[word] = 1
print("word counts:")
for word in counts:
    print(" -", word, "appears", counts[word], "time(s)")
