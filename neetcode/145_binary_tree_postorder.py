# 145. Binary Tree Postorder Traversal
# Given the root of a binary tree, return the postorder traversal of its nodes' values.
# Example
# 1
# |- null
# | - 2
#     |- 3
#     |- null
# Input: root = [1, null, 2, 3]
# Output: [3, 2, 1]

# binary tree postorder traveral is left-right-root order
from collections import deque


def print_tree(tree):
    result = []
    if len(tree) == 0:
        return result
    dq = deque([0])
    adjusted_null_index = 0
    while len(dq) != 0:
        # extract left-most item
        current_index = dq.popleft()
        if tree[current_index] is None:
            adjusted_null_index += 1
        else:
            print(f"root: {tree[current_index]}")
            left_child_index = 2 * (current_index - adjusted_null_index) + 1
            right_child_index = 2 * (current_index - adjusted_null_index) + 2
            if left_child_index < len(tree):
                print(f"\tleft_child: {tree[left_child_index]}")
                dq.append(left_child_index)
            else:
                print(f"\tleft_child: None")
            if right_child_index < len(tree):
                print(f"\tright_child: {tree[right_child_index]}")
                dq.append(right_child_index)
            else:
                print(f"\tright_child: None")
    return result


def post_order_traversal(tree):
    result = []  # holds the return value
    # state_of_node - 'not_processed', 'processed'
    adjusted_null_index = 0
    null_index_count = []
    for i in range(len(tree)):
        if tree[i] is None:
            adjusted_null_index += 1
        null_index_count.append(adjusted_null_index)

    print(f"null_index_count: {null_index_count}")

    index_of_nodes_to_process = [(0, 'not_processed', tree[0])]  # hold tuple (index_in_tree, state_of_node)
    while len(index_of_nodes_to_process) != 0:
        # pop the stack
        t = index_of_nodes_to_process.pop()
        current_index_in_tree = t[0]
        if t[2] is None:
            adjusted_null_index = adjusted_null_index + 1
            continue

        if t[1] == 'not_processed':
            # put it back on the stack
            index_of_nodes_to_process.append((t[0], 'processed', t[2]))
        else:
            # we must have processed the left and right subtrees for this node already
            result.append(tree[t[0]])
            continue

        # find out left and right children and put on stack as unprocessed (right first) (left second)
        left_child_index = 2 * (current_index_in_tree - null_index_count[t[0]]) + 1
        right_child_index = 2 * (current_index_in_tree - null_index_count[t[0]]) + 2
        if 0 <= right_child_index < len(tree):
            index_of_nodes_to_process.append((right_child_index, 'not_processed', tree[right_child_index]))

        if 0 <= left_child_index < len(tree):
            index_of_nodes_to_process.append((left_child_index, 'not_processed', tree[left_child_index]))


    return result


if __name__ == '__main__':
    x = [1, 2, 3, 4, 5, None, 8, None, None, 6, 7, 9]
    # Output: [4,6,7,5,2,9,8,3,1]
    print(f"x={x} is {post_order_traversal(x)}.")
