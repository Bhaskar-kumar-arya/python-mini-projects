#
# @lc app=leetcode id=94 lang=python3
#
# [94] Binary Tree Inorder Traversal
#

# @lc code=start
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def inorderTraversal(self, root: TreeNode) -> list[int]:
        res = []
        stack = []
        curr = root
        while stack or curr : 
            while curr :
                stack.append(curr) 
                curr = curr.left
            node = stack.pop() 
            res.append(node.val) 
            curr = node.right    
        return res                
        
# @lc code=end

