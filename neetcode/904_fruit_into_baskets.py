from typing import List

class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        # no fruits to process
        if len(fruits) == 0:
            return 0

        # only one fruit - so that is the total
        if len(fruits) == 1:
            return 1

        last_fruit_seen = -1                # use to calculate
        total_fruits = 0
        if fruits[0] == fruits[1]:
            # same fruit in slot #1 and #2, put them both in basket_1
            basket_1 = [fruits[0], 2, 0, 1]  # [fruit_type, count, start_index, end_index]
            basket_2 = [-1, 0, -1, -1]       # basket 2 is empty
            last_fruit_seen = basket_1[0]
        else:
            basket_1 = [fruits[0], 1, 0, 0]
            basket_2 = [fruits[1], 1, 1, 1]
            last_fruit_seen = basket_2[0]

        total_fruits = max(total_fruits, basket_1[1] + basket_2[1])

        for right in range(2,len(fruits)):
            current_fruit = fruits[right]
            if (current_fruit == basket_1[0]) or (current_fruit == basket_2[0]):
                # this fruit belongs in basket_1 or basket_2
                if current_fruit == basket_1[0]:
                    # belongs in basket_1
                    basket_1[1] += 1    # increase the count
                    if current_fruit == last_fruit_seen:
                        basket_1[3] += 1    # increase the end_index (for run we have seen)
                    else:
                        basket_1[2] = basket_1[3] = right

                    last_fruit_seen = current_fruit
                    total_fruits = max(total_fruits, basket_1[1] + basket_2[1])
                    continue

                if current_fruit == basket_2[0]:
                    # this fruit belongs in basket_2
                    basket_2[1] += 1    # increase the count
                    if current_fruit == last_fruit_seen:
                        basket_2[3] += 1
                    else:
                        basket_2[2] = basket_2[3] = right
                    last_fruit_seen = current_fruit
                    total_fruits = max(total_fruits, basket_1[1] + basket_2[1])
                    continue
            else:
                # this is fruit we have not seen in our baskets yet
                if basket_2[0] == -1:
                    # enter this new fruit into basket_2 which is unused yet
                    basket_2 = [current_fruit, 1, right, right]
                    total_fruits = max(total_fruits, basket_1[1] + basket_2[1])
                    last_fruit_seen = current_fruit
                    continue
                else:
                    # the last_fruit_seen must have matched either basket_1 or basket_2, keep that
                    # and clear the other basket
                    if basket_1[0] == last_fruit_seen:
                        # keep basket_1, change total to end_index-start_index+1
                        basket_1[1] = basket_1[3] - basket_1[2] + 1 # update total to match the last sequence
                        # move new fruit into basket_2
                        basket_2 = [current_fruit, 1, right, right]
                    else:
                        # keep basket_2, place new fruit into basket_1
                        basket_2[1] = basket_2[3] - basket_2[2] + 1
                        basket_1 = [current_fruit, 1, right, right]
                    last_fruit_seen = current_fruit
                    total_fruits = max(total_fruits, basket_1[1] + basket_2[1])

        return total_fruits

solution = Solution()
s = [1,2,3,2,2]

print(f"total_fruits: {solution.totalFruit(s)}")