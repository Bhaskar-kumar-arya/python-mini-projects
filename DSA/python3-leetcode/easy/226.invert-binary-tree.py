#
# @lc app=leetcode id=226 lang=python3
#
# [226] Invert Binary Tree
#

# @lc code=start
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        if not root : return root
        stack = [root]
        while stack :
            node = stack.pop()
            node.left , node.right = node.right , node.left
            if node.right : stack.append(node.right)
            if node.left  : stack.append(node.left)
        return root
# @lc code=end

