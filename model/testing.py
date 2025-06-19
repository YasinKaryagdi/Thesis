import sys
import os

# Add the parent directory of the parent directory, so the directory Thesis, to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from model.statistics import Stats
import timeit

def main():
    real = []
    for x in range(4999, -1, -1):
        real.append(x)

    approx = []
    for x in range(0, 5000):
        approx.append(x)

    assert len(real) == len(approx)
    assert real[-1] == approx[0]
    assert real[0] == approx[-1]


    stats = Stats()
    
    t1 = timeit.default_timer()
    stats.add_curr_distance(real, approx)
    t2 = timeit.default_timer()
    list_time = t2 - t1

    t3 = timeit.default_timer()
    stats.add_curr_distance_dict(real, approx)
    t4 = timeit.default_timer()
    dict_time = t4 - t3

    assert stats.distances[0] == stats.distances[1]
    print(f"for n = 5000")
    print(f"list took = {list_time}")
    print(f"dit took = {dict_time}")
    print(f"difference is {list_time - dict_time}")
    print(f"answer they got was: {stats.distances[0]}")
    # results was about 0.7 seconds faster with dict, so about 40x faster
    print("\n")

    real = []
    for x in range(9999, -1, -1):
        real.append(x)

    approx = []
    for x in range(0, 10000):
        approx.append(x)

    assert len(real) == len(approx)
    assert real[-1] == approx[0]
    assert real[0] == approx[-1]


    stats = Stats()
    
    t1 = timeit.default_timer()
    stats.add_curr_distance(real, approx)
    t2 = timeit.default_timer()
    list_time = t2 - t1

    t3 = timeit.default_timer()
    stats.add_curr_distance_dict(real, approx)
    t4 = timeit.default_timer()
    dict_time = t4 - t3

    assert stats.distances[0] == stats.distances[1]
    print(f"for n = 10000")
    print(f"list took = {list_time}")
    print(f"dict took = {dict_time}")
    print(f"difference is {list_time - dict_time}")
    print(f"answer they got was: {stats.distances[0]}")
    # results was about 3 seconds faster with dict, so about 60x faster
    

main()