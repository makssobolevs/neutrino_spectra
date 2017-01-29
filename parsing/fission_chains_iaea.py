import json
import requests
import logging
from lxml import etree
from init_elements import elements, Element
from parsing.symbols_qmax import get_data_by_element
import re

log_level = logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')


filename = "dumps/yields_symbols_qmax.json"
data = open(filename, 'r')
yields = json.load(data)


def get_table_element(root, row, col):
    return root.xpath('//table[@class="tbl-nucs"]/tr[{}]/td[{}]'.format(row, col))[0]


def get_table_size(root):
    trs = root.xpath('//table[@class="tbl-nucs"]/tr')
    return len(trs)


def get_child_from_td(parent, td):
    el = td.xpath('./table/tr/td')
    s1 = el[0].xpath("./font")[0]
    s1_string = etree.tostring(s1)
    search = re.search("(\d+)<br/>(\d+)", str(s1_string))
    if search:
        a = int(search.group(1))
        z = int(search.group(2))
        child_data = get_data_by_element(z, a)
        child_data['parent'] = parent
        child = Element(child_data)
        return child
    else:
        raise ValueError("child element data not found")


def get_decay(root, r):
    td = get_table_element(root, r, 5)
    return td.text.strip()


session = requests.Session()
def get_child_element(element):
    search_symbol = re.search("\d+-([a-zA-z]{2})-\d+", element.symbol)
    symbol = search_symbol.group(1)
    payload = str(element.a) + symbol
    request_url = "https://www-nds.iaea.org/relnsd/LCServlet?tbltype" \
          "=NR&qry=NUCID={}&dojo.preventCache=1485513319221".format(payload)
    result = session.get(request_url)
    root = etree.HTML(result.text)
    td = get_table_element(root, 1, 7)
    child = get_child_from_td(element, td)
    element.decay = get_decay(root, 1)
    logging.info("Childs size: {}".format(get_table_size(root)))
    return child

i = 1
for element in elements:
    logging.info("Now element {}/{}: {}".format(i, len(elements), element))
    child = get_child_element(element)
    element.child = child
    logging.info("Child: {}".format(child))

