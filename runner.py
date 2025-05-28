# TODO: want to run a certain configuration of an experiment and then in main use this class in order to run all the experiments

from model.dynamic_list import DynamicList
from algorithms.algorithms import *
import pandas as pd


class Runner:
    algorithm: str
    curr_list: DynamicList
    time_limit: int

    def __init__(
        self,
        rand_seed: int,
        probe_rate: int,
        change_rate: int,
        algorithm: str,
        input_size: int,
        time_limit: int,
        sample_rate: int,
        config: str,
    ):
        self.algorithm = algorithm
        self.time_limit = time_limit
        self.curr_list = DynamicList(
            rand_seed, probe_rate, change_rate, input_size, sample_rate, time_limit
        )

        # currently only valid options are sorted and reverse-sorted
        if config == "reverse-sorted":
            self.curr_list.reverse_order()
        elif config != "sorted":
            raise Exception("Invalid config")

    def run(self):
        if self.algorithm == "rep-quick":
            repeated_quicksort(self.curr_list, self.time_limit)
        elif self.algorithm.startswith("block"):
            temp = self.algorithm.split("-")
            i = temp[len(temp) - 1]
            blocked_quicksort(self.curr_list, self.time_limit, int(i))
        elif self.algorithm == "rep-insertion":
            repeated_insertion_sort(self.curr_list, self.time_limit)
        elif self.algorithm == "quick-rep-insertion":
            quick_then_insertion_sort(self.curr_list, self.time_limit)
        elif self.algorithm.startswith("rep-quick-rep-insertion"):
            temp = self.algorithm.split("-")
            i = temp[len(temp) - 1]
            rep_quick_then_insertion_sort(self.curr_list, self.time_limit, int(i))
        else:
            raise Exception("No correct alg given as input")

    def store_results(self, file_name):
        results = pd.DataFrame(self.curr_list.stats.distances)
        datatoexcel = pd.ExcelWriter(path=file_name)
        results.to_excel(datatoexcel)
        datatoexcel.close()
