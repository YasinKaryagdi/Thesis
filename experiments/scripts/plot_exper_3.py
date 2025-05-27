import sys
import os

# Add the parent directory (/home/yasin/Thesis) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from runner import Runner
import math
import pandas as pd
import matplotlib.pyplot as plt

def store_average(input_size, algorithm, config, seed, probe_rate, change_rate):
    for n in input_size:
        for c in change_rate:
            for alg in algorithm:
                for con in config:
                    for p in probe_rate:
                        run_file_names = []
                        for i in seed:
                            time_limit = int(math.pow(n, 2))

                            # taking the same as what Besa et al. did
                            sample_rate = int(n / 20)
                            file_name = "experiments/results/experiment3/" + alg + "-"+ str(n) + "-" + str(c) + "-" + str(i) + ".xlsx"
                            run_file_names.append(file_name)
                        
                        results = []
                        for files in run_file_names:
                            temp = pd.read_excel(files,  index_col=0)
                            results.append(temp)
                        mean_results = pd.concat(results).groupby(level=0).mean()
                        mean_results = mean_results[:time_limit] # supposed to be test[:time_limit]

                        sample_rate = n / 20
                        mean_results["temp"] = mean_results.index * sample_rate
                        mean_results.set_index("temp")

                        # writing to Excel
                        file_name = "experiments/results/experiment3/avg-" + alg + "-"+ str(n) + "-" + str(c) + ".xlsx"
                        datatoexcel = pd.ExcelWriter(path = file_name)
                        mean_results.to_excel(datatoexcel)
                        datatoexcel.close()


                        #plt.plot(mean_results["index"][:time_limit], mean_results.iloc[:time_limit, 0], label = alg + " " + "alpha = " + change_rate)

def plot_figures(input_size, algorithm, change_rate):
    for n in input_size:
        for c in change_rate:
            plt.figure(figsize=(10, 6))
            for alg in algorithm:
                file_name = f"experiments/results/experiment3/avg-{alg}-{n}-{c}.xlsx"
                try:
                    df = pd.read_excel(file_name, index_col=0)

                    # Ensure 'temp' is used as the x-axis
                    if 'temp' in df.columns:
                        x = df['temp']
                        y = df.iloc[:, 0]  # assuming the first column (excluding index) is the target metric
                    else:
                        sample_rate = input_size / 20
                        x = df.index * sample_rate
                        y = df.iloc[:, 0]

                    plt.plot(x, y, label=alg)
                except FileNotFoundError:
                    print(f"File not found: {file_name}")
                    continue

            plt.title(f"Algorithm Performance (input size = {n}, change rate = {c})")
            plt.xlabel("Time")
            plt.ylabel("Average Value")
            plt.legend()
            plt.grid(True)
            plt.tight_layout()

            # Save each plot
            plot_file = f"experiments/results/experiment3/plots/plot-{n}-{c}.png"
            plt.savefig(plot_file)
            plt.close()


def main():
    input_size = [20] # range(100, 50001, 100)
    algorithm = ["rep-insertion", "quick-rep-insertion", "rep-quick-rep-insertion-1", "rep-quick-rep-insertion-2"]
    config = ["sorted"]
    seed = range(0,3)
    probe_rate = [1]
    change_rate = [1, 2, 10, 20]

    store_average(input_size, algorithm, config, seed, probe_rate, change_rate)
    plot_figures(input_size, algorithm, change_rate)

main()