# Used for tracking the time by means of storing the probes,
# and for tracking the Kendall tau distances at certain time steps,
# which depends on the sampling rate
class Stats:
    probes: list[list[int]]
    distances: list[int]
    
    def __init__(self):
        self.distances = []
        self.probes = []

    # Adds the current probe and the probes indexes to the list
    def add_probe(self, i, j):
        self.probes.append([i, j])


    # Allows comparison based on the index of int i and j in the real list, 
    # so based on their positions in the real
    def probe(self, real: dict, i: int, j: int):
        index_i = real.get(i)
        index_j = real.get(j)
        return index_i < index_j


    def merge_sort(self, real: dict, temp: list[int]):
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
        temp = approx.copy()
        real_dict = dict(zip(real, range(0, len(real))))

        distance = self.merge_sort(real_dict, temp)
        self.distances.append(distance)