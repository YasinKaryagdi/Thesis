# TODO: write class that can be used to store the whole state of an interation, 
# so for example the curr kendall tau distance and the state of the real and the approx of both quicksorts,
# maybe also how many inversions they fixed and how many occured? and also the conditions they occured in, 
# so for example change rate alpha

import random

class Stats:
    temp : int

    def __init__(self, rand_seed, n, *args):
        random.seed(rand_seed)
        