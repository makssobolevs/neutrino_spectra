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


def populate_cfy(elements):
    for el in elements:
        el['cfy'] = get_cfy_for_z_a(el['z'], el['a'])
        for c in el['chain']:
            c['cfy'] = get_cfy_for_z_a(c['z'], c['a'])

        # if 'chain' in el:
        #     last = el['chain'][-1]
        #     last['cfy'] = get_cfy_for_z_a(last['z'], last['a'])
