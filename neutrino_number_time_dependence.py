import numpy as np
import setup
import math
import calculation.summation as summation
import os


class NeutrinoNumberCaller(object):

    def __init__(self, time):
        self.time = time

    def __call__(self, element):
        return summation.get_neutrino_number_for_time(element, self.time)


def export_neutrino_number_time_dependence(x_all, y_all):
    current_dir = os.path.dirname(__file__)
    filepath = os.path.join(current_dir, "plots",
                            export_filename_template.format(setup.element_name))
    with open(filepath, 'w') as file:
        for k in range(x_all.shape[0]):
            file.write("{} {}\n".format(x_all[k], y_all[k]))


def get_neutrino_number_for_time(ind_data, time):
    list_of_numbers = list(map(NeutrinoNumberCaller(time), ind_data))
    return np.sum(list_of_numbers)



export_filename_template = "{}_neutrino_number.dat"

start_time = 0.0
end_time = math.log(10000000000.0)
dt = 0.1

log_times = np.arange(start_time, end_time, dt)


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

