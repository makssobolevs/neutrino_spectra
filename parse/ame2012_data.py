import os

dir = os.path.dirname(__file__)
filename = os.path.join(dir, '..', 'resources', 'decay_data', 'ame2012', 'mass.mas12')
f = open(filename, "r")
lines = f.readlines()

index_line = lines[30]

a = index_line.find('+')

header_length = 39

data = lines[39:]

offset = {
    "beta-decay": (75, 86),
    "symbol": (20, 25),
    "z": (10, 16),
    "a": (16, 20)
}


def get_int_element(line, off):
    return int(line[off[0]:off[1]].strip())


def get_float_element(line, off):
    return float(line[off[0]:off[1]].strip())


def get_string_element(line, off):
    return line[off[0]:off[1]].strip()


def ame2012_search_line(z, a):
    search = list(filter(lambda l: get_int_element(l, offset["z"]) == z
                                   and get_int_element(l, offset["a"]) == a, data))
    if len(search) == 1:
        return search[0]
    else:
        raise KeyError("Element {}-{} not found in ame2012".format(z, a))


def get_beta_decay_energy(z, a):
    line = ame2012_search_line(z, a)
    try:
        q = get_float_element(line, offset["beta-decay"])
        return q
    except ValueError:
        raise KeyError("No value for element {}-{}".format(z, a))


def get_element_symbol(z, a):
    line = ame2012_search_line(z, a)
    return get_string_element(line, offset['symbol'])
