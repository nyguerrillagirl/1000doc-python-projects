'''
--- Day 5: Cafeteria ---
As the forklifts break through the wall, the Elves are delighted to discover that there was a cafeteria on the other side after all.

You can hear a commotion coming from the kitchen. "At this rate, we won't have any time left to put the wreaths up in the dining hall!" Resolute in your quest, you investigate.

"If only we hadn't switched to the new inventory management system right before Christmas!" another Elf exclaims. You ask what's going on.

The Elves in the kitchen explain the situation: because of their complicated new inventory management system, they can't figure out which of their ingredients are fresh and which are spoiled. When you ask how it works, they give you a copy of their database (your puzzle input).

The database operates on ingredient IDs. It consists of a list of fresh ingredient ID ranges, a blank line, and a list of available ingredient IDs. For example:

3-5
10-14
16-20
12-18

1
5
8
11
17
32
The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs 3, 4, and 5 are all fresh. The ranges can also overlap; an ingredient ID is fresh if it is in any range.

The Elves are trying to determine which of the available ingredient IDs are fresh. In this example, this is done as follows:

Ingredient ID 1 is spoiled because it does not fall into any range.
Ingredient ID 5 is fresh because it falls into range 3-5.
Ingredient ID 8 is spoiled.
Ingredient ID 11 is fresh because it falls into range 10-14.
Ingredient ID 17 is fresh because it falls into range 16-20 as well as range 12-18.
Ingredient ID 32 is spoiled.
So, in this example, 3 of the available ingredient IDs are fresh.

Process the database file from the new inventory management system. How many of the available ingredient IDs are fresh?

To begin, get your puzzle input.

Answer:


You can also [Share] this puzzle.
'''
def read_in_next_line(filename):
    '''
    This function opens a files and yields the next rotation value, until none remains
    :return:
    '''
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()


def process_puzzle_input(filename):
    '''
    Processes the file consisting of fresh food ranges, followed by a blank line, food available list
    :param filename:
    :return: (dict_of_ranges,fresh_food_list)
    '''
    gen = read_in_next_line(filename)

    fresh_food_ranges_dict = {}
    food_available_list = []
    processing_available_food_list = False
    for line in gen:
        if line == "":
            processing_available_food_list = True
            continue
        if not processing_available_food_list:
            # line must be in the form <number_start_range>-<number_end_range>
            number_start_range, number_end_range = line.split("-")
            number_start_range, number_end_range = int(number_start_range), int(number_end_range)
            fresh_food_ranges_dict[line] = [number_start_range, number_end_range]
        else:
            food_id = int(line)
            food_available_list.append(food_id)

    return (fresh_food_ranges_dict, food_available_list)

def print_input_data(range_dict, food_id_list):
    print("Fresh ingredient ranges")
    for key, value in range_dict.items():
        print(f"range key: {key} range:{value[0]}-{value[1]}")

    print(" ")
    for food_id in food_id_list:
        print(food_id)

def food_in_fresh_inventory(food_id,fresh_food_inventory_dict):
    for key, value in fresh_food_inventory_dict.items():
        if (food_id >= value[0]) and (food_id <= value[1]):
            return True
        
    return False

def main():
    fresh_food_inventory_dict, food_id_list =   process_puzzle_input("puzzle05_input.txt")
    #print_input_data(fresh_food_inventory_dict,food_id_list )

    # process every food_id
    fresh_food_count = []
    for food_id in food_id_list:
        if food_in_fresh_inventory(food_id,fresh_food_inventory_dict):
            fresh_food_count.append(food_id)

    print(len(fresh_food_count))
    
if __name__ == "__main__":
    main()