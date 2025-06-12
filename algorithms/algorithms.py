from model.dynamic_list import DynamicList
from model.q_sort_state import QSortState
import random
import math


def partition(list: DynamicList, to_sort, low: int, high: int):
    ranges = high - low + 1

    # We randomly pick a pivot, probably should have done random.randint(low, high)
    pivotChoice = low + random.randint(0, 32767) % ranges

    temp = to_sort[high]
    to_sort[high] = to_sort[pivotChoice]
    to_sort[pivotChoice] = temp

    i = low - 1
    for j in range(low, high):
        # Extra check that makes sure that we don't go over time
        if list.get_time() >= list.time_limit:
            return -1

        if list.probe_with_swap(to_sort[j], to_sort[high]):
            i += 1
            temp = to_sort[i]
            to_sort[i] = to_sort[j]
            to_sort[j] = temp
    temp = to_sort[i + 1]
    to_sort[i + 1] = to_sort[high]
    to_sort[high] = temp
    return i + 1


def quicksort(list: DynamicList, to_sort, low: int, high: int):
    if low < high:
        pivot = partition(list, to_sort, low, high)

        # Pivot of -1 means that list.get_time() >= list.time_limit so we return,
        # introduced in order to stop running the algorithm after the time limit has passed
        if pivot == -1:
            return

        quicksort(list, to_sort, low, pivot - 1)
        quicksort(list, to_sort, pivot + 1, high)


# Given a random list that goes from 0 to n-1 sort it based on the order in the real list,
# afterwards update the curr_approx to the result,
# this is the initial quicksort called when a run of quicksort is performed
def quicksort_base(list: DynamicList, n: int):
    to_sort = []
    for i in range(0, n):
        to_sort.append(i)

    quicksort(list, to_sort, 0, n - 1)
    list.permute_answer(to_sort)


def repeated_insertion_sort(list: DynamicList, time_limit: int):
    n = list.size()
    while list.get_time() < time_limit:
        for i in range(1, n):
            j = i
            # Probe the ints at approx[j] with approx[j - 1]
            while j > 0 and list.probe_with_swap(
                list.curr_approx[j], list.curr_approx[j - 1]
            ):
                temp = list.curr_approx[j - 1]
                list.curr_approx[j - 1] = list.curr_approx[j]
                list.curr_approx[j] = temp
                j -= 1

                # Extra check that makes sure that we don't go over time
                if list.get_time() >= time_limit:
                    return


# Perform one run of quicksort, followed by repeated insertion sort
def quick_then_insertion_sort(list: DynamicList, time_limit: int):
    n = list.size()
    quicksort_base(list, n)
    repeated_insertion_sort(list, time_limit)


# Perform repeated runs of one quicksort, followed by a certain amount of insertion sort runs
def rep_quick_then_insertion_sort(list: DynamicList, time_limit: int, iterations: int):
    n = list.size()

    while list.get_time() < time_limit:
        quicksort_base(list, n)

        k = 0
        while (list.get_time() < time_limit) and (k < iterations):
            for i in range(1, n):
                j = i
                # Probe the ints at approx[j] with approx[j - 1]
                while j > 0 and list.probe_with_swap(
                    list.curr_approx[j], list.curr_approx[j - 1]
                ):
                    temp = list.curr_approx[j - 1]
                    list.curr_approx[j - 1] = list.curr_approx[j]
                    list.curr_approx[j] = temp
                    j -= 1

                    # Extra check that makes sure that we don't go over time
                    if list.get_time() >= time_limit:
                        return
            k += 1


# Repeatedly perform quicksort until the time limit is reached
def repeated_quicksort(list: DynamicList, time_limit: int):
    n = list.size()
    while list.get_time() < time_limit:
        quicksort_base(list, n)


