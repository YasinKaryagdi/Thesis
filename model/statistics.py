# Used for tracking the time by means of storing the probes,
# and for tracking the Kendall tau distances at certain time steps,
# which depends on the sampling rate
class Stats:
    probes: list[list[int]]
    distances: list[int]
    
    def __init__(self, n):
        self.distances = []
        self.distances2 = []
        self.probes = []
        self.mistakes_real= []
        self.mistakes_approx = []

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


    # Allows comparison based on the index of int i and j in the real list, 
    # so based on their positions in the real
    def probe(self, real: list[int], i: int, j: int):
        index_i = real.index(i)
        index_j = real.index(j)
        return index_i < index_j

    def merge_sort(self, real: list[int], temp: list[int]):
        if len(temp) <= 1:
            return 0
        
        # essentially splitting the list like mozes split the seas
        left_size = len(temp) // 2
        right_size = len(temp) - left_size


        left = []
        for i in range(0, left_size):
            left.append(temp[i])

        right = []
        for i in range(left_size, len(temp)):
            right.append(temp[i])

        left_invs = self.merge_sort(real, left)
        right_invs = self.merge_sort(real, right)
        between_invs = 0
        i = 0
        j = 0 
        k = 0
        while i < left_size and j < right_size:

            if self.probe(real, left[i], right[j]):
                temp[k] = left[i]
                k += 1
                i += 1
            else:
                temp[k] = right[j]

                # Something on the right being smaller means that there are a certain number
                # of inversions, namely (left_size - i), where i is the index of the current element on the left,
                # so we essentially have that this right side element agrees with i elements but is discordant with the rest of the left array
                between_invs += (left_size - i)
                print(f"discordant element: {right[j]}, putting it in spot {k}, adding {(left_size - i)}, total : {between_invs}")

                k += 1
                j += 1
            
        # Copy over the remaining elements in either left or right,
        # the while loop will fail for at least one
        while i < left_size:
            temp[k] = left[i]
            k += 1
            i += 1

        while j < right_size:
            temp[k] = right[j]
            k += 1
            j += 1
        

        return left_invs + right_invs + between_invs


    # Adds the current distance between the real order and our approximation
    def add_curr_distance(self, real: list[int], approx: list[int]):
        distance = self.calc_kendall_tau(real, approx)
        self.distances.append(distance)

        temp = approx.copy()
        distance2 = self.merge_sort(real, temp)
        self.distances2.append(distance2)

        if distance != distance2:
            self.mistakes_approx.append(approx)
            
            self.mistakes_real.append(real)
            print(real)
            print(approx)
            print(distance2)
            print(f"went bad ^ \n")
            print(f"\n")
        else:
            print(f"went well \n")


    # Adds the current distance between the real order and our approximation
    def add_curr_distance_merge(self, real: list[int], approx: list[int]):
        temp = approx.copy()
        distance = self.merge_sort(real, temp)
        self.distances2.append(distance)