import parse.endf_yields_loader as yields
import parse.ensdf_parser as ensdf
from constants import Database
import utils.filters as filters
import json
import os

scriptdir = os.path.dirname(__file__)

element = "u235"
database = Database.JENDL
database_name = Database.NAME_JENDL.value

exportfilename = os.path.join(scriptdir, "dumps",  "{}_{}_ensdf.json".format(element, database_name))
exportcfyfilename = os.path.join(scriptdir, "dumps",  "{}_{}_ensdf_cfy.json".format(element, database_name))


def map_yield_data(y):
    branch = ensdf.get_decay_branch(y['z'], y['a'], y['fps'])
    if len(branch) > 0:
        print("Ok")
    y.update({'branch': branch})
    return y


def main_cumulative():
    cfy_yields = yields.get_cumulative_yields(element, Database.JENDL)
    cfy_yields = filters.filter_light_elements(cfy_yields, 15)
    cfy_yields = filters.filter_by_yields(cfy_yields, 1E-10)

    for cfy in cfy_yields:
        try:
            data = ensdf.get_data_for_z_a(cfy['z'], cfy['a'], cfy['fps'])
            if data is not None:
                cfy.update({'nuclide': data})
        except ImportError:
            pass
    with open(exportcfyfilename, 'w') as file:
        json.dump(cfy_yields, file)


def main_independent():
    yields_data = yields.get_independent_yields(element, database)

    yields_data = filters.filter_by_yields(yields_data, 1E-10)
    yields_data = filters.filter_light_elements(yields_data, 15)

    print(len(yields_data))
    print(yields_data[0])

    data = list(map(map_yield_data, yields_data))
    with open(exportfilename, 'w') as file:
        json.dump(data, file)


if __name__ == '__main__':
    main_independent()
    main_cumulative()

