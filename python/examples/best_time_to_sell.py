# LeetCode 121 — Best Time to Buy and Sell Stock
# Given daily stock prices, find the maximum profit from a single buy
# followed later by a single sell. If no profit is possible, return 0.
# O(n) time, O(1) space: track the lowest price seen so far and the
# best profit at each step.

def max_profit(prices):
    min_price = 9999999999
    best = 0
    for price in prices:
        if price < min_price:
            min_price = price
        profit = price - min_price
        if profit > best:
            best = profit
    return best


# ---- Tests ----
print("[7,1,5,3,6,4]:", max_profit([7, 1, 5, 3, 6, 4]))   # 5  (buy 1, sell 6)
print("[7,6,4,3,1]:", max_profit([7, 6, 4, 3, 1]))         # 0  (no profit)
print("[]:", max_profit([]))                                # 0
print("[2,4,1]:", max_profit([2, 4, 1]))                    # 2  (buy 2, sell 4)
print("[1,2]:", max_profit([1, 2]))                        # 1
print("[3,3,3,3]:", max_profit([3, 3, 3, 3]))              # 0
print("[2,1,2,1,0,1,2]:", max_profit([2, 1, 2, 1, 0, 1, 2]))  # 2 (buy 0, sell 2)
