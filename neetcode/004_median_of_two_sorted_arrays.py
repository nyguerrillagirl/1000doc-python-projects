# https://leetcode.com/problems/median-of-two-sorted-arrays/description/
# HARD
# BRUTE FORCE


def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    len1 = len(nums1)
    len2 = len(nums2)
    total_len = len1 + len2
    requires_two = total_len % 2 == 0
    stop_point = total_len // 2
    iIndex = -1 # current position in nums1
    jIndex = -1 # current position in nums2
    index_counter = -1
    prev_value = None   # Holds the previous/last value processed BEFORE we reached stop_point
    current_value = None
    exhausted1 = False or len1 == 0
    exhausted2 = False or len2 == 0
    while index_counter < stop_point:
        if exhausted1 or exhausted2:
            break
        prev_value = current_value  # let's remember the last value we processed
        if nums1[iIndex+1] < nums2[jIndex+1]:
            iIndex += 1
            current_value = nums1[iIndex]
        else:
            jIndex += 1
            current_value = nums2[jIndex]
        index_counter += 1
        # before we go back up see if num1 and/or num2 are exhausted
        if iIndex+1 == len1:
            exhausted1 = True
            break
        if jIndex+1 == len2:
            exhausted2 = True
            break

    # check if we stopped due to exhaustion. Note: It will NOT be possible to exhaust
    # both at the same time!!
    if exhausted2:
        while index_counter < stop_point:
            prev_value = current_value
            iIndex += 1
            current_value = nums1[iIndex]
            index_counter += 1
    elif exhausted1:
        while index_counter < stop_point:
            prev_value = current_value
            jIndex += 1
            current_value = nums2[jIndex]
            index_counter += 1

    if requires_two:
        return (prev_value + current_value) / 2
    else:
        return current_value


if __name__ == '__main__':
    num1 = [3,4]
    num2 = []
    print(f"median: {findMedianSortedArrays(num1, num2)}")