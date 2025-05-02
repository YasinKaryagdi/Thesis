import numpy
import matplotlib
import pandas
import os

# implementation of blocksort
def blocksort():
   return ordered_list

# implementation of quicksort
def quicksort():
   return ordered_list

def record_approximation():
   # want to write the step and the approx into a map with the inputfile as name, so for example:
   # for each step of input_file_size10.txt we write to a dir input_file_size10, stepi.txt for the ith approximation
   return temp

# used in order to create initial input files
def create_input_file(input_size):
   file = open("input_file_size" +  str(input_size) + ".txt", "x")
   for i in range(0, input_size):
      file.write(str(i + 1) + "\n")

# read from a file the input and return it as a list
def read_input(file_name):
   my_list = []

   with open(file_name) as file:
      for line in file:
         line.replace("\n", "")
         my_list.append(int(line))
   return my_list

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


# recurcive function that makes n switches and calculates the max error based on current approximation
def calc_max_error(approximation, currlist, switches):
  if switches == 0:
     calc_kendall_tau()


def del_input_files(filename):
   os.remove(filename)

def main():
   return



main()