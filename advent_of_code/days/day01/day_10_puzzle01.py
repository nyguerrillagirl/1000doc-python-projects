'''
--- Day 10: Factory ---
Just across the hall, you find a large factory. Fortunately, the Elves here have plenty of time to decorate.
Unfortunately, it's because the factory machines are all offline, and none of the Elves can figure out the
initialization procedure.

The Elves do have the manual for the machines, but the section detailing the initialization procedure was eaten by a
Shiba Inu. All that remains of the manual are some indicator light diagrams, button wiring schematics,
and joltage requirements for each machine.

For example:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}

The manual describes one machine per line. Each line contains a single indicator light diagram in [square brackets],
one or more button wiring schematics in (parentheses), and joltage requirements in {curly braces}.

To start a machine, its indicator lights must match those shown in the diagram, where . means off and # means on.
The machine has the number of indicator lights shown, but its indicator lights are all initially off.

So, an indicator light diagram like [.##.] means that the machine has four indicator lights which are initially off
and that the goal is to simultaneously configure the first light to be off, the second light to be on, the third to be on,
and the fourth to be off.

You can toggle the state of indicator lights by pushing any of the listed buttons. Each button lists which indicator
lights it toggles, where 0 means the first light, 1 means the second light, and so on. When you push a button,
each listed indicator light either turns on (if it was off) or turns off (if it was on). You have to push each
button an integer number of times; there's no such thing as "0.5 presses" (nor can you push a button a
negative number of times).

So, a button wiring schematic like (0,3,4) means that each time you push that button, the first, fourth, and fifth
indicator lights would all toggle between on and off. If the indicator lights were [#.....], pushing the button would
change them to be [...##.] instead.

Because none of the machines are running, the joltage requirements are irrelevant and can be safely ignored.

You can push each button as many times as you like. However, to save on time, you will need to determine the
fewest total presses required to correctly configure all indicator lights for all machines in your list.

There are a few ways to correctly configure the first machine:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}

You could press the first three buttons once each, a total of 3 button presses.
You could press (1,3) once, (2,3) once, and (0,1) twice, a total of 4 button presses.
You could press all of the buttons except (1,3) once each, a total of 5 button presses.
However, the fewest button presses required is 2. One way to do this is by pressing the last two buttons
((0,2) and (0,1)) once each.

The second machine can be configured with as few as 3 button presses:

[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
One way to achieve this is by pressing the last three buttons ((0,4), (0,1,2), and (1,2,3,4)) once each.

The third machine has a total of six indicator lights that need to be configured correctly:

[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
The fewest presses required to correctly configure it is 2; one way to do this is by pressing buttons (0,3,4)
and (0,1,2,4,5) once each.

So, the fewest button presses required to correctly configure the indicator
lights on all of the machines is 2 + 3 + 2 = 7.

Analyze each machine's indicator light diagram and button wiring schematics. What is the fewest button presses
required to correctly configure the indicator lights on all of the machines?

To begin, get your puzzle input.

Answer:

'''
import ast
from collections import deque

def process_button_input(s):
    """
    Convert a string like '(3)', '(1,3)', '(2)' into a tuple of ints.
    """
    result = ast.literal_eval(s)
    # Ensure it's always a tuple
    if isinstance(result, int):
        return (result,)

    return tuple(result)

def process_input_manual(filename):
    '''
    This function processes a file in the form:
    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
    [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
    [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}

    Each line describes the specifications for each machine.

    [] is the "target" indicator light diagram
    ()...() is the list of button wiring schematics
    and {} are the joltage requirements
    :return: ([], [(), (),...()], {})
    '''
    '''
    This function opens a files and yields the next machine specification
    :return:
    '''
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()


def process_machine_spec(machine_spec):
    '''
    Processes machine specification in the form:
     [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7} and returns ( target_state_str, button_list, joltage_requirements

    :param machine_spec:
    :return:
    '''
    target_light_configuration = []
    button_list = []
    joltage_requirements = None
    parts = machine_spec.strip().split(" ")
    for part in parts:
        if part.startswith("["):
            target_light_configuration = list(part[1:-1])
        elif part.startswith("("):
            # part = part[1:-2]
            button_list.append(process_button_input(part))
        else:
            # must be joltage requirements
            joltage_requirements = part

    return (target_light_configuration, button_list, joltage_requirements)

def process_current_state(current_state, button_action):
    '''
    This function returns the next state after applying the button_action to the current_state
    :param current_state:
    :param button_action:
    :return:
    '''
    next_state = current_state[:]
    for button_number in button_action:
        # flip the corresponding number in current_state
        char_to_flip_to = '#' if next_state[button_number] == '.' else '.'
        next_state[button_number] = char_to_flip_to

    return next_state


def is_repeat_state(next_state, seen_states):
    '''
    maps next_state into a number and sends back True if seen_state[number] == 1
    :param next_state:
    :param seen_states:
    :return:
    '''
    result = False
    binary_str = ''.join('1' if ch == '#' else '0' for ch in next_state)
    number = int(binary_str, 2)

    return seen_states[number] == 1

def update_seen_state(next_state, seen_states):
    '''
    determines the # associated with next_state and update seen_states[number]
    :param next_state:
    :param seen_states:
    :return:
    '''
    binary_str = ''.join('1' if ch == '#' else '0' for ch in next_state)
    number = int(binary_str, 2)
    seen_states[number] = 0

def determine_button_count_to_reach_target(target_state, button_list):
    number_of_lights = len(target_state)
    # create an array of state_seen from 0..2^(number_of_lights)-1
    seen_states = [0 for _ in range(2**number_of_lights)]
    # create initial_state of machine
    initial_state = list("." * number_of_lights)

    # set state 0 (no lights on) to 1
    seen_states[0] = 1

    # place the initial state in the queue as (current_state, None, 0)
    queue = deque()
    queue.append( (initial_state, None, 0))
    current_level_processing = 0
    while True:
        if len(queue) == 0:
            print("SOMETHING IS VERY VERY WRONG!!!")
            break;

        # peek at the item on top of the queue
        next_item = queue[0]
        while next_item[2] == current_level_processing:
            # pop the item (it is at the current processing level)
            item_to_process = queue.popleft();
            current_state = item_to_process[0]
            last_button_applied = item_to_process[1]
            current_level = item_to_process[2]
            for button_action in button_list:
                if not button_action == last_button_applied:
                    next_state = process_current_state(current_state, button_action)
                    if next_state == target_state:
                        # we have reached the finish line
                        return current_level + 1

                    if not is_repeat_state(next_state, seen_states):
                        # add to queue the next state at the next level to explore
                        update_seen_state(next_state, seen_states)
                        queue.append( (next_state, button_action, current_level+1))


        current_level_processing += 1

def main():
    gen = process_input_manual("puzzle10_input.txt")
    total_button_presses_across_all_machines = 0
    for machine_spec in gen:
        print(f"machine spec: {machine_spec}")
        target_state, button_list, joltage_requirements = process_machine_spec(machine_spec)
        button_count = determine_button_count_to_reach_target(target_state, button_list)
        total_button_presses_across_all_machines += button_count

    print(f"total number of button presses: {total_button_presses_across_all_machines}")



# def main():
#     target_state = list(".##.")
#     button_list = [(3,), (1,3), (2,), (2,3), (0,2), (0,1)]
#
#     count = determine_button_count_to_reach_target(target_state, button_list)
#     print(f"count: {count}")

if __name__ == "__main__":
    main()