# TODO: write class that can be used to store the whole state of an interation, 
# so for example the curr kendall tau distance and the state of the real and the approx of both quicksorts,
# maybe also how many inversions they fixed and how many occured? and also the conditions they occured in, 
# so for example change rate alpha

import random

class Stats:
    approx_list: list[list[int]]
    real_list: list[list[int]]
    distances: list[int]
    seed: int

    def __init__(self, rand_seed, n, *args):
        self.seed = rand_seed
        self.approx_list = []
        self.real_list = []
        self.distances = []

        
    def add_approx(self, curr_approx):
        self.approx_list.append(curr_approx)
        
    def add_real(self, curr_real):
        self.approx_list.append(curr_real)

    # calculates the K error given two lists x and y
    def calc_kendall_tau(x, y):
        discordant_pairs = 0
        
        for i in range(0, len(x)):
            for j in range(i + 1, len(x)):
                a = x[i] - x[j]
                b = y[i] - y[j]

                # if discordant (different signs)
                if (a * b < 0):
                    discordant_pairs += 1

        return discordant_pairs
    
    def add_curr_distance(self):
        # TODO: check if the order is correct and if it matters
        distance = self.calc_kendall_tau(self.real_list, self.approx_list)
        self.distances.append(distance)

    def print_latest_updates(self):
        print("current iteration is: " + str(len(self.real_list)))
        print("curr real list is: \n")
        print(self.real_list)
        print("\n")

        print("curr approx list is: \n")
        print(self.approx_list[len(self.approx_list)])
        print("\n")

        print("their distance is: \n")
        print(self.distances[len(self.distances)])
        print("\n")
        print("\n")