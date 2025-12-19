# aoc_template.py

import pathlib
import sys


def parse(puzzle_input):
    """Parse input."""
    segments = []

    for line in puzzle_input.splitlines():
        left, right = line.split(" -> ")
        x1, y1 = map(int, left.split(","))
        x2, y2 = map(int, right.split(","))
        segments.append([(x1, y1), (x2, y2)])

    return segments


def filter_lines(data):
    '''
    This function removes from data: [[(x1, y1),(x2, y2)], ...] all line segments that are not vertical
    or horizontal
    :param data:
    :return:
    '''
    new_data = []
    for line_segment in data:
        point1 = line_segment[0]
        point2 = line_segment[1]
        if (point1[0] == point2[0]) or (point1[1] == point2[1]):
            # add to the new_data
            new_data.append(line_segment)

    return new_data


def check_col_overlap(target_col, from_row, to_row, col_dict):
    ranges_to_check = col_dict[target_col]
    for t in ranges_to_check:
        # check if there is any overlap from from_row and to_row


def determine_all_overlapping_lines(data2):
    row_dict = {}
    col_dict = {}
    overlap_count = 0
    for line_segment in data2:
        # line_segment = [(x1, y1), (x2, y2)]
        # detemine if this is a vertical or horizontal line
        x1 = line_segment[0][0]
        y1 = line_segment[0][1]
        x2 = line_segment[1][0]
        y2 = line_segment[1][1]
        if x1 == x2:
            # this is a vertical line, add to col_dict and row_dict
            if x1 in col_dict:
                ## see if overlap with existing entries
                overlap_count += check_col_overlap(x1,min(y1, y2), max(y1,y2), col_dict )
            else:
                # just enter the first col entry
                col_dict[x1] = [((min(y1, y2), max(y1,y2)))]

def part1(data):
    """Solve part 1."""
    data2 = filter_lines(data)
    return determine_all_overlapping_lines(data2)

def part2(data):
    """Solve part 2."""
    pass


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    print(f"data: {data}")
    solution1 = part1(data)
    solution2 = part2(data)

    return solution1, solution2


if __name__ == "__main__":
    for path in sys.argv[1:]:
        print(f"{path}:")
        puzzle_input = pathlib.Path(path).read_text().strip()
        solutions = solve(puzzle_input)
        print("\n".join(str(solution) for solution in solutions))