import requests
import json
import time
from lxml import etree
from json_loader import yields_base as yields
import logging
import re

log_level = logging.INFO
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

request_url = "http://wwwndc.jaea.go.jp/cgi-bin/cn2014.cgi"
export_filename = "dumps/yields_symbols_qmax.json"

session = requests.Session()

def parse_qmax(root):
    tags = root.xpath("(//b | //pre)")
    index_energy_label = 0
    for i in range(len(tags)):
        if "Beta-decay energy" in tags[i].text:
            index_energy_label = i
            break
    energy = tags[index_energy_label + 1].text.strip().split()[0]
    return float(energy)


def parse_symbol(root):
    h2 = root.xpath("string(//h2[1])").strip()
    return h2

FLOAT_REGEXP = '(\d+(\.\d+)?)\s?'


def parse_half_life(root):
    pre = root.xpath("//pre")
    hl_el = [el for el in pre if "Abundance or Half-life" in el.text]
    logging.debug('Half-life pre length: {}'.format(len(hl_el)))
    logging.debug(hl_el[0].text)
    hl_ms = re.search(FLOAT_REGEXP + 'ms', hl_el[0].text)
    hl_s = re.search(FLOAT_REGEXP + 's', hl_el[0].text)
    hl_m = re.search(FLOAT_REGEXP + 'm', hl_el[0].text)
    hl_h = re.search(FLOAT_REGEXP + 'h', hl_el[0].text)
    hl_d = re.search(FLOAT_REGEXP + 'd', hl_el[0].text)
    hl_y = re.search(FLOAT_REGEXP + 'y', hl_el[0].text)
    hl_unknown = re.search(FLOAT_REGEXP + '[a-z]+', hl_el[0].text)
    hl_abu = re.search(FLOAT_REGEXP, hl_el[0].text)
    hl_value = 0
    if hl_ms:
        hl_value = float(hl_ms.group(1))*1E-3
    elif hl_s:
        hl_value = float(hl_s.group(1))
    elif hl_m:
        hl_value = float(hl_m.group(1))*60
    elif hl_h:
        hl_value = float(hl_h.group(1))*60*60
    elif hl_d:
        hl_value = float(hl_d.group(1))*60*60*24
    elif hl_y:
        hl_value = float(hl_y.group(1))*60*60*24*365
    elif hl_unknown:
        hl_value = hl_unknown.group(0)
    elif hl_abu:
        hl_value = '{}%'.format(hl_abu.group(0))
    return hl_value


def get_data_by_element(z, a):
    payload = {'atomic': z, 'mass': a}
    result = session.post(request_url, data=payload)
    root = etree.HTML(result.text)
    logging.debug(result.text)
    data = {}
    data['symbol'] = parse_symbol(root)
    data['qmax'] = parse_qmax(root)
    data['hl'] = parse_half_life(root)
    data['z'] = z
    data['a'] = a
    return data

# temp = get_data_by_element(26, 66)
# logging.info(temp)

if __name__ == "__main__":
    i = 0
    for el in yields:
        try:
            el_data = get_data_by_element(el['z'], el['a'])
            el['symbol'] = el_data['symbol']
            el['qmax'] = el_data['qmax']
            el['hl'] = el_data['hl']
        except IndexError:
            logging.error('Index error')
            break
        except ValueError as e:
            logging.error(e, exc_info=True)
            logging.error('Value error: z:%d,a:%d', el['z'], el['a'])
        except AttributeError as e:
            logging.exception(e)

        logging.info("success fetch (%d/%d): %s", i, len(yields), str(el))
        i += 1
    # time.sleep(0.5)
    with open(export_filename, "w") as file:
        json.dump(yields, file, ensure_ascii=False)
