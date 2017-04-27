import json
import os
import math
from scipy.optimize import minimize
import numpy as np
from constants import Database

from utils.filters import filter_beta_decayable
from calculation.summation import get_spectrum_value, get_spectrum_for_cfy, populate_lmdb, get_ibd_cross_section

# element_name = 'u238'
# element_name = 'pu239'
element_name = 'u235'

database_name = Database.NAME_JENDL.value

current_dir = os.path.dirname(__file__)


def load_independent_base_data():
    filename = "{}_{}_final.json".format(element_name, database_name)
    loadfilename = os.path.join(current_dir, "parse", "dumps", filename)
    file = open(loadfilename, "r")
    data = json.load(file)
    file.close()
    # print("Base elements number:{}".format(len(data)))
    data = filter_beta_decayable(data)
    populate_lmdb(data)
    return data


def load_cfy_data():
    filename = "{}_{}_cfy_final.json".format(element_name, database_name)
    loadfilename = os.path.join(current_dir, "parse", "dumps", filename)
    file = open(loadfilename, "r")
    data = json.load(file)
    file.close()
    # print("Base elements number:{}".format(len(data)))
    data = filter_beta_decayable(data)

    populate_lmdb(data)
    return data

base_data = load_independent_base_data()
cfy_data = load_cfy_data()

exportfilename = os.path.join(current_dir, "plots", element_name + "time{}.dat")


start_energy = 0.0  # MeV
finish_energy = 12.0  # MeV

points = 500

h = (finish_energy - start_energy) / points

# time = 1  # Second
times = {
    "1s": 1,
    "1minute": 60,
    "1hour": 3600,
    "24hours": 24 * 3600,
    "1week": 7 * 24 * 3600,
    "1year": 1 * 365 * 24 * 3600
}

min_x0 = 10  # MeV


def get_maximum(data, time):

    def minimize_f(x):
        return -get_spectrum_value(data, x[0], time)

    max = minimize(minimize_f, min_x0, method='nelder-mead')
    return max.x[0]

if __name__ == "__main__":
    for tk in times.keys():
        print(tk)
        time = times[tk]
        export_file = open(exportfilename.format(tk), "w")
        for p in range(points):
            energy = start_energy + h * p
            value = get_spectrum_value(base_data, energy, time)
            print("energy:{}, value:{}".format(energy, value))
            export_file.write("{} {}\n".format(energy, value))

        export_file.close()

    export_file = open(exportfilename.format('CFY'), "w")
    for p in range(points):
        energy = start_energy + h * p
        value = get_spectrum_for_cfy(cfy_data, energy)
        print("energy:{}, value:{}".format(energy, value))
        export_file.write("{} {}\n".format(energy, value))

    export_file.close()

