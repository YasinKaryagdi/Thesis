from runner import Runner
import math

input_size = 1000 # range(100, 50001, 100)
algorithm = ["rep-insertion", "quick-rep-insertion", "rep-quick-rep-insertion-1", "rep-quick-rep-insertion-2"]
config = ["reverse-sorted"]
seed = range(0,101)
probe_rate = [1]
change_rate = [1, 2, 10, 20]


for n in input_size:
    for alg in algorithm :
        for con in config:
            for p in probe_rate:
                for c in change_rate:
                    for i in seed:
                        time_limit = math.pow(n, 3)

                        # taking the same as what Besa et al. did
                        sample_rate = n / 20
                        file_name = "results/experiment3" + alg + "-"+ str(n) + "-" + str(c) + "-" + str(seed)
                        cur_run = Runner(i, p, c, alg, n, time_limit, sample_rate, con)
                        cur_run.run()
                        cur_run.store_results(file_name)
