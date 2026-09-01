# LeetCode 122 — Best Time to Buy and Sell Stock II
# As in LC 121, but you may complete as many transactions as you
# like (buy one, sell one, buy again, sell again...). You may not
# hold more than one share at a time.
#
# Approach: greedy — every time tomorrow's price is higher than
# today's, capture that difference. Visually, the total profit is
# the sum of all the upward segments of the price curve.
# O(n) time, O(1) space.

def max_profit_ii(prices):
    profit = 0
    n = len(prices)
    for i in range(1, n):
        diff = prices[i] - prices[i - 1]
        if diff > 0:
            profit = profit + diff
    return profit


# ---- Tests ----
print(max_profit_ii([7, 1, 5, 3, 6, 4]))   # 7  (1->5=4, 3->6=3)
print(max_profit_ii([1, 2, 3, 4, 5]))      # 4  (1->5)
print(max_profit_ii([7, 6, 4, 3, 1]))      # 0  (always down)
print(max_profit_ii([1]))                  # 0
print(max_profit_ii([]))                   # 0
print(max_profit_ii([5, 5, 5, 5]))         # 0
print(max_profit_ii([2, 1, 2, 0, 1]))      # 2  (1->2=1, 0->1=1)
print(max_profit_ii([3, 3, 5, 0, 0, 3, 1, 4]))  # 8 (5->3 later, etc.)
print(max_profit_ii([1, 9, 2, 8, 3, 7]))  # 17
