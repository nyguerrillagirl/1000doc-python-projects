from collections import deque

# THIS IS A BETTER SOLUTION but the number is negative of the real number ....need to fix this!!

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
    print(f"processing result for (row,col) result ({row},{col})")
    max_rows = len(tachyon_manifold_lines)
    if row > max_rows - 1:
        print(f"1 - returning (row,col) result ({row},{col}) of {memo[row-1][col]}")
        return memo[row-1][col]

    result = 0
    if memo[row][col] != -1:
        result =  memo[row][col]
    elif tachyon_manifold_lines[row][col] == SPLITTER:
        result =   calcuate_paths_to_bottom(tachyon_manifold_lines, row, col-1, memo) + \
                            calcuate_paths_to_bottom(tachyon_manifold_lines, row, col + 1, memo)
        memo[row][col] = result
    else:
        result = calcuate_paths_to_bottom(tachyon_manifold_lines, row+1, col, memo)
        memo[row][col] = result
    print(f"2 - returning (row,col) result ({row},{col}) of {result}")
    return result

def main():
    gen = process_tachyon_manifold_lines('day_07_test_data.txt')
    tachyon_manifold_lines = []     # holds the entire tachyon_manifold diagram
    dq = deque()                    # beam positions
    total_number_of_splits = 0      # tracks number of splits we have made

    # process the tachyon manifold diagram
    count=0
    for manifold_line in gen:
        tachyon_manifold_lines.append(manifold_line)
        count += 1
        if (count == 4):
            break

    n = len(tachyon_manifold_lines)  # size
    m = len(tachyon_manifold_lines[0])
    print(f"number of rows: {n}")
    # use this list to update paths from S to any point(x,y)
    memo  = [[-1 for _ in range(m)] for _ in range(n)]
    # make row 0, path_length=0
    for index in range(0, m):
        memo[0][index] = 0
        memo[1][index] = 0

    row = 2
    col = find_S_position(tachyon_manifold_lines[0])

    quantum_count = calcuate_paths_to_bottom(tachyon_manifold_lines, row, col, memo)


    print(f"Number quantum count: {quantum_count}")



if __name__ == "__main__":
    main()