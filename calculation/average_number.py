import setup
import functools
import json
import os

setup.element_name = 'u235'


def print_results(full_count, length):
    print("Nuclide: {}".format(setup.element_name))
    print("Beta decayable: {}".format(length))
    print("Average filters in chain: {}".format(full_count / length))
    print("\n")


def ensdf():
    data = setup.load_independent_base_data()
    afasd = [a for a in data if len(a['branch']) > 0]
    full_count = functools.reduce(lambda res, b: res + len(b['branch']), afasd, 0)
    print_results(full_count, len(afasd))
    plot_distribution(data)


def wolfram_research():
    path = os.path.join("..", "parse", "dumps", "{}_{}_final.json".format(setup.element_name, setup.database_name))
    with open(path, 'r') as file:
        data = json.load(file)
    decayable = [el for el in data if el['qmax'] > 0 and '%' not in str(el['hl'])]
    full_count = functools.reduce(lambda res, b: res + 1 + len(b['chain']), decayable, 0)
    print_results(full_count, len(decayable))


def plot_distribution(data):
    import pylab as plt
    x = [i for i in range(8)]
    y = []
    for i in x:
        number = len([x for x in data if len(x['branch']) == i])
        y.append(num    plt.hist([x, y])
    plt.show()ber)

    print(x)
    print(y)






if __name__ == '__main__':
    print("Ensdf")
    ensdf()
    print("Wolfram research")
    wolfram_research()
