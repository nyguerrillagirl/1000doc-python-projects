'''
--- Day 12: Christmas Tree Farm ---
You're almost out of time, but there can't be much left to decorate. Although there are no stairs, elevators,
escalators, tunnels, chutes, teleporters, firepoles, or conduits here that would take you deeper into
the North Pole base, there is a ventilation duct. You jump in.

After bumping around for a few minutes, you emerge into a large, well-lit cavern full of Christmas trees!

There are a few Elves here frantically decorating before the deadline.
They think they'll be able to finish most of the work, but the one thing they're worried about is the presents
for all the young Elves that live here at the North Pole.
It's an ancient tradition to put the presents under the trees, but the Elves are worried they won't fit.

The presents come in a few standard but very weird shapes.
The shapes and the regions into which they need to fit are all measured in standard units.
To be aesthetically pleasing, the presents need to be placed into the regions in a way that
follows a standardized two-dimensional unit grid; you also can't stack presents.

As always, the Elves have a summary of the situation (your puzzle input) for you.
First, it contains a list of the presents' shapes. Second, it contains the size of the region under each
tree and a list of the number of presents of each shape that need to fit into that region. For example:

0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2

The first section lists the standard present shapes. For convenience, each shape starts with its index and a colon;
then, the shape is displayed visually, where # is part of the shape and . is not.

The second section lists the regions under the trees. Each line starts with the width and length of the region;
12x5 means the region is 12 units wide and 5 units long. The rest of the line describes the presents that need
to fit into that region by listing the quantity of each shape of present; 1 0 1 0 3 2 means you need to fit one
present with shape index 0, no presents with shape index 1, one present with shape index 2,
no presents with shape index 3, three presents with shape index 4, and two presents with shape index 5.

Presents can be rotated and flipped as necessary to make them fit in the available space,
but they have to always be placed perfectly on the grid.
Shapes can't overlap (that is, the # part from two different presents can't go in the same place on the grid),
but they can fit together (that is, the . part in a present's shape's diagram does not block another present
from occupying that space on the grid).

The Elves need to know how many of the regions can fit the presents listed.
In the above example, there are six unique present shapes and three regions that need checking.

The first region is 4x4:

....
....
....
....

In it, you need to determine whether you could fit two presents that have shape index 4:

###
#..
###

After some experimentation, it turns out that you can fit both presents in this region. Here is one way to do it,
using A to represent one present and B to represent the other:

AAA.
ABAB
ABAB
.BBB

The second region, 12x5: 1 0 1 0 2 2, is 12 units wide and 5 units long.
In that region, you need to try to fit one present with shape index 0, one present with shape index 2,
two presents with shape index 4, and two presents with shape index 5.

It turns out that these presents can all fit in this region. Here is one way to do it,
again using different capital letters to represent all the required presents:

....AAAFFE.E
.BBBAAFFFEEE
DDDBAAFFCECE
DBBB....CCC.
DDD.....C.C.

The third region, 12x5: 1 0 1 0 3 2, is the same size as the previous region;
the only difference is that this region needs to fit one additional present with shape index 4.
Unfortunately, no matter how hard you try, there is no way to fit all of the presents into this region.

So, in this example, 2 regions can fit all of their listed presents.

Consider the regions beneath each tree and the presents the Elves would like to fit into each of them.
How many of the regions can fit all of the presents listed?

To begin, get your puzzle input.

Answer:

'''
from dataclasses import dataclass
import re


@dataclass
class region_data:
    width: int
    height: int
    presents: list

def is_number_colon(line):
    return bool(re.fullmatch(r'\d+:', line))

def is_region_specification(line):
    return bool(re.match(r'^\d+x\d+:', line))

def parse_region_line(line):
    # Match "<num>x<num>:" at the start
    m = re.match(r'^\s*(\d+)x(\d+):\s*(.*)$', line)
    if not m:
        raise ValueError(f"Line not in expected format: {line!r}")

    w = int(m.group(1))
    h = int(m.group(2))
    rest = m.group(3)

    # Parse the remaining numbers into a list
    nums = [int(x) for x in rest.split()]

    return (w, h, nums)

def process_hash_count(line):
    return line.count('#')

def process_input_data(filename):
    '''
    this function simply processes the input (see above) and returns a presents_list which for each present
    just calculates the number of "#' space the present requires and a regions_list that holds objects of the type
    region_data
    Output for test data:
    presents_list: [7, 7, 7, 7, 7, 7]
    regions_list: [(4, 4, [0, 0, 0, 0, 2, 0]), (12, 5, [1, 0, 1, 0, 2, 2]), (12, 5, [1, 0, 1, 0, 3, 2])]
    :return:
    '''
    presents_list = []
    regions_list = []

    processing_presents = True
    next_present = -1               # updated when present marker is found <number>:
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue

            # if line of the type <number>: then this is the start of a present description
            if is_number_colon(line):
                next_present += 1       # processing new present
                presents_list.append(0)
                continue

            if is_region_specification(line):
                processing_presents = False

            if processing_presents:
                # count the number of '#' and add to count
                number_of_hashes = process_hash_count(line)
                presents_list[next_present] += number_of_hashes
            else:
                # processing a region line
                a_region_data = parse_region_line(line)
                regions_list.append(a_region_data)

    return (presents_list, regions_list)

def presents_fit_in_region(width, height, region_present_list, presents_list):
    total_region_area = width * height
    total_present_area = 0;
    for index in range(len(region_present_list)):
        if region_present_list[index] > 0:
            total_present_area +=  region_present_list[index] * presents_list[index]

    return total_region_area > total_present_area

def main():
    presents_list, regions_list = process_input_data('puzzle_12_input.txt')
    good_region_count = 0       # counts how many regions fit the designated present list!
    for region in regions_list:
        width, height, region_present_list = region
        if presents_fit_in_region(width, height, region_present_list, presents_list):
            good_region_count += 1

    print(f"number of regions that fit designated presents: {good_region_count}")

if __name__ == "__main__":
    main()