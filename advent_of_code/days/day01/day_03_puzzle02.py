# See details in day_03_puzzle01.py
'''
--- Part Two ---
The escalator doesn't move. The Elf explains that it probably needs more joltage to overcome the static friction
of the system and hits the big red "joltage limit safety override" button.
You lose count of the number of times she needs to confirm "yes, I'm sure" and decorate the lobby a bit while you wait.

Now, you need to make the largest joltage by turning on exactly twelve batteries within each bank.

The joltage output for the bank is still the number formed by the digits of the batteries you've turned on;
the only difference is that now there will be 12 digits in each bank's joltage output instead of two.

Consider again the example from before:

987654321111111
811111111111119
234234234234278
818181911112111

Now, the joltages are much larger:

In 987654321111111, the largest joltage can be found by turning on everything
    except some 1s at the end to produce 987654321111.
In the digit sequence 811111111111119, the largest joltage can be found by turning on everything except some 1s,
    producing 811111111119.
In 234234234234278, the largest joltage can be found by turning on everything except a 2 battery, a 3 battery,
    and another 2 battery near the start to produce 434234234278.
In 818181911112111, the joltage 888911112111 is produced by turning on everything except some 1s near the front.
The total output joltage is now much larger: 987654321111 + 811111111119 + 434234234278 + 888911112111 = 3121910778619.

What is the new total output joltage?

This requires a different approach from day_03_puzzle01.py.  I cannot generate 999999999999..111111111111 and
try to find if that value exists within the battery bank

I propose a greedy algorithm.  I will preprocess the battery bank creating a dictionary {number: [list of indices]}

Note: I should have solved the first puzzle this way.

Answer:
'''
def read_in_next_battery_bank(filename):
    '''
    This function opens a files and yields the next rotation value, until none remains
    :return:
    '''
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()

def process_battery_bank(battery_bank):
    number_indices_dict = {9:[], 8:[], 7:[], 6:[], 5:[], 4:[], 3:[], 2:[], 1:[]}
    for index, char in enumerate(battery_bank):
        number_indices_dict[int(char)].append(index)

    return number_indices_dict

def find_number(dict_number_indices,first_index, last_index ):
    for key, index_list in dict_number_indices.items():
        for index in index_list:
            if (index < first_index):
                continue

            if (index > last_index):
                continue

            return (key, index)

def find_largest_number(dict_number_indices, battery_bank, n_digits, current_index):
    '''
    process the battery_bank (really represented in dict_number_indices)
    :param dict_number_indices:
    :param battery_bank:
    :param n_digits:
    :param current_index:
    :return:
    '''
    first_index = current_index
    new_battery_bank = battery_bank
    len_battery_bank = len(battery_bank)
    last_index_possible = len_battery_bank - n_digits
    count = n_digits
    result = ""
    while count > 0:
        # find largest number from first_index..max_last_index
        largest_digit, index = find_number(dict_number_indices,first_index, last_index_possible )
        result = result + str(largest_digit)

        count = count - 1
        # get ready for the next number
        first_index = index+1
        last_index_possible += 1

    return int(result)

def main():

    gen = read_in_next_battery_bank("puzzle03_input.txt")
    total_battery_bank_value = 0
    n_digits = 12
    start_index = 0
    for battery_bank in gen:
        # dictionary of {number: [list_of_indices]}
        dict_number_indices = process_battery_bank(battery_bank)
        last_index = len(battery_bank) - n_digits
        largest_number = int(find_largest_number(dict_number_indices, battery_bank, n_digits, start_index))
        total_battery_bank_value += largest_number

    print("total_battery_bank_value: ", total_battery_bank_value)

if __name__ == "__main__":
    main()