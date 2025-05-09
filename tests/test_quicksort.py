from main import randomized_quicksort
import pytest 

@pytest.mark.parametrize("list, expected", [
    ([3, 2, 1], [1, 2, 3]),
    ([3, 1, 2], [1, 2, 3]),
    ([2, 3, 1], [1, 2, 3])
    
])

def test_randomized_quicksort(list, expected):
    assert randomized_quicksort(list) == expected