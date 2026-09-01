# Demonstrate tuples: literals, indexing, length, iteration, and concatenation.
# Demonstrates: tuple literals, indexing, `len()`, `+`, `for ... in ...`.

# Tuple literals — note the trailing comma for a 1-tuple.
empty = ()
single = (42,)
pair = ("hello", "world")
point = (3, 7)

print("empty:", empty)
print("single:", single)
print("pair:", pair)
print("point:", point)
print("len(point):", len(point))

# Indexing works just like lists, including negative indices.
print("point[0]:", point[0])
print("point[-1]:", point[-1])

# Tuples are iterable.
print("iterate:")
for value in point:
    print(" -", value)

# Tuples are immutable at the Python level (we use native Python tuples).
# That means `point[0] = 99` would raise TypeError — exactly what real
# Python does, which is the design goal of this interpreter.

# Concatenation builds a new tuple.
combined = pair + point
print("combined:", combined)

# Tuples in containers: lists of tuples are very common.
records = [("Alice", 30), ("Bob", 25), ("Carol", 40)]
print("records:")
for record in records:
    print(" -", record[0], "is", record[1])
