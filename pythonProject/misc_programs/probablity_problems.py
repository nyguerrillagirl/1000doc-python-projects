import itertools
die = [1, 2, 3, 4, 5, 6]
all_combos = list(itertools.product(die, repeat=2))
print(all_combos)

# What is the probability of rolling over 7 with two dice?
over_7 = 0
for combo in all_combos:
    if sum(combo) > 7:
        over_7 += 1

print(over_7 / len(all_combos)) # 0.4166666666666667

# What is the probability of throwing three die and getting over 7?
all_combos_3 = list(itertools.product(die, repeat=3))
over_7_3 = 0
for combo in all_combos_3:
    if sum(combo) > 7:
        over_7_3 += 1

print(over_7_3 / len(all_combos_3)) # 0.8379629629629629

