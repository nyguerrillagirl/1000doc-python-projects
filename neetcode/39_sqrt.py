# 69. Sqrt(x)
# From https://www.youtube.com/watch?v=zdMhGxRWutQ&list=PLQpVsaqBj4RIJdYW6Y-iAswxCZeocfoRW&index=1
#
# Given a non-negative integer x, return the square root of x rounded down
# to the nearest integer. The returned integer should be non-negative as well.

# You MUST NOT USE any built-in exponent function or operator.

# Example 1:
#   Input: x = 4
#   Output: 2
#   Explanation: The square root of 4 is 2, so we return 2.

# Example 2:
#   Input: x = 8
#   Output: 2
#   Explanation: The square root of 8 is 2.82842..., and since we round it down
#                   to the nearest integer, 2 is returned.

delta = 0.001
def my_sqrt(x):
    sqrt_bottom_estimate = 0.0
    sqrt_top_estimate = x / 2.0

    while True:
        if ((sqrt_top_estimate * sqrt_top_estimate) - x) < delta:
            return round(sqrt_top_estimate)

        # adjust top_estimate
        sqrt_top_estimate = sqrt_top_estimate - 0.5


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x = 25
    print(f"x={x} is {my_sqrt(x)}.")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
