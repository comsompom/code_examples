# pylint: disable=E0401
# pylint: disable=E0602
# pylint: disable=C0103
"""
2965. Find Missing and Repeated Values
You are given a 0-indexed 2D integer matrix grid of size n * n with values in the range [1, n2]. 
Each integer appears exactly once except a which appears twice and b which is missing. 
The task is to find the repeating and missing numbers a and b.
Return a 0-indexed integer array ans of size 2 where ans[0] equals to a and ans[1] equals to b.

Example 1:
Input: grid = [[1,3],[2,2]]
Output: [2,4]
Explanation: Number 2 is repeated and number 4 is missing so the answer is [2,4].

Example 2:
Input: grid = [[9,1,7],[8,9,2],[3,4,6]]
Output: [9,5]
Explanation: Number 9 is repeated and number 5 is missing so the answer is [9,5].
"""
def find_missing_and_repeated_values(grid: List[List[int]]) -> List[int]:
    """return found the repeating and missing numbers"""
    range_size = len(grid[1]) ** 2
    list_grid_nums = []
    for x in grid:
        list_grid_nums.extend(x)

    double_nums_list = [key for key, val in Counter(list_grid_nums).items() if val > 1]
    uniq_nums_set = set(list_grid_nums)
    full_nums_set = set(range(1, range_size + 1))
    missed_nums_list = list(full_nums_set.difference(uniq_nums_set))
    double_nums_list.extend(missed_nums_list)
    return double_nums_list
