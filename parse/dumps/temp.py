import json

with open("/home/ace/Документы/Физика"
          "/Элементарные частицы/neutrino/spectrums/python/parse/dumps/u235_JENDL_ensdf.json", 'r') as file:
    data = json.load(file)

with open("u235_pretty.json", "w") as file:
    json.dump(data, file, indent=4, sort_keys=True)