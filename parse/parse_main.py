from constants import Database
import os
from parse.endf_yields_loader import get_independent_yields, get_cumulative_yields
from parse.jendl_wesite_parser import get_data_by_element
import utils.filters as filters
import json
import subprocess
import time


def get_yields_data(str_element, database):
    elements = get_cumulative_yields(str_element, database)
    return elements


element_name = 'u235'
database_name = Database.NAME_JENDL.value

# dump_filenames = {
#     "yields": "{}_{}_yields.json",
#     "yields_filtered": "{}_{}_yields_filtered.json",
#     "chains": "{}_{}_yields_filtered_math.json",
#     "final": "{}_{}_final.json"
# }

dump_filenames = {
    "yields": "{}_{}_cfy.json",
    "yields_filtered": "{}_{}_cfy_filtered.json",
    "chains": "{}_{}_cfy_filtered_math.json",
    "final": "{}_{}_final.json"
}


def create_filepath(template, element_name, database_name):
    dir = os.path.dirname(__file__)
    fn = template.format(element_name, database_name)
    path = os.path.join(dir, "dumps", fn)
    return path


def export_json(filename, data):
    path = create_filepath(filename, element_name, database_name)
    with open(path, "w") as file:
        json.dump(data, file, ensure_ascii=False)
    return path


def load_json(filename):
    path = create_filepath(filename, element_name, database_name)
    with open(path, "r") as file:
        data = json.loads(file.read().replace(".e-", "e-"))
    return data


elements = get_yields_data(element_name, Database.JENDL)
print("Length before: {}".format(len(elements)))
elements = [el for el in elements if el['fps'] != 1.0]
print("Length after removing fps not 1: {}".format(len(elements)))
elements = filters.filter_by_yields(elements, 1E-10)
elements = filters.filter_light_elements(elements, 15)
print("Length after: {}".format(len(elements)))


i = 1
for element in elements:
    try:
        data = get_data_by_element(element["z"], element["a"])
    except ImportError:
        elements.remove(element)
        continue
    time.sleep(1)
    for key in data.keys():
        element[key] = data[key]
    print("{}/{}, {}".format(i, len(elements), element))
    i += 1

elements = filters.filter_beta_decayable(elements)

export_json(dump_filenames['yields_filtered'], elements)

elements = load_json(dump_filenames['yields_filtered'])

# to_remove = [(30, 84), (31, 87), (35, 98), (51, 140)]

# for el in elements:
#     for r in to_remove:
#         if el['a'] == r[1] and el['z'] == r[0]:
#             elements.remove(el)

export_json(dump_filenames['yields_filtered'], elements)

export_json(dump_filenames['final'], elements)

# path = create_filepath(dump_filenames['yields_filtered'], element_name, database_name)

# subprocess.check_call(['/usr/local/bin/MathematicaScript', '-script', './script.m', path])
# subprocess.check_call(['/home/ace/apps/Mathematica_10/MathematicaScript', '-script', './script.m', path])


# elements_chains = load_json(dump_filenames['chains'])

# elements_chains = load_json(dump_filenames['yields_filtered'])
#
#
# i = 1
# for el in elements_chains:
#     print("Now base element: {}/{}".format(i, len(elements_chains)))
#     if 'chain' in el:
#         for child in el['chain']:
#             child_data = get_data_by_element(child['z'], child['a'])
#             for key in child_data.keys():
#                 child[key] = child_data[key]
#             print(child)
#             time.sleep(0.5)
#     i += 1
#
# export_json(dump_filenames['final'], elements_chains)


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
