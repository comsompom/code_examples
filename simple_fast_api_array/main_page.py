# pylint: disable=E0401
# pylint: disable=R1718
"""Simple example of using the array checking inside the FastAPI"""
from itertools import permutations
from collections import Counter
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index_page():
    """the main route to check the GET response from FastAPI"""
    return {'message': 'Success messageFrom Great Fast API example'}


@app.post('/arr')
def check_arr(num_arr):
    """The route for POST request for return the values from the array"""
    input_arr = [int(x) for x in num_arr.split(',')]

    iters = list(permutations(input_arr, 2))
    unique_pairs = set([tuple(sorted(x)) for x in iters])
    list_double_sums = list({key for key, val in
                             dict(Counter([sum(x) for x in unique_pairs])).items() if val == 2})
    result_list = [[pair for pair in unique_pairs if sum(pair) == pair_sum]
                   for pair_sum in list_double_sums]
    return_dict = {}
    for idx, same_pair in enumerate(result_list):
        return_dict[idx] = f"Pairs : {same_pair[0]} {same_pair[1]} have sum : {sum(same_pair[0])}"
    return return_dict
