import json
import os
import utils.filters as filters

element_name = 'pu239'

dir = os.path.dirname(__file__)
load_filename = os.path.join(dir, 'dumps', 'base_{}.json')
load_filename = str(load_filename).format(element_name)

export_filename = os.path.join(dir, 'dumps', 'base_filtered_{}.json')
export_filename = str(export_filename).format(element_name)


with open(load_filename, "r") as file:
    elements = json.load(file)

elements = filters.filter_beta_decayable(elements)

with open(export_filename, "w") as file:
    json.dump(elements, file, ensure_ascii=False)





