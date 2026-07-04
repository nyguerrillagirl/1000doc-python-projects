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
# see notes: https://github.com/nyguerrillagirl/1000doc-docs/blob/main/repo_docs/1000doc-python-projects/neetcode/39_sqrt_notes.docx
import math
eplison = 0.0001
def my_sqrt(x):
    y1 = x / 2.0
    y0 = 0
    while True:
        if ((y1 * y1) - x) < eplison:
            return round(y1)

        # adjust top_estimate
        y1 = 0.5 * (y1 + (x / y1))

        # check if we can stop now
        if math.floor(y0) == math.floor(y1):
            return math.floor(y1)
        else:
            y0 = y1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    x = 8
    print(f"x={x} is {my_sqrt(x)}.")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
