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
                        
                        if experiment_num == 1:
                            sample_rate = n / 20
                        else:
                            sample_rate = n / 10

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


def load_xy_from_excel(file_name, sample_rate):
    df = pd.read_excel(file_name, index_col=0, engine="openpyxl")
    if "temp" in df.columns:
        x = df["temp"]
        y = df.iloc[:, 0]
    else:
        x = df.index * sample_rate
        y = df.iloc[:, 0]
    return x, y


def plot_algorithm_line(ax, x, y, alg, style=None):
    if style:
        line, = ax.plot(x, y, label=alg, **style)
    else:
        line, = ax.plot(x, y, label=alg)
    return line


def plot_figures(input_size, algorithm, change_rate, experiment_num):
    for n in input_size:
        time_limit = int(math.pow(n, 2))
        for c in change_rate:
            plt.figure(figsize=(6, 4))
            if experiment_num == 1:
                sample_rate = n / 20
            else:
                sample_rate = n / 10

            ax = plt.gca()
            ax.ticklabel_format(style="plain")
            lines = []
            labels = []
            for alg in algorithm:
                file_name = f"experiments/results/experiment{experiment_num}/avg/{alg}-{n}-{c}.xlsx"
                try:
                    x, y = load_xy_from_excel(file_name, sample_rate)
                    line = plot_algorithm_line(ax, x, y, alg)
                    lines.append(line)
                    labels.append(alg)
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

            ax.grid(True)
            ax.set_xlim(0, time_limit)
            plot_file = f"experiments/results/experiment{experiment_num}/plots/plot-{n}-{c}.pdf"
            plt.savefig(plot_file, bbox_inches="tight", format="pdf")
            # Save legend as a separate PDF
            save_legend_pdf(lines, labels, experiment_num)
            plt.close()


def plot_end_point(input_size, algorithm, change_rate, experiment_num):
    for n in input_size:
        time_limit = int(math.pow(n, 2))
        for c in change_rate:
            # since the algorithm reach the steady behavior we are only interested,
            # in what happens at the end
            if c == 250:
                amount_of_precentage = 0.4
            else:
                if n == 100:
                    amount_of_precentage = 0.4
                elif n == 500:
                    amount_of_precentage = 0.1
                # FIXME:might cause issues in case the last thing is not 1000 but something else
                else:
                    amount_of_precentage = 0.05

            plt.figure(figsize=(6, 4))
            if experiment_num == 1:
                sample_rate = n / 20
            else:
                sample_rate = n / 10
            ax = plt.gca()
            ax.ticklabel_format(style="plain")

            inset_start = int(time_limit * (1 - amount_of_precentage))
            inset_end = time_limit
            y_values = []
            lines = []
            labels = []
            for alg in algorithm:
                file_name = f"experiments/results/experiment{experiment_num}/avg/{alg}-{n}-{c}.xlsx"
                try:
                    x, y = load_xy_from_excel(file_name, sample_rate)
                    # Limit data to inset x-range
                    mask = (x >= inset_start) & (x <= inset_end)
                    line = plot_algorithm_line(ax, x[mask], y[mask], alg)
                    lines.append(line)
                    labels.append(alg)
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
            if experiment_num == 1:
                ax.set_title(f"Zoomed Endpoint (n = {n}, change rate = {c})")
                ax.set_xlabel("Number of Comparisons")
                ax.set_ylabel("Average Kendall-Tau Distance")
                ax.legend().remove()
            else:
                ax.legend().remove()

            ax.grid(True)

            plot_file = f"experiments/results/experiment{experiment_num}/plots/endpoint-{n}-{c}.pdf"
            plt.savefig(plot_file, bbox_inches="tight", format="pdf")
            # Save legend as a separate PDF
            save_legend_pdf(lines, labels, experiment_num)
            plt.close()


