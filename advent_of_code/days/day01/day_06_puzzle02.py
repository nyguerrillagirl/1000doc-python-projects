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

--- Part Two ---
 The big cephalopods come back to check on how things are going. When they see that your grand total doesn't
 match the one expected by the worksheet, they realize they forgot to explain how to read cephalopod math.

 Cephalopod math is written right-to-left in columns. Each number is given in its own column, with the
 most significant digit at the top and the least significant digit at the bottom.
 (Problems are still separated with a column consisting only of spaces, and the symbol at the bottom of the problem
 is still the operator to use.)

 Here's the example worksheet again:

 123 328  51 64
  45 64  387 23
   6 98  215 314
 *   +   *   +
 Reading the problems right-to-left one column at a time, the problems are now quite different:

 The rightmost problem is 4 + 431 + 623 = 1058
 The second problem from the right is 175 * 581 * 32 = 3253600
 The third problem from the right is 8 + 248 + 369 = 625
 Finally, the leftmost problem is 356 * 24 * 1 = 8544
 Now, the grand total is 1058 + 3253600 + 625 + 8544 = 3263827.

 Solve the problems on the math worksheet again. What is the grand total found by adding together all of
 the answers to the individual problems?

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
            yield line.rstrip('\n')

def parse_operators(worksheet_line):
    operator_list = re.findall(r"[+*]", worksheet_line)
    return operator_list

def process_final_work_sheet(worksheet_list):
    '''
    This figures out the total for each section by extracting the last number (or blank), from
    the end of each worksheet string, if worksheet_list has n entries, I know that the section list has at MOST n entries
    :param worksheet_lines:
    :param operator_list:
    :return:
    '''
    worksheet_line_len = len(worksheet_list[0]) # this is the number of loops we must make to extract each char in a row
    number_group_lists = []  # holds the list of numbers in a group [[4, 431, 623]...], etc
    number_group_list = []   # holds all the numbers in a vertical section
    for char_index in range(0, worksheet_line_len):
        processing_index = worksheet_line_len - char_index - 1

        # iterate through each worksheet string extracting the char at char_index
        # construct the number in this position
        number_str = ''     # append the char found to number_str (skip blanks)
        found_nonblank_flag = False     # if still False when we exit for loop we completely processed a group of numbers
        for index, worksheet_line in enumerate(worksheet_list):
            char = worksheet_line[processing_index]
            if char != ' ':
                found_nonblank_flag = True      # we found a number
                number_str += char

        if found_nonblank_flag:
           # add number_str to current number_group_list
           number_group_list.append(number_str)
        else:
           # add current number_group_list to number_group_lists and start a fresh list
           number_group_lists.insert(0,number_group_list)
           # start a new list
           number_group_list = []

    # add last number_group
    number_group_lists.insert(0, number_group_list)

    return number_group_lists

def process_list_on_operator(number_str_list, op):
    total_sum = 0
    if op == '*':
        total_sum = 1

    for number in number_str_list:
        if op == '+':
            total_sum += int(number)
        else:
            total_sum *= int(number)

    return total_sum

def main():

    gen = read_in_worksheet_line("puzzle06_input.txt")
    worksheet_lines = []
    for worksheet_line in gen:
        if "+" in worksheet_line or "*" in worksheet_line:
            operator_list = parse_operators(worksheet_line)
            break
        else:
            # add line to worksheet_lines
            worksheet_lines.append(worksheet_line)

    # process worksheet_lines re-organizing things down each column for each group
    number_of_group_list = process_final_work_sheet(worksheet_lines)
    # we now have something like the following:
    # [['356', '24', '1'], ['8', '248', '369'], ['175', '581', '32'], ['4', '431', '623']]

    # process each one  with the associated operator, add result to final total
    final_operator_list = []
    for index, op in enumerate(operator_list):
        list_total = process_list_on_operator(number_of_group_list[index], op)
        final_operator_list.append(list_total)

    # total the final values
    print(f"total: {sum(final_operator_list)}")

if __name__ == "__main__":
    main()