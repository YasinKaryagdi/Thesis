# TODO: want to run a certain configuration of an experiment and then in main use this class in order to run all the experiments

from model.dynamic_list import DynamicList

class Runner:
    def __init__(self, rand_seed, probe_rate, change_rate, algorithm, input_size):
        self.probe_rate = probe_rate
        self.change_rate = change_rate
        self.algorithm = algorithm
        self.curr_list = DynamicList(rand_seed, probe_rate, change_rate, input_size)


    # TODO
    def run(self):
        return