'''
--- Day 2: Gift Shop ---
You get inside and take the elevator to its only other stop: the gift shop.
"Thank you for visiting the North Pole!" gleefully exclaims a nearby sign.
You aren't sure who is even allowed to visit the North Pole, but you know you can access the lobby through here,
and from there you can access the rest of the North Pole base.

As you make your way through the surprisingly extensive selection, one of the clerks recognizes you and asks for your help.

As it turns out, one of the younger Elves was playing on a gift shop computer and managed to add a
whole bunch of invalid product IDs to their gift shop database!
Surely, it would be no trouble for you to identify the invalid product IDs for them, right?

They've even checked most of the product ID ranges already; they only have a few product ID ranges (your puzzle input)
that you'll need to check. For example:

11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124

(The ID ranges are wrapped here for legibility; in your input, they appear on a single long line.)

The ranges are separated by commas (,); each range gives its first ID and last ID separated by a dash (-).

Since the young Elf was just doing silly patterns, you can find the invalid IDs by looking for any ID which
is made only of some sequence of digits repeated twice. So, 55 (5 twice), 6464 (64 twice), and 123123 (123 twice)
would all be invalid IDs.

None of the numbers have leading zeroes; 0101 isn't an ID at all. (101 is a valid ID that you would ignore.)

Your job is to find all of the invalid IDs that appear in the given ranges. In the above example:

11-22 has two invalid IDs, 11 and 22.
95-115 has one invalid ID, 99.
998-1012 has one invalid ID, 1010.
1188511880-1188511890 has one invalid ID, 1188511885.
222220-222224 has one invalid ID, 222222.
1698522-1698528 contains no invalid IDs.
446443-446449 has one invalid ID, 446446.
38593856-38593862 has one invalid ID, 38593859.
The rest of the ranges contain no invalid IDs.
Adding up all the invalid IDs in this example produces 1227775554.

What do you get if you add up all of the invalid IDs?

'''
def process_input_range(filename):
    '''
    opens the filename, reads in first line in the form <start_range_number>-<end_range_number>,...
    :param filename:
    :return: a tuple str (<start_range_number>, <end_range_number)
    '''
    with open(filename, "r") as f:
        line = f.readline().strip()

    rangeList = line.split(",")
    for range in rangeList:
        numbers = range.split("-")
        yield (numbers[0], numbers[1])

def find_all_duplicates(start_range_str, end_range_str):
    '''
    processes all numbers from start_range_str .. end_range_str and tags all
    numbers that contain a duplicate, e.g. 1188511885
    :param start_range_str:
    :param end_range_str:
    :return:
    '''
    duplicate_list = []
    next_number_in_range = start_range_str
    next_number_as_int = int(next_number_in_range)
    while True:
        # process next_number_in_range
        len_next_number_in_range = len(next_number_in_range)
        if len_next_number_in_range % 2 == 0:
            # skip odd numbered len strings
            half_point = len_next_number_in_range // 2
            first_half = next_number_in_range[0:half_point]
            second_half = next_number_in_range[half_point:]
            if first_half == second_half:
                duplicate_list.append(next_number_in_range)

        if next_number_in_range == end_range_str:
            break

        # update to the next number
        next_number_as_int = next_number_as_int + 1
        next_number_in_range = str(next_number_as_int)

    return duplicate_list

def main():
    gen = process_input_range("puzzle02_input.txt")
    invalid_id_count = 0
    for range_tuple in gen:
        start_range_number, end_range_number = range_tuple
        print(f"range: {start_range_number}-{end_range_number}")
        duplicateList = find_all_duplicates(start_range_number, end_range_number)
        for a_duplicate in duplicateList:
            invalid_id_count = invalid_id_count + int(a_duplicate)

    print(f"total invalid ids: {invalid_id_count}")

if __name__ == "__main__":
    main()