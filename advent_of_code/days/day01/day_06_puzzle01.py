'''
--- Day 6: Trash Compactor ---
After helping the Elves in the kitchen, you were taking a break and helping them re-enact a movie scene when you
over-enthusiastically jumped into the garbage chute!

A brief fall later, you find yourself in a garbage smasher. Unfortunately, the door's been magnetically sealed.

As you try to find a way out, you are approached by a family of cephalopods!
They're pretty sure they can get the door open, but it will take some time. While you wait, they're curious
if you can help the youngest cephalopod with her math homework.

Cephalopod math doesn't look that different from normal math.
The math worksheet (your puzzle input) consists of a list of problems; each problem has a group of numbers
that need to either be either added (+) or multiplied (*) together.

However, the problems are arranged a little strangely; they seem to be presented next to each other in a
very long horizontal list. For example:

123 328  51 64
 45 64  387 23
  6 98  215 314
*   +   *   +

Each problem's numbers are arranged vertically; at the bottom of the problem is the symbol for the operation
that needs to be performed. Problems are separated by a full column of only spaces.
The left/right alignment of numbers within each problem can be ignored.

So, this worksheet contains four problems:

123 * 45 * 6 = 33210
328 + 64 + 98 = 490
51 * 387 * 215 = 4243455
64 + 23 + 314 = 401

To check their work, cephalopod students are given the grand total of adding together all of the answers
to the individual problems. In this worksheet, the grand total is 33210 + 490 + 4243455 + 401 = 4277556.

Of course, the actual worksheet is much wider. You'll need to make sure to unroll it completely so
that you can read the problems clearly.

Solve the problems on the math worksheet. What is the grand total found by adding together all of the answers
to the individual problems?

To begin, get your puzzle input.

Answer:

'''
import re

def read_in_worksheet_line(filename):
    '''
    This function opens a files and yields the next rotation value, until none remains
    :return:
    '''
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()

def parse_numbers(worksheet_line):
    str_numbers = re.findall(r"\d+", worksheet_line)
    int_numbers = list(map(int, str_numbers))
    return int_numbers

def parse_operators(worksheet_line):
    operator_list = re.findall(r"[+*]", worksheet_line)
    return operator_list

def main():

    gen = read_in_worksheet_line("puzzle06_input.txt")
    total_add_list = []
    total_mult_list = []
    final_operator_list = []
    for worksheet_line in gen:
        if "+" in worksheet_line or "*" in worksheet_line:
            # parse_operators
            operator_list = parse_operators(worksheet_line)
            # determine final values
            for index, op in enumerate(operator_list):
                if op == '+':
                    final_operator_list.append(total_add_list[index])
                else:
                    final_operator_list.append(total_mult_list[index])

            break
        else:
            # parse set of numbers
            number_list = parse_numbers(worksheet_line)

        # since I don't know if I have to + or * this number_list to total I will do both
        if total_add_list == []:
            total_add_list = number_list
        else:
            # add current number to total
            total_add_list = list(map(lambda x: x[0] + x[1], zip(total_add_list, number_list)))

        if total_mult_list == []:
            total_mult_list = number_list
        else:
            total_mult_list = list(map(lambda x: x[0] * x[1], zip(total_mult_list, number_list)))

    # total the final values
    print(f"total: {sum(final_operator_list)}")

if __name__ == "__main__":
    main()