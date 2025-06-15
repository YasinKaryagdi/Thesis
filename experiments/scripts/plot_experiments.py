import sys
import os

# Add the parent directory of the parent directory, so the directory Thesis, to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import math
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset


def store_average(input_size, algorithm, config, seed, change_rate, experiment_num):
    for n in input_size:
        for c in change_rate:
            for alg in algorithm:
                for con in config:
                    file_name_avg = f"experiments/results/experiment{experiment_num}/avg/{alg}-{n}-{c}.xlsx"

                    # Check if file already exists
                    if os.path.exists(file_name_avg):
                        print(f"Skipped (already exists): {file_name_avg}")

                    else:
                        print(f"Working on: {file_name_avg}")
                        run_file_names = []
                        for i in seed:

                            file_name = f"experiments/results/experiment{experiment_num}/runs/{alg}-{n}-{c}-{i}.xlsx"
                            run_file_names.append(file_name)

                        time_limit = int(math.pow(n, 2))
                        sample_rate = n / 20
                        results = []
                        for files in run_file_names:
                            # Print statement
                            print(f"Current file: {files}")
                            temp = pd.read_excel(files, index_col=0, engine="openpyxl")
                            results.append(temp)
                        mean_results = pd.concat(results).groupby(level=0).mean()
                        mean_results = mean_results[:time_limit]

                        mean_results["temp"] = mean_results.index * sample_rate
                        mean_results.set_index("temp")

                        # writing to Excel
                        file_name = f"experiments/results/experiment{experiment_num}/avg/{alg}-{n}-{c}.xlsx"
                        datatoexcel = pd.ExcelWriter(path=file_name)
                        mean_results.to_excel(datatoexcel)
                        datatoexcel.close()


def plot_figures(input_size, algorithm, change_rate, experiment_num):
    for n in input_size:
        time_limit = int(math.pow(n, 2))
        for c in change_rate:
            plt.figure(figsize=(6, 4))
            sample_rate = n / 20
            ax = plt.gca()
            ax.ticklabel_format(style="plain")

            for alg in algorithm:
                file_name = f"experiments/results/experiment{experiment_num}/avg/{alg}-{n}-{c}.xlsx"
                try:
                    df = pd.read_excel(file_name, index_col=0, engine="openpyxl")

                    if "temp" in df.columns:
                        x = df["temp"]
                        y = df.iloc[:, 0]
                    else:
                        x = df.index * sample_rate
                        y = df.iloc[:, 0]

                    ax.plot(x, y, label=alg)
                except FileNotFoundError:
                    print(f"File not found: {file_name}")
                    continue

            if experiment_num == 1:
                ax.set_title(f"Algorithm Behavior (input size = {n}, change rate = {c})")
                ax.set_xlabel("Number of Comparisons")
                ax.set_ylabel("Average Kendall-Tau Distance")
                ax.legend(loc="upper right")
            else:
                ax.legend(loc="upper left")

                if not (experiment_num == 3 and c == 1):
                    axins = zoomed_inset_axes(ax, zoom=6, loc="lower right")
                    inset_start = int(time_limit * 0.9)
                    inset_end = int(time_limit * 0.99)
                    y_values = []

                    for alg in algorithm:
                        file_name = f"experiments/results/experiment{experiment_num}/avg/{alg}-{n}-{c}.xlsx"
                        try:
                            df = pd.read_excel(
                                file_name, index_col=0, engine="openpyxl"
                            )

                            if "temp" in df.columns:
                                x = df["temp"]
                                y = df.iloc[:, 0]
                            else:
                                x = df.index * sample_rate
                                y = df.iloc[:, 0]

                            # Limit data to inset x-range
                            mask = (x >= inset_start) & (x <= inset_end)
                            axins.plot(x[mask], y[mask], label=alg)
                            y_values.extend(y[mask].values)
                        except FileNotFoundError:
                            continue

                    axins.set_xlim(inset_start, inset_end)

                    if y_values:
                        y_min = min(y_values)
                        y_max = max(y_values)
                        if experiment_num == 1 or experiment_num == 5:
                            padding = (y_max - y_min) * 1
                        else:
                            padding = (y_max - y_min) * 0.1
                        axins.set_ylim(y_min - padding, y_max + padding)

                    axins.grid(True)
                    axins.axes.get_xaxis().set_visible(False)
                    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")

            ax.grid(True)
            ax.set_xlim(0, time_limit)
            plot_file = f"experiments/results/experiment{experiment_num}/plots/plot-{n}-{c}.pdf"
            plt.savefig(plot_file, bbox_inches="tight", format="pdf")
            plt.close()


