import json
import os
from constants import Database
from multiprocessing import cpu_count

from utils.filters import filter_beta_decayable, filter_beta_decayable_cfy
from calculation import summation
from parse.parse_full import export_cfy_filename_template, export_filename_template

# element_name = 'u238'
# element_name = 'pu239'
element_name = 'u235'
WITH_GAMMA = True
WITH_FERMI = False

database_name = Database.NAME_JENDL.value
current_dir = os.path.dirname(__file__)
threads = cpu_count()
export_filename = os.path.join(current_dir, "plots", element_name + "time{}.dat")

start_energy = 0.0  # MeV
finish_energy = 12.0  # MeV

points = 500

h = (finish_energy - start_energy) / points

times = {
    "1s": 1,
    "1minute": 60,
    "1hour": 3600,
    "24hours": 24 * 3600,
    "1week": 7 * 24 * 3600,
    "1year": 1 * 365 * 24 * 3600
}


def load_independent_base_data():
    filename = export_filename_template.format(element_name, database_name)
    loadfilename = os.path.join(current_dir, "parse", "dumps", filename)
    file = open(loadfilename, "r")
    data = json.load(file)
    file.close()
    # print("Base fission elements number:{}".format(len(data)))
    # data = filter_beta_decayable(data)
    # print("Beta decayable branches number:{}".format(len(data)))
    summation.populate_lmdb(data)
    return data


def load_cfy_data():
    filename = export_cfy_filename_template.format(element_name, database_name)
    loadfilename = os.path.join(current_dir, "parse", "dumps", filename)
    file = open(loadfilename, "r")
    data = json.load(file)
    file.close()
    # print("Base cfy:{}".format(len(data)))
    #data = filter_beta_decayable_cfy(data)
    # print("Filter cfy:{}".format(len(data)))
    # summation.populate_lmdb_cfy(data)
    return data