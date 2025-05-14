from algorithms.algorithms import *
import pytest 
from model.dynamic_list import DynamicList
import random


@pytest.mark.parametrize("n, ex", [
    (5, [0, 1, 2, 3, 4])
])

def test_quicksort_sorted_list(n, ex):
    list = DynamicList(0, 1, 1, n)
    quicksortBase(list, n)
    assert list.curr_approx == ex


@pytest.mark.parametrize("n, initial, ex", [
    (5, [4, 3, 2, 1, 0], [4, 3, 2, 1, 0]),
])

def test_quicksort_reversed_list(n, initial, ex):
    list = DynamicList(0, 1, 1, n)
    list.real = initial.copy()
    quicksortBase(list, n)
    assert list.curr_approx == ex