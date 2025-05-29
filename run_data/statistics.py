# TODO: write class that can be used to store the whole state of an interation,
# so for example the curr kendall tau distance and the state of the real and the approx of both quicksorts,
# maybe also how many inversions they fixed and how many occured? and also the conditions they occured in,
# so for example change rate alpha

import random


class Stats:
    probes: list[list[int]]
    distances: list[int]
    input_size: int

    def __init__(self, n):
        self.distances = []
        self.probes = []
        self.input_size = n

    def add_probe(self, i, j):
        self.probes.append([i, j])

    def total_inversions(self, real):
        vec = real.copy()
        return self.merge_sort_inversions(vec)

    def merge_sort_inversions(self, v):
        n = len(v)
        if n <= 1:
            return 0

        mid = n // 2
        left = v[:mid]
        right = v[mid:]

        left_invs = self.merge_sort_inversions(left)
        right_invs = self.merge_sort_inversions(right)

        invs_between = 0
        i = j = k = 0

        while i < len(left) and j < len(right):
            if self.aprox[left[i]] < self.aprox[right[j]]:
                v[k] = left[i]
                i += 1
            else:
                v[k] = right[j]
                j += 1
                invs_between += len(left) - i
            k += 1

        while i < len(left):
            v[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            v[k] = right[j]
            j += 1
            k += 1

        return left_invs + right_invs + invs_between

    def add_curr_distance(self, real, approx):
        self.aprox = (
            approx  # ensure self.aprox is set correctly for inversion calculation
        )
        distance = self.total_inversions(real)
        self.distances.append(distance)
