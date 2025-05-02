import pytest
from main import calc_kendall_tau, get_all_permutations, calc_max_error

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
    assert calc_kendall_tau(x, y) == expected


@pytest.mark.parametrize("list, n, expected", [
    ([], 1, [[]]),
    ([1, 2, 3], 0, [[1, 2, 3]]),
    ([1, 2, 3], 1, [[1, 2, 3], [2, 1, 3], [1, 3, 2]]),
    ([1, 2, 3], 2, [[1, 2, 3], [2, 1, 3], [1, 3, 2], [2, 3, 1], [3, 1, 2]]),
    ([1, 2, 3], 3, [[1, 2, 3], [2, 1, 3], [1, 3, 2], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
])

# testing whether all permutations possible permutations are returned,
# given a list and int n we should get all permutations of that list which requires at most n swaps to go to
def test_get_all_permutations(list, n, expected):
    assert get_all_permutations(list, n) == expected

# @pytest.mark.parametrize("approximation, currlist, n, expected", [
    
# ])

# def test_calc_max_error(approximation, currlist, n, expected):
#     assert calc_max_error(approximation, currlist, n) == expected