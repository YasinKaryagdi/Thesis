from model.dynamic_list import DynamicList
import pytest 

@pytest.mark.parametrize("expected", [
    ([1, 2, 3, 4, 5])
    
])

def test_init(expected):
    list = DynamicList(1, 1, 1, 5)
    assert list.real == expected

@pytest.mark.parametrize("probe_rate, ex1, ex2", [
    (1, [1,2], [2, 1])
    # (2, [1,2], [1, 2])
])

def test_random_swap(probe_rate, ex1, ex2):
    for x in range(0, 100):
        list = DynamicList(x, probe_rate, 1, 2)

        assert list.real == ex1

        for y in range(0, 100):
            list.random_swap()
            assert list.real == ex2
            list.random_swap()
            assert list.real == ex1

@pytest.mark.parametrize("ex1, ex2, ex3, ex4", [
    ([1,2, 3], [2, 1, 3], [2, 3, 1], [1,3,2])
])

def test_swap(ex1, ex2, ex3, ex4):
    
        list = DynamicList(0,1,1, 3)

        assert list.real == ex1
        
        list.swap(0, 1)
        assert list.real == ex2
        list.swap(1, 2)
        assert list.real == ex3
        list.swap(0, 2)
        assert list.real == ex4

@pytest.mark.parametrize("n, i, j, truth", [
    (3, 1, 2, True),
    (3, 2, 1, False)
])

def test_probe(n, i, j, truth):
    
        list = DynamicList(0,1,1, n)

        assert list.probe(i, j) == truth

@pytest.mark.parametrize("n, i, j,l,m, truth1, ex, truth2", [
    (3, 1, 2, 1, 2, True, [1,3,2], True),

    # swapping 1 and 2 in the list and then afterwards checking if probe returns false after the swap
    (3, 1, 2, 0, 1, True, [2,1,3], False)

])

def test_old_probe_with_swap(n, i, j, l, m, truth1, ex, truth2):
    
        list = DynamicList(0,1,1, n)

        assert list.real == [1,2,3]
        assert list.probe(i, j) == truth1

        list.swap(l, m)
        assert list.real == ex
        assert list.probe(i, j) == truth2

@pytest.mark.parametrize("n, i, j, change_rate, truth1, ex, truth2", [
    # swaps 1 and 2 and then returns if the index where 1 is at < index where 2 is at, so if 1 is ranked lower than 2, 
    # which can't be the case since we started with [1,2]
    (2, 1, 2, 1, False, [2,1], True),

    # swapping 1 and 2 in the list and then afterwards checking if probe returns false after the swap
    (2, 1, 2, 2, True, [1,2], True),

])

def test_new_probe_with_swap(n, i, j, change_rate, truth1, ex, truth2):
    
        list = DynamicList(0,1,change_rate, n)

        assert list.real == [1,2]
        assert list.probe_with_swap(i, j) == truth1

        assert list.real == ex
        assert list.probe_with_swap(i, j) == truth2
