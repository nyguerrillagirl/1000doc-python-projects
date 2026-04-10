# In this program we attempt to calculate the probability of getting over 22 heads
# when tossing a coin 30 times
import numpy as np

NUMBER_OF_TRIALS = 100000
count_over_22_heads = 0
for i in range(NUMBER_OF_TRIALS):
    trials = np.random.choice(['H', 'T'], size=30, replace=True)
    num_heads = (trials == 'H').sum()
    if num_heads >= 22:
        count_over_22_heads += 1

prob = count_over_22_heads / NUMBER_OF_TRIALS
print("probability of getting 22 heads or over", prob)
