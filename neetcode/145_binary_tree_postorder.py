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


def post_order_traversal(tree, root_index):
    result = []
    if root_index >= len(tree):
        return result

    # process right sub-tree (if it exists)
    left_child_index = 2 * root_index + 1
    right_child_index = 2 * root_index + 2

    if (left_child_index < len(tree)) and (tree[left_child_index] is not None):
        result.extend(post_order_traversal(tree, left_child_index))

    if (right_child_index < len(tree)) and (tree[right_child_index] is not None):
        result.extend(post_order_traversal(tree, right_child_index))

    # now add this root to the result
    result.append(tree[root_index])

    return result


if __name__ == '__main__':
    x = [1,2,3,4,5,None,8,None,None,6,7,9]
    # Output: [4,6,7,5,2,9,8,3,1]
    print(f"x={x} is {post_order_traversal(x, 0)}.")