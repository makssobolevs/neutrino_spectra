"""
MT=454 - Independent fission product yield data.
MT=459 - Cumulative fission product yield data.
MT=451 - Heading or title information
MF=8 - Radioactivity and fission-product yield data
"""
import lib.pyENDF6.ENDF6 as ENDF6
import os
import logging
from parse.endf_utils import get_z_a
from constants import Database


def _read_file_lines(element, database):
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '..', 'resources', 'fission_yields')
    if database == Database.JENDL:
        filename = os.path.join(filename, 'jendl', element + '.endf')
    elif database == Database.ENDF:
        filename = os.path.join(filename, 'endf', element + '.endf')
    f = open(filename, "r")
    return f.readlines()


def get_cumulative_yields(element, database):

    lines = _read_file_lines(element, database)
    sec = ENDF6.find_section(lines, MF=8, MT=459)

    line0 = ENDF6.read_line(sec[0])
    line1 = ENDF6.read_line(sec[1])

    nfp = int(line1[5])

    logging.debug("Fission yields for: {}".format(get_z_a(line0[0])))
    logging.debug("Energy: {} eV".format(line1[0]))
    logging.debug("Number of fission products: {}".format(nfp))

    all = []
    for e in sec[2:]:
        all += ENDF6.read_line(e)
    all = all[: 4 * nfp]

    result = []

    i = 0
    for x in range(nfp):
        chunk = all[i:i + 4]
        data = get_fission_product(chunk)
        i += 4
        result.append(data)
    return result


def get_independent_yields(element, database):

    lines = _read_file_lines(element, database)
    sec = ENDF6.find_section(lines, MF=8, MT=454)

    line0 = ENDF6.read_line(sec[0])
    line1 = ENDF6.read_line(sec[1])

    nfp = int(line1[5])

    logging.debug("Fission yields for: {}".format(get_z_a(line0[0])))
    logging.debug("Energy: {} eV".format(line1[0]))
    logging.debug("Number of fission products: {}".format(nfp))

    all = []
    for e in sec[2:]:
        all += ENDF6.read_line(e)
    all = all[: 4 * nfp]

    result = []

    i = 0
    for x in range(nfp):
        chunk = all[i:i + 4]
        data = get_fission_product(chunk)
        i += 4
        result.append(data)
    return result


def get_fission_product(line):
    zafp = line[0]
    za = get_z_a(zafp)
    # Floating point number - state designator, 0.0 - ground state
    za['fps'] = line[1]
    za['y'] = line[2]
    za['er'] = line[3]
    return za


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    result = get_independent_yields('u235', Database.ENDF)
    sorted_data = sorted(result, key=lambda k: k['y'], reverse=True)
    for e in sorted_data:
        if e['z'] == 34 and e['a'] == 80:
            logging.debug(e)

