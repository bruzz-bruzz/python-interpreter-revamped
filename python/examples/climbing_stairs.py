# LeetCode 70 — Climbing Stairs
# You are climbing a staircase. Each step you can take 1 or 2 stairs.
# How many distinct ways can you reach the top of n stairs?
# Approach: this is the Fibonacci sequence. f(n) = f(n-1) + f(n-2).
# Compute iteratively, keeping only the last two values.
# O(n) time, O(1) space.

def climb_stairs(n):
    if n <= 2:
        return n
    prev2 = 1  # f(1)
    prev1 = 2  # f(2)
    for i in range(3, n + 1):
        cur = prev1 + prev2
        prev2 = prev1
        prev1 = cur
    return prev1


# ---- Tests ----
print("n=1 :", climb_stairs(1))   # 1
print("n=2 :", climb_stairs(2))   # 2
print("n=3 :", climb_stairs(3))   # 3
print("n=4 :", climb_stairs(4))   # 5
print("n=5 :", climb_stairs(5))   # 8
print("n=6 :", climb_stairs(6))   # 13
print("n=10:", climb_stairs(10))  # 89
print("n=20:", climb_stairs(20))  # 10946
print("n=30:", climb_stairs(30))  # 1346269
