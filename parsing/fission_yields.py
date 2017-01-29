import json

data_filename = "parsing/dumps/u235_fission_yields.dat"
export_filename = "parsing/dumps/yields_basic.json"


def parse_data(file):
    yields = []
    for line in file:
        data = line.strip().split()
        now = {
            'z': int(data[0]),
            'n': int(data[1]),
            'y': float(data[2])
        }
        yields.append(now)
    return yields


def filter_yields(yields):
    low_border = 1E-10
    return [el for el in yields if el['y'] > low_border]


def set_a(yields):
    for el in yields:
        el['a'] = el['z'] + el['n']
    return yields


if __name__ == "__main__":
    data = open(data_filename, "r")
    next(data)  # skip first comment line

    yields = parse_data(data)
    length_before_filter = len(yields)

    yields = filter_yields(yields)
    length_after_filter = len(yields)
    print('Yields before filtering: {}'.format(length_before_filter))
    print('Yields after filtering: {}'.format(length_after_filter))

    yields = set_a(yields)

    with open(export_filename, "w") as file:
        json.dump(yields, file, ensure_ascii=False)
