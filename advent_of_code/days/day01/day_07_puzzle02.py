from collections import deque

# THIS SOLUTION SUCKS....changing to use dynamic programming

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


def calcuate_paths_to_bottom(tachyon_manifold_lines, row, col, memo):
    '''
    we use a recursive algorithm to calucate the number of paths from this point to the last line
    :param tachyon_manifold_lines:
    :param row:
    :param col:
    :return:
    '''
def main():
    gen = process_tachyon_manifold_lines('day_07_test_data.txt')
    tachyon_manifold_lines = []     # holds the entire tachyon_manifold diagram
    dq = deque()                    # beam positions
    total_number_of_splits = 0      # tracks number of splits we have made

    # process the tachyon manifold diagram
    for manifold_line in gen:
        tachyon_manifold_lines.append(manifold_line)

    print("total number of lines: ", len(tachyon_manifold_lines))
    n = len(tachyon_manifold_lines)  # size
    memo  = [[-1 for _ in range(n)] for _ in range(n)]
    print(memo)
    s_position = (0, find_S_position(tachyon_manifold_lines[0]))
    path_list = [[s_position]]

    for current_index in range(1, len(tachyon_manifold_lines)-1):
        # examine each current path and build a new_path_list
        new_path_list = []
        print(f"current_index: {current_index} size of current path_list: {len(path_list)}")
        for path in path_list:
            if (current_index % 2 == 1):
                # this is a all EMPTY_SPACE line
                row, col = path[-1]
                path.append((row+1, col))
                new_path_list.append(path)
            else:
                # check if next line col position has slitter or not
                row, col = path[-1]
                if tachyon_manifold_lines[current_index][col] == EMPTY_SPACE:
                    # just attach next position to the current path
                    path.append((row+1, col))
                    new_path_list.append(path)
                else:
                    # this must be a splitter so add (row, col-1) and (row, col+1) to two new path
                    new_path_list.append(path + [(row+1, col-1)])
                    new_path_list.append(path + [(row+1, col+1)])

        path_list = new_path_list

    # for path in path_list:
    #     print(f"path: {path}" )

    quantum_count = len(path_list)

    print(f"Number quantum count: {quantum_count}")

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