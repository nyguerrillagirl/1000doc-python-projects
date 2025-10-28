# This is a sample Python script.

"""
A wanderer lives in a remote landscape with three villages: Avalon, Belthar and Cresthaven.
Every morning, they leave the village they are in and travel to one of the other two villages,
choosing between the two destinations at random with an equal 50–50 chance.
If the wanderer begins in their home village of Avalon and stops after 100 days of travel,
are they more likely to end up in Avalon or in Belthar? Or are both destinations equally likely?
"""


def solve_puzzle():
    from random import choice

    villages = ['Avalon', 'Belthar', 'Cresthaven']
    home_village = 'Avalon'
    days = 100
    simulations = 100000

    results = {'Avalon': 0, 'Belthar': 0, 'Cresthaven': 0}

    for _ in range(simulations):
        current_village = home_village
        for _ in range(days):
            # a cute way to pick one of the other two villages!!
            next_villages = [v for v in villages if v != current_village]
            current_village = choice(next_villages)
        results[current_village] += 1

    print(f"After {simulations} simulations of {days} days:")
    for village, count in results.items():
        print(f"{village}: {count} times ({(count / simulations) * 100:.2f}%)")


# The above function was actually filled in by copilot.
if __name__ == '__main__':
    solve_puzzle()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
