from model.dynamic_list import DynamicList
import pytest 

@pytest.mark.parametrize("expected", [
    ([1, 2, 3, 4, 5])
    
])

def test_init(expected):
    list = DynamicList(1, 5)
    assert list.real == expected

@pytest.mark.parametrize("ex1, ex2", [
    ([1,2], [2, 1])
])

def test_swap(ex1, ex2):
    for x in range(0, 100):
        list = DynamicList(x, 2)

        assert list.real == ex1

        for y in range(0, 100):
            list.swap()
            assert list.real == ex2
            list.swap()
            assert list.real == ex1

