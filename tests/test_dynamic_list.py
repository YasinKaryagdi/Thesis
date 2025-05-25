from model.dynamic_list import DynamicList
import pytest 

@pytest.mark.parametrize("expected", [
    ([0, 1, 2, 3, 4])
    
])

def test_init(expected):
    list = DynamicList(1, 1, 1, 5, 5, 25)
    assert list.real == expected

@pytest.mark.parametrize("probe_rate, ex1, ex2", [
    (1, [0, 1], [1,0])
    # (2, [1,2], [1, 2])
])

def test_random_swap(probe_rate, ex1, ex2):
    for x in range(0, 100):
        list = DynamicList(x, probe_rate, 1, 2, 2, 10)

        assert list.real == ex1

        for y in range(0, 100):
            list.random_swap()
            assert list.real == ex2
            list.random_swap()
            assert list.real == ex1

@pytest.mark.parametrize("ex1, ex2, ex3, ex4", [
    ([0,1, 2], [1, 0, 2], [1, 2, 0], [0,2,1])
])

def test_swap(ex1, ex2, ex3, ex4):
    
        list = DynamicList(0,1,1, 3, 3, 10)

        assert list.real == ex1
        
        list.swap_real(0, 1)
        assert list.real == ex2
        list.swap_real(1, 2)
        assert list.real == ex3
        list.swap_real(0, 2)
        assert list.real == ex4

@pytest.mark.parametrize("n, i, j, truth", [
    (3, 1, 2, True),
    (3, 2, 1, False)
])

def test_probe(n, i, j, truth):
        list = DynamicList(0,1,1, n, n, n*n)
        assert list.probe(i, j) == truth

@pytest.mark.parametrize("n, i, j,l,m, truth1, ex, truth2", [
    (3, 0, 1, 1, 2, True, [0,2,1], True),

    # swapping 0 and 1 in the list and then afterwards checking if probe returns false after the swap
    (3, 0, 1, 0, 1, True, [1,0,2], False)

])

def test_old_probe_with_swap(n, i, j, l, m, truth1, ex, truth2):
    
        list = DynamicList(0,1,1, n, n, n*n)

        assert list.real == [0,1,2]
        assert list.probe(i, j) == truth1

        list.swap_real(l, m)
        assert list.real == ex
        assert list.probe(i, j) == truth2

@pytest.mark.parametrize("n, i, j, change_rate, truth1, ex, truth2", [
    # swaps 0 and 1 and then returns if the index where 0 is at < index where 1 is at, so if 0 is ranked lower than 1, 
    # which can't be the case since we started with [0,1]
    (2, 0, 1, 1, False, [1,0], True),

    # swapping 0 and 1 in the list and then afterwards checking if probe returns false after the swap
    (2, 0, 1, 2, True, [0,1], True),

])

def test_new_probe_with_swap(n, i, j, change_rate, truth1, ex, truth2):
    
        list = DynamicList(0,1,change_rate, n, n, n*n)

        assert list.real == [0,1]
        assert list.probe_with_swap(i, j) == truth1

        assert list.real == ex
        assert list.probe_with_swap(i, j) == truth2


@pytest.mark.parametrize("n", [
    (10),(100)
])

def test_get_size(n):
        list = DynamicList(0,1,1, n, n, n*n)
        assert list.size() == n

@pytest.mark.parametrize("n", [
    (10),(100)
])

def test_get_time(n):
        list = DynamicList(0,1,1, n, n, n*n)
        assert list.get_time() == 0

        # perform some probes
        for i in range(0, n-1):
            list.probe(i, i+1)

        assert list.get_time() == n-1