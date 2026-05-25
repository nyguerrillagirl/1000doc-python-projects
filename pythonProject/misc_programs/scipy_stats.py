from scipy.stats import binom
import math
import matplotlib.pyplot as plt

# when we’re
# calculating the probability of flipping two heads in three coin tosses:
print(binom.pmf(12, 24, 0.5))

# from n choose k
print(math.comb(5,2))

results = binom.rvs(n=10, p=0.5, size=10000)
plt.hist(results, bins=range(12), align='left', density=True)
plt.xlabel('Number of successes')
plt.ylabel('Probability')
plt.title('Binomial Distribution (n=10, p=0.5)')
plt.show()
