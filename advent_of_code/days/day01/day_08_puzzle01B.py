'''
--- Day 8: Playground ---
Equipped with a new understanding of teleporter maintenance, you confidently step onto the repaired teleporter pad.

You rematerialize on an unfamiliar teleporter pad and find yourself in a vast underground space which contains a giant playground!

Across the playground, a group of Elves are working on setting up an ambitious Christmas decoration project. Through careful rigging, they have suspended a large number of small electrical junction boxes.

Their plan is to connect the junction boxes with long strings of lights. Most of the junction boxes don't provide electricity; however, when two junction boxes are connected by a string of lights, electricity can pass between those two junction boxes.

The Elves are trying to figure out which junction boxes to connect so that electricity can reach every junction box. They even have a list of all of the junction boxes' positions in 3D space (your puzzle input).

For example:

162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689

This list describes the position of 20 junction boxes, one per line. Each position is given as X,Y,Z coordinates.
So, the first junction box in the list is at X=162, Y=817, Z=812.

To save on string lights, the Elves would like to focus on connecting pairs of junction boxes that are as close
together as possible according to straight-line distance.
In this example, the two junction boxes which are closest together are 162,817,812 and 425,690,689.

By connecting these two junction boxes together, because electricity can flow between them, they become part of the
same circuit. After connecting them, there is a single circuit which contains two junction boxes, and the remaining 18
junction boxes remain in their own individual circuits.

Now, the two junction boxes which are closest together but aren't already directly connected are 162,817,812 and
431,825,988. After connecting them, since 162,817,812 is already connected to another junction box,
there is now a single circuit which contains three junction boxes and an additional 17 circuits which contain one
junction box each.

The next two junction boxes to connect are 906,360,560 and 805,96,715. After connecting them, there is a circuit
containing 3 junction boxes, a circuit containing 2 junction boxes, and 15 circuits which contain one junction box each.

The next two junction boxes are 431,825,988 and 425,690,689. Because these two junction boxes were already in the
same circuit, nothing happens!

This process continues for a while, and the Elves are concerned that they don't have enough extension cables for all
these circuits. They would like to know how big the circuits will be.

After making the ten shortest connections, there are 11 circuits: one circuit which contains 5 junction boxes,
one circuit which contains 4 junction boxes, two circuits which contain 2 junction boxes each, and seven circuits
which each contain a single junction box. Multiplying together the sizes of the three largest circuits
(5, 4, and one of the circuits of size 2) produces 40.

Your list contains many junction boxes; connect together the 1000 pairs of junction boxes which are closest together.
Afterward, what do you get if you multiply together the sizes of the three largest circuits?

To begin, get your puzzle input.

Answer:

'''
import heapq
import itertools
from collections import defaultdict
from typing import List, DefaultDict
import math

MAX_ITERATIONS = 1000
MAX_CONNECTIONS = 10
TOP_N = 3

def read_in_all_3D_points(filename):
    '''
    This function opens a files and reads in all 3D points and returns them in a list of tuples in the form
    (a, b, c)
    :return:
    '''
    point_list = []
    with open(filename, "r") as f:
        for line in f:
            num1, num2, num3 = line.strip().split(",")
            point_list.append((int(num1), int(num2), int(num3)))

    return point_list

def calculate_distance(p1, p2):
    '''
    We will skip using the sqrt since we don't care about the actual distance but just the size
    relative to other points
    :param p1:
    :param p2:
    :return:
    '''
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2

def build_heap(points):
    heap = []
    # generate all pairwise distance
    for i, j in itertools.combinations(range(len(points)), 2):
        d = calculate_distance(points[i], points[j])
        heapq.heappush(heap, (d, i, j))

    return heap

