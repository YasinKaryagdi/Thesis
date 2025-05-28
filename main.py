import numpy
import matplotlib.pyplot as plt
import pandas
import os
import random
from model.dynamic_list import DynamicList
from algorithms.algorithms import *


# implementation of quicksort
def randomized_quicksort(list):
    if len(list) <= 1:
        return list
    index_pivot = random.randrange(0, len(list), 1)
    pivot = list[index_pivot]

    left = []
    right = []
    for x in list:
        if x < pivot:
            left.append(x)
        elif x > pivot:
            right.append(x)
    pivot_arr = [pivot]
    return randomized_quicksort(left) + pivot_arr + randomized_quicksort(right)


# implementation of blocksort
def blocksort():
    return ordered_list


# calculates the K error given two lists x and y
def calc_kendall_tau(x, y):
    discordant_pairs = 0

    for i in range(0, len(x)):
        for j in range(i + 1, len(x)):
            a = x[i] - x[j]
            b = y[i] - y[j]

            # if discordant (different signs)
            if a * b < 0:
                discordant_pairs += 1

    return discordant_pairs


# get all possible permutations from currlist with at most n swaps
def get_all_permutations(currlist, n):
    all_permutations = [currlist]

    for switch in range(0, n):
        curr_list_size = len(all_permutations)
        for x in range(0, curr_list_size):
            for i in range(0, len(currlist) - 1):
                temp_list = all_permutations[x].copy()

                # swap i and i + 1
                temp = temp_list[i]
                temp_list[i] = temp_list[i + 1]
                temp_list[i + 1] = temp

                if not temp_list in all_permutations:
                    all_permutations.append(temp_list)
    return all_permutations


# when given an approxamation it tries to maximize the distance with the real list by making at most n switches to it
# prioritizes the permutations where the switches have been made at the higher rank,
# this is due to the for loop that loops through all permutations,
# could try and see what happenens if we reverse the order and it prioritizes the bottom switches, this should be worse for our algorithm in theory
def calc_max_error(approximation, currlist, n):
    all_permutations = get_all_permutations(currlist, n)
    worst_case = currlist.copy()
    max_distance = calc_kendall_tau(approximation, currlist)

    for x in all_permutations:
        curr_distance = calc_kendall_tau(approximation, x)
        if curr_distance > max_distance:
            max_distance = curr_distance
            worst_case = x.copy()
    return worst_case


# writes the approximation and the corresponding step into a dir with the inputfile as name
def record_approximation(list, curr_step):
    file = open(
        "/home/yasin/Thesis/approx_input_size"
        + str(len(list))
        + "/step_"
        + str(curr_step)
        + ".txt",
        "x",
    )
    for i in range(0, len(list)):
        file.write(str(list[i]) + "\n")


# used in order to create initial input files
def create_input_file(input_size):
    file = open("input_size" + str(input_size) + ".txt", "x")
    for i in range(0, input_size):
        file.write(str(i + 1) + "\n")
    os.mkdir("approx_input_size" + str(input_size))


# read from a file the input and return it as a list
def read_input(file_name):
    my_list = []

    with open(file_name) as file:
        for line in file:
            line.replace("\n", "")
            my_list.append(int(line))
    return my_list


# deletes files, used for testing
def del_input_files(filename):
    os.remove(filename)


def main():
    # x = [1, 2, 3]
    # y = [1, 2, 3]
    # calc_max_error(x, y, 4)
    # print(str(calc_kendall_tau(x, y)))
    # list = DynamicList(0, 1, 1, 3)
    # assert list.real == [1, 2, 3]
    # list.real = [3, 2, 1]
    # print (list.probe(1, 3))
    # sort = [1, 2, 3]
    return


main()
