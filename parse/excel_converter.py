import json
import xlsxwriter
import os

dir = os.path.dirname(__file__)
filename = os.path.join(dir, 'dumps', 'yields_symbols_qmax.json')
out_filename = os.path.join(dir, 'dumps', 'data.xlsx')

data = open(filename, 'r')

yields = json.load(data)

workbook = xlsxwriter.Workbook(out_filename)
worksheet = workbook.add_worksheet()


def write_header(element, worksheet):
    c = 0
    for key in element.keys():
        worksheet.write(0, c, key)
        c += 1

write_header(yields[0], worksheet)


row = 1

for y in yields:
    col = 0
    for val in y.values():
        worksheet.write(row, col, val)
        col += 1
    row += 1

workbook.close()

