import math


def lmbd(element):
    hl = element['hl']
    l = math.log(2) / hl
    return l


def populate_lambda(data):
    for branch in data:
        for el in branch['branch']:
            el['l'] = lmbd(el)


def populate_lambda_cfy(data):
    for element in data:
        nuclide = element['nuclide']
        nuclide['l'] = lmbd(nuclide)
        nuclide['z'] = element['z']

