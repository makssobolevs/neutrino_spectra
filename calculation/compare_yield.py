import calculation.cumulative_yields as cfy
import parse.endf_yields_loader as endf_loader
import constants
import setup
from calculation.summation import bateman_solving

element = "u235"

independent = endf_loader.get_cumulative_yields(element, constants.Database.JENDL)

for el in independent:
    print("ind:{} -- cfy:{}".format(el['y'], cfy.get_cfy_for_z_a(el['z'], el['a'])))

