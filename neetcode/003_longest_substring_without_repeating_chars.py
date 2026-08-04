# Description:
# Given a string s, find the length of the longest substring without duplicate characters.

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = {}
        left = 0
        longest = 0

        for right, ch in enumerate(s):
            if ch in seen and seen[ch] >= left:
                left = seen[ch] + 1
            seen[ch] = right
            longest = max(longest, right - left + 1)

        return longest

solution = Solution()
s = "baaabca"

print(solution.lengthOfLongestSubstring(s))