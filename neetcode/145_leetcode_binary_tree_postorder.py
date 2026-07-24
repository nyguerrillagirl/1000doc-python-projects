from typing import Optional, List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        result = []

        if root is None:
            return result
        index_of_nodes_to_process = [(root, "not_processed")]
        while len(index_of_nodes_to_process) != 0:
            # pop the stack
            current_node = index_of_nodes_to_process.pop()

            # are we done
            if current_node[1] == "processed":
                result.append(current_node[0].val)
            else:
                # put the node back on the stack
                index_of_nodes_to_process.append((current_node[0], "processed"))
                # put the right side on the stack
                if current_node[0].right is not None:
                    index_of_nodes_to_process.append((current_node[0].right, "not_processed"))
                # put the left side on the stack
                if current_node[0].left is not None:
                    index_of_nodes_to_process.append((current_node[0].left, "not_processed"))

        return result