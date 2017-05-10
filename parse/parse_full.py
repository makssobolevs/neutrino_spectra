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

yields_data = yields.get_independent_yields(element, database)

yields_data = filters.filter_by_yields(yields_data, 1E-10)
yields_data = filters.filter_light_elements(yields_data, 15)

print(len(yields_data))
print(yields_data[0])


def map_yield_data(y):
    branch = ensdf.get_decay_branch(y['z'], y['a'], y['fps'])
    if len(branch) > 0:
        print("Ok")
    y.update({'branch': branch})
    return y

data = list(map(map_yield_data, yields_data))


with open(exportfilename, 'w') as file:
    json.dump(data, file)


cfy_yields = yields.get_cumulative_yields(element, Database.JENDL)

for cfy in cfy_yields:
    symbol = ensdf.get_symbol_for_z_a(cfy['z'], cfy['a'])
    branches = []  # branches that lead to this cfy
    for b in data:
        if b['z'] == cfy['z'] and b['a'] == cfy['a']:
            branches.append(b)
        elif len(b['branch']) > 0 and b['branch'][-1]['child'] == symbol:
            branches.append(b)
    cfy.update({'branches': branches})

cfy_data = [y for y in cfy_yields if len(y['branches']) > 0]


with open(exportcfyfilename, 'w') as file:
    json.dump(cfy_data, file)