def plot_end_point(input_size, algorithm, change_rate, experiment_num):
    for n in input_size:
        time_limit = int(math.pow(n, 2))
        for c in change_rate:
            plt.figure(figsize=(6, 4))
            sample_rate = n / 20
            ax = plt.gca()
            ax.ticklabel_format(style="plain")

            inset_start = int(time_limit * 0.9)
            inset_end = time_limit
            y_values = []

            for alg in algorithm:
                file_name = f"experiments/results/experiment{experiment_num}/avg/{alg}-{n}-{c}.xlsx"
                try:
                    df = pd.read_excel(file_name, index_col=0, engine="openpyxl")

                    if "temp" in df.columns:
                        x = df["temp"]
                        y = df.iloc[:, 0]
                    else:
                        x = df.index * sample_rate
                        y = df.iloc[:, 0]

                    # Limit data to inset x-range
                    mask = (x >= inset_start) & (x <= inset_end)
                    ax.plot(x[mask], y[mask], label=alg)
                    y_values.extend(y[mask].values)
                except FileNotFoundError:
                    print(f"File not found: {file_name}")
                    continue

            ax.set_xlim(inset_start, inset_end)

            # Set dynamic y-axis limits based on data range
            if y_values:
                y_min = min(y_values)
                y_max = max(y_values)
                padding = (y_max - y_min) * 0.1 if y_max > y_min else 0.05
                ax.set_ylim(y_min - padding, y_max + padding)

            ax.set_title(f"Zoomed Endpoint (n = {n}, change rate = {c})")
            ax.set_xlabel("Number of Comparisons")
            ax.set_ylabel("Average Kendall-Tau Distance")
            ax.legend(loc="upper left")
            ax.grid(True)

            plot_file = f"experiments/results/experiment{experiment_num}/plots/endpoint-{n}-{c}.pdf"
            plt.savefig(plot_file, bbox_inches="tight", format="pdf")
            plt.close()


def main():
    input_size = [1000]
    algorithm = ["rep-quick", "block-10", "rep-insertion", "quick-rep-insertion", "rep-quick-rep-insertion-1"]
    config = ["reverse-sorted"]
    seed = range(0, 100)
    change_rate = [1]
    experiment_num = 1
    store_average(input_size, algorithm, config, seed, change_rate, experiment_num)
    plot_figures(input_size, algorithm, change_rate, experiment_num)
    plot_end_point(input_size, algorithm, change_rate, experiment_num)

    input_size = [100, 500, 1000]
    algorithm = ["block-1", "block-5", "block-10", "block-20", "block-40"]
    config = ["sorted"]
    seed = range(0, 100)
    change_rate = [1, 5, 10, 20]
    experiment_num = 2
    store_average(input_size, algorithm, config, seed, change_rate, experiment_num)
    plot_figures(input_size, algorithm, change_rate, experiment_num)

    input_size = [100, 500, 1000]
    algorithm = [
        "rep-insertion",
        "quick-rep-insertion",
        "rep-quick-rep-insertion-1",
        "rep-quick-rep-insertion-2",
        "rep-quick-rep-insertion-5",
        "rep-quick-rep-insertion-10"
    ]
    config = ["sorted"]
    seed = range(0, 100)
    change_rate = [1, 5, 10, 20, 250]
    experiment_num = 3
    store_average(input_size, algorithm, config, seed, change_rate, experiment_num)
    plot_figures(input_size, algorithm, change_rate, experiment_num)


    input_size = [100, 500, 1000, 5000, 10000]
    algorithm = [
        "rep-quick", "block-10", "quick-rep-insertion", "rep-insertion"
    ]
    config = ["reverse-sorted"]
    seed = range(0, 100)
    change_rate = [1, 2, 10]
    experiment_num = 4
    store_average(input_size, algorithm, config, seed, change_rate, experiment_num)
    plot_figures(input_size, algorithm, change_rate, experiment_num)

    input_size = [100, 500, 1000, 5000, 10000]
    algorithm = ["block-1", "block-5", "block-10", "block-20", "block-40"]
    config = ["reverse-sorted"]
    seed = range(0, 100)
    change_rate = [1, 5, 10, 20]
    experiment_num = 5
    store_average(input_size, algorithm, config, seed, change_rate, experiment_num)
    plot_figures(input_size, algorithm, change_rate, experiment_num)

    input_size = [100, 500, 1000, 5000, 10000]
    algorithm = [
        "rep-insertion",
        "quick-rep-insertion",
        "rep-quick-rep-insertion-1",
        "rep-quick-rep-insertion-2",
        "rep-quick-rep-insertion-5",
        "rep-quick-rep-insertion-10"
    ]
    config = ["reverse-sorted"]
    seed = range(0, 100)
    change_rate = [1, 5, 10, 20]
    experiment_num = 6
    store_average(input_size, algorithm, config, seed, change_rate, experiment_num)
    plot_figures(input_size, algorithm, change_rate, experiment_num)

main()
