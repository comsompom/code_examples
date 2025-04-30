"""
1295. Find Numbers with Even Number of Digits

Given an array nums of integers, return how many of them 
contain an even number of digits.

Examples:
Input: nums = [12,345,2,6,7896]
Output: 2

Input: nums = [555,901,482,1771]
Output: 1 
"""
def find_even_len(nums):
    """
    Solution used list comprehension
    """
    return len([x for x in nums if len(str(x)) % 2 == 0])


nums = [555, 901, 482, 1771]
print(find_even_len(nums))

nums = [555, 901, 482, 1771]
print(find_even_len(nums))
