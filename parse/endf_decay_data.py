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


def create_filename(z, a, s):
    name = ''
    if z < 100:
        name += '0'
    name += str(z)
    name += '_' + s + '_'
    if a < 100:
        name += '0'
    name += str(a)
    return name


# 38-Sr-95
lines = _read_file_lines(create_filename(38, 95, 'Sr'), 'jendl2015')

content = ENDF6.list_content(lines)


sec = ENDF6.find_section(lines, MF=8, MT=457)

print("Length of file: {}".format(len(sec)))

line = []

for s in range(len(sec)):
    line.append(ENDF6.read_line(sec[s]))

print(line[0])
za = get_z_a(line[0][0])
hl = line[1][0]
# NC - total number of energies
nc = line[1][4] / 2
# SPI - Spin of the nuclide in its LIS state
spi = line[3][0]
ndk = line[3][5]
print(za)
print("Half-life: {}".format(hl))
print("NC: {}".format(nc))
print("SPI: {}".format(spi))
print("NDK: {}".format(ndk))

rtyp = line[4][0]
rfs = line[4][1]
qmax = line[4][2] * 1E-3
br = line[4][4]
print("RTYP: {}".format(rtyp))
print("RFS: {}".format(rfs))
print("Q: {}".format(qmax))
print("BR: {}".format(br))

for l in line[0:50]:
    print(l)


with open("endf.txt", mode="w") as file:
    for s in line:
        file.write(str(s))
        file.write("\n")

# for l in sec:
#     try:
#         print(ENDF6.read_line(l))
#     except ValueError:
#         print("Value error:{}".format(l))
