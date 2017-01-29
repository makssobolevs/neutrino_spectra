import json
from parsing.symbols_qmax import get_data_by_element
import os

dir = os.path.dirname(__file__)
filename = os.path.join(dir, 'dumps', 'chains_mathematica.json')
expfilename = os.path.join(dir, "dumps", "final_fission_data.json")

data = open(filename, "r")

elements = json.load(data)

i = 1
for el in elements:
    print("Now base element: {}/{}".format(i, len(elements)))
    if 'chain' in el:
        for child in el['chain']:
            child_data = get_data_by_element(child['z'], child['a'])
            for key in child_data.keys():
                child[key] = child_data[key]
            print(child)
    i += 1

with open(expfilename, "w") as file:
    json.dump(elements, file, ensure_ascii=False)

