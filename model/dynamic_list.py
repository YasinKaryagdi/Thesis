from model.statistics import Stats
import random


class DynamicList:
    real: list[int]
    curr_approx: list[int]
    change_rate: int
    stats: Stats
    start_time: int

    # Is currently unused but it seems to be too late to remove it without
    # potentially breaking something, can be used in the future but would most likely require
    # you to change the way the probe method works.
    probe_rate: int

    def __init__(
        self,
        rand_seed: int,
        probe_rate: int,
        change_rate: int,
        n: int,
        sample_rate: int,
        time_limit: int,
        start_time: int
    ):
        random.seed(rand_seed)
        self.stats = Stats(n)
        self.probe_rate = probe_rate
        self.change_rate = change_rate
        self.sample_rate = sample_rate
        self.time_limit = time_limit
        self.start_time = start_time

        # We start with a real that goes from 0, to n
        self.real = []
        for i in range(0, n):
            self.real.append(i)

        # We start with an approximation that goes from 0, to n
        self.curr_approx = []
        for i in range(0, n):
            self.curr_approx.append(i)

    # Performs change_rate amount of uniformly random swaps before probe,
    # sorts based on the index of int i and j in the real list, so based on their positions in the real
    def probe_with_swap(self, i: int, j: int):
        self.stats.add_probe(i, j)

        if (self.get_time() % self.sample_rate == 0) and (self.get_time() > self.start_time):
            self.stats.add_curr_distance(self.real, self.curr_approx)

        self.random_swap(self.change_rate)

        index_i = self.real.index(i)
        index_j = self.real.index(j)
        return index_i < index_j

    # Used to perform random swaps in the real
    def random_swap(self, change_rate):
        n = len(self.real)

        # Perform change rate amount of random swaps in the real, swapping i with i + 1
        for x in range(0, change_rate):
            i = random.randint(0, n - 2)
            temp = self.real[i]
            self.real[i] = self.real[i + 1]
            self.real[i + 1] = temp

    # Used to update the current approximation
    def permute_answer(self, ans_perm: list[int]):
        self.curr_approx = ans_perm.copy()

    # Used to get the size of the dynamic list
    def size(self):
        return len(self.real)

    # Used to get the current number of probes performed,
    # we only consider the case where the probe rate = 1,
    # so this is the same as taking the len of the list keeping track of all the probes
    def get_time(self):
        return len(self.stats.probes)

    # Used to start with a real list that is reverse sorted,
    # so it is sorted decreasingly
    def reverse_order(self):
        n = self.size()
        for i in range(0, n):
            self.real[i] = (n - 1) - i
