'''
--- Day 5: Cafeteria ---
As the forklifts break through the wall, the Elves are delighted to discover that there was a cafeteria on the
other side after all.

You can hear a commotion coming from the kitchen. "At this rate, we won't have any time left to put the wreaths
up in the dining hall!" Resolute in your quest, you investigate.

"If only we hadn't switched to the new inventory management system right before Christmas!" another Elf exclaims.
You ask what's going on.

The Elves in the kitchen explain the situation: because of their complicated new inventory management system,
they can't figure out which of their ingredients are fresh and which are spoiled.
When you ask how it works, they give you a copy of their database (your puzzle input).

The database operates on ingredient IDs. It consists of a list of fresh ingredient ID ranges, a blank line,
and a list of available ingredient IDs. For example:

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
The fresh ID ranges are inclusive: the range 3-5 means that ingredient IDs 3, 4, and 5 are all fresh.
The ranges can also overlap; an ingredient ID is fresh if it is in any range.

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

--- Part Two ---
The Elves start bringing their spoiled inventory to the trash chute at the back of the kitchen.

So that they can stop bugging you when they get new inventory, the Elves would like to know all of the IDs
that the fresh ingredient ID ranges consider to be fresh. An ingredient ID is still considered fresh if it is in any range.

Now, the second section of the database (the available ingredient IDs) is irrelevant.
Here are the fresh ingredient ID ranges from the above example:

3-5
10-14
16-20
12-18

The ingredient IDs that these ranges consider to be fresh are 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, and 20.

So, in this example, the fresh ingredient ID ranges consider a total of 14 ingredient IDs to be fresh.

Process the database file again. How many ingredient IDs are considered to be fresh according to the fresh ingredient
ID ranges?

Answer:

'''
from collections import deque


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

    fresh_food_ranges_queue = deque()
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
            fresh_food_ranges_queue.append((line, [number_start_range, number_end_range]))
        else:
            food_id = int(line)
            food_available_list.append(food_id)

    return (fresh_food_ranges_queue, food_available_list)


def print_input_data(range_queue):
    print("Fresh ingredient ranges")
    for item in range_queue:
        print(item)

    print(" ")



def food_in_fresh_inventory(food_id, fresh_food_inventory_dict):
    for key, value in fresh_food_inventory_dict.items():
        if (food_id >= value[0]) and (food_id <= value[1]):
            return True

    return False

def is_first_list_subsumed_by_second_list(list1, list2):
    '''
    returns true if list1 [start, end] completely falls into list2 (start2, end2], otherwise false
    :param list1:
    :param list2:
    :return:
    '''
    start_list_1 = list1[0]
    end_list_1 = list1[1]
    start_list_2 = list2[0]
    end_list_2 = list2[1]

    return (start_list_1 >= start_list_2) and (end_list_1 <= end_list_2)



def process_all_ranges(fresh_food_inventory_queue):
    '''
    We construct a dictionary where all entries DO NOT overlap any other entries. We iterate through the current
    accepted_range_dict for every item in the queue until the queue is exhausted
    :param fresh_food_inventory_queue:
    :return:
    '''
    accepted_dict = {}      # this is what we build and return
    while fresh_food_inventory_queue:
        new_range_candidate = fresh_food_inventory_queue.popleft()
        new_range_str, new_range_list = new_range_candidate
        stop_processing_this_new_range = False
        # now examine each new_range_candidate with each accepted_range
        for accepted_range_key, accepted_range_list in accepted_dict.items():
            # check if new_range is subsumed by this accepted_range
            if is_first_list_subsumed_by_second_list(new_range_list,accepted_range_list):
                # throw this new_range_list away
                stop_processing_this_new_range = True
                break

            # check if accepted_range falls completely into new_range_candidate
            if is_first_list_subsumed_by_second_list(accepted_range_list, new_range_list):
                # remove this accepted range from accepted_dict
                del accepted_dict[accepted_range_key]
                # add new_range_candidate back to the queue (it may get trimmed by another range)
                fresh_food_inventory_queue.append(new_range_candidate)
                stop_processing_this_new_range = True
                break

            # values to use to determine if we overlap on the left or right side of accepted_range
            new_range_start = new_range_list[0]
            new_range_end = new_range_list[1]
            accepted_range_start = accepted_range_list[0]
            accepted_range_end = accepted_range_list[1]

            # now check for overlap with existing accepted_range_list on the left side
            if (new_range_start < accepted_range_start)   \
                and (new_range_end >= accepted_range_start) \
                and (new_range_end <= accepted_range_end):
                # trim the new_range and add back into the queue
                update_new_range_str = str(new_range_start) + "-" + str(accepted_range_start-1)
                fresh_food_inventory_queue.append((update_new_range_str, [new_range_start, accepted_range_start-1]))
                stop_processing_this_new_range = True
                break

            # now check if we overlap with existing accepted_range_list, on the right side
            if (new_range_start > accepted_range_start) \
                and (new_range_start <= accepted_range_end) \
                and (new_range_end > accepted_range_end):
                # trim the new_range from accepted_range_end+1 .. new_range_end
                update_new_range_str = str(accepted_range_end+1) + "-" + str(new_range_end)
                fresh_food_inventory_queue.append((update_new_range_str, [accepted_range_end+1, new_range_end]))
                stop_processing_this_new_range = True
                break

        # at this point this new_range_candidate does not overlap in any way any existing range so we can
        # add to accepted_dict list as a new unique range
        if not stop_processing_this_new_range:
            # this new_range_candidate does not overlap, or subsume any other blocks - hence clean
            accepted_dict[new_range_str] = new_range_list

    return accepted_dict

def total_all_ranges(accepted_dict):
    total = 0
    for key, value in accepted_dict.items():
        print(f"value: {value}")
        start_range = value[0]
        end_range = value[1]
        total += end_range - start_range + 1

    return total

def main():
    # puzzle05_input.txt
    fresh_food_inventory_queue, food_id_list = process_puzzle_input("puzzle05_input.txt")

    # let's print out queue items
    print_input_data(fresh_food_inventory_queue)
    accepted_dict = process_all_ranges(fresh_food_inventory_queue)
    print(total_all_ranges(accepted_dict))


if __name__ == "__main__":
    main()