'''
--- Day 5: Binary Boarding ---
You board your plane only to discover a new problem: you dropped your boarding pass! You aren't sure which seat is
yours, and all of the flight attendants are busy with the flood of people that suddenly made it through passport control.

You write a quick program to use your phone's camera to scan all of the nearby boarding passes (your puzzle input);
perhaps you can find your seat through process of elimination.

Instead of zones or groups, this airline uses binary space partitioning to seat people.
A seat might be specified like FBFBBFFRLR, where F means "front", B means "back", L means "left", and R means "right".

The first 7 characters will either be F or B; these specify exactly one of the 128 rows on the plane
(numbered 0 through 127).
Each letter tells you which half of a region the given seat is in. Start with the whole list of rows;
the first letter indicates whether the seat is in the front (0 through 63) or the back (64 through 127).
The next letter indicates which half of that region the seat is in, and so on until you're left with exactly one row.

For example, consider just the first seven characters of FBFBBFFRLR:

Start by considering the whole range, rows 0 through 127.
F means to take the lower half, keeping rows 0 through 63.
B means to take the upper half, keeping rows 32 through 63.
F means to take the lower half, keeping rows 32 through 47.
B means to take the upper half, keeping rows 40 through 47.
B keeps rows 44 through 47.
F keeps rows 44 through 45.
The final F keeps the lower of the two, row 44.
The last three characters will be either L or R; these specify exactly one of the 8 columns of seats on the
plane (numbered 0 through 7). The same process as above proceeds again, this time with only three steps.
L means to keep the lower half, while R means to keep the upper half.

For example, consider just the last 3 characters of FBFBBFFRLR:

Start by considering the whole range, columns 0 through 7.
R means to take the upper half, keeping columns 4 through 7.
L means to take the lower half, keeping columns 4 through 5.
The final R keeps the upper of the two, column 5.
So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

Every seat also has a unique seat ID: multiply the row by 8, then add the column.
In this example, the seat has ID 44 * 8 + 5 = 357.

Here are some other boarding passes:

BFFFBBFRRR: row 70, column 7, seat ID 567.
FFFBBBFRRR: row 14, column 7, seat ID 119.
BBFFBBFRLL: row 102, column 4, seat ID 820.
As a sanity check, look through your list of boarding passes. What is the highest seat ID on a boarding pass?


--- Part Two ---
Ding! The "fasten seat belt" signs have turned on. Time to find your seat.

It's a completely full flight, so your seat should be the only missing boarding pass in your list.
However, there's a catch: some of the seats at the very front and back of the plane don't exist on this aircraft,
so they'll be missing from your list as well.

Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1 from yours will be in your list.

What is the ID of your seat?

Answer:

'''

import pathlib
import sys

# This is a dictionary that tracks previous processing. The key = ( (start_range, end_range), 'B' | 'F'), the
# the value is the new range. For example, the entry for ( (0, 127), 'F') maps to (0,63) another entry will be
# ( (0, 127), 'B') which maps to (64, 127.
memo_fb = {}

# This is a dictionary that tracks previous processing. The key = ( (start_range, end_range), 'R' | 'L'), the
# value is the new range. For example, the entry for ( (0,7), 'R') ==> (4,7) and ( (0,7), 'L') ==> (0,3)
memo_lr = {}

# This dictionary holds all the taken seats. key: seat_id, value = (row, col, boarding_pass)
seats_taken = [0 for i in range(1024)]

def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split()]


def processFB(rowString):
    result = -1
    current_range = (0,127)
    for char in rowString:
        # first check if we already have this split
        if ((current_range), char) in memo_fb:
            current_range = memo_fb[((current_range), char)]
            continue

        # check if this range represents an entry of the form (n,n) (found row)
        if current_range[0] == current_range[1]:
            result = current_range[0]
            break

        # split the current range
        f_high_range = current_range[0] + ((current_range[1] - current_range[0]) // 2)
        b_low_range = f_high_range+1

        if char == 'F':
            memo_fb[((current_range), 'F')] = (current_range[0], f_high_range)
            # add the other side too
            memo_fb[((current_range), 'B')] = (b_low_range, current_range[1])
            current_range = memo_fb[((current_range), 'F')]
        else:
            # char must be 'B'
            memo_fb[((current_range), 'B')] = ( b_low_range, current_range[1])
            # add the other side too
            memo_fb[((current_range), 'F')] = (current_range[0], f_high_range)
            current_range = memo_fb[((current_range), 'B')]

    if result == -1:
        result = current_range[0]

    return result


def processLR(colString):
    result = -1
    current_range = (0, 7)
    for char in colString:
        # first check if we already have this split
        if ((current_range), char) in memo_lr:
            current_range = memo_lr[((current_range), char)]
            continue

        # check if this range represents an entry of the form (n,n) (found row)
        if current_range[0] == current_range[1]:
            result = current_range[0]
            break

        # split the current range
        l_high_range = current_range[0] + ((current_range[1] - current_range[0]) // 2)
        r_low_range = l_high_range+1

        if char == 'L':
            memo_lr[((current_range), 'L')] = (current_range[0], l_high_range)
            # add the other side too
            memo_lr[((current_range), 'R')] = (r_low_range, current_range[1])
            current_range = memo_lr[((current_range), 'L')]
        else:
            # char must be 'R'
            memo_lr[((current_range), 'R')] = (r_low_range, current_range[1])
            # add the other side too
            memo_lr[((current_range), 'L')] = (current_range[0], l_high_range)
            current_range = memo_lr[((current_range), 'R')]

    if result == -1:
        result = current_range[0]

    return result

def calculate_seat_id_using_row_and_col(row_number, col_number):
    return  row_number * 8 + col_number


def calculate_seat_id(boarding_pass):
    # process the first 7 characters to find row number
    row_number = processFB(boarding_pass[0:7])
    # process the next 3 characters to find col number
    col_number = processLR(boarding_pass[7:])
    seat_id = row_number * 8 + col_number
    # tracks if a seat has been taken
    seats_taken[seat_id] = 1

    return seat_id

def part1(data):
    """Solve part 1."""
    highest_seat_id = 0
    for data_item in data:
        seat_id = calculate_seat_id(data_item)
        if seat_id > highest_seat_id:
            highest_seat_id = seat_id

    return highest_seat_id

def my_seat():
    # iterate through the array seats_taken
    # find first occupied seat
    first_non_zero_index = -1
    for index in range(len(seats_taken)):
        if seats_taken[index] == 1:
            first_non_zero_index = index
            break

    # now look for the first 0 after first occupied seat
    zero_index = -1
    for index in range(first_non_zero_index,len(seats_taken) ):
        if seats_taken[index] == 0:
            # this is my seat
            zero_index = index
            break
    # this must be my seat
    return zero_index
def part2(data):
    """Solve part 2."""
    for data_item in data:
        seat_id = calculate_seat_id(data_item)
        seats_taken[seat_id] = 1
    return my_seat()

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))