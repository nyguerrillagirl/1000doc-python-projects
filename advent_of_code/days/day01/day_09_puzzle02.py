'''
NOTE: D O E S   N O T  W O R K - Y E T !
WORKING ON A NEW VERSION

--- Part Two ---
The Elves just remembered: they can only switch out tiles that are red or green. So, your rectangle can only include red or green tiles.

In your list, every red tile is connected to the red tile before and after it by a straight line of green tiles. The list wraps, so the first red tile is also connected to the last red tile. Tiles that are adjacent in your list will always be on either the same row or the same column.

Using the same example as before, the tiles marked X would be green:

..............
.......#XXX#..
.......X...X..
..#XXXX#...X..
..X........X..
..#XXXXXX#.X..
.........X.X..
.........#X#..
..............
In addition, all of the tiles inside this loop of red and green tiles are also green. So, in this example, these are the green tiles:

..............
.......#XXX#..
.......XXXXX..
..#XXXX#XXXX..
..XXXXXXXXXX..
..#XXXXXX#XX..
.........XXX..
.........#X#..
..............
The remaining tiles are never red nor green.

The rectangle you choose still must have red tiles in opposite corners, but any other tiles it includes must now be red or green. This significantly limits your options.

For example, you could make a rectangle out of red and green tiles with an area of 15 between 7,3 and 11,1:

..............
.......OOOOO..
.......OOOOO..
..#XXXXOOOOO..
..XXXXXXXXXX..
..#XXXXXX#XX..
.........XXX..
.........#X#..
..............
Or, you could make a thin rectangle with an area of 3 between 9,7 and 9,5:

..............
.......#XXX#..
.......XXXXX..
..#XXXX#XXXX..
..XXXXXXXXXX..
..#XXXXXXOXX..
.........OXX..
.........OX#..
..............
The largest rectangle you can make in this example using only red and green tiles has area 24. One way to do this is between 9,5 and 2,3:

..............
.......#XXX#..
.......XXXXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
..OOOOOOOOXX..
.........XXX..
.........#X#..
..............
Using two red tiles as opposite corners, what is the largest area of any rectangle you can make using only red and green tiles?
'''
import itertools

def absolute_value(x):
    if x >= 0:
        return x
    else:
        return -x

def read_in_all_red_tile_positions(filename):
    '''
    reads in the data - and sends back a list of red tiles [(r1, c1), (r2,c2), ...] and
    the maximum number of rows (highest row index + 1) and maximum number of cols
    (highest col index + 1
    :return:
    '''
    red_tile_positions = []
    max_row = -1
    max_col = -1
    with open(filename, "r") as f:
        for line in f:
            col, row = line.strip().split(",")
            red_tile_positions.append((int(row), int(col)))
            if red_tile_positions[-1][0] > max_row:
                max_row = red_tile_positions[-1][0]
            if red_tile_positions[-1][1] > max_col:
                max_col = red_tile_positions[-1][1]

    return (red_tile_positions, max_row+1, max_col+1)

def create_psuedo_grids(red_tile_positions, max_rows, max_cols):
    '''
    creates a two 2D list, where one is the row_grid, where every row has the (lowest_col, highest_col)
    and a col_grid, where every col has the (lowest_row, highest_row)
    :param red_tile_positions:
    :return:
    '''
    row_grid = [[max_cols+1, -1] for i in range(max_rows)]
    col_grid = [[max_rows+1, -1  ] for i in range(max_cols)]

    for red_tile_position in red_tile_positions:
        row, col = red_tile_position
        # process row_grid[row] first
        grid_row_list = row_grid[row]
        if col < grid_row_list[0]:
            grid_row_list[0] = col

        if col > grid_row_list[1]:
            grid_row_list[1] = col

        #process col_grid[col]
        grid_cow_list = col_grid[col]
        if row < grid_cow_list[0]:
            grid_cow_list[0] = row

        if row > grid_cow_list[1]:
            grid_cow_list[1] = row

    # any grid[row] == [max_cols+1, -1] means not red_tiles on this line
    return row_grid, col_grid

def empty_row_or_col(the_list):
    return (the_list[0] == -1) or (the_list[1] == -1)

