import calculation.summation as summ
import setup
import scipy.integrate as integrate
import matplotlib.pyplot as plt
import numpy as np
import math
import constants
from calculation.cumulative_yields import get_cfy_for_z_a
from parse.endf_yields_loader import get_independent_yields


element = setup.data[0]

print(element)

chain = [element]
chain += element['chain']

time = np.arange(0.0, 100.0, 0.01)
n = [[] for i in range(len(chain))]

for k in range(len(chain)):
    for t in np.nditer(time):
        n[k].append(summ.bateman_solving(chain, k, t))


fig, ax = plt.subplots()
for k in range(len(chain)):
    ax.plot(time, n[k], label=chain[k]['symbol'])

legend = ax.legend(loc='upper center')

ind_yields = get_independent_yields('u235', constants.Database.ENDF)
# plt.grid(True)
for e in chain:
    e['cfy'] = get_cfy_for_z_a(e['z'], e['a'])
    e['ind'] = [y for y in ind_yields if y['z'] == e['z'] and y['a'] == e ['a']][0]['y']

for i in range(len(chain)):
    el = chain[i]
    ysum = el['ind']
    for k in range(i):
        ysum += chain[k]['ind']
    print("{}: cfy={}, ind={}, ind_sum={}".format(el['symbol'], el['cfy'], el['ind'], ysum))

plt.show()

