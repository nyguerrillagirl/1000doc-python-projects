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

# NOT WORKING
from collections import deque

def post_order_traversal(tree):
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


if __name__ == '__main__':
    x = [1,2,3,4,5,None,8,None,None,6,7,9]
    # Output: [4,6,7,5,2,9,8,3,1]
    print(f"x={x} is {post_order_traversal(x)}.")