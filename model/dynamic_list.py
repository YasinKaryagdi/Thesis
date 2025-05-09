# TODO: write class that has methods for probing and for the introduction of inversions,
# also want to store the real ranking and the approxamation, maybe also want to store last full quicksort
# and two lists for the two seperate versions of quicksort?

import math
import random

class DynamicList:
    real : list[int]
    curr_approx : list[int]

    def __init__(self, rand_seed, n, *args):
        random.seed(rand_seed)
        