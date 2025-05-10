# TODO: want to implement randomized quicksort and blocksort, 
# also want to maybe implement mergesort

from model.dynamic_list import DynamicList


# implementation of quicksort
def randomized_quicksort(list: DynamicList):
   if len(list) <= 1:
      return list
   index_pivot = random.randrange(0, len(list), 1)
   pivot =  list[index_pivot]
   
   left = []
   right = []
   for x in list:
      if probe(x, pivot):
         left.append(x)
      elif x > pivot:
         right.append(x)
   pivot_arr = [pivot]
   return randomized_quicksort(left) + pivot_arr + randomized_quicksort(right)