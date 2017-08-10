import json
import os
from multiprocessing import pool

import calculation.filters as filters
import parse.endf_yields_loader as yields
import parse.ensdf_parser as ensdf
from constants import Database

scriptdir = os.path.dirname(__file__)
export_filename_template = "{}_{}_ensdf.json"
export_cfy_filename_template = "{}_{}_ensdf_cfy.json"


def map_yield_data(y):
    branch = ensdf.get_decay_branch(y['z'], y['a'], y['fps'])
    if len(branch) > 0:
        print("Ok")
    y.update({'branch': branch})
    return y


def map_cfy_data(cfy):
    data = ensdf.get_data_for_z_a(cfy['z'], cfy['a'], cfy['fps'])
    if data is not None and not data['isStable']:
        cfy.update({'nuclide': data})
    return cfy


def main_cumulative(element, database, export_filename):
    cfy_yields = yields.get_cumulative_yields(element, database)
    cfy_yields = filters.filter_light_nuclides(cfy_yields, 15)
    cfy_yields = filters.filter_by_yields(cfy_yields, 1E-10)

    data = pool.ThreadPool(4).imap_unordered(map_cfy_data, cfy_yields)

    with open(export_filename, 'w') as file:
        json.dump(list(data), file)


def main_independent(element, database, export_filename):
    yields_data = yields.get_independent_yields(element, database)

    yields_data = filters.filter_by_yields(yields_data, 1E-10)
    yields_data = filters.filter_light_nuclides(yields_data, 15)

    print(len(yields_data))
    print(yields_data[0])

    data = pool.ThreadPool(4).imap_unordered(map_yield_data, yields_data)
    # data = map(map_yield_data, yields_data)

    with open(export_filename, 'w') as file:
        json.dump(list(data), file)


def main():
    element = "u235"
    database = Database.JENDL
    database_name = Database.NAME_JENDL.value
    exportfilename = os.path.join(scriptdir, "dumps",  export_filename_template.format(element, database_name))
    exportcfyfilename = os.path.join(scriptdir, "dumps",  export_cfy_filename_template.format(element, database_name))
    main_independent(element, database, exportfilename)
    main_cumulative(element, database, exportcfyfilename)


if __name__ == '__main__':
    main()
    # data =ensdf.get_decay_branch(40, 100, 0.0)
    # print(data)
    # print(len(data))

