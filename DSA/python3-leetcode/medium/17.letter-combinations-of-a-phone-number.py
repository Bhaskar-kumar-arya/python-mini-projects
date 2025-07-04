#
# @lc app=leetcode id=17 lang=python3
#
# [17] Letter Combinations of a Phone Number
#

# @lc code=start
class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        if digits == "" : return []
        numtoChar = {
            2 : ['a','b','c'],
            3 : ['d','e','f'],
            4 : ['g','h','i'],
            5 : ['j','k','l'],
            6 : ['m','n','o'],
            7 : ['p','q','r','s'],
            8 : ['t','u','v'],
            9 : ['w','x','y','z']
        }
        res = []
        def backtrack (index,path : str) :
            if index == len(digits) : 
                res.append(path)
                return
            for char in numtoChar[int(digits[index])] : 
                backtrack(index + 1,path + char)
        backtrack(0,"")        
        return res        


        
# @lc code=end
