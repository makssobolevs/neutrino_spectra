"""
MT=457 - Radioactive decay data
"""
import lib.pyENDF6.ENDF6 as ENDF6
import os
from parse.endf_utils import get_z_a
import logging


def _read_file_lines(element, database="jendl2015"):
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, '..', 'resources', 'decay_data', database, element + '.jddf15')
    f = open(filename, "r")
    return f.readlines()


def create_filename(z, a, s, metaStable=False):
    name = ''
    if z < 100:
        name += '0'
    name += str(z)
    name += '_' + s + '_'
    if a < 100:
        name += '0'
    name += str(a)
    if metaStable:
        name += 'm'
    return name


def get_data_for_z_a(z, a, symbol, fps):
    lines = _read_file_lines(create_filename(z, a, symbol, metaStable=False if fps == 0.0 else True), 'jendl2015')
    sec = ENDF6.find_section(lines, MF=8, MT=457)

    line = []

    for s in range(len(sec)):
        line.append(ENDF6.read_line(sec[s]))

    za = get_z_a(line[0][0])
    nst = line[0][4]
    isStable = False if nst == 0.0 else True

    ndk = int(line[3][5])

    if line[3][4] != 6*ndk:
        raise ImportError("Number of decay branches is not valid")

    branches = line[4:4+ndk]

    br = {}
    for l in branches:
        rtyp = l[0]
        if rtyp == 1.0:
            br['rfs'] = l[1]
            br['q'] = l[2] * 1E-6   # MeV
            br['ratio'] = l[4]
            break

    if not br:
        raise ImportError("No decay branch found in endf z:{}, a:{}, fps:{}".format(z, a, fps))

    child = {}
    if not isStable:
        child = {'z': z + 1, 'a': a, 'fps': br['rfs']}

    return {
        'z': z,
        'a': a,
        'fps': fps,
        'hl': float(line[1][0]),
        'child': child,
        'q': br['q'],
        'ratio': br['ratio'],
        'isStable': isStable,
        'branches': [],
        's': symbol
    }


if __name__ == '__main__':
    data = get_data_for_z_a(52, 133, 'Te', 0.0)
    print(data)





# print(line[0])
# hl = line[1][0]
# # NC - total number of energies
# nc = line[1][4] / 2
# # SPI - Spin of the nuclide in its LIS state
# spi = line[3][0]
# ndk = line[3][5]
# print(za)
# print("Half-life: {}".format(hl))
# print("NC: {}".format(nc))
# print("SPI: {}".format(spi))
# print("NDK: {}".format(ndk))
#
# rtyp = line[4][0]
# rfs = line[4][1]
# qmax = line[4][2] * 1E-3
# br = line[4][4]
# print("RTYP: {}".format(rtyp))
# print("RFS: {}".format(rfs))
# print("Q: {}".format(qmax))
# print("BR: {}".format(br))
#
# for l in line[0:50]:
#     print(l)


# with open("endf.txt", mode="w") as file:
#     for s in line:
#         file.write(str(s))
#         file.write("\n")

# for l in sec:
#     try:
#         print(ENDF6.read_line(l))
#     except ValueError:
#         print("Value error:{}".format(l))
