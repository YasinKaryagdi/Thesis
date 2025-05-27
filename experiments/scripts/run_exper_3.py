import sys
import os

# Add the parent directory (/home/yasin/Thesis) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import math
from multiprocessing import Pool, cpu_count
import pandas as pd
import matplotlib.pyplot as plt
from runner import Runner

# Run a single experiment (called in parallel)
def run_single_experiment(args):
    i, c, alg, n, con, experiment_num = args
    file_name = f"experiments/results/experiment{experiment_num}/{alg}-{n}-{c}-{i}.xlsx"
    
    # Check if file already exists
    if os.path.exists(file_name):
        print(f"Skipped (already exists): " + file_name)
        return

    time_limit = int(math.pow(n, 2) * 10)
    sample_rate = n / 5
    probe_rate = 1
    cur_run = Runner(i, probe_rate, c, alg, n, time_limit, sample_rate, con)

    print(f"Running: n={n}, alg={alg}, change={c}, seed={i}")
    cur_run.run()
    cur_run.store_results(file_name)

def run_experiment_parallel(input_size, algorithm,config,seed,change_rate, experiment_num):
    # Prepare list of tasks
    tasks = [
        (i, c, alg, n, con, experiment_num)
        for n in input_size
        for alg in algorithm
        for con in config
        for c in change_rate
        for i in seed
    ]

    # Use all available CPU cores - 3
    num_processes = cpu_count() - 3
    with Pool(processes=num_processes) as pool:
        pool.map(run_single_experiment, tasks)




def main():
    input_size = [1000]
    algorithm = ["rep-insertion", "quick-rep-insertion", "rep-quick-rep-insertion-1", "rep-quick-rep-insertion-2"]
    config = ["sorted"]
    seed = range(0,1)
    change_rate = [1, 2, 10, 20]
    experiment_num = 3

    run_experiment_parallel(input_size, algorithm,config,seed,change_rate, experiment_num)


main()