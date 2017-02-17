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

for tk in times.keys():
    time = times[tk]
    export_file = open(exportfilename.format(tk), "w")
    for p in range(points):
        energy = start_energy + h * p
        value = get_spectrum_value(data, energy, time)
        print("energy:{}, value:{}".format(energy, value))
        export_file.write("{} {}\n".format(energy, value))

    export_file.close()