def update_circuit_points(circuit_list,  from_circuit_id, to_circuit_id):
    '''
    This merges two two lists
    :param circuit_list:
    :param from_circuit_id:
    :param to_circuit_id:
    :return:
    '''
    #debugging
    number_in_from_circuit_id = 0
    number_in_to_circuit_id =0
    for i in range(len(circuit_list)):
        if circuit_list[i] == to_circuit_id:
            number_in_to_circuit_id += 1
        if circuit_list[i] == from_circuit_id:
            number_in_from_circuit_id += 1
            circuit_list[i] = to_circuit_id

    #print(f"transferred {number_in_from_circuit_id} from {from_circuit_id} to {to_circuit_id}")
    #print(f"current to_circuit_id boxes: {number_in_to_circuit_id}")
def extract_top_n_circuits(circuit_list):
    '''
    processes the circuit_list ...adds each
    :param circuit_list:
    :param n:
    :return:
    '''
    top_n_circuits: DefaultDict[int, int] = defaultdict(int)

    for index, circuit_number in enumerate(circuit_list):
        if circuit_number != 0:
            top_n_circuits[circuit_number] += 1

    return top_n_circuits

def calculate_top_n(top_n_circuits, n):
    total = 1;
    top_n_list = []
    # create list of top n
    for key, value in top_n_circuits.items():
        top_n_list.append(value)
    top_n_list.sort(reverse=True)
    result = math.prod(top_n_list[:n])
    return result

def main():
    # our points from p0..pn (n=19 for test and 999 for puzzle)
    point_list = read_in_all_3D_points('puzzle08_input.txt')

    # tracks for each junction_box what circuit they are associated with
    # 0 - means junction box is not associated with any circuit
    circuit_list = [0 for _ in range(len(point_list))]

    current_circuit_list_number = 1 # holds the next available circuit

    # Note: The puzzle either ends up with 0 .. m circuits

    # create min-max heap (a priority queue) of (distance, p1, p2) pi is the index of the point in point_list
    # so an entry (distance, 10, 15) is the distance from point_list[10] to point_list[15]
    heap = build_heap(point_list)
    iterations = 0
    number_of_connections = 1           # tracks the number of connections we have made
    for _ in range(len(heap)):
        d, i , j = heapq.heappop(heap)
        # now put point_list[i] with point_list[j] in the same circuit
        is_point_i_in_a_circuit = circuit_list[i] != 0
        is_point_j_in_a_circuit = circuit_list[j] != 0
        if is_point_i_in_a_circuit and is_point_j_in_a_circuit:
            # merge the circuits
            if (circuit_list[i] != circuit_list[j]):
                number_of_connections += 1
                #print(f"merging all junction boxes in circuit {circuit_list[j]} into circuit {circuit_list[i]}")
                update_circuit_points(circuit_list,  circuit_list[j], circuit_list[i])
        elif is_point_i_in_a_circuit and (not is_point_j_in_a_circuit):
            # add point j to i's circuit
            #print(f"adding point {point_list[j]} to circuit: {circuit_list[i]} ")
            circuit_list[j] = circuit_list[i]
            number_of_connections += 1
        elif (not is_point_i_in_a_circuit) and is_point_j_in_a_circuit:
            # add point i the j's circuit
            #print(f"adding point {point_list[i]} to circuit: {circuit_list[j]} ")
            number_of_connections += 1
            circuit_list[i] = circuit_list[j]
        else:
            # add these to a new circuit and bump up the next new circuit_number
            #print(f"point {i} and point {j} are not in any circuits yet, current_circuit_number: {current_circuit_list_number}")
            number_of_connections += 1
            circuit_list[i] = current_circuit_list_number
            circuit_list[j] = current_circuit_list_number
            current_circuit_list_number += 1

        iterations += 1
        if iterations > MAX_ITERATIONS:
            break

    print(f"circuit_list: {circuit_list}")
    print(f"number_of_connections: {number_of_connections}")
    top_n_circuits:CircuitDict = extract_top_n_circuits(circuit_list)
    print(f"Top multiplied: {calculate_top_n(top_n_circuits, TOP_N )}")


if __name__ == "__main__":
    main()