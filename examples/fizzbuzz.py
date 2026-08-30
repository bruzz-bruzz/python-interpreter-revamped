# FizzBuzz example - prints numbers 1 to 20, but for multiples of 3 prints "Fizz",
# for multiples of 5 prints "Buzz", and for multiples of both 3 and 5 prints "FizzBuzz".
# Demonstrates: modulo (%), if/elif/else chains, and for-loops.

for i in range(1, 21):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
