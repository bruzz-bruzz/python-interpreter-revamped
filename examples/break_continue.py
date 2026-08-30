# Demonstrate `break` and `continue` for early-exit and skip-iteration in
# both `for` and `while` loops.
# Demonstrates: `break`, `continue`, `for ... in ...`, `while`, and `if`.

# `break` exits the loop early.
print("First three numbers:")
for i in range(10):
    if i == 3:
        break
    print(" ", i)

# `continue` skips the rest of the current iteration.
print("\nOdd numbers up to 10:")
for i in range(10):
    if i % 2 == 0:
        continue
    print(" ", i)

# Same idea, but in a while loop.
print("\nFirst three powers of 2:")
n = 1
count = 0
while True:
    if n > 16:
        break
    print(" ", n)
    n *= 2
    count += 1
    if count >= 3:
        break
