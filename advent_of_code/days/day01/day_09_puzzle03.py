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


# ------------------------------
# Integer geometry primitives
# ------------------------------

def orient(a, b, c):
    """
    Orientation of triplet (a, b, c):
    >0 = CCW, <0 = CW, 0 = collinear.
    All integer math.
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - \
           (b[1] - a[1]) * (c[0] - a[0])


def on_segment(a, b, c):
    """
    Returns True if point c lies on segment ab.
    Assumes a, b, c are collinear.
    """
    return (min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and
            min(a[1], b[1]) <= c[1] <= max(a[1], b[1]))


def proper_intersection(A, B, C, D):
    """
    Returns True only if segments AB and CD intersect
    at a point strictly inside both segments.
    No touching, no collinearity.
    """
    o1 = orient(A, B, C)
    o2 = orient(A, B, D)
    o3 = orient(C, D, A)
    o4 = orient(C, D, B)

    # If any orientation is zero → touching or collinear → NOT proper
    if o1 == 0 or o2 == 0 or o3 == 0 or o4 == 0:
        return False

    # Proper intersection requires opposite orientations
    return (o1 > 0) != (o2 > 0) and (o3 > 0) != (o4 > 0)


# ------------------------------
# Point-in-polygon (integer)
# Ray casting method
# ------------------------------

def point_in_polygon(pt, poly):
    """
    Returns True if point is inside or on boundary.
    poly = list of vertices [(x,y), ...] in order.
    """
    x, y = pt
    inside = False
    n = len(poly)

    for i in range(n):
        a = poly[i]
        b = poly[(i + 1) % n]

        # Check if point is exactly on an edge
        if orient(a, b, pt) == 0 and on_segment(a, b, pt):
            return True

        # Ray casting: check if edge crosses horizontal ray
        xi, yi = a
        xj, yj = b

        intersects = ((yi > y) != (yj > y)) and \
                     (x < (xj - xi) * (y - yi) / (yj - yi) + xi)

        if intersects:
            inside = not inside

    return inside


# ------------------------------
# Main function:
# Is segment AB fully inside polygon?
# ------------------------------

def segment_inside_polygon(A, B, poly):
    """
    Returns True if segment AB lies completely inside (or on boundary of) polygon poly.
    poly is a list of vertices in order.
    """

    # 1. Endpoints must be inside or on boundary
    if not point_in_polygon(A, poly):
        return False
    if not point_in_polygon(B, poly):
        return False

    # 2. Segment must not properly intersect any polygon edge
    n = len(poly)
    for i in range(n):
        C = poly[i]
        D = poly[(i + 1) % n]   # this connects the last point in poly with first

        if proper_intersection(A, B, C, D):
            return False

    # 3. If segment lies on an edge or touches edges, that's allowed
    return True


def is_rectangle_in_bounds(p1, p2, polygon_edges):
    # generate p3 and p4
    p3 = (p1[0], p2[1])
    p4 = (p2[0], p1[1])

    if p1[0] == p2[0]:
        return segment_inside_polygon(p1, p2, polygon_edges)

    if p1[1] == p2[1]:
        return segment_inside_polygon(p1, p2, polygon_edges)

    line_segment_list = [(p1, p4), (p4, p2), (p1, p3), (p3, p2)]

    result = True
    for point1, point2 in line_segment_list:
        if  not segment_inside_polygon(point1, point2, polygon_edges):
            result = False
            break

    return result

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

def find_largest_legal_rect(red_tile_positions):
    largest_area_found = -1
    red_tile_index_1 = -1
    red_tile_index_2 = -1

    for i, j in itertools.combinations(range(len(red_tile_positions)), 2):
        if is_rectangle_in_bounds(red_tile_positions[i], red_tile_positions[j], red_tile_positions):
            area_candidate = calculate_area(red_tile_positions[i], red_tile_positions[j])
            if area_candidate > largest_area_found:
                largest_area_found = area_candidate
                red_tile_index_1 = i
                red_tile_index_2 = j

    return (red_tile_positions[red_tile_index_1], red_tile_positions[red_tile_index_2], largest_area_found)

def process_red_tiles(red_tile_positions):
    polygon_edges = []
    first_point = None
    previous_point = None
    for tile_point in red_tile_positions:
        if first_point is None:
            first_point = tile_point
            previous_point = first_point
            continue
        new_edge = [previous_point, tile_point]
        polygon_edges.append(new_edge)
        previous_point = tile_point

    new_edge = [previous_point, first_point]
    polygon_edges.append(new_edge)

    return polygon_edges

def main():
    # test file: day_09_test_data.txt, puzzle file:puzzle09_input.txt
    # another test file: day_09_test_data2.txt
    red_tile_positions, max_rows, max_cols = read_in_all_red_tile_positions("puzzle_09_input.txt")
    print(f"red_tile_positions: {red_tile_positions}")
    #polygon_edges = process_red_tiles(red_tile_positions)
    #print(f"polygon_edges: {polygon_edges}")
    position_1, position_2, area_of_rect = find_largest_legal_rect(red_tile_positions)

    print(f"tile at {position_1} and tile at {position_2} form the largest legal rect of: {area_of_rect}")


if __name__ == "__main__":
    main()