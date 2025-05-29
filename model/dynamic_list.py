# TODO: write class that has methods for probing and for the introduction of inversions,
# also want to store the real ranking and the approxamation, maybe also want to store last full quicksort
# and two lists for the two seperate versions of quicksort?

from run_data.statistics import Stats
import random
import math as math


class DynamicList:
    real: list[int]
    curr_approx: list[int]
    probe_rate: int
    change_rate: int
    curr_quicksort_list: list[int]
    curr_blocksort_list: list[int]
    stats: Stats
    random_swap_index: list[int]

    def __init__(
        self,
        rand_seed: int,
        probe_rate: int,
        change_rate: int,
        n: int,
        sample_rate: int,
        time_limit: int,
    ):
        random.seed(rand_seed)
        self.stats = Stats(n)
        self.probe_rate = probe_rate
        self.change_rate = change_rate
        self.sample_rate = sample_rate
        self.time_limit = time_limit

        # maybe I want to initialize this as reverse ordered, so that we always start at maximal distance
        self.real = []
        for i in range(0, n):
            self.real.append(i)

        self.curr_approx = []
        for i in range(0, n):
            self.curr_approx.append(i)

        self.random_swap_index = []

        # for i in range(0, change_rate * (time_limit + n)):
        #     # from 0 to n-2, since the last swap we can do is n-1 with n-2
        #     random_int = random.randint(0, n - 2)
        #     self.random_swap_index.append(random_int)

    # used for testing
    def probe(self, i: int, j: int):
        self.stats.add_probe(i, j)

        # it's expensive timewise to calc this each iter so I'm also adding a samplerate to speed things up
        if self.get_time() % self.sample_rate == 0:
            self.stats.add_curr_distance(self.real, self.curr_approx)
        index_i = self.real.index(i)
        index_j = self.real.index(j)
        return index_i < index_j

    # todo, finish and test
    def probe_with_swap(self, i: int, j: int):
        self.stats.add_probe(i, j)

        if self.get_time() % self.sample_rate == 0:
            self.stats.add_curr_distance(self.real, self.curr_approx)

        self.random_swap(self.change_rate)

        index_i = self.real.index(i)
        index_j = self.real.index(j)
        return index_i < index_j

    def swap_real(self, i: int, j: int):
        temp = self.real[i]
        self.real[i] = self.real[j]
        self.real[j] = temp

    def random_swap(self, change_rate):
        n = len(self.real)

        for x in range(0, change_rate):
            # this way we have that all the different algorithms get the same swaps in the real,
            # so we can more accurately compare them on the same seed
            # i = self.random_swap_index[((self.get_time() - 1) * change_rate) + x]
            i = random.randint(0, n - 2)
            temp = self.real[i]
            self.real[i] = self.real[i + 1]
            self.real[i + 1] = temp

    def permute_answer(self, ans_perm: list[int]):
        self.curr_approx = ans_perm.copy()

    def size(self):
        return len(self.real)

    def get_time(self):
        return len(self.stats.probes)

    def reverse_order(self):
        n = self.size()
        for i in range(0, n):
            self.real[i] = (n - 1) - i
