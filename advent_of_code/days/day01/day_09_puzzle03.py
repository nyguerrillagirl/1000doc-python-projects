'''
--- Part Two ---
The Elves just remembered: they can only switch out tiles that are red or green.
So, your rectangle can only include red or green tiles.

In your list, every red tile is connected to the red tile before and after it by a straight line of green tiles.
The list wraps, so the first red tile is also connected to the last red tile.
Tiles that are adjacent in your list will always be on either the same row or the same column.

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
In addition, all of the tiles inside this loop of red and green tiles are also green.
So, in this example, these are the green tiles:

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

The rectangle you choose still must have red tiles in opposite corners, but any other tiles it includes must
now be red or green. This significantly limits your options.

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


def smartly_merge_tuple(t_under_consideration, tuple_list):
    '''
    This function smartly places t_under_consideration on to the tuple_list.
    We return a new tuple_list
    case #0 if tuple is of the form (x,y) and there exists a tuple of the form (a,b) where x <= a and b <= y the
            replace (a,b) with (x,y)
    case #1 if tuple is of the form (x,x) and there exists a range that includes x ...drop (x,x)
    case #2 if tuple is of the form (x,y) remove any entries that are of the form (x,x),....up to (y,y)
    case #3 if tuple is of the form (x,y) and there exists another tuple of the form (y,z) then combine into (x,z)
    case #4 if tuple is of the form (x,y) and there exists another tuple of the form (y+1,z) the combine into (x,z)
    '''
    t_x = t_under_consideration[0]
    t_y = t_under_consideration[1]

    for index, tuple_point in enumerate(tuple_list):
        x = tuple_point[0]
        y = tuple_point[1]
        # see if t_under_consideration is subsumed by this tuple_point
        if (x <= t_x) and (y >= t_y):
            # t_under_consideration is included in this tuple range point
            return tuple_list
        # does t_under_consideration subsume  this tuple?
        if (x >= t_x) and (y <= t_y):
            # this point is covered by (t_x, t_y)
            tuple_list[index] = t_under_consideration
            return tuple_list
        if (t_y == x) or (t_y == x + 1):
            # merge the new tuple into this tuple
            new_tuple = (x, t_y)
            tuple_list[index] = new_tuple
            return tuple_list
        if (y == t_x) or (y == t_x + 1):
            new_tuple = (t_x, y)
            tuple_list[index] = new_tuple
            return tuple_list
        if (t_y == x - 1):
            # fold t_under_consideration into current tuple
            new_tuple = (t_x, y)
            tuple_list[index] = new_tuple
            return tuple_list
        if (y == t_x - 1):
            # fold t_under_consideration into current tuple
            new_tuple = (x, t_y)
            tuple_list[index] = new_tuple
            return tuple_list

    # just add tuple
    print(f"appending {t_under_consideration} to current tuple_list: {tuple_list}")
    return tuple_list.append(t_under_consideration)


def update_grids(previous_tile_position, current_tile_position, row_grid, col_grid):
    '''
    Updates either the row_grid or col_grid depending on the line segment orientation
    The line segment is defined as previous_tile_position to current_tile_position
    :param previous_tile_position:
    :param current_tile_position:
    :param row_grid:
    :param col_grid:
    :return:
    '''
    # connect this red_tile_position with the previous position
    prev_row, prev_col = previous_tile_position
    current_row, current_col = current_tile_position
    # Determine if we update row_grid or col_grid
    if prev_row == current_row:
        low_col_index = min(prev_col, current_col)
        high_col_index = max(prev_col, current_col)
        # enter new tuple
        #row_grid[prev_row].append((low_col_index, high_col_index))
        print(f"\trow: {prev_row} adding range: ")
        print(f"\trow: {prev_row} adding range: {(low_col_index, high_col_index)} to current {row_grid[prev_row]} ")
        smartly_merge_tuple((low_col_index, high_col_index),row_grid[prev_row] )
        print(f"\trow: {prev_row} adding range: {(low_col_index, high_col_index)} changed {row_grid[prev_row]} ")
        for c in range(low_col_index, high_col_index+1):
            #col_grid[c].append((prev_row, prev_row))
            print(f"\tcol: {c} adding range: {(prev_row, prev_row)} to current {col_grid[c]} ")
            smartly_merge_tuple((prev_row, prev_row),col_grid[c] )
            print(f"\tcol: {c} adding range: {(prev_row, prev_row)} changed {col_grid[c]} ")
    else:
        # the prev_col == current_col
        low_row_index = min(prev_row, current_row)
        high_row_index = max(prev_row, current_row)
        # enter the new tuple into col_grid
        #col_grid[prev_col].append((low_row_index, high_row_index))
        print(f"\tcol: {prev_col} adding range: {(low_row_index, high_row_index)} to current {col_grid[prev_col]} ")
        smartly_merge_tuple((low_row_index, high_row_index),col_grid[prev_col] )
        print(f"\tcol: {prev_col} adding range: {(low_row_index, high_row_index)} changed {col_grid[prev_col]} ")
        for r in range(low_row_index, high_row_index+1):
            #row_grid[r].append((prev_col, prev_col))
            print(f"\trow: {r} adding range: {(prev_col, prev_col)} to current {row_grid[r]} ")
            smartly_merge_tuple((prev_col, prev_col), row_grid[r])
            print(f"\trow: {r} adding range: {(prev_col, prev_col)} changed {row_grid[r]} ")


def create_psuedo_grids(red_tile_positions, max_rows, max_cols):
    '''
    creates a two 2D list, where one is the row_grid, where every row has a list of [ (lowest_col1, highest_col1),
    (lowest_col2, highest_col2)...] of all the line segments on row[0], etc.
    and a col_grid, where every col has the[(lowest_row1, highest_row1), (lowest_row2, highest_row2)...]
    The above define the line segments created to define the polygon created by the red tiles
    :param red_tile_positions:
    :return:
    '''
    row_grid = [[] for i in range(max_rows)]
    col_grid = [[] for i in range(max_cols)]

    first_tile_position = None
    previous_tile_position = None
    for current_tile_position in red_tile_positions:
        if first_tile_position is None:
            # remember the very first tile_position to connect to last_tile_position
            first_tile_position = current_tile_position

        if previous_tile_position is None:
            previous_tile_position = current_tile_position
            continue

        update_grids(previous_tile_position, current_tile_position, row_grid, col_grid)

        previous_tile_position = current_tile_position

    # connect previous_tile_position to first_tile_position
    update_grids(previous_tile_position, first_tile_position, row_grid, col_grid)
    return row_grid, col_grid


def find_largest_rect_legal(red_tile_positions,  row_grid, col_grid):
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
    print(f"red_tile_positions: {red_tile_positions}")
    # red_tile_positions in the form: [(r1, c1), (r2,c2), ...]
    # we process all red_tiles obtaining the boundary of red/green tiles
    #row_grid, col_grid = create_psuedo_grids(red_tile_positions, max_rows, max_cols)

    #print(f"row_grid: {row_grid}")
    #print(f"col_grid: {col_grid}")
    #position_1, position_2, area_of_rect = find_largest_legal_rect(red_tile_positions, row_grid, col_grid)
    #print(f"tile at {position_1} and tile at {position_2} form the largest legal rect of: {area_of_rect}")

    candidate_tuple = (0, 3)
    tuple_list = [(0, 0), (3, 3)]
    _ = smartly_merge_tuple(candidate_tuple, tuple_list)
    print(f"new tuple list: {tuple_list}")

if __name__ == "__main__":
    main()