from model.dynamic_list import DynamicList
from model.q_sort_state import QSortState
import random
import math as math


def partition(list:DynamicList, toSort, low, high):
    range = high - low + 1
    pivotChoice = low + random.randint(0, 32767) % range; # temp, fix random
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


def quicksort_base(list: DynamicList, n):
    toSort = []
    for i in range(0, n):
        toSort.append(i)

    quicksort(list, toSort, 0, n - 1)
    list.permute_answer(toSort)


def repeated_insertion_sort(list: DynamicList, time_limit):
    n = list.size()
    while list.get_time() < time_limit:
        for i in range(1, n):
            j = i
            # probe the ints at approx[j] with approx[j - 1]
            while j > 0 and list.probe(list.curr_approx[j], list.curr_approx[j - 1]):
                temp = list.curr_approx[j-1]
                list.curr_approx[j-1] = list.curr_approx[j]
                list.curr_approx[j] = temp
                j -= 1

                # extra check that makes sure that we don't go over time
                if list.get_time() >= time_limit:
                    return


def quick_then_insertion_sort(list: DynamicList, time_limit):
    n = list.size()
    quicksort_base(list,n)
    repeated_insertion_sort(list,time_limit)


def rep_quick_then_insertion_sort(list: DynamicList, time_limit: int, iterations: int):
    n = list.size()

    while list.get_time() < time_limit:
        quicksort_base(list,n)

        k = 0
        while (list.get_time() < time_limit) and (k < iterations):
            for i in range(1, n):
                j = i
                # probe the ints at approx[j] with approx[j - 1]
                while j > 0 and list.probe(list.curr_approx[j], list.curr_approx[j - 1]):
                    temp = list.curr_approx[j-1]
                    list.curr_approx[j-1] = list.curr_approx[j]
                    list.curr_approx[j] = temp
                    j -= 1

                    # extra check that makes sure that we don't go over time
                    if list.get_time() >= time_limit:
                        return
            k += 1


def repeated_quicksort(list: DynamicList, time_limit):
    n = list.size()
    while(list.get_time() < time_limit):
        quicksort_base(list,n)


def startNewQuicksortCall(toSort: list[int], callStack: list[QSortState], low: int, high: int):
  if low < high:
    range = high - low + 1
    pivotChoice = low + random.randint(0, 32767) % range; # temp, fix random
    temp = toSort[high]
    toSort[high] = toSort[pivotChoice]
    toSort[pivotChoice] = temp
    newCall = QSortState(low,high)
    callStack.push(newCall)


def stackQuicksortRunStep(list: DynamicList, toSort: list[int], callStack: list[QSortState]):
    stepPerformed = False 

    while(not stepPerformed):

        # if there are no quicksort calls on the stack, terminate
        if len(callStack) == 0:
            return False
 
        # otherwise attempt to run a step of the top call
        currCall = callStack[-1]
        low = currCall.low 
        high = currCall.high 
        i = currCall.i
        j = currCall.j  
  
        if(j < high):
            if(list.probe(toSort[j],toSort[high])):
                currCall.i += 1
                temp = toSort[i+1]
                toSort[i+1] = toSort[j]
                toSort[j] = temp
            currCall.j += 1
            stepPerformed = True
        else:
            callStack.pop()
            # if the quicksort call finished
            # move the pivot into the correct position
            temp = toSort[i+1]
            toSort[i+1] = toSort[high]
            toSort[high] = temp

            # and start the two new recursive calls
            lowLeft = low
            highLeft = i
            lowRight = i+2
            highRight = high   
            startNewQuicksortCall(toSort,callStack,lowLeft,highLeft)
            startNewQuicksortCall(toSort,callStack,lowRight,highRight)
    return True


def stackQuicksort(list: DynamicList, time_limit: int):
    n = list.size()
    while list.get_time() < time_limit:
        callStack = []
        toSort = []
        for i in range(0, n):
            toSort.append(i) = i
        startNewQuicksortCall(toSort,callStack,0,n-1)

        j = 0
        while stackQuicksortRunStep(list,toSort,callStack):
            j += 1
        list.permuteAnswer(toSort)
  

def permuteVector(vec: list[int],  perm: list[int]):
    n = len(perm)
    oldVec = vec.copy()
    for i in range(0, n):
        vec[i] = perm[oldVec[i]]


def blockedQuicksort(list: DynamicList, time_limit: int):
    n = list.size()
  
    # Find a block size close to 10 ln n
    m = int(10 * math.log(n))
    if m % 2 == 1:
        m += 1
    if m > n:
        m = n
    while n % m != 0:
        m+=2

    fullStack = []
    toFullSort = []
    for i in range(0, n):
        toFullSort.append(i)
    # Begin with a normal quicksort run
    startNewQuicksortCall(toFullSort,fullStack,0,n-1)

    q = 0
    while(stackQuicksortRunStep(list,toFullSort,fullStack)):
        q += 1
    list.permute_answer(toFullSort)
    
    lastFullAnswer = []
    nextFullAnswer = []
    for i in range(0, n):
        lastFullAnswer.append(i)
        nextFullAnswer.append(i)
  
    newFullAnswer = False

    startNewQuicksortCall(toFullSort,fullStack,0,n-1)
    blockStack = []

    while(list.get_time() < time_limit):
        toBlockSort = [None] * m
        blockAnswer = [None] * n

        # Switch to the answer from the newest full quicksort run
        if newFullAnswer:
            newFullAnswer = False
            lastFullAnswer = nextFullAnswer

        # Start with the m/2 smallest elements in the block
        for i in range(0, m/2):
            toBlockSort[i] = lastFullAnswer[i]
        for i in range(1, 2 * n/m):
        
            # Place the next m/2 smallest elements in the block
            for j in range(0, m/2):
                toBlockSort[m/2 + j] = lastFullAnswer[i*m/2 + j]

            startNewQuicksortCall(toBlockSort,blockStack,0,m-1)
            while(stackQuicksortRunStep(list,toBlockSort,blockStack)):
                fullQuickSortFinished = not stackQuicksortRunStep(list,toFullSort,fullStack)
                if(fullQuickSortFinished):
                    newFullAnswer = True
                    nextFullAnswer = toFullSort
                    startNewQuicksortCall(toFullSort,fullStack,0,n-1)

            # Copy over the smallest m/2 elements in the block to the answer
            # and shift over the largest m/2 elements to the left
            for j in range(0, m/2):
                blockAnswer[(i-1) * m/2 + j] = toBlockSort[j]
                toBlockSort[j] = toBlockSort[m/2+j]
        
        # Copy over the last set of m/2 elements in the block into the answer
        for j in range(0, m/2):
            blockAnswer[n - m/2 + j] = toBlockSort[j]
        
        list.permute_answer(blockAnswer)
        # After publishing new answer, update several lists of element indexes
        permuteVector(lastFullAnswer,blockAnswer)
        permuteVector(nextFullAnswer,blockAnswer)
        permuteVector(toFullSort,blockAnswer)
