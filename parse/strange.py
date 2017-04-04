import constants
import json
import os
import pprint

dump_filenames = {
    "yields": "{}_{}_yields.json",
    "yields_filtered": "{}_{}_yields_filtered.json",
    "chains": "{}_{}_yields_filtered_math.json",
    "final": "{}_{}_final.json"
}


def create_filepath(template, element_name, database_name):
    dir = os.path.dirname(__file__)
    fn = template.format(element_name, database_name)
    path = os.path.join(dir, "dumps", fn)
    return path


def load_json(filename, element_name, database_name):
    path = create_filepath(filename, element_name, database_name)
    with open(path, "r") as file:
        data = json.loads(file.read().replace(".e-", "e-"))
    return data


data = load_json(dump_filenames['final'], 'u235', constants.Database.NAME_JENDL.value)

strange = []

x = set()

for el in data:
    if 'gamma' in el:
        s = 0
        for gel in el['gamma']:
            s += gel['pgamma']
        if s > 1:
            el1 = dict(el)
            del el1['chain']
            strange.append(el1)
            x.add((el1['z'], el1['a']))

    for child in el['chain']:
        if 'gamma' in child:
            s = 0
            for gel in child['gamma']:
                s += gel['pgamma']
            if s > 1:
                strange.append(child)
                x.add((child['z'], child['a']))

print(len(strange))

with open("strange.txt", "w") as file:
    pprint.pprint(x, stream=file)
