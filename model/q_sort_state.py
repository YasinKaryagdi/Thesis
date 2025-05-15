# TODO: write class that has methods for probing and for the introduction of inversions,
# also want to store the real ranking and the approxamation, maybe also want to store last full quicksort
# and two lists for the two seperate versions of quicksort?

from run_data.statistics import Stats
import random

class QSortState:
    low: int
    high: int
    i: int
    j: int

    def __init__(self, l, h):
        low = l
        high = h
        i = low-1
        j = low