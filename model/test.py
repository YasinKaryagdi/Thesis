import pytest

class KendallTau:
    def probe(self, position: dict[int, int], i: int, j: int):
        return position[i] < position[j]

    def merge_sort(self, position: dict[int, int], temp: list[int]):
        if len(temp) <= 1:
            return 0

        left_size = len(temp) // 2
        right_size = len(temp) - left_size

        left = temp[:left_size]
        right = temp[left_size:]

        left_invs = self.merge_sort(position, left)
        right_invs = self.merge_sort(position, right)
        between_invs = 0
        i = j = k = 0

        while i < left_size and j < right_size:
            if self.probe(position, left[i], right[j]):
                temp[k] = left[i]
                i += 1
            else:
                temp[k] = right[j]
                j += 1
                between_invs += (left_size - i)
            k += 1

        while i < left_size:
            temp[k] = left[i]
            i += 1
            k += 1

        while j < right_size:
            temp[k] = right[j]
            j += 1
            k += 1

        return left_invs + right_invs + between_invs


@pytest.fixture
def kt():
    return KendallTau()

def kendall_distance(real, approx):
    kt = KendallTau()
    position = {val: i for i, val in enumerate(real)}
    return kt.merge_sort(position, approx.copy())

def test_basic_case(kt):
    real = [0, 1, 2, 3]
    approx = [0, 1, 2, 3]
    assert kendall_distance(real, approx) == 0

def test_one_inversion(kt):
    real = [0, 1, 2, 3]
    approx = [0, 2, 1, 3]
    assert kendall_distance(real, approx) == 1

def test_full_reverse(kt):
    real = [0, 1, 2, 3]
    approx = [3, 2, 1, 0]
    assert kendall_distance(real, approx) == 6

def test_case_from_question(kt):
    real = [2, 3, 1, 0]
    approx = [0, 2, 3, 1]
    assert kendall_distance(real, approx) == 3

def test_large_case(kt):
    real = [7, 1, 4, 9, 5, 6, 3, 8, 0, 2]
    approx = [2, 4, 1, 9, 0, 3, 7, 8, 6, 5]
    assert kendall_distance(real, approx) == 13
