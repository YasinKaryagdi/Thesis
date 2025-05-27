import sys
import os

# Add the parent directory (/home/yasin/Thesis) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from runner import Runner
import math

def run_experiment3():
    input_size = [20] # range(100, 50001, 100)
    algorithm = ["rep-insertion", "quick-rep-insertion", "rep-quick-rep-insertion-1", "rep-quick-rep-insertion-2"]
    config = ["sorted"]
    seed = range(0,3)
    probe_rate = [1]
    change_rate = [1, 2, 10, 20]


    for n in input_size:
        for alg in algorithm :
            for con in config:
                for p in probe_rate:
                    for c in change_rate:
                        for i in seed:
                            time_limit = int(math.pow(n, 2))
                            
                            # taking the same as what Besa et al. did
                            sample_rate = int(n / 20)
                            file_name = "experiments/results/experiment3/" + alg + "-"+ str(n) + "-" + str(c) + "-" + str(i) + ".xlsx"
                            cur_run = Runner(i, p, c, alg, n, time_limit, sample_rate, con)

                            print("curr i: " + str(i) + " \n") # used to see if anything is running
                            cur_run.run()
                            cur_run.store_results(file_name)

run_experiment3()