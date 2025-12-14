def is_point_in_red_green_space(point, row_grid, col_grid):
    '''
    determines if point falls into a red/green spot
    '''
    r = point[0]
    c = point[1]
    if (r < 0) or (r > len(row_grid)):
        return False

    if (c < 0) or (c > len(col_grid)):
        return False

    falls_inside_red_green_space = False
    # if this point is bounded by a range above, below, left and right than it is inside the polygon
    range_above = False
    range_below = False
    range_left = False
    range_right = False

    # get row this point is on
    row_list = row_grid[r]      # contains a list of tuples
    for interval in row_list:
        range_low = interval[0]
        range_high = interval[1]
        if (c >= range_low) and (c <= range_high):
            return True
        else:
            # check of col to the left and right
            if range_low > c:
                range_left = True
            elif range_high < c:
                range_right = True

    # check if this r falls into any col_list
    col_list = col_grid[c]      # contains a list of tuples
    for interval in col_list:
        range_low = interval[0]
        range_high = interval[1]
        if (r >= range_low and (r <= range_high)):
            return True
        else:
            if range_low > r:
                range_above = True
            elif range_high < r:
                range_below = True

    falls_inside_red_green_space = range_left and range_right and range_above and range_below

    return falls_inside_red_green_space

def is_rectangle_in_bounds(point_1, point_2,row_grid, col_grid):
    '''
    We figure out the other end p
    :param point_1: one end-point of a rectangle
    :param point_2: the diagonal end-point of a rectangle
    :param row_grid: the col bounds of the red/green area
    :param col_grid: the row bounds of the red/green area
    :return:
    '''
    result = False
    point_3 = (point_1[0], point_2[1])
    point_4 = (point_2[0], point_1[1])

    result =  is_point_in_red_green_space(point_3, row_grid, col_grid) and \
           is_point_in_red_green_space(point_4, row_grid, col_grid)

    if result:
        # check that there exists in bounding row interval and bounding col interval
        # for the line (p1, p3) and (p2, p4)
        if point_1[1] < point_3[1]:
            pass
    else:
        return result

def smartly_merge_tuple(new, intervals, merge_touching=True):
    """
     intervals: sorted, non-overlapping list of (start, end)
     new: (start, end)
     merge_touching:
         True  => [1,3] and [4,5] merge -> [1,5]
         False => [1,3] and [4,5] stay separate
     """
    new_start, new_end = new
    result = []
    if len(intervals) == 0:
        return [new]

    # define gap condition based on merge_touching
    if merge_touching:
        # touching counts as overlapping
        def is_before(start, end, new_start, new_end):
            return end < new_start - 0  # strictly before, no touch

        def is_after(start, end, new_start, new_end):
            return start > new_end + 0  # strictly after, no touch
    else:
        # touching does NOT merge
        def is_before(start, end, new_start, new_end):
            return end < new_start  # can touch at new_start

        def is_after(start, end, new_start, new_end):
            return start > new_end  # can touch at new_end

    for start, end in intervals:

        if (end == new_start) or (end+1 == new_start):  # new_start - 1:
            new_start = start
            continue

        if (new_end == start) or (new_end+1 == start):
            new_end = end
            continue

        if is_before(start, end, new_start, new_end):
            # current interval is completely before new interval
            result.append((start, end))

        elif is_after(start, end, new_start, new_end):
            # current interval is completely after new interval
            # push the merged new interval once, then shift "new" forward
            result.append((new_start, new_end))
            new_start, new_end = start, end

        else:
            # overlap (or touch, depending on merge_touching)
            new_start = min(new_start, start)
            new_end = max(new_end, end)

    # add the last merged/new interval
    result.append((new_start, new_end))
    return result


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
        row_grid[prev_row] = smartly_merge_tuple((low_col_index, high_col_index),row_grid[prev_row] )
        for c in range(low_col_index, high_col_index+1):
            #col_grid[c].append((prev_row, prev_row))
            col_grid[c] = smartly_merge_tuple((prev_row, prev_row),col_grid[c] )
    else:
        # the prev_col == current_col
        low_row_index = min(prev_row, current_row)
        high_row_index = max(prev_row, current_row)
        # enter the new tuple into col_grid
        #col_grid[prev_col].append((low_row_index, high_row_index))
        col_grid[prev_col] = smartly_merge_tuple((low_row_index, high_row_index),col_grid[prev_col] )
        for r in range(low_row_index, high_row_index+1):
            #row_grid[r].append((prev_col, prev_col))
            row_grid[r] = smartly_merge_tuple((prev_col, prev_col), row_grid[r])


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


# red_tile_positions in the form: [(r1, c1), (r2,c2), ...]
# we process all red_tiles obtaining the boundary of red/green tiles
red_tile_positions, max_rows, max_cols = read_in_all_red_tile_positions("day_09_test_data.txt")

row_grid, col_grid = create_psuedo_grids(red_tile_positions, max_rows, max_cols)