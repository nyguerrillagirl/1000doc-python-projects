# Description:
# Given a string s, find the length of the longest substring without duplicate characters.

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) == 0:
            return 0

        # change to a dictionary key: 'char', value: position in string
        left_pointer = 0
        right_pointer = 0
        seen_chars = {s[right_pointer]:0}
        max_len_seen = right_pointer - left_pointer + 1
        seen_chars[s[right_pointer]] = right_pointer
        len_s = len(s)
        # start the sliding window technique here
        right_pointer += 1
        while right_pointer < len_s:
            # check if str[right_pointer] has been seen
            if s[right_pointer] in seen_chars:
                # move the left_pointer up pass str[right_pointer], note: we are not cleaning up prev.
                # seen characters!
                left_pointer = max(left_pointer, seen_chars[s[right_pointer]]+1)
                # update position
                seen_chars[s[right_pointer]] = right_pointer
            else:
                # add this char
                seen_chars[s[right_pointer]] = right_pointer

            # recalculate for max_len_seen
            max_len_seen = max(right_pointer - left_pointer + 1, max_len_seen)

            right_pointer += 1

        return max_len_seen


solution = Solution()
s = "baaabca"

print(solution.lengthOfLongestSubstring(s))