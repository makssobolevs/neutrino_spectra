import calculation.cumulative_yields as cfy
import parse.endf_yields_loader as endf_loader
import constants
import main
from calculation.summation import bateman_solving

element = "u235"

independent = endf_loader.get_cumulative_yields(element, constants.Database.JENDL)

for el in independent:
    print("ind:{} -- cfy:{}".format(el['y'], cfy.get_cfy_for_z_a(el['z'], el['a'])))

# t = 1 * 365 * 24 * 3600
#
# for el in main.data:
#     chain = [el]
#     chain += el['chain']
#
#     ii = 0
#     for e in chain:
#         ii += 1
#         if e['hl'] == float("inf"):
#             break
#
#     last = chain[ii - 1]
#
#     def f_last():
#         return bateman_solving(chain, ii - 1, t)
#
#     cfy_calc = f_last()
#     cfy_table = cfy.get_cfy_for_z_a(last['z'], last['a'])
#
#     print("calc:{}, table:{}, diff:{}".format(cfy_calc, cfy_table, cfy_table - cfy_calc))
#
#
# al = []
#
# for el in main.data:
#     al += el
#     al += el['chain']
#
# print(len(al))

