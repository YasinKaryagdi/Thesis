# TODO: want to run a certain configuration of an experiment and then in main use this class in order to run all the experiments

from model.dynamic_list import DynamicList
from algorithms.algorithms import *

class Runner:
    def __init__(self, rand_seed, probe_rate, change_rate, algorithm, input_size, time_limit, sample_rate):
        self.algorithm = algorithm
        self.curr_list = DynamicList(rand_seed, probe_rate, change_rate, input_size, sample_rate)
        self.time_limit = time_limit


    # TODO
    def run(self):
        if self.algorithm == "rep-quick":
            repeated_quicksort(self.curr_list, self.time_limit)
        elif self.algorithm == "block":
            return #temp
        elif self.algorithm == "rep-insert":
            repeated_insertion_sort(self.curr_list, self.time_limit)
        elif self.algorithm == "quick-rep-insert":
            quick_then_insertion_sort(self.curr_list, self.time_limit)
        elif self.algorithm == "rep-quick-rep-insert":
            return #temp
        else:
            raise Exception("No correct alg given as input")

        return
    
    def store_results(self, file_name):
        #self.curr_list.stats.
        return