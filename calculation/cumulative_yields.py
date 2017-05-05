from constants import Database
import logging
import parse.endf_yields_loader as parser

cumulative_yields = parser.get_cumulative_yields('u235', Database.ENDF)

logging.basicConfig(level=logging.DEBUG)


def get_cfy_for_z_a(z, a, all=False):
    result = [cy for cy in cumulative_yields if cy['a'] == a and cy['z'] == z]
    if len(result) > 0:
        if not all:
            return result[0]['y']
        else:
            return result
    else:
        return None


elements = parser.get_independent_yields("u235", Database.JENDL)
elements_fps = [el for el in elements if el['fps'] == 1.0]
elements_not_fps = [el for el in elements if el['fps'] != 1.0]

s1 = 0
for el in elements_fps:
    s1 += el['y']
print("Elements fps == 1 - {}: sum yield {}".format(len(elements_fps), s1))

s2 = 0
for el in elements_not_fps:
    s2 += el['y']
print("Elements fps != 1 - {}: sum yield {}".format(len(elements_not_fps), s2))
print(s1 + s2)

elements_fps = sorted(elements_fps, key=lambda el: el['y'], reverse=True)

for el in elements_fps:
    print(el)
