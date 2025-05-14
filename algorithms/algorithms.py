# TODO: want to implement randomized quicksort and blocksort, 
# also want to maybe implement mergesort

from model.dynamic_list import DynamicList
import random


def partition(list:DynamicList, toSort, low, high):
    ranges = high - low + 1
    pivotChoice = low + random.randint(0, 32767) % ranges; # temp, fix random
    temp = toSort[high]
    toSort[high] = toSort[pivotChoice]
    toSort[pivotChoice] = temp

    i = low - 1
    for j in range(low, high):
        if(list.probe(toSort[j],toSort[high])):
            i += 1
            temp = toSort[i]
            toSort[i] = toSort[j]
            toSort[j] = temp
    temp = toSort[i + 1]
    toSort[i + 1] = toSort[high]
    toSort[high] = temp
    return i+1


def quicksort(list: DynamicList, toSort, low, high):
  if low < high:
    pivot = partition(list, toSort, low, high)
    quicksort(list,toSort,low,pivot-1)
    quicksort(list,toSort,pivot+1,high)


def quicksortBase(list: DynamicList, n):
    toSort = []
    for i in range(0, n):
        toSort.append(i)

    print("toSort:before\n")
    print(toSort)
    print("\n")
    quicksort(list, toSort, 0, n - 1)
    print("toSort:after\n")
    print(toSort)
    list.permuteAnswer(toSort)