import json
import os
import math
from scipy.optimize import minimize
import numpy as np

from utils.filters import filter_beta_decayable
from calculation.summation import get_spectrum_value

# element_name = 'pu239'
element_name = 'u235'

dir = os.path.dirname(__file__)
loadfilename = os.path.join(dir, "parse", "dumps", "final_{}.json".format(element_name))
exportfilename = os.path.join(dir, "plots", element_name + "time{}.dat")

export_max_moving = os.path.join(dir, "plots", "maximum_time.dat")

file = open(loadfilename, "r")

data = json.load(file)
file.close()

data = filter_beta_decayable(data)

start_energy = 0.0  # MeV
finish_energy = 12.0  # MeV

points = 500

h = (finish_energy - start_energy) / points

# time = 1  # Second
times = {"1s": 1,
         "1minute": 60,
         "1hour": 3600,
         "24hours": 24 * 3600,
         "1week": 7 * 24 * 3600,
         "1year": 365 * 24 * 3600
         }

min_x0 = 10  # MeV


def get_maximum(data, time):

    def minimize_f(x):
        return -get_spectrum_value(data, x[0], time)

    max = minimize(minimize_f, min_x0, method='nelder-mead')
    return max.x[0]

# # start_time = math.log(1)
# # middle_time = math.log(100)
# # finish_time = math.log(times["1year"])
# start_time = 1
# middle_time = 100
# finish_time = times["1year"]
#
# dt1 = (middle_time - start_time) / 200
# dt2 = (finish_time - middle_time) / 200
#
# t1 = np.arange(start_time, middle_time, dt1)
# t2 = np.arange(middle_time, finish_time, dt2)
# t = np.concatenate((t1, t2))
#
# with open(export_max_moving, "w") as file:
#     for ti in t:
#         # time = math.exp(ti)
#         time = ti
#         max = get_maximum(data, time)
#         file.write("{}  {}\n".format(max, time))
#         print("Time:{}, max:{}".format(time, max))

for tk in times.keys():
    time = times[tk]
    export_file = open(exportfilename.format(tk), "w")
    for p in range(points):
        energy = start_energy + h * p
        value = get_spectrum_value(data, energy, time)
        print("energy:{}, value:{}".format(energy, value))
        export_file.write("{} {}\n".format(energy, value))

    export_file.close()

