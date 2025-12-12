'''
--- Part Two ---
Thanks in part to your analysis, the Elves have figured out a little bit about the issue. They now know that the problematic data path passes through both dac (a digital-to-analog converter) and fft (a device which performs a fast Fourier transform).

They're still not sure which specific path is the problem, and so they now need you to find every path from svr (the server rack) to out. However, the paths you find must all also visit both dac and fft (in any order).

For example:

svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out

This new list of devices contains many paths from svr to out:

svr,aaa,fft,ccc,ddd,hub,fff,ggg,out
svr,aaa,fft,ccc,ddd,hub,fff,hhh,out
svr,aaa,fft,ccc,eee,dac,fff,ggg,out
svr,aaa,fft,ccc,eee,dac,fff,hhh,out
svr,bbb,tty,ccc,ddd,hub,fff,ggg,out
svr,bbb,tty,ccc,ddd,hub,fff,hhh,out
svr,bbb,tty,ccc,eee,dac,fff,ggg,out
svr,bbb,tty,ccc,eee,dac,fff,hhh,out

However, only 2 paths from svr to out visit both dac and fft.

Find all of the paths that lead from svr to out. How many of those paths visit both dac and fft?
'''
from collections import defaultdict, deque

def extract_key(device_line):
    '''
    Processes a string of the form aaa: you hhh and returns a tuple: ('aaa', 'you hhh') the device
    key and the devices it is connected to
    :param device_line:
    :return:
    '''
    the_split_on_device_key = device_line.split(":")
    device_key = the_split_on_device_key[0]
    rest_of_line = the_split_on_device_key[1]

    return (device_key, rest_of_line)

def process_device_information(filename):
    '''
    This function opens a files and processing the list of devices and their outputs.
    We return a dictionary {'aaa': ['you', 'hhh'] ... etc.

    :return:
    '''
    puzzle_dict = defaultdict(list)

    with open(filename, "r") as f:
        for line in f:
            key, rest_of_line = extract_key(line.strip())
            device_list = rest_of_line.strip().split(" ")
            for device in device_list:
                puzzle_dict[key].append(device)


    return puzzle_dict



def path_count_seen_fft_and_dac(from_device, to_device, puzzle_device_dict, visited_nodes, overall_nodes, has_seen_fft, has_seen_dac):
    '''
    :param from_device:
    :param to_device:
    :param puzzle_device_dict:
    :param visited_nodes:
    :param overall_list_of_nodes
    :return:
    '''

    # if from_device in overall_nodes:
    #     # this means this node has been visited or is 'out'
    #     if has_seen_fft and has_seen_dac:
    #         return (overall_nodes[from_device], has_seen_fft, has_seen_dac)
    #     else:
    #         return (0, has_seen_fft, has_seen_dac)

    if from_device == 'out':
        if has_seen_fft and has_seen_dac:
            return (1, has_seen_fft, has_seen_dac)
        else:
            return (0, has_seen_fft, has_seen_dac)
    # check if I have visited this node before
    if (from_device, has_seen_fft, has_seen_dac) in overall_nodes:
        return (overall_nodes[(from_device, has_seen_fft, has_seen_dac)], has_seen_fft, has_seen_dac)

    my_visited_nodes = set(visited_nodes)

    # check if this is a cycle
    if my_visited_nodes and (from_device in my_visited_nodes):
        return (0, has_seen_fft, has_seen_dac)

    if my_visited_nodes is None:
        my_visited_nodes = set()

    my_visited_nodes.add(from_device)

    seen_fft = has_seen_fft or (from_device == 'fft')
    seen_dac = has_seen_dac or (from_device == 'dac')

    counter = 0
    # the number of paths for this node is the sum of the path_count for all the devices it connects to
    connect_list = puzzle_device_dict[from_device]
    for device in connect_list:
        this_device_path_count, seen_fft1, seen_dac1 = path_count_seen_fft_and_dac(device, to_device, puzzle_device_dict, my_visited_nodes, overall_nodes, seen_fft, seen_dac)
        # add this node to overall_nodes
        overall_nodes[(device, seen_fft1, seen_dac1)] = this_device_path_count

        if seen_fft1 and seen_dac1:
            counter += this_device_path_count

    #print(f"returning {my_visited_nodes} counter: {counter} seen_fft1: {seen_fft1} seen_dac: {seen_dac}")
    return (counter, seen_fft1, seen_dac1)

memo = {}
def process_node(node, seen_fft, seen_dac, puzzle_device_dict, nodes_visited):
    state = (node, seen_fft, seen_dac)

    if nodes_visited == None:
        nodes_visited = set()

    nodes_visited = nodes_visited.add(node)

    if state in memo:
        return memo[state]

    if node == 'fft':
        seen_fft = True

    if node == 'dac':
        seen_dac = True

    if node == 'out':
        return memo[state]

    total = 0
    connect_list = puzzle_device_dict[node]
    for device in connect_list:
        total += process_node(device, seen_fft, seen_dac, puzzle_device_dict, nodes_visited )

    memo[state] = total
    return total

def main():
    puzzle_device_dict = process_device_information('puzzle_11B_input.txt')
    #for key, device_list in puzzle_device_dict.items():
    #    print(f"device: {key} list of connections: {device_list}")
    nodes_visited = set()                       # tracks the nodes visited so far to from_device
                                                # if a device has reached the end we place its path entry


    memo[('out',True, True)] = 1    # we know that we stop here
    memo[('out', True, False)] = 0
    memo[('out', False, True)] = 0
    memo[('out', False, False)] = 0

    #count = path_count_seen_fft_and_dac('svr', 'out', puzzle_device_dict, visited_nodes_from_device, overall_visited_nodes_from_device, False, False)
    count = process_node('svr', False, False, puzzle_device_dict, nodes_visited)
    print(f"number of paths from 'svr' to 'out' with fft and dac is {count}")

if __name__ == "__main__":
    main()