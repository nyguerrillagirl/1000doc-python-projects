'''
SOLUTION: TAKES TOO DAMN LONG ...trying an ILP Solver
--- Part Two ---
All of the machines are starting to come online! Now, it's time to worry about the joltage requirements.

Each machine needs to be configured to exactly the specified joltage levels to function properly.
Below the buttons on each machine is a big lever that you can use to switch the buttons from configuring the indicator lights to increasing the joltage levels. (Ignore the indicator light diagrams.)

The machines each have a set of numeric counters tracking its joltage levels, one counter per joltage requirement.
The counters are all initially set to zero.

So, joltage requirements like {3,5,4,7} mean that the machine has four counters which are initially 0 and that the
goal is to simultaneously configure the first counter to be 3, the second counter to be 5, the third to be 4,
and the fourth to be 7.

The button wiring schematics are still relevant: in this new joltage configuration mode, each button now indicates
which counters it affects, where 0 means the first counter, 1 means the second counter, and so on.
When you push a button, each listed counter is increased by 1.

So, a button wiring schematic like (1,3) means that each time you push that button, the second and fourth counters
would each increase by 1. If the current joltage levels were {0,1,2,3}, pushing the button would change them to be {0,2,2,4}.

You can push each button as many times as you like. However, your finger is getting sore from all the button pushing,
and so you will need to determine the fewest total presses required to correctly configure each machine's joltage level counters to match the specified joltage requirements.

Consider again the example from before:

[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}

Configuring the first machine's counters requires a minimum of 10 button presses. One way to do this is
by pressing (3) once, (1,3) three times, (2,3) three times, (0,2) once, and (0,1) twice.

Configuring the second machine's counters requires a minimum of 12 button presses. One way to do this is
by pressing (0,2,3,4) twice, (2,3) five times, and (0,1,2) five times.

Configuring the third machine's counters requires a minimum of 11 button presses. One way to do this is by
pressing (0,1,2,3,4) five times, (0,1,2,4,5) five times, and (1,2) once.

So, the fewest button presses required to correctly configure the joltage level counters on all of the
machines is 10 + 12 + 11 = 33.

Analyze each machine's joltage requirements and button wiring schematics. What is the fewest button presses
required to correctly configure the joltage level counters on all of the machines?
'''
from collections import deque
import ast
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


def process_button_input(s):
    """
    Convert a string like '(3)', '(1,3)', '(2)' into a tuple of ints.
    """
    result = ast.literal_eval(s)
    # Ensure it's always a tuple
    if isinstance(result, int):
        return (result,)

    return tuple(result)

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
            joltage_requirements =  [int(x) for x in part.strip("{}").split(",")]

    return (target_light_configuration, button_list, joltage_requirements)

def process_current_state(current_state, button_action):
    next_state = current_state[:]
    for button_number in button_action:
        next_state[button_number] += 1

    return next_state

def is_this_state_feasible(next_state, target_joltage_configuration):
    '''
    This state is not feasible if at least one index entry is greater than the corresponding
    index entry in target_joltage_configuration
    :param next_state:
    :param target_joltage_configuration:
    :return:
    '''
    result = True
    for index in range(len(next_state)):
        if next_state[index] > target_joltage_configuration[index]:
            return False

    return result

def determine_button_count_to_reach_target(target_joltage_configuration, button_list):
    '''
    For part #2 the final state is target_joltage_configuration a list
    :param target_joltage_configuration: the target counter configuration
    :param button_list:
    :return:
    '''
    number_of_joltage_values = len(target_joltage_configuration)
    # create an array of state_seen from 0..2^(number_of_lights)-1
    seen_states = set()     # holds a list of tuples, we convert [] => () in order to stop repeated states
    # create initial_state of machine
    initial_counter_state = [0 for _ in range(0, number_of_joltage_values)]

    # we will use seen_state to save each joltage_values_configuration as a tuple and avoid
    # exploring duplicate states
    seen_states.add(tuple(initial_counter_state))

    # place the initial state in the queue as (initial_counter_state, 0)
    queue = deque()
    queue.append( (initial_counter_state, 0))
    current_level_processing = 0
    iteration_counter = 0
    while True:
        if len(queue) == 0:
            print("SOMETHING IS VERY VERY WRONG!!!")
            break;

        # peek at the item on top of the queue
        next_item = queue[0]
        while next_item[1] == current_level_processing:
            # pop the item (it is at the current processing level)
            item_to_process = queue.popleft();
            current_state = item_to_process[0]
            last_button_applied = item_to_process[1]
            current_level = item_to_process[1]
            for button_action in button_list:
                next_state = process_current_state(current_state, button_action)
                if next_state == target_joltage_configuration:
                    # we have reached the finish line
                    return current_level + 1

                t = tuple(next_state)
                if not t in seen_states:
                    # add to queue the next state at the next level to explore
                    seen_states.add(t)
                    if is_this_state_feasible(next_state, target_joltage_configuration):
                        # only add states that can provide the answer
                        queue.append( (next_state, current_level+1))

            next_item = queue[0]
            # iteration_counter += 1
            # if (iteration_counter % 10000):
            #     print(".")
        current_level_processing += 1

def main():
    gen = process_input_manual("day_10_test_data1.txt")
    total_button_presses_across_all_machines = 0
    for machine_spec in gen:
        #print(f"machine spec: {machine_spec}")
        target_state, button_list, joltage_requirements = process_machine_spec(machine_spec)
        print(f"joltage_requirements: {joltage_requirements}")
        button_count = determine_button_count_to_reach_target(joltage_requirements, button_list)
        print(f"button_count: {button_count}")
        total_button_presses_across_all_machines += button_count

    print(f"total number of button presses: {total_button_presses_across_all_machines}")


if __name__ == "__main__":
    main()