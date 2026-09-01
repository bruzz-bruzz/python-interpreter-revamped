# Print the prime numbers up to 30.
# Demonstrates: for-loops, if/elif/else, modulo (%), and `not`.

n = 2
while n <= 30:
    # Use a sentinel to remember whether we found a divisor.
    divisor = 0
    for d in range(2, n):
        if n % d == 0:
            divisor = d
    if not divisor:
        print(n, "is prime")
    n += 1