def average_kendall_tau(input_size, algorithm, change_rate, experiment_num):
    for n in input_size:
        time_limit = int(math.pow(n, 2))
        avg_results = pd.DataFrame(index=algorithm, columns=change_rate)

        for c in change_rate:
            if c == 250:
                amount_of_percentage = 0.4
            elif experiment_num == 4:
                amount_of_percentage = 1
            else:
                if n == 100:
                    amount_of_percentage = 0.4
                elif n == 500:
                    amount_of_percentage = 0.1
                else:
                    amount_of_percentage = 0.05

            if experiment_num == 1:
                sample_rate = n / 20
            else:
                sample_rate = n / 10

            for alg in algorithm:
                file_name = f"experiments/results/experiment{experiment_num}/avg/{alg}-{n}-{c}.xlsx"
                try:
                    x, y = load_xy_from_excel(file_name, sample_rate)
                    x_min = x.min()
                    x_max = x.max()
                    inset_start = x_max - (x_max - x_min) * amount_of_percentage
                    inset_end = x_max

                    mask = (x >= inset_start) & (x <= inset_end)
                    y_avg = y[mask].mean()
                    avg_results.at[alg, c] = y_avg

                except FileNotFoundError:
                    print(f"File not found: {file_name}")
                    avg_results.at[alg, c] = None  # Or leave as NaN

        output_dir = f"experiments/results/experiment{experiment_num}/avg_tables"
        os.makedirs(output_dir, exist_ok=True)
        output_file = f"{output_dir}/average_kendall_tau_{n}.xlsx"
        avg_results.to_excel(output_file, engine="openpyxl")

# Save the legend as a separate PDF file
def save_legend_pdf(lines, labels, experiment_num):
    if lines:
        fig_legend = plt.figure(figsize=(6, 2))
        fig_legend.legend(lines, labels, loc='center', ncol=len(labels), frameon=False)
        legend_file = f"experiments/results/experiment{experiment_num}/plots/legend.pdf"
        fig_legend.savefig(legend_file, bbox_inches='tight', format='pdf')
        plt.close(fig_legend)


def plot_theoretical_bound_kendall_tau(input_sizes, algorithms, change_rates, experiment_num):
    # Define a color map and marker style for each algorithm
    markers = ['o', 's', '^', 'D']
    alg_styles = {}
    for i, alg in enumerate(algorithms):
        alg_styles[alg] = {
            'marker': markers[i]
        }
    
    for c in change_rates:
        plt.figure(figsize=(10, 6))
        for alg in algorithms:
            x_vals = []
            y_vals = []

            for n in input_sizes:
                file_path = f"experiments/results/experiment{experiment_num}/avg_tables/average_kendall_tau_{n}.xlsx"
                df = pd.read_excel(file_path, index_col=0, engine="openpyxl")
                y = df.at[alg, c]
                y = y / n
                x_vals.append(n)
                y_vals.append(y)

            if x_vals and y_vals:
                style = alg_styles[alg]
                plt.plot(x_vals, y_vals, label=alg, 
                         marker=style['marker'], linestyle='-')


        plt.xlabel("Input size (n)")
        plt.ylabel("Average Kendall tau distance/Input size (n)")
        plt.title(f"Validating Theoretical Bound for Change Rate {c}")
        plt.legend()
        plt.grid(True, which='both', ls='--', lw=0.5)
        plt.tight_layout()

        plot_file = f"experiments/results/experiment{experiment_num}/plots/plot{c}.pdf"
        plt.savefig(plot_file, bbox_inches="tight", format="pdf")



def main():
    input_size = [100, 1000]
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
    plot_end_point(input_size, algorithm, change_rate, experiment_num)
    average_kendall_tau(input_size, algorithm, change_rate, experiment_num)

    input_size = [100, 500, 1000]
    algorithm = [
        "rep-quick",
        "rep-insertion",
        "rep-quick-rep-insertion-1",
        "rep-quick-rep-insertion-2"
    ]
    config = ["sorted"]
    seed = range(0, 100)
    change_rate = [1, 5, 10, 20, 250]
    experiment_num = 3
    store_average(input_size, algorithm, config, seed, change_rate, experiment_num)
    plot_figures(input_size, algorithm, change_rate, experiment_num)
    plot_end_point(input_size, algorithm, change_rate, experiment_num)
    average_kendall_tau(input_size, algorithm, change_rate, experiment_num)


    input_size = []
    temp = [1000, 2000, 3000, 5000, 10000]
    for i in range(100, 1000, 100):
        input_size.append(i)
    
    for i in temp:
        input_size.append(i)

    algorithm = [
        "rep-quick", "block-10", "quick-rep-insertion", "rep-insertion"
    ]
    config = ["reverse-sorted"]
    seed = range(0, 30)
    change_rate = [1, 2, 10]
    experiment_num = 4
    store_average(input_size, algorithm, config, seed, change_rate, experiment_num)
    average_kendall_tau(input_size, algorithm, change_rate, experiment_num)
    plot_theoretical_bound_kendall_tau(input_size, algorithm, change_rate, experiment_num)

main()
