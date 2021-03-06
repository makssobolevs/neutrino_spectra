import json
import os

import xlsxwriter

import calculation.filters as filters

dir = os.path.dirname(__file__)

filename = os.path.join(dir, 'dumps', 'final_pu239.json')
out_filename = os.path.join(dir, 'dumps', 'final_data_pu239.xlsx')
#
with open(filename, 'r') as file:
    elements = json.load(file)

data = filters.filter_beta_decayable(elements)

workbook = xlsxwriter.Workbook(out_filename)
worksheet = workbook.add_worksheet()

format = workbook.add_format()
format.set_bg_color('red')

headers = ['symbol', 'a', 'z', 'n', 'qmax', 'hl', 'ratio', 'y']

i = 0
for h in headers:
    worksheet.write(0, i, h)
    i += 1


def write_element_data(row, el, format=None):
    col = 0
    for h in headers:
        if h in el:
            worksheet.write(row, col, el[h], format)
        col += 1


row = 1
print(len(data))

sorted_data = sorted(data, key=lambda k: k['y'], reverse=True)

for el in sorted_data:
    write_element_data(row, el, format=format)
    row += 1
    for child in el['chain']:
        write_element_data(row, child)
        row += 1

workbook.close()