def is_point_in_red_green_space(point, row_grid, col_grid):
    '''
    determines if point falls into a red/green spot
    '''
    r = point[0]
    c = point[1]
    if (r < 0) or (r > len(row_grid)):
        return false

    if (c < 0) or (c > len(col_grid)):
        return false

    falls_inside_red_green_space = False

    # get row this point is on
    row_list = row_grid[r]
    if not empty_row_or_col(row_list):
        # check if c falls beteen col range
        if (c >= row_list[0]) and (c <= row_list[1]):
            return True

    # check if this r falls into any col_list
    col_list = col_grid[c]
    if not empty_row_or_col(col_list):
        if (r >= col_list[0] and (r <= col_list[1])):
            return True

    return falls_inside_red_green_space

def process_grids(row_grid, col_grid):
    '''
    For empty rows, determine if there is a X bound - mark it
    For empty cols
    :param row_grid:
    :param col_grid:
    :return:
    '''
    # process the rows first to set the row bounds on all columns this occupies
    print("processing the column bounds for this row")
    for row_index in range(len(row_grid)):
        list_bounds = row_grid[row_index]
        if not empty_row_or_col(list_bounds):
            col_low_on_row_index = list_bounds[0]
            col_high_on_row_index = list_bounds[1]
            # examine each col (in this row range) see if we need to update the cols [row_low, row_high]
            for col_index in range(col_low_on_row_index, col_high_on_row_index+1):
                col_list_bounds = col_grid[col_index]
                if col_list_bounds[0] > row_index:
                    col_list_bounds[0] = row_index
                if col_list_bounds[1] < row_index:
                    col_list_bounds[1] = row_index

    print("processing the row bounds for the columns")
    for col_index in range(len(col_grid)):
        row_bounds_list = col_grid[col_index]
        if not empty_row_or_col(row_bounds_list):
            row_low_on_col_index = row_bounds_list[0]
            row_high_on_col_index = row_bounds_list[1]
            # examine each row in col range to see if we need to update the rows (low_col, high_col) value
            for row in range(row_low_on_col_index, row_high_on_col_index+1):
                row_list_bounds = row_grid[row]
                if row_list_bounds[0] > col_index:
                    row_list_bounds[0] = col_index
                if row_list_bounds[1] < col_index:
                    row_list_bounds[1] = col_index

    print("*** process_grids completed ***")

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

def is_rectangle_in_bounds(point_1, point_2,row_grid, col_grid):
    '''
    We figure out the other end p
    :param point_1: one end-point of a rectangle
    :param point_2: the diagonal end-point of a rectangle
    :param row_grid: the col bounds of the red/green area
    :param col_grid: the row bounds of the red/green area
    :return:
    '''
    point_3 = (point_1[0], point_2[1])
    point_4 = (point_2[0], point_1[1])

    return is_point_in_red_green_space(point_3, row_grid, col_grid) and \
           is_point_in_red_green_space(point_4, row_grid, col_grid)

def find_largest_rect(red_tile_positions,  row_grid, col_grid):
    print("*** find_largest_rect ***")
    largest_area_found = -1
    red_tile_index_1 = -1
    red_tile_index_2 = -1

    for i, j in itertools.combinations(range(len(red_tile_positions)), 2):
        if (is_rectangle_in_bounds(red_tile_positions[i], red_tile_positions[j], row_grid, col_grid)):
            area_candidate = calculate_area(red_tile_positions[i], red_tile_positions[j])
            if area_candidate > largest_area_found:
                largest_area_found = area_candidate
                red_tile_index_1 = i
                red_tile_index_2 = j

    return (red_tile_positions[red_tile_index_1], red_tile_positions[red_tile_index_2], largest_area_found)

def main():
    # test file: day_09_test_data.txt, puzzle file:puzzle09_input.txt
    # another test file: day_09_test_data2.txt
    red_tile_positions, max_rows, max_cols = read_in_all_red_tile_positions("day_09_test_data2.txt")
    # red_tile_positions in the form: [(r1, c1), (r2,c2), ...]
    # we process all red_tiles obtaining the boundary of red/green tiles
    row_grid, col_grid = create_psuedo_grids(red_tile_positions, max_rows, max_cols)
    process_grids(row_grid, col_grid);

    # at this point I know the bounds of red/green tiles on each row and column

    position_1, position_2, area_of_rect = find_largest_rect(red_tile_positions, row_grid, col_grid)
    print(f"tile at {position_1} and tile at {position_2} form the largest legal rect of: {area_of_rect}")

if __name__ == "__main__":
    main()