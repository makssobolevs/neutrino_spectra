import json
import os
import math

dir = os.path.dirname(__file__)
loadfilename = os.path.join(dir, "parsing", "dumps", "final_fission_data.json")
exportfilename = os.path.join(dir, "plots", "u235time{}.dat")

file = open(loadfilename, "r")

data = json.load(file)
file.close()

data = [e for e in data if e['qmax'] > 0]


def filter_beta_decayable(data):
    for el in data:
        childs = el['chain']
        el['chain'] = [c for c in childs if (c['qmax'] > 0) and ('%' not in str(c['hl']))]


filter_beta_decayable(data)


def distribution(element, energy):
    qbeta = element['qmax'] * 1E-3
    m_e = 0.511
    if energy > qbeta:
        return 0
    elif qbeta - energy > m_e:
        mult1 = energy * energy * (qbeta - energy)
        mult2 = math.sqrt(math.pow(qbeta - energy, 2) - m_e * m_e)
        return mult1 * mult2
    else:
        return 0


def coefficient(element, time, parent_coeff=0):
    hl = element['hl']
    l = math.log(2) / hl
    coeff = math.exp(-l * time)
    if 'y' in element:
        return (1 - coeff) * element['y'] / 2
    else:
        return (1 - coeff) * parent_coeff

start_energy = 0.0  # MeV
finish_energy = 12.0  # MeV

points = 100

h = (finish_energy - start_energy) / points

# time = 1  # Second
times = {"1s": 1,
         "1minute": 60,
         "1hour": 3600,
         "24hours": 24 * 3600,
         "1week": 7 * 24 * 3600,
         "1year": 365 * 24 * 3600
         }


def get_spectrum_value(energy, time):
    s = 0
    for element in data:
        coeff = coefficient(element, time)
        s += coeff * distribution(element, energy)
        for child in element['chain']:
            coeff = coefficient(child, time, coeff)
            try:
                s += coeff * distribution(child, energy)
            except ValueError:
                print(child)
    return s


for tk in times.keys():
    time = times[tk]
    export_file = open(exportfilename.format(tk), "w")
    for p in range(points):
        energy = start_energy + h * p
        value = get_spectrum_value(energy, time)
        print("energy:{}, value:{}".format(energy, value))
        export_file.write("{} {}\n".format(energy, value))

    export_file.close()
