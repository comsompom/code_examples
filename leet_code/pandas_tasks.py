# pylint: disable=E0401
# pylint: disable=E0602
# pylint: disable=W0105
"""leetcode pandas tasks solutions"""
# 2879. Display the First Three Rows
import pandas as pd


def select_first_row(employees: pd.DataFrame) -> pd.DataFrame:
    """get the first 3 rows"""
    return employees.head(3)

'''
The time complexity of the selectFirstRows function is O(1) because retrieving the first 
few rows of a dataframe is a constant time operation. It does not depend on the size of 
the dataframe, as the number of rows to retrieve is always fixed at 3
'''

# 2878. Get the Size of a DataFrame
"""
Write a solution to calculate and display the number of rows and columns of players.
Return the result as an array:
[number of rows, number of columns]
The result format is in the following example.
"""
def get_data_frame_size(players: pd.DataFrame) -> List[int]:
    """get data frame size"""
    return list(players.shape)

# 2877. Create a DataFrame from List
'''
Write a solution to create a DataFrame from a 2D list called student_data. This 2D list contains the IDs and ages of some students.
The DataFrame should have two columns, student_id and age, and be in the same order as the original 2D list.
The result format is in the following example.
'''
def create_data_frame(student_data: List[List[int]]) -> pd.DataFrame:
    """create the new dataframe"""
    return pd.DataFrame(student_data, columns=['student_id', 'age'])

# 2880. Select Data
'''
Write a solution to select the name and age of the student with student_id = 101.
The result format is in the following example.
'''
def select_data(students: pd.DataFrame) -> pd.DataFrame:
    """select data from dataframe"""
    student_condition = students.loc[students["student_id"]==101]
    return student_condition[['name', 'age']]

# 2881. Create a New Column
'''
A company plans to provide its employees with a bonus.
Write a solution to create a new column name bonus that contains the doubled values of the salary column.
The result format is in the following example.
'''
def create_bonus_column(employees: pd.DataFrame) -> pd.DataFrame:
    """create and extra column"""
    employees['bonus'] = employees['salary'] * 2
    return employees

# 2882. Drop Duplicate Rows
'''
There are some duplicate rows in the DataFrame based on the email column.
Write a solution to remove these duplicate rows and keep only the first occurrence.
'''
def drop_duplicated_emails(customers: pd.DataFrame) -> pd.DataFrame:
    """drop duplicates"""
    return customers.drop_duplicates(subset=['email'])

# 2883. Drop Missing Data
'''
There are some rows having missing values in the name column.
Write a solution to remove the rows with missing values.
'''
def drop_missing_data(students: pd.DataFrame) -> pd.DataFrame:
    """drop missing variables"""
    return students.dropna(subset=['name'])
