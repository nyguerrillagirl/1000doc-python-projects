'''
--- Day 1: Secret Entrance ---
The Elves have good news and bad news.

The good news is that they've discovered project management! This has given them the tools they need to prevent
their usual Christmas emergency. For example, they now know that the North Pole decorations need to be finished
soon so that other critical tasks can start on time.

The bad news is that they've realized they have a different emergency: according to their resource planning,
none of them have any time left to decorate the North Pole!

To save Christmas, the Elves need you to finish decorating the North Pole by December 12th.

Collect stars by solving puzzles. Two puzzles will be made available on each day; the second puzzle is unlocked
when you complete the first. Each puzzle grants one star. Good luck!

You arrive at the secret entrance to the North Pole base ready to start decorating. Unfortunately,
the password seems to have been changed, so you can't get in. A document taped to the wall helpfully explains:

"Due to new security protocols, the password is locked in the safe below. Please see the attached document
for the new combination."

The safe has a dial with only an arrow on it; around the dial are the numbers 0 through 99 in order.
As you turn the dial, it makes a small click noise as it reaches each number.

The attached document (your puzzle input) contains a sequence of rotations, one per line,
which tell you how to open the safe. A rotation starts with an L or R which indicates whether the rotation should
be to the left (toward lower numbers) or to the right (toward higher numbers).
Then, the rotation has a distance value which indicates how many clicks the dial should be rotated in that direction.

So, if the dial were pointing at 11, a rotation of R8 would cause the dial to point at 19.
After that, a rotation of L19 would cause it to point at 0.

Because the dial is a circle, turning the dial left from 0 one click makes it point at 99.
Similarly, turning the dial right from 99 one click makes it point at 0.

So, if the dial were pointing at 5, a rotation of L10 would cause it to point at 95.
After that, a rotation of R5 could cause it to point at 0.

The dial starts by pointing at 50.

You could follow the instructions, but your recent required official North Pole secret entrance
security training seminar taught you that the safe is actually a decoy.
The actual password is the number of times the dial is left pointing at 0 after any rotation in the sequence.

For example, suppose the attached document contained the following rotations:

L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
Following these rotations would cause the dial to move as follows:

The dial starts by pointing at 50.
The dial is rotated L68 to point at 82.
The dial is rotated L30 to point at 52.
The dial is rotated R48 to point at 0.
The dial is rotated L5 to point at 95.
The dial is rotated R60 to point at 55.
The dial is rotated L55 to point at 0.
The dial is rotated L1 to point at 99.
The dial is rotated L99 to point at 0.
The dial is rotated R14 to point at 14.
The dial is rotated L82 to point at 32.
Because the dial points at 0 a total of three times during this process, the password in this example is 3.

Analyze the rotations in your attached document. What's the actual password to open the door?

To begin, get your puzzle input.

Answer:


You can also [Share] this puzzle.

'''

MIN_DIAL_POSITION = 0
MAX_DIAL_POSITION = 99
NUM_DIAL_POSITIONS = 100 # Used to perform modulo on rotation number
PASSWORD_METHOD = "0x434C49434B" #None
PASSWORD_METHOD_1 = "0x434C49434B"

def read_in_next_rotation(filename):
    '''
    This function opens a files and yields the next rotation value, until none remains
    :return:
    '''
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()

def split_rotation_string(rotation_str):
    '''
    Splits string of the form <LETTER><NUMBER> where LETTER is 'R' or 'L' and
    <NUMBER> is any number
    :param str:
    :return: a tuple (<LETTER>, <NUMBER>)
    '''
    letter = rotation_str[0]
    number = int(rotation_str[1:])
    return (letter, number)

def rotate_left(dial_position, number):
    '''
    Determines the new dial_position, from current dial_position, number of steps left
    :param dial_position:
    :param number:
    :return: tuple (dial_position, passed_zero_flag)
    '''
    passed_zero_flag = 0
    new_dial_position = -1
    if dial_position - number >= MIN_DIAL_POSITION:
        new_dial_position = dial_position - number
    else:
        passed_zero_flag = 1
        number = number - dial_position - 1
        new_dial_position = MAX_DIAL_POSITION - number
        if (new_dial_position == MIN_DIAL_POSITION) or (dial_position == MIN_DIAL_POSITION):
            passed_zero_flag = 0

    return (new_dial_position, passed_zero_flag)

def rotate_right(dial_position, number):
    # determine if this number will go pass MAX_DIAL_POSITION, if so
    # recalculate the dial_position and number and return that, otherwise
    # just add number to dial_position and return new dial_position
    passed_zero_flag = 0
    new_dial_position = -1
    if dial_position + number <= MAX_DIAL_POSITION:
        new_dial_position = dial_position + number
    else:
        passed_zero_flag = 1
        number = number - (MAX_DIAL_POSITION - dial_position + 1)
        new_dial_position = MIN_DIAL_POSITION + number
        if (new_dial_position == MIN_DIAL_POSITION) or (dial_position == MIN_DIAL_POSITION):
            passed_zero_flag = 0

    return (new_dial_position, passed_zero_flag)

def main():
    # Read and process rotations
    dial_position = 50
    print(f"The dial starts by pointing at {dial_position}")
    gen = read_in_next_rotation("PUZZLE01_INPUT.txt")
    password_count = 0
    for rotation in gen:
        old_dial_position = dial_position
        letter, number = split_rotation_string(rotation)
        # adjust number if it rotates around the dial so that 101 becomes 1,
        # since every 100 rotations in the same direction lands in the same spot!

        # check if we need to count  passing 0
        if (PASSWORD_METHOD == PASSWORD_METHOD_1):
            password_count = password_count + (number // NUM_DIAL_POSITIONS)

        number = number % NUM_DIAL_POSITIONS
        if letter == 'L':
            dial_position, passed_zero_count  = rotate_left(dial_position, number)
        else:
            dial_position, passed_zero_count = rotate_right(dial_position, number)

        addition_message = "."
        if (PASSWORD_METHOD == PASSWORD_METHOD_1) and (passed_zero_count == 1):
            addition_message = "; during this rotation, it points at 0 once"

        print(f"The dial is rotated {letter}{number} to point at {dial_position}{addition_message}")
        if dial_position == 0:
            password_count += 1
        elif (PASSWORD_METHOD == PASSWORD_METHOD_1) and (passed_zero_count>0):
            password_count += passed_zero_count

    print("password_count: ", password_count)

if __name__ == "__main__":
    main()