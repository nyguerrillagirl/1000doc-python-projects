import ast
import pulp

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


def min_operations(target, operations):
    """
    Solve for the minimum number of operations needed to reach `target`
    starting from [0,...,0], given a list of operations.

    Parameters:
        target (list[int]): desired final state, e.g. [3,5,4,7]
        operations (list[tuple[int]]): each tuple lists indices incremented by +1,
                                       e.g. [(3,), (1,3), (2,), (2,3), (0,2), (0,1)]

    Returns:
        dict: solution with counts for each operation and total operations
    """

    n = len(target)

    # Define the problem
    prob = pulp.LpProblem("MinOps", pulp.LpMinimize)

    # Decision variables: one per operation
    vars = [pulp.LpVariable(f"x{i}", lowBound=0, cat='Integer')
            for i in range(len(operations))]

    # Constraints: for each index in target, sum contributions == target[index]
    for idx in range(n):
        prob += sum(var for var, op in zip(vars, operations) if idx in op) == target[idx]

    # Objective: minimize total number of operations
    prob += sum(vars)

    # Solve
    prob.solve()

    # Collect results
    solution = {
        "status": pulp.LpStatus[prob.status],
        "operations": {f"op{i} {operations[i]}": int(pulp.value(var))
                       for i, var in enumerate(vars)},
        "total": int(pulp.value(sum(vars)))
    }
    return solution

def main():
    gen = process_input_manual("puzzle10_input.txt")
    total_button_presses_across_all_machines = 0
    for machine_spec in gen:
        #print(f"machine spec: {machine_spec}")
        target_state, button_list, joltage_requirements = process_machine_spec(machine_spec)
        print(f"joltage_requirements: {joltage_requirements}")
        solution = min_operations(joltage_requirements, button_list)
        button_count = solution["total"]
        print(f"button_count: {button_count}")
        total_button_presses_across_all_machines += button_count

    print(f"total number of button presses: {total_button_presses_across_all_machines}")


if __name__ == "__main__":
    main()