def start_new_quicksort_call(
    to_sort: list[int], call_stack: list[QSortState], low: int, high: int
):
    if low < high:
        range = high - low + 1
        pivotChoice = low + random.randint(0, 32767) % range
        temp = to_sort[high]
        to_sort[high] = to_sort[pivotChoice]
        to_sort[pivotChoice] = temp
        newCall = QSortState(low, high)
        call_stack.append(newCall)


def stack_quicksort_run_step(
    list: DynamicList, to_sort: list[int], call_stack: list[QSortState]
):
    step_performed = False

    while not step_performed:

        # If there are no quicksort calls on the stack, terminate
        if len(call_stack) == 0:
            return False

        # Otherwise attempt to run a step of the top call
        curr_call = call_stack[-1]
        low = curr_call.low
        high = curr_call.high
        i = curr_call.i
        j = curr_call.j

        if j < high:
            if list.probe_with_swap(to_sort[j], to_sort[high]):
                curr_call.i += 1
                temp = to_sort[i + 1]
                to_sort[i + 1] = to_sort[j]
                to_sort[j] = temp
            curr_call.j += 1
            step_performed = True
        else:
            call_stack.pop()
            # If the quicksort call finished,
            # then move the pivot into the correct position
            temp = to_sort[i + 1]
            to_sort[i + 1] = to_sort[high]
            to_sort[high] = temp

            # And start the two new recursive calls
            low_left = low
            high_left = i
            low_right = i + 2
            high_right = high
            start_new_quicksort_call(to_sort, call_stack, low_left, high_left)
            start_new_quicksort_call(to_sort, call_stack, low_right, high_right)
    return True


def blocked_quicksort(list: DynamicList, time_limit: int, block_constant: int):
    n = list.size()

    # Determine block size m close to 10 * ln(n)
    m = int(block_constant * math.log(n))
    if m % 2 == 1:
        m += 1
    if m > n:
        m = n
    while n % m != 0:
        m += 2

    # Initial full quicksort
    full_stack = []
    quicksort_base(list, n)
    to_full_sort = list.curr_approx.copy()

    last_full_answer = list.curr_approx.copy()
    next_full_answer = list.curr_approx.copy()
    new_full_answer = False

    start_new_quicksort_call(to_full_sort, full_stack, 0, n - 1)
    block_stack = []

    while list.get_time() < time_limit:
        to_blocksort = [None] * m
        block_answer = [None] * n

        # Switch to new full answer if available
        if new_full_answer:
            new_full_answer = False
            last_full_answer = next_full_answer.copy()

        # Fill first m/2 items
        for i in range(m // 2):
            temp = last_full_answer[i]
            to_blocksort[i] = temp

        for i in range(1, (2 * n) // m):
            # Fill next m/2 items
            for j in range(m // 2):
                temp = last_full_answer[i * (m // 2) + j]
                to_blocksort[m // 2 + j] = temp

            # Sort current block
            start_new_quicksort_call(to_blocksort, block_stack, 0, m - 1)
            while stack_quicksort_run_step(list, to_blocksort, block_stack):
                full_sort_done = not stack_quicksort_run_step(
                    list, to_full_sort, full_stack
                )
                if full_sort_done:
                    new_full_answer = True
                    next_full_answer = to_full_sort.copy()
                    start_new_quicksort_call(to_full_sort, full_stack, 0, n - 1)

            # Copy smallest half to block answer, shift larger half forward
            for j in range(m // 2):
                temp1 = to_blocksort[j]
                block_answer[(i - 1) * (m // 2) + j] = temp1
                temp2 = to_blocksort[m // 2 + j]
                to_blocksort[j] = temp2

        # Handle last m/2 elements
        for j in range(m // 2):
            temp = to_blocksort[j]
            block_answer[n - (m // 2) + j] = temp

        list.permute_answer(block_answer)

        # Update all working answers
        last_full_answer = block_answer.copy()
        next_full_answer = block_answer.copy()
        to_full_sort = block_answer.copy()
