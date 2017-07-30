import json
import configparser
from multiprocessing import cpu_count

import calculation.populators as populators
from calculation.filters import filter_beta_decayable, filter_beta_decayable_cfy, filter_by_yields
import api.resources_access as resources


config = configparser.ConfigParser()
config.read(resources.get_settings_filepath())

config_spectrum = config['spectrum']
main_nuclide_name = config_spectrum['main_nuclide_name']
with_gamma = config_spectrum.getboolean('with_gamma')
database_name = config_spectrum['database']
independent_yields_low_border = float(config_spectrum['independent_yields_low_border'])
threads = cpu_count()
start_energy = float(config_spectrum['start_energy'])  # MeV
finish_energy = float(config_spectrum['finish_energy'])  # MeV
points = int(config_spectrum['points'])

times = {
    "1s": 1,
    "1minute": 60,
    "1hour": 3600,
    "24hours": 24 * 3600,
    "1week": 7 * 24 * 3600,
    "1year": 1 * 365 * 24 * 3600
}
WITH_FERMI = False  # Not working

time_dep_config = config['time_dependence']
start_time = float(time_dep_config['start_time'])
end_time = float(time_dep_config['end_time'])
dt = float(time_dep_config['dt'])


def load_independent_base_data():
    loadfilename = resources.get_independent_base_data_filepath(main_nuclide_name, database_name)
    print(loadfilename)
    file = open(loadfilename, "r")
    data = json.load(file)
    file.close()
    print("Base fission elements number:{}".format(len(data)))
    data = filter_beta_decayable(data)
    data = filter_by_yields(data, independent_yields_low_border)
    print("Beta decayable branches number:{}".format(len(data)))
    populators.populate_lambda(data)
    return data


def load_cfy_data():
    loadfilename = resources.get_cfy_data_filepath(main_nuclide_name, database_name)
    file = open(loadfilename, "r")
    data = json.load(file)
    file.close()
    # print("Base cfy:{}".format(len(data)))
    data = filter_beta_decayable_cfy(data)
    # print("Filter cfy:{}".format(len(data)))
    populators.populate_lambda_cfy(data)
    return data
