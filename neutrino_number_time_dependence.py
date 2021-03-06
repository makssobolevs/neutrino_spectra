import math
import numpy as np

import calculation.summation as summation
from config import setup


class NeutrinoNumberCaller(object):

    def __init__(self, time):
        self.time = time

    def __call__(self, element):
        return summation.get_neutrino_number_for_time(element, self.time)


def export_neutrino_number_time_dependence(x_all, y_all):
    import api.resources_access as resources

    filepath = resources.get_dat_export_filepath(setup.main_nuclide_name, '_neutrino_number')
    with open(filepath, 'w') as file:
        for k in range(x_all.shape[0]):
            file.write("{} {}\n".format(x_all[k], y_all[k]))


def get_neutrino_number_for_time(ind_data, time):
    list_of_numbers = list(map(NeutrinoNumberCaller(time), ind_data))
    return np.sum(list_of_numbers)


log_times = np.arange(setup.start_time, math.log(setup.end_time), setup.dt)


if __name__ == '__main__':
    ind_data = setup.load_independent_base_data()
    neutrino_numbers = []
    i = 1
    for log_time in np.nditer(log_times):
        print("time {}/{}".format(i, log_times.shape[0]))
        i += 1
        real_time = math.exp(log_time)
        result = get_neutrino_number_for_time(ind_data, real_time)
        neutrino_numbers.append(result)
    times = np.exp(log_times)
    export_neutrino_number_time_dependence(times, neutrino_numbers)
    
    number_inf = get_neutrino_number_for_time(ind_data, float("inf"))
    print("Infinite time neutrino number:{}".format(number_inf))

