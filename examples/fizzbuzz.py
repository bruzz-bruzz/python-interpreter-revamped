# FizzBuzz example - prints numbers 1 to 20, but for multiples of 3 prints "Fizz",
# for multiples of 5 prints "Buzz", and for multiples of both 3 and 5 prints "FizzBuzz".
# Demonstrates: modulo (%), and nested if/else control flow.

for i in range(1, 21):
    if i % 3 == 0:
        if i % 5 == 0:
            print("FizzBuzz")
        else:
            print("Fizz")
    else:
        if i % 5 == 0:
            print("Buzz")
        else:
            print(i)
