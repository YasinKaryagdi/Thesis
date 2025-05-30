# Used for tracking the time by means of storing the probes, 
# and for tracking the Kendall tau distances at certain time steps
class Stats:
    probes: list[list[int]]
    distances: list[int]
    input_size: int

    def __init__(self, n):
        self.distances = []
        self.probes = []
        self.input_size = n

    def add_probe(self, i, j):
        self.probes.append([i, j])

    # calculates the K error given two lists x and yAdd commentMore actions
    def calc_kendall_tau(self, x, y):
        discordant_pairs = 0

        for i in range(0, len(x)):
            for j in range(i + 1, len(x)):
                a = x[i] - x[j]
                b = y[i] - y[j]

                # if discordant (different signs)
                if (a * b < 0):
                    discordant_pairs += 1

        return discordant_pairs

    def add_curr_distance(self, real, approx):
        distance = self.calc_kendall_tau(real, approx)
        self.distances.append(distance)