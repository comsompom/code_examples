from fastapi import FastAPI
from itertools import permutations
from collections import Counter

app = FastAPI()

@app.get('/')
def index_page():
    return {'message': 'Success messageFrom Great Fast API example'}


@app.post('/arr')
def check_arr(num_arr):
    input_arr = [int(x) for x in num_arr.split(',')]

    iters = list(permutations(input_arr, 2))
    unique_pairs = set([tuple(sorted(x)) for x in iters])
    list_double_sums = list({key for key, val in dict(Counter([sum(x) for x in unique_pairs])).items() if val == 2})
    result_list = [[pair for pair in unique_pairs if sum(pair) == pair_sum] for pair_sum in list_double_sums]
    return_dict = {}
    for idx, same_pair in enumerate(result_list):
        return_dict[idx] = f"Pairs : {same_pair[0]} {same_pair[1]} have sum : {sum(same_pair[0])}"
    return return_dict
