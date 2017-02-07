
def filter_by_yields(elements, low_border):
    return [el for el in elements if el['y'] > low_border]


def filter_light_elements(elements, min_a):
    return [el for el in elements if el["a"] > min_a]


def filter_beta_decayable(data):
    d = [e for e in data if e['qmax'] > 0 and ('%' not in str(e['hl']))]
    for el in d:
        if 'chain' in el:
            childs = el['chain']
            el['chain'] = [c for c in childs if (c['qmax'] > 0) and ('%' not in str(c['hl']))]
    return d
