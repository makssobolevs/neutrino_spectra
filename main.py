import time as tt
from functools import reduce
from multiprocessing import Pool
from typing import List, Dict

from calculation.summation import get_spectrum_value_for_branch, get_spectrum_value_for_element_cfy
from config import setup as setup


def init_energy_cells():
    cells = []
    d_e = (setup.finish_energy - setup.start_energy) / setup.points
    for i in range(setup.points):
        energy = setup.start_energy + d_e * i
        d = {"e": energy, "s": 0}
        cells.append(d)
    return cells


def export_spectrum(spectrum, time_str):
    import api.resources_access as resources

    postfix = "time" + time_str
    if setup.with_gamma:
        postfix += "_gamma"
    export_filepath = resources.get_dat_export_filepath(setup.main_nuclide_name, postfix)
    with open(export_filepath, 'w') as file:
        for c in spectrum:
            file.write("{} {}\n".format(c['e'], c['s']))


def add_element_spectrum_value(full_value, element_value):
    for i in range(len(full_value)):
        full_value[i]['s'] += element_value[i]['s']
    return full_value


def calculate_individual_spectrum(element, time):
    element_spectrum_values = init_energy_cells()
    for cell in element_spectrum_values:
        energy = cell['e']
        cell['s'] = get_spectrum_value_for_branch(element, energy, time)
    return element_spectrum_values


def calculate_individual_spectrum_cfy(element: Dict):
    element_spectrum_values = init_energy_cells()
    for cell in element_spectrum_values:
        energy = cell['e']
        cell['s'] = get_spectrum_value_for_element_cfy(element, energy)
    return element_spectrum_values


class TimeSpectrumCaller(object):

    def __init__(self, time):
        self.time = time

    def __call__(self, element):
        return calculate_individual_spectrum(element, self.time)


def calculate_spectrum_for_time(data: List[Dict], time: int, time_str: str) -> None:
    full_spectrum_values = init_energy_cells()
    start = tt.time()

    spectra_list = Pool(setup.threads).imap_unordered(TimeSpectrumCaller(time), data)
    # spectra_list = list(map(calculate_individual_spectrum, base_data))
    result = reduce(add_element_spectrum_value, spectra_list, full_spectrum_values)
    end = tt.time()
    print(end - start)
    export_spectrum(result, time_str)


def calculate_spectrum_for_cfy(data: List[Dict]):
    full_spectrum_values = init_energy_cells()
    spectra_list = Pool(setup.threads).imap_unordered(calculate_individual_spectrum_cfy, data)
    result = reduce(add_element_spectrum_value, spectra_list, full_spectrum_values)
    export_spectrum(result, "CFY")


if __name__ == "__main__":
    base_data = setup.load_independent_base_data()
    cfy_data = setup.load_cfy_data()
    for tk in setup.times.keys():
        t = setup.times[tk]
        print("Calculating {} for time {}".format(setup.main_nuclide_name, tk))
        calculate_spectrum_for_time(base_data, t, tk)
    print("Calculation for CFY")
    calculate_spectrum_for_cfy(cfy_data)
