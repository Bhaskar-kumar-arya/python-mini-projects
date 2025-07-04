#
# @lc app=leetcode id=144 lang=python3
#
# [144] Binary Tree Preorder Traversal
#

# @lc code=start
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def preorderTraversal(self, root: TreeNode) -> list[int]:
        if not root : return []
        res = []
        stack = [root]
        
        while stack :
            node = stack.pop()
            res.append(node.val)
            if node.right : stack.append(node.right)
            if node.left : stack.append(node.left) 

        return res    
# @lc code=end

