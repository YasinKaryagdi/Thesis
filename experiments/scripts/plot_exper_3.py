import sys
import os

# Add the parent directory (/home/yasin/Thesis) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from runner import Runner
import math
import pandas as pd
import matplotlib.pyplot as plt

def store_average(input_size, algorithm, config, seed, change_rate, experiment_num):
    for n in input_size:
        for c in change_rate:
            for alg in algorithm:
                for con in config:
                        file_name_avg = f"experiments/results/experiment{experiment_num}/avg/{alg}-{n}-{c}.xlsx"
                        sample_rate = n / 20
                        # Check if file already exists
                        if os.path.exists(file_name_avg):
                            print(f"Skipped (already exists): {file_name_avg}")
                            
                        else:
                            run_file_names = []
                            for i in seed:
                                time_limit = int(math.pow(n, 2) * 2)

                                # taking the same as what Besa et al. did
                                file_name = f"experiments/results/experiment{experiment_num}/{alg}-{n}-{c}-{i}.xlsx"
                                run_file_names.append(file_name)
                            
                            results = []
                            for files in run_file_names:
                                temp = pd.read_excel(files,  index_col=0)
                                results.append(temp)
                            mean_results = pd.concat(results).groupby(level=0).mean()
                            mean_results = mean_results[:time_limit] # supposed to be test[:time_limit]

                            mean_results["temp"] = mean_results.index * sample_rate
                            mean_results.set_index("temp")

                            # writing to Excel
                            file_name = f"experiments/results/experiment{experiment_num}/avg/{alg}-{n}-{c}.xlsx"
                            datatoexcel = pd.ExcelWriter(path = file_name)
                            mean_results.to_excel(datatoexcel)
                            datatoexcel.close()

def plot_figures(input_size, algorithm, change_rate, experiment_num):
    for n in input_size:
        for c in change_rate:
            # One plot for all algorithms with same n and c
            plt.figure(figsize=(10, 6))
            sample_rate = n / 20
            for alg in algorithm:
                file_name = f"experiments/results/experiment{experiment_num}/avg/{alg}-{n}-{c}.xlsx"
                try:
                    df = pd.read_excel(file_name, index_col=0)

                    if 'temp' in df.columns:
                        x = df['temp']
                        y = df.iloc[:, 0]
                    else:
                        x = df.index * sample_rate
                        y = df.iloc[:, 0]

                    plt.plot(x, y, label=alg)
                except FileNotFoundError:
                    print(f"File not found: {file_name}")
                    continue

            plt.title(f"Algorithm Behavior (input size = {n}, change rate = {c})")
            plt.xlabel("Number of Probes")
            plt.ylabel("Average Kendall-Tau Distance")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            plot_file = f"experiments/results/experiment{experiment_num}/plots/plot-{n}-{c}.png"
            plt.savefig(plot_file)
            plt.close()



def main():
    input_size = [1000, 10000]
    algorithm = ["rep-insertion", "quick-rep-insertion", "rep-quick-rep-insertion-1", "rep-quick-rep-insertion-2"]
    config = ["reverse-sorted"]
    seed = range(0,1)
    change_rate = [1, 2, 10, 20]
    experiment_num = 3

    store_average(input_size, algorithm, config, seed, change_rate, experiment_num)
    plot_figures(input_size, algorithm, change_rate, experiment_num)

main()