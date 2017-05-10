import math

def filter_by_yields(elements, low_border):
    return [el for el in elements if el['y'] > low_border]


def filter_light_elements(elements, min_a):
    return [el for el in elements if el["a"] > min_a]


def filter_beta_decayable(data):
    d = [e for e in data if e['branch']]
    return d
