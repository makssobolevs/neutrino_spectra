import json
import os
from parse.jendl_wesite_parser import get_data_by_element

element_name = "pu239"

dir = os.path.dirname(__file__)

load_filename = os.path.join(dir, 'dumps', 'result_{}.json')
load_filename = str(load_filename).format(element_name)

export_filename = os.path.join(dir, 'dumps', 'final_{}.json')
export_filename = str(export_filename).format(element_name)

data = open(load_filename, "r")

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

with open(export_filename, "w") as file:
    json.dump(elements, file, ensure_ascii=False)

