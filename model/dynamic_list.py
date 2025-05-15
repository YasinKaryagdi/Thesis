# TODO: write class that has methods for probing and for the introduction of inversions,
# also want to store the real ranking and the approxamation, maybe also want to store last full quicksort
# and two lists for the two seperate versions of quicksort?

from run_data.statistics import Stats
import random

class DynamicList:
    real: list[int]
    curr_approx: list[int]
    probe_rate: int
    change_rate: int
    curr_quicksort_list: list[int]
    curr_blocksort_list: list[int]
    stats: Stats

    def __init__(self, rand_seed, probe_rate, change_rate, n):
        random.seed(rand_seed)
        self.stats = Stats(rand_seed, n)
        self.probe_rate = probe_rate
        self.change_rate = change_rate

        # maybe I want to initialize this as reverse ordered, so that we always start at maximal distance
        self.real = []
        for i in range(0, n):
            self.real.append(i)

        self.curr_approx = []
        for i in range(0, n):
            self.curr_approx.append(i)
        
    # todo, finish and test
    def probe(self, i, j):
        self.stats.add_probe(i, j)
        self.stats.add_curr_distance(self.real, self.curr_approx)
        index_i = self.real.index(i)
        index_j = self.real.index(j)
        return index_i < index_j

    # todo, finish and test
    def probe_with_swap(self, i, j):
        self.stats.add_probe(i, j)
        self.stats.add_curr_distance(self.real, self.curr_approx)


        for x in range(0, self.change_rate):
            self.random_swap()

        index_i = self.real.index(i)
        index_j = self.real.index(j)
        return index_i < index_j

        
    def swap_real(self, i, j):
        temp = self.real[i]
        self.real[i] =  self.real[j]
        self.real[j] = temp

    def random_swap(self):
        n = len(self.real)

        # from 0 to n-2, since the last swap we can do is n-1 with n-2 
        i = random.randint(0, n - 2)

        # for testing
        # print(str(i) + "\n")
        
        temp = self.real[i]
        self.real[i] =  self.real[i + 1]
        self.real[i + 1] = temp
        # print("current real list is: \n")
        # print(self.real)
    
    def permute_answer(self, ans_perm):
        self.curr_approx = ans_perm.copy()

    def size(self):
        return len(self.real)
    
    def get_time(self):
        return len(self.stats.probes)
    
    def reverse_order(self):
        n = self.size()
        for i in range(0, n):
            self.real[i] = (n - 1)- i