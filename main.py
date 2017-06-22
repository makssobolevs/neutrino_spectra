import setup as setup
from calculation.summation import get_spectrum_value_for_branch, get_spectrum_value_for_element_cfy

from functools import reduce
from multiprocessing import Pool
import time as tt


def init_energy_cells(points, start_energy, d_energy):
    cells = []
    for i in range(points):
        energy = start_energy + d_energy * i
        d = {"e": energy, "s": 0}
        cells.append(d)
    return cells


def export_spectrum(spectrum, time_str):
    postfix = time_str
    if setup.WITH_GAMMA:
        postfix += "_gamma"
    export_file = open(setup.get_export_filename().format(postfix), "w")
    for c in spectrum:
        export_file.write("{} {}\n".format(c['e'], c['s']))
    export_file.close()


def add_element_spectrum_value(full_value, element_value):
    for i in range(len(full_value)):
        full_value[i]['s'] += element_value[i]['s']
    return full_value


def calculate_individual_spectrum(element, time):
    element_spectrum_values = init_energy_cells(setup.points, setup.start_energy, setup.h)
    for cell in element_spectrum_values:
        energy = cell['e']
        cell['s'] = get_spectrum_value_for_branch(element, energy, time)
    return element_spectrum_values


def calculate_individual_spectrum_cfy(element):
    element_spectrum_values = init_energy_cells(setup.points, setup.start_energy, setup.h)
    for cell in element_spectrum_values:
        energy = cell['e']
        cell['s'] = get_spectrum_value_for_element_cfy(element, energy)
    return element_spectrum_values


class TimeSpectrum(object):

    def __init__(self, time):
        self.time = time

    def __call__(self, element):
        return calculate_individual_spectrum(element, self.time)


def calculate_spectrum_for_time(data, time, time_str):
    full_spectrum_values = init_energy_cells(setup.points, setup.start_energy, setup.h)
    start = tt.time()

    spectra_list = Pool(setup.threads).imap_unordered(TimeSpectrum(time), data)
    # spectra_list = list(map(calculate_individual_spectrum, base_data))
    result = reduce(add_element_spectrum_value, spectra_list, full_spectrum_values)
    end = tt.time()
    print(end - start)
    export_spectrum(result, time_str)


def calculate_spectrum_for_cfy(data):
    full_spectrum_values = init_energy_cells(setup.points, setup.start_energy, setup.h)
    spectra_list = Pool(setup.threads).imap_unordered(calculate_individual_spectrum_cfy, data)
    result = reduce(add_element_spectrum_value, spectra_list, full_spectrum_values)
    export_spectrum(result, "CFY")


if __name__ == "__main__":
    base_data = setup.load_independent_base_data()
    cfy_data = setup.load_cfy_data()
    for tk in setup.times.keys():
        t = setup.times[tk]
        print("Calculating {} for time {}".format(setup.element_name, tk))
        calculate_spectrum_for_time(base_data, t, tk)
    print("Calculation for CFY")
    calculate_spectrum_for_cfy(cfy_data)
