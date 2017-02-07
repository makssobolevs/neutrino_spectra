from constants import Database
import os
from parse.endf_yields_loader import get_base_yields
from parse.jendl_wesite_parser import get_data_by_element
import utils.filters as filters
import json


def get_yields_data(str_element, database):
    elements = get_base_yields(str_element, database)
    return elements


element_name = 'pu239'

dir = os.path.dirname(__file__)
export_filename = os.path.join(dir, 'dumps', 'base_{}.json')
export_filename = str(export_filename).format(element_name)


elements = get_yields_data(element_name, Database.JENDL)

print("Length before: {}".format(len(elements)))
elements = filters.filter_by_yields(elements, 1E-10)
elements = filters.filter_light_elements(elements, 15)
print("Length after: {}".format(len(elements)))


i = 1
for element in elements:
    data = get_data_by_element(element["z"], element["a"])
    element['symbol'] = data['symbol']
    element['hl'] = data['hl']
    element['qmax'] = data['qmax']
    print("{}/{}".format(i, len(elements)))
    i += 1


with open(export_filename, "w") as file:
    json.dump(elements, file, ensure_ascii=False)



# import matplotlib.pyplot as plt
# import numpy as np
#
# k = []
#
#
# a = list(set([el['a'] for el in elements]))
#
# for e in a:
#     maxy = max([el['yi'] for el in elements if el['a'] == e])
#     k.append(maxy)
#
#
# y = [el['yi'] for el in elements]
#
# print(a)
#
# plt.semilogy(a, k, 'ro')
# plt.xlabel("atomic number")
# plt.ylabel("yield")
#
#
# # print([el for el in elements if el['a'] < 20])
#
# plt.show()
