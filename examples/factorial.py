# Compute factorial using recursion
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)

for i in range(1, 8):
    print("factorial of", i, "is", fact(i))
