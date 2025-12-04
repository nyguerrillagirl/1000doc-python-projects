'''
--- Day 3: Lobby ---
You descend a short staircase, enter the surprisingly vast lobby, and are quickly cleared by the security checkpoint.
When you get to the main elevators, however, you discover that each one has a red light above it: they're all offline.

"Sorry about that," an Elf apologizes as she tinkers with a nearby control panel.
"Some kind of electrical surge seems to have fried them. I'll try to get them online soon."

You explain your need to get further underground. "Well, you could at least take the escalator down to the printing
department, not that you'd get much further than that without the elevators working.
That is, you could if the escalator weren't also offline."

"But, don't worry! It's not fried; it just needs power. Maybe you can get it running while I keep working on the elevators."

There are batteries nearby that can supply emergency power to the escalator for just such an occasion.
The batteries are each labeled with their joltage rating, a value from 1 to 9.
You make a note of their joltage ratings (your puzzle input). For example:

987654321111111
811111111111119
234234234234278
818181911112111

The batteries are arranged into banks; each line of digits in your input corresponds to a single bank of batteries.
Within each bank, you need to turn on exactly two batteries; the joltage that the bank produces is equal to
the number formed by the digits on the batteries you've turned on.
For example, if you have a bank like 12345 and you turn on batteries 2 and 4, the bank would produce 24 jolts.
(You cannot rearrange batteries.)

You'll need to find the largest possible joltage each bank can produce. In the above example:

In 987654321111111, you can make the largest joltage possible, 98, by turning on the first two batteries.
In 811111111111119, you can make the largest joltage possible by turning on the batteries labeled 8 and 9, producing 89 jolts.
In 234234234234278, you can make 78 by turning on the last two batteries (marked 7 and 8).
In 818181911112111, the largest joltage you can produce is 92.

The total output joltage is the sum of the maximum joltage from each bank, so in this example,
the total output joltage is 98 + 89 + 78 + 92 = 357.

There are many batteries in front of you.
Find the maximum joltage possible from each bank; what is the total output joltage?

To begin, get your puzzle input.

Answer:


You can also [Share] this puzzle.
'''
import re

def read_in_next_battery_bank(filename):
    '''
    This function opens a files and yields the next rotation value, until none remains
    :return:
    '''
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()

def allowed_digits(target_number):
    '''
    The two-digit target_number is separated and we construct a new string
    with all digits from 1..9 sans the two digits. example if target number is 99
    we return "12345678"
    :param target_number:
    :return:
    '''
    starting_allowed = "123456789"
    target_number_str = str(target_number)
    starting_allowed = starting_allowed.replace(target_number_str[0], "")
    starting_allowed = starting_allowed.replace(target_number_str[1], "")
    return starting_allowed

def create_voltages_possible():
    voltages = {}
    for x in range(99, 10, -1):
        if (x % 10 == 0):
            continue
        # create entry in dictionary for the number and allowed digits
        voltages[x] = allowed_digits(x)

    return voltages

def find_largest_voltage(battery_bank, voltage_dict):
    '''
    Given a battery bank (e.g. 234234234234278) we return the largest voltage
    that is possible to be generated. In the above case it is 78. We iterate
    through the voltage_dict keys, (from 99..11) trying to find the first occurence of a key
    in the bank
    :param battery_bank:
    :return:
    '''
    key_str = ""
    for key, allowed_digits in voltage_dict.items():
        # try to find the key in the battery_bank
        key_str = str(key)
        pattern = r"".join([f"{digit}[{allowed_digits}]*" for digit in key_str])
        match = re.search(pattern, battery_bank)
        if match:
            #print(f"Found {key_str} at position {match.start()} ? {match.group()}")
            break

    return int(key_str)

def main():
    # create datastructures to use
    voltages = create_voltages_possible()

    # # Read and process battery banks
    gen = read_in_next_battery_bank("puzzle03_input.txt")
    total_battery_bank_value = 0
    for battery_bank in gen:
        highest_bank_value = find_largest_voltage(battery_bank, voltages)
        total_battery_bank_value += highest_bank_value

    print("total_battery_bank_value: ", total_battery_bank_value)

if __name__ == "__main__":
    main()