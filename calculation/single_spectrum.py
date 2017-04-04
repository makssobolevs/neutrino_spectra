import calculation.summation as summation
from main import base_data
from main import points
from main import start_energy
from main import h
import matplotlib.pyplot as plt

el = base_data[234]

print(el)

for_plot = []


summation.distribution(el, 2)

time = 24 * 3600

value_list = []
energy_list = []

for p in range(points):
    energy = start_energy + h * p
    value = summation.get_spectrum_value([el], energy, time)
    print("energy:{}, value:{}".format(energy, value))
    energy_list.append(energy)
    value_list.append(value)


plt.plot(energy_list, value_list)

plt.show()
