'''
--- Day 11: Reactor ---
You hear some loud beeping coming from a hatch in the floor of the factory, so you decide to check it out.
Inside, you find several large electrical conduits and a ladder.

Climbing down the ladder, you discover the source of the beeping: a large, toroidal reactor which powers
the factory above. Some Elves here are hurriedly running between the reactor and a nearby server rack,
apparently trying to fix something.

One of the Elves notices you and rushes over. "It's a good thing you're here! We just installed a new server rack,
 but we aren't having any luck getting the reactor to communicate with it!" You glance around the room and see
 a tangle of cables and devices running from the server rack to the reactor.
 She rushes off, returning a moment later with a list of the devices and their outputs (your puzzle input).

For example:

aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out

Each line gives the name of a device followed by a list of the devices to which its outputs are attached.
So, bbb: ddd eee means that device bbb has two outputs, one leading to device ddd and the other leading to device eee.

The Elves are pretty sure that the issue isn't due to any specific device, but rather that the issue is
triggered by data following some specific path through the devices. Data only ever flows from a device
through its outputs; it can't flow backwards.

After dividing up the work, the Elves would like you to focus on the devices starting with the one next
to you (an Elf hastily attaches a label which just says you) and ending with the main output to the reactor
(which is the device with the label out).

To help the Elves figure out which path is causing the issue, they need you to find every path from you to out.

In this example, these are all of the paths from you to out:

Data could take the connection from you to bbb, then from bbb to ddd, then from ddd to ggg, then from ggg to out.
Data could take the connection to bbb, then to eee, then to out.
Data could go to ccc, then ddd, then ggg, then out.
Data could go to ccc, then eee, then out.
Data could go to ccc, then fff, then out.
In total, there are 5 different paths leading from you to out.

How many different paths lead from you to out?

To begin, get your puzzle input.

Answer:

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

def path_count(from_device, to_device, puzzle_device_dict, visited_nodes, overall_nodes):
    '''

    :param from_device:
    :param to_device:
    :param puzzle_device_dict:
    :param visited_nodes:
    :return:
    '''
    if overall_nodes[from_device]:
        # this means this node has been visited or is 'out'
        return overall_nodes[from_device]

    # check if this is a cycle
    if visited_nodes and (from_device in visited_nodes):
        return 0
    if visited_nodes is None:
        visited_nodes = set()
    else:
        visited_nodes.add(from_device)

    counter = 0
    # the number of paths for this node is the sum of the path_count for all the devices it connects to
    connect_list = puzzle_device_dict[from_device]
    for device in connect_list:
        this_path_count = path_count(device, to_device, puzzle_device_dict, visited_nodes.add(from_device), overall_nodes)
        # add this node to overall_nodes
        overall_nodes[device] = this_path_count
        counter += this_path_count

    return counter

def main():
    puzzle_device_dict = process_device_information('puzzle_11_input.txt')

    visited_nodes_from_device = set()                       # tracks the nodes visited so far to from_device
    overall_visited_nodes_from_device = defaultdict(int)    # if a device has reached the end we place its path entry
                                                            # into this dictionary

    overall_visited_nodes_from_device['out'] = 1            # we know that we stop here

    count = path_count('you', 'out', puzzle_device_dict, visited_nodes_from_device, overall_visited_nodes_from_device)
    print(f"number of paths from 'you' to 'out' are {count}")

if __name__ == "__main__":
    main()