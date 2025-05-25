from algorithms.algorithms_no_rand_swap import *
import pytest 
from model.dynamic_list import DynamicList
import random
import math

# these tests are not well made and are mainly used to quickly check if everything functions as should be,
# would have loved to perfect these but time is running out unfortunately

# testing quicksort
@pytest.mark.parametrize("n, ex", [
    (5, [0, 1, 2, 3, 4])
])

def test_quicksort_sorted_list(n, ex):
    list = DynamicList(0, 1, 1, n, n, n*n)
    quicksort_base(list, n)
    assert list.curr_approx == ex


@pytest.mark.parametrize("n, initial, ex", [
    (5, [4, 3, 2, 1, 0], [4, 3, 2, 1, 0]),
])

def test_quicksort_reversed_list(n, initial, ex):
    list = DynamicList(0, 1, 1, n, n, n)
    list.real = initial.copy()
    quicksort_base(list, n)
    assert list.curr_approx == ex


@pytest.mark.parametrize("n, initial", [
    (5, [4, 3, 2, 1, 0])
])

def test_quicksort_changed_real(n, initial):
    list = DynamicList(0, 1, 1, n, n, n*n)
    list.real = initial.copy()
    quicksort_base(list, n)
    assert list.curr_approx == [4, 3, 2, 1, 0]
    list.swap_real(0,1)
    assert list.curr_approx == [4, 3, 2, 1, 0]
    assert list.real == [3, 4, 2, 1, 0]
    quicksort_base(list, n)
    assert list.curr_approx == [3, 4, 2, 1, 0]


# testing repeated insertion sort
@pytest.mark.parametrize("n, ex", [
    (5, [0, 1, 2, 3, 4])
])

def test_insertion_sorted_list(n, ex):
    list = DynamicList(0, 1, 1, n, n, n*n)

    # basically it will do one whole run of it because the while loop executes once wholly
    repeated_insertion_sort(list, 1)
    assert list.curr_approx == ex


@pytest.mark.parametrize("n, initial, ex", [
    (5, [4, 3, 2, 1, 0], [4, 3, 2, 1, 0]),
])

def test_insertion_reversed_list(n, initial, ex):
    list = DynamicList(0, 1, 1, n, n, n*n)
    list.real = initial.copy()

    # basically it will do one whole run of it because the while loop executes once wholly
    repeated_insertion_sort(list, n*n)
    assert list.curr_approx == ex


@pytest.mark.parametrize("n, initial", [
    (5, [4, 3, 2, 1, 0])
])

# bad test, will need to change later tbh
def test_insertion_changed_real(n, initial):
    list = DynamicList(0, 1, 1, n, n, n*n)
    list.real = initial.copy()
    assert list.curr_approx == [0, 1, 2, 3, 4]
    repeated_insertion_sort(list, 10)
    assert list.get_time() == 10
    assert list.curr_approx == [4, 3, 2, 1, 0]
    list.swap_real(0,1)
    assert list.curr_approx == [4, 3, 2, 1, 0]
    assert list.real == [3, 4, 2, 1, 0]

    # curr time is 10 so 11 will make it so that the whole while loop runs once
    repeated_insertion_sort(list, 11)
    assert list.real == [3, 4, 2, 1, 0]
    assert list.curr_approx == [3, 4, 2, 1, 0]


# testing quicksort then insertionsort
@pytest.mark.parametrize("n, ex", [
    (5, [0, 1, 2, 3, 4])
])

def test_quick_then_insertion_sorted_list(n, ex):
    list = DynamicList(0, 1, 1, n, n, n*n)

    # basically it will do one whole run of it because the while loop executes once wholly
    quick_then_insertion_sort(list, 1)
    assert list.curr_approx == ex


@pytest.mark.parametrize("n, initial, ex", [
    (5, [4, 3, 2, 1, 0], [4, 3, 2, 1, 0]),
])

def test_quick_then_insertion_reversed_list(n, initial, ex):
    list = DynamicList(0, 1, 1, n, n, n*n)
    list.real = initial.copy()

    # basically it will do one whole run of it because the while loop executes once wholly
    quick_then_insertion_sort(list, 1)
    assert list.curr_approx == ex


@pytest.mark.parametrize("n, initial", [
    (5, [4, 3, 2, 1, 0])
])

def test_quick_then_insertion_changed_real(n, initial):
    list = DynamicList(0, 1, 1, n, n, n*n)
    list.real = initial.copy()
    assert list.curr_approx == [0, 1, 2, 3, 4]
    quick_then_insertion_sort(list, 1)
    # assert list.get_time() == 8 # meaning that it checked everything but it was already sorted, check this later
    assert list.curr_approx == [4, 3, 2, 1, 0]
    list.swap_real(0,1)
    assert list.curr_approx == [4, 3, 2, 1, 0]
    assert list.real == [3, 4, 2, 1, 0]

    # 5 is below the curr time so we have that insertion sort does nothing, 
    # meaning the quicksort part functions well
    quick_then_insertion_sort(list, 5) 
    assert list.real == [3, 4, 2, 1, 0]
    assert list.curr_approx == [3, 4, 2, 1, 0]




# testing blocksort