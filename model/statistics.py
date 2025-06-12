# Used for tracking the time by means of storing the probes,
# and for tracking the Kendall tau distances at certain time steps,
# which depends on the sampling rate
class Stats:
    probes: list[list[int]]
    distances: list[int]

    def __init__(self, n):
        self.distances = []
        self.probes = []

    # Adds the current probe and the probes indexes to the list
    def add_probe(self, i, j):
        self.probes.append([i, j])

    # Calculates the Kendall tau distance between two lists x and y
    def calc_kendall_tau(self, x, y):
        discordant_pairs = 0

        for i in range(0, len(x)):
            for j in range(i + 1, len(x)):
                a = x[i] - x[j]
                b = y[i] - y[j]

                # If discordant (different signs)
                if a * b < 0:
                    discordant_pairs += 1

        return discordant_pairs

    # Adds the current distance between the real order and our approximation
    def add_curr_distance(self, real, approx):
        distance = self.calc_kendall_tau(real, approx)
        self.distances.append(distance)
