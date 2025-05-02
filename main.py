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

def record_approximation(list, curr_step):
   # want to write the step and the approx into a map with the inputfile as name, so for example:
   # for each step of input_file_size10.txt we write to a dir input_file_size10, stepi.txt for the ith approximation
   file = open("/home/yasin/Thesis/apprx_input_size" + str(len(list)) + "/step_" +  str(curr_step) + ".txt", "x")
   for i in range(0, len(list)):
      file.write(str(list[i]) + "\n")


# used in order to create initial input files
def create_input_file(input_size):
   file = open("input_size" +  str(input_size) + ".txt", "x")
   for i in range(0, input_size):
      file.write(str(i + 1) + "\n")
   os.mkdir("apprx_input_size" + str(input_size))

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
   temp = [1, 2, 3]
   record_approximation(temp, 1)

   temp = [1, 3, 2]
   record_approximation(temp, 2)

   step_one = read_input("apprx_input_size3/step_1.txt")
   print(step_one)

   step_two = read_input("apprx_input_size3/step_2.txt")
   print(step_two)
   return



main()