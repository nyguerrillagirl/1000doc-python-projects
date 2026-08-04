from typing import List

class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        # no fruits to process
        if len(fruits) == 0:
            return 0

        # only one fruit - so that is the total
        if len(fruits) == 1:
            return 1

        left = 0
        max_fruits = 0

        # tracks information on first basket
        has_basket1_fruits = False
        basket1_fruit = -1
        basket1_total = 0
        basket1_longest_seq = 0

        # tracks information on second basket
        has_basket2_fruits = False
        basket2_fruit = -1
        basket2_total = 0
        basket2_longest_seq = 0

        for right, fruit_type in enumerate(fruits):
            if has_basket1_fruits and basket1_fruit == fruit_type:
                basket1_total += 1
                if fruits[right-1] == fruit_type:
                    basket1_longest_seq += 1
                    #basket2_longest_seq = 0
                max_fruits = max(max_fruits, basket1_total+basket2_total)
                continue
            elif not has_basket1_fruits:
                has_basket1_fruits = True
                basket1_fruit = fruits[right]
                basket1_total = 1
                basket1_longest_seq = 1
                #basket2_longest_seq = 1
                max_fruits = max(max_fruits, basket1_total + basket2_total)
                continue
            if has_basket2_fruits and basket2_fruit == fruit_type:
                basket2_total += 1
                if fruits[right-1] == fruit_type:
                    basket2_longest_seq += 1
                    #basket1_longest_seq = 0
                max_fruits = max(max_fruits, basket1_total + basket2_total)
                continue
            elif not has_basket2_fruits:
                has_basket2_fruits = True
                basket2_fruit = fruits[right]
                basket2_longest_seq = 1
                #basket1_longest_seq = 0
                basket2_total = 1
                max_fruits = max(max_fruits, basket1_total + basket2_total)
                continue

            # if we get here than fruit_type was not found in basket1 or basket2
            # figure out previous fruit_type
            if basket1_fruit == fruits[right-1]:
                # update 2nd basket
                basket2_fruit = fruits[right]
                basket2_total = 1
                basket2_longest_seq = 1
                basket1_fruit = basket1_longest_seq
            else:
                # update 1st basket
                basket1_fruit = fruits[right]
                basket1_total = 1
                basket1_longest_seq = 1
                basket2_fruit = basket2_longest_seq

            max_fruits = max(max_fruits, basket1_total + basket2_total)

        return max_fruits


solution = Solution()
s = [1,0,1,4,1,4,1,2,3]

print(solution.totalFruit(s))