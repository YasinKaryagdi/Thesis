# TODO: write class that has methods for probing and for the introduction of inversions,
# also want to store the real ranking and the approxamation, maybe also want to store last full quicksort
# and two lists for the two seperate versions of quicksort?

from run_data.statistics import Stats
import random

class DynamicList:
    real : list[int]
    curr_approx : list[int]
    stats: Stats

    def __init__(self, rand_seed, n, *args):
        random.seed(rand_seed)
        self.stats = Stats()
        self.real = []
        for i in range(0, n):
            self.real.append(i + 1)
        
    # todo, finish and test
    def probe(self, num1, num2):
        
        i = self.real.index(num1)
        j = self.real.index(num2)
        return 
        
    def swap(self):
        n = len(self.real)

        # from 0 to n-2, since the last swap we can do is n-1 with n-2 
        i = random.randint(0, n - 2)
        temp = self.real[i]
        self.real[i] =  self.real[i + 1]
        self.real[i + 1] = temp