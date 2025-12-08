from collections import deque

EMPTY_SPACE = '.'
SPLITTER = '^'

def process_tachyon_manifold_lines(filename):
    '''
    This function opens a files and yields the next rotation value, until none remains
    :return:
    '''
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()

def find_S_position(manifold_line):
    return manifold_line.index('S')

def is_current_item_on_same_line(current_line_index, dq):
    '''
    Returns True if the left-most queue item is a tuple of the form (current_line_index, ?), else returns False
    :param current_line_index:
    :param dq:
    :return:
    '''
    result = False
    if dq:
        left_most_item = dq[0]
        result =  left_most_item[0] == current_line_index

    return result

def split_beam(col, next_manifold_line):
    '''
    returns tuple of locations to the left and right of the splitter col.
    note: if right or left is not possible send back None for that location (not possible, given the current
    maps ...but future proof.
    :param col:
    :param next_manifold_line:
    :return:
    '''
    left_col_position = col-1
    right_col_position = col+1

    if left_col_position < 0:
        left_col_position = None    # cannot use this spot

    if right_col_position >= len(next_manifold_line):
        right_col_position = None

    #print(f"left_col_position: {left_col_position}, right_col_position: {right_col_position}")
    return (left_col_position, right_col_position)

def move_down(current_line_index, next_manifold_line,  dq):
    number_of_splits_required = 0
    # remove items from queue as long as they are in the form of (current_line_index, ?)
    # note, we will only place on the queue locations in the form (current_line_index+1, ?)
    # so basically we pop the queue until we are done with all locations on this line
    while dq and (is_current_item_on_same_line(current_line_index, dq)):
        # pop the queue on the left and process
        current_position = dq.popleft()
        row = current_position[0]
        col = current_position[1]
        # can we move down?
        if next_manifold_line[col] == EMPTY_SPACE:
            # place beam (row+1, col) to the queue
            new_beam = (row+1, col)
            if new_beam not in dq:
                dq.append((row+1, col))
        else:
            # we must have hit a splitter
            number_of_splits_required += 1
            split_beam_1, split_beam_2 = split_beam(col, next_manifold_line)
            if split_beam_1 is not None:
                # add new beam location to the queue
                new_beam = (current_line_index+1, split_beam_1)
                if new_beam not in dq:
                    dq.append(new_beam)
            if split_beam_2 is not None:
                # add new beam location to the queue
                new_beam = (current_line_index+1, split_beam_2)
                if new_beam not in dq:
                    dq.append(new_beam)

    return number_of_splits_required

def main():
    gen = process_tachyon_manifold_lines('puzzle07_input.txt')
    tachyon_manifold_lines = []     # holds the entire tachyon_manifold diagram
    dq = deque()                    # beam positions
    total_number_of_splits = 0      # tracks number of splits we have made

    # process the tachyon manifold diagram
    for manifold_line in gen:
        tachyon_manifold_lines.append(manifold_line)

    #print(f"total # of line: {len(tachyon_manifold_lines)}")

    # find 'S' position
    s_position = find_S_position(tachyon_manifold_lines[0])

    dq.append((0, s_position))    # put starting beam position
    current_line = 0              # we are at this manifold line, trying to move down
    while current_line < len(tachyon_manifold_lines)-1:
        # keep moving down
        splits_required = move_down(current_line, tachyon_manifold_lines[current_line+1], dq)
        #print(f"line {current_line} required {splits_required} splits")
        total_number_of_splits += splits_required
        current_line += 1

    print(f"Number of total splits: {total_number_of_splits}")

# def main():
#     dq = deque([(13,1),(13,3),(13,4),(13,5),(13,7),(13,8),(13,10),(13,11),(13,13)])
#     current_index = 13
#     next_line = ".^.^.^.^.^...^."
#
#     split_number = move_down(current_index, next_line, dq)
#
#     print(f"split_number: {split_number}")
#     print(f"deque: {dq}")

if __name__ == "__main__":
    main()