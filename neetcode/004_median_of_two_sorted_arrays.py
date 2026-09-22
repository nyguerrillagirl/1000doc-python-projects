# BROKEN
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    total_len = len(nums1) + len(nums2)
    requires_two = total_len % 2 == 0
    stop_point = total_len // 2
    print(f"midpoint: {stop_point}")
    iIndex = -1 # current position in nums1
    jIndex = -1 # current position in nums2
    index_counter = -1
    prev_value = None   # Holds the previous/last value processed BEFORE we reached stop_point
    current_value = None
    while index_counter < stop_point:
        prev_value = current_value  # let's remember the last value we processed
        if nums1[iIndex+1] < nums2[jIndex+1]:
            iIndex += 1
            current_value = nums1[iIndex]
        else:
            jIndex += 1
            current_value = nums2[jIndex]
        index_counter += 1

    if requires_two:
        return (prev_value + current_value) / 2
    else:
        return current_value

if __name__ == '__main__':
    num1 = [1,3,4,5]
    num2 = [2]
    print(f"median: {findMedianSortedArrays(num1, num2)}")