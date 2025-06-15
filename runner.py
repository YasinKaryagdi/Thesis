from model.dynamic_list import DynamicList
from algorithms.algorithms import *
import pandas as pd


class Runner:
    alg: str
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
        start_time: int = 0
    ):
        self.alg = algorithm
        self.time_limit = time_limit
        self.curr_list = DynamicList(
            rand_seed, probe_rate, change_rate, input_size, sample_rate, time_limit, start_time
        )

        # Currently only valid options are sorted and reverse-sorted
        if config == "reverse-sorted":
            self.curr_list.reverse_order()
        elif config != "sorted":
            raise Exception("Invalid config")

    # Runs the relevant algorithm with the current configuration
    def run(self):
        if self.alg == "rep-quick":
            repeated_quicksort(self.curr_list, self.time_limit)
        elif self.alg.startswith("block"):
            temp = self.alg.split("-")
            block_constant = temp[len(temp) - 1]
            blocked_quicksort(self.curr_list, self.time_limit, int(block_constant))
        elif self.alg == "rep-insertion":
            repeated_insertion_sort(self.curr_list, self.time_limit)
        elif self.alg == "quick-rep-insertion":
            quick_then_insertion_sort(self.curr_list, self.time_limit)
        elif self.alg.startswith("rep-quick-rep-insertion"):
            temp = self.alg.split("-")
            i = temp[len(temp) - 1]
            rep_quick_then_insertion_sort(self.curr_list, self.time_limit, int(i))
        else:
            raise Exception("No correct alg given as input")
    	
    # Saves the results of the current run in the for of an excel sheet
    def store_results(self, file_name):
        results = pd.DataFrame(self.curr_list.stats.distances)
        datatoexcel = pd.ExcelWriter(path=file_name)
        results.to_excel(datatoexcel)
        datatoexcel.close()
