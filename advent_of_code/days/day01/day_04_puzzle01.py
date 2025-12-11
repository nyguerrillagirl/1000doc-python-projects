'''
--- Day 4: Printing Department ---
You ride the escalator down to the printing department. They're clearly getting ready for Christmas; they have lots of large rolls of paper everywhere, and there's even a massive printer in the corner (to handle the really big print jobs).

Decorating here will be easy: they can make their own decorations. What you really need is a way to get further into the North Pole base while the elevators are offline.

"Actually, maybe we can help with that," one of the Elves replies when you ask for help. "We're pretty sure there's a cafeteria on the other side of the back wall. If we could break through the wall, you'd be able to keep moving. It's too bad all of our forklifts are so busy moving those big rolls of paper around."

If you can optimize the work the forklifts are doing, maybe they would have time to spare to break through the wall.

The rolls of paper (@) are arranged on a large grid; the Elves even have a helpful diagram (your puzzle input) indicating where everything is located.

For example:

..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

The forklifts can only access a roll of paper if there are fewer than four rolls of paper in the eight adjacent positions. If you can figure out which rolls of paper the forklifts can access, they'll spend less time looking and more time breaking down the wall to the cafeteria.

In this example, there are 13 rolls of paper that can be accessed by a forklift (marked with x):

..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Consider your complete diagram of the paper roll locations. How many rolls of paper can be accessed by a forklift?

To begin, get your puzzle input.

Answer:

SEE docs/20251204/SOULTION_NOTES.docx for my thoughts
'''
from collections import defaultdict
from typing import List, Tuple, DefaultDict

ColumnDict = DefaultDict[int, List]
RowDict = DefaultDict[int, ColumnDict]

PAPER_ROLL = "@"
EMPTY_DOT = "."
ACCESSIBLE_PAPER_ROLL = 'x'

# define our dictionary <int, <inner_dict>> where <inner_dict> is
# <int, [string, int]> structure



def read_in_next_paper_roll_line(filename):
    '''
    This function opens a files and yields the next rotation value, until none remains
    :return:
    '''
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()

def print_grid(grid:RowDict):
    for row_number, inner_dict in grid.items():
        # contruct row
        row_value = ""
        for col_number, the_list in inner_dict.items():
            tuple_value = the_list[0]
            if tuple_value == PAPER_ROLL:
                row_value += PAPER_ROLL
            elif tuple_value == EMPTY_DOT:
                row_value += EMPTY_DOT
            else:
                row_value += ACCESSIBLE_PAPER_ROLL

        print(row_value)
def process_for_adjacent_paper_rolls(grid, number_of_rows, number_of_cols):
    for row in range(number_of_rows):
        for col in range(number_of_cols):
            # processing all adjacent cells to (row,col) if PAPER_ROLL
            if grid[row][col][0] == EMPTY_DOT:
                continue
            # check grid position at (row-1, col-1)
            if (row-1 >= 0) and (col-1 >=0):
                if grid[row-1][col-1][0] == PAPER_ROLL:
                    grid[row][col][1] += 1

            # check grid position at (row-1, col)
            if row-1 >= 0:
                if grid[row-1][col][0] == PAPER_ROLL:
                    grid[row][col][1] += 1

            # check grid position at (row-1, col+1)
            if (row-1 >= 0) and (col+1 < number_of_cols):
                if grid[row-1][col+1][0] == PAPER_ROLL:
                    grid[row][col][1] += 1

            # check grid position at (row, col-1)
            if col-1 >= 0:
                if grid[row][col-1][0] == PAPER_ROLL:
                    grid[row][col][1] += 1

            # check grid position at (row, col+1)
            if col+1 < number_of_cols:
                if grid[row][col+1][0] == PAPER_ROLL:
                    grid[row][col][1] += 1

            # check grid position at (row+1, col-1)
            if (row+1 < number_of_rows) and (col-1 >=0):
                if grid[row+1][col-1][0] == PAPER_ROLL:
                    grid[row][col][1] += 1

            # check grid position at (row+1, col)
            if row+1 < number_of_rows:
                if grid[row+1][col][0] == PAPER_ROLL:
                    grid[row][col][1] += 1

            # check grid position at (row+1, col+1)
            if (row+1 < number_of_rows) and (col+1 < number_of_cols):
                if grid[row+1][col+1][0] == PAPER_ROLL:
                    grid[row][col][1] += 1

def mark_accessible_paper_rolls(grid, number_of_rows, number_of_cols):
    accessible_paper_roll_count = 0
    for row in range(number_of_rows):
        for col in range(number_of_cols):
            adjacent_paper_rolls = grid[row][col][1]
            if (grid[row][col][0] == PAPER_ROLL) and (grid[row][col][1] < 4):
                grid[row][col][0] = ACCESSIBLE_PAPER_ROLL
                accessible_paper_roll_count += 1

    return accessible_paper_roll_count

def main():

    # this is our grid
    grid:RowDict = defaultdict(lambda: defaultdict(list))

    gen = read_in_next_paper_roll_line("puzzle04_input.txt")

    # track number of rows and columns in our grid
    number_of_rows = 0      # currently unknown
    number_of_cols = 0      # also unknown at this time
    # process each row into our grid
    row_number = 0
    for paper_roll_line in gen:
        # process line
        if number_of_cols == 0:
            number_of_cols = len(paper_roll_line)   # only determine this one time
        col_number = 0
        for char in paper_roll_line:
            if char == PAPER_ROLL:
                grid[row_number][col_number].append(PAPER_ROLL)
            else:
                grid[row_number][col_number].append(EMPTY_DOT)

            grid[row_number][col_number].append(0)

            col_number += 1
        row_number+=1   # go to the next row

    number_of_rows = row_number

    # Now process each grid[row_number][col_number] of a PAPER_ROLL and
    process_for_adjacent_paper_rolls(grid, number_of_rows, number_of_cols)
    accessible_paper_roll_count = mark_accessible_paper_rolls(grid, number_of_rows, number_of_cols)

    print(f"accessible_paper_roll_count:  {accessible_paper_roll_count}")

if __name__ == "__main__":
    main()