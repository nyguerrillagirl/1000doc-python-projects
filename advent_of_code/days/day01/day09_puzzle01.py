'''
--- Day 9: Movie Theater ---
You slide down the firepole in the corner of the playground and land in the North Pole base movie theater!

The movie theater has a big tile floor with an interesting pattern. Elves here are redecorating the theater by switching out some of the square tiles in the big grid they form. Some of the tiles are red; the Elves would like to find the largest rectangle that uses red tiles for two of its opposite corners. They even have a list of where the red tiles are located in the grid (your puzzle input).

For example:

My note: The list below is col, row order. In addition all the counts start at 0.
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3

Showing red tiles as # and other tiles as ., the above arrangement of red tiles would look like this:

..............
.......#...#..
..............
..#....#......
..............
..#......#....
..............
.........#.#..
..............

You can choose any two red tiles as the opposite corners of your rectangle; your goal is to find the largest rectangle possible.

For example, you could make a rectangle (shown as O) with an area of 24 between 2,5 and 9,7:

..............
.......#...#..
..............
..#....#......
..............
..OOOOOOOO....
..OOOOOOOO....
..OOOOOOOO.#..
..............
Or, you could make a rectangle with area 35 between 7,1 and 11,7:

..............
.......OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
..#....OOOOO..
.......OOOOO..
.......OOOOO..
..............
You could even make a thin rectangle with an area of only 6 between 7,3 and 2,3:

..............
.......#...#..
..............
..OOOOOO......
..............
..#......#....
..............
.........#.#..
..............
Ultimately, the largest rectangle you can make in this example has area 50. One way to do this is between 2,5 and 11,1:

..............
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..............
.........#.#..
..............

Using two red tiles as opposite corners, what is the largest area of any rectangle you can make?

To begin, get your puzzle input.

Answer:

'''
import itertools

def read_in_all_red_tile_positions(filename):
    '''
    This function opens a files and reads in all 3D points and returns them in a list of tuples in the form
    (a, b, c)
    :return:
    '''
    red_tile_positions = []
    with open(filename, "r") as f:
        for line in f:
            col, row = line.strip().split(",")
            red_tile_positions.append((int(row), int(col)))

    return red_tile_positions

def absolute_value(x):
    if x >= 0:
        return x
    else:
        return -x

def calculate_area(red_tile_1, red_tile_2):
    '''
    Returns the area if these two tiles were the corners of a rectangle
    :param red_tile_1:
    :param red_tile_2:
    :return:
    '''
    width = (absolute_value(red_tile_1[0] - red_tile_2[0])) + 1
    height = (absolute_value(red_tile_1[1] - red_tile_2[1])) + 1

    return width * height

def find_largest_rect(red_tile_positions):
    largest_area_found = -1
    red_tile_index_1 = -1
    red_tile_index_2 = -1

    for i, j in itertools.combinations(range(len(red_tile_positions)), 2):
        area_candidate = calculate_area(red_tile_positions[i], red_tile_positions[j])
        if area_candidate > largest_area_found:
            largest_area_found = area_candidate
            red_tile_index_1 = i
            red_tile_index_2 = j

    return (red_tile_positions[red_tile_index_1], red_tile_positions[red_tile_index_2], largest_area_found)

def main():
    red_tile_positions = read_in_all_red_tile_positions("puzzle09_input.txt")
    position_1, position_2, area_of_rect = find_largest_rect(red_tile_positions)
    print(f"tile at {position_1} and tile at {position_2} form the largest rect of: {area_of_rect}")

if __name__ == "__main__":
    main()