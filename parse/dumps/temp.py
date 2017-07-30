import json

from config import setup

with open("/home/ace/Документы/Физика"
          "/Элементарные частицы/neutrino/spectrums/python/parse/dumps/u235_JENDL_ensdf.json", 'r') as file:
    data = json.load(file)

# with open("u235_pretty.json", "w") as file:
#     json.dump(data, file, indent=4, sort_keys=True)


# setup.element_name = 'u238'
setup.main_nuclide_name = 'pu239'
cfy = setup.load_independent_base_data()

with open("{}aaaa.dat".format(setup.main_nuclide_name), 'w') as file:
    dis = []
    for el in cfy:
        i = 0
        for d in dis:
            if d['a'] == el['a']:
                d['y'] += el['y']
                break
            i += 1
        if i == len(dis):
            dis.append({'a': el['a'], 'y': el['y']})

    for el in dis:
        file.write("{} {}\n".format(el['a'], el['y']))
