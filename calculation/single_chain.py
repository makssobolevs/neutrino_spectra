import calculation.summation as summ
import setup
import matplotlib.pyplot as plt
import numpy as np


ind_data = setup.load_independent_base_data()

element = ind_data[0]
print(element)

cfy_data = setup.load_cfy_data()


def populate_cfy(nuclide):
    for cfy in cfy_data:
        if cfy['z'] == nuclide['z'] and cfy['a'] == nuclide['a'] and cfy['fps'] == nuclide['fps']:
            nuclide['cfy'] = cfy['y']
            break
    if not 'cfy' in nuclide:
        nuclide['cfy'] = None


def populate_ind(nuclide):
    for ind in ind_data:
        if ind['z'] == nuclide['z'] and ind['a'] == nuclide['a'] and ind['fps'] == nuclide['fps']:
            nuclide['y'] = ind['y']
            break
    if not 'y' in nuclide:
        nuclide['y'] = None


print("YIELD={}".format(element['y']))

chain = element['branch']
for el in chain:
    populate_cfy(el)
    populate_ind(el)
    print("{}-{}-{}, q={}, hl={}, l={}, cfy={}, ind={}"
          .format(el['s'], el['z'], el['a'], el['q'], el['hl'], el['l'], el['cfy'], el['y']))

start_time = 0.0
end_time = 20.0
dt = 0.005

# start_time = 0.0
# end_time = 1000000.0
# dt = 100

time = np.arange(start_time, end_time, dt)
n = [[] for i in range(len(chain))]

for k in range(len(chain)):
    for t in np.nditer(time):
        n[k].append(chain[k]['l'] * summ.bateman_solving_with_source(element, k, t))


colors = ['blue', 'black', 'red', 'green', 'cyan']

fig, ax = plt.subplots()
for k in range(len(chain)):
    ax.plot(time, n[k], label=chain[k]['s'], color=colors[k])
    # ax.plot((start_time, end_time), (chain[k]['cfy'], chain[k]['cfy']), color=colors[k])

legend = ax.legend(loc='upper center')

plt.show()

