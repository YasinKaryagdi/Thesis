import pytest
from statistics import Stats

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from runner import Runner

@pytest.mark.parametrize("x, y, expected", [
    ([1, 2, 3], [1, 2, 3], 0),
    ([1, 2, 3], [1, 3, 2], 1),
    ([1, 2, 3], [3, 1, 2], 2),
    ([1, 2, 3], [3, 2, 1], 3),
    ([1, 2, 3, 4], [1, 2, 3, 4], 0),
    ([1, 2, 3, 4], [2, 1, 3, 4], 1),
    ([1, 2, 3, 4], [1, 3, 2, 4], 1),
    ([1, 2, 3, 4], [1, 2, 4, 3], 1),
    ([1, 2, 3, 4], [2, 3, 1, 4], 2),
    ([1, 2, 3, 4], [2, 1, 4, 3], 2),
    ([1, 2, 3, 4], [3, 1, 2, 4], 2),
    ([1, 2, 3, 4], [1, 3, 4, 2], 2),
    ([1, 2, 3, 4], [1, 4, 2, 3], 2),
    ([1, 2, 3, 4], [3, 2, 1, 4], 3),
    ([1, 2, 3, 4], [2, 3, 4, 1], 3),
    ([1, 2, 3, 4], [2, 4, 1, 3], 3),
    ([1, 2, 3, 4], [3, 1, 4, 2], 3),
    ([1, 2, 3, 4], [1, 4, 3, 2], 3),
    ([1, 2, 3, 4], [4, 1, 2, 3], 3),
    ([1, 2, 3, 4], [3, 2, 4, 1], 4),
    ([1, 2, 3, 4], [2, 4, 3, 1], 4),
    ([1, 2, 3, 4], [4, 2, 1, 3], 4),
    ([1, 2, 3, 4], [3, 4, 1, 2], 4),
    ([1, 2, 3, 4], [4, 1, 3, 2], 4),
    ([1, 2, 3, 4], [3, 4, 2, 1], 5),
    ([1, 2, 3, 4], [4, 2, 3, 1], 5),
    ([1, 2, 3, 4], [4, 3, 1, 2], 5),
    ([1, 2, 3, 4], [4, 3, 2, 1], 6)
])

# testing whether kendall tau distances are calculated correctly, 
# given two lists we should get the amount of swaps minimally required to go from one to the other list
def test_calc_kendall_tau(x, y, expected):
    temp = Stats(10)
    assert temp.calc_kendall_tau(x, y) == expected
    assert temp.merge_sort(x, y) == expected


# testing whether kendall tau distances are calculated correctly, 
# given two lists we should get the amount of swaps minimally required to go from one to the other list
def test_calc_kendall_tau_run():

    temp = Runner(0, 1, 5, "block-10", 1000, 100000, 10, "sorted", 0)
    
    assert temp.curr_list.stats.distances == temp.curr_list.stats.distances2
