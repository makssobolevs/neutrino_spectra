import requests
from lxml import etree
import logging
import re
from bs4 import BeautifulSoup
import os

dir = os.path.dirname(__file__)
log_path = os.path.join(dir, 'logs', 'parsing.log')

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=log_path,
                    filemode='w'
                    )

request_url = "http://wwwndc.jaea.go.jp/cgi-bin/cn2014.cgi"

session = requests.Session()


FLOAT_REGEXP = '(\d+(\.\d+)?)\s?'


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


def parse_gamma(html):
    soup = BeautifulSoup(html, 'html.parser')
    pres = soup.find_all('pre')
    gamma_data = []
    for pre in pres:
        if 'γ-ray energy(keV)' in pre.text:
            table = re.search('(-{20,}$\n)(?P<data>(.|\n)*)\s-{20,}', pre.text, re.MULTILINE)
            if table:
                table_data = table.group('data')
                rows = table_data.splitlines()
                for row in rows:
                    if '---' in row:
                        break
                    data = row.split()
                    if 'B-' in data:
                        gamma_data.append({
                            'qgamma': float(data[0]),
                            'pgamma': float(data[1]) * 1E-2
                        })

    return gamma_data


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
    data = {}
    payload = {'atomic': z, 'mass': a}
    result = session.post(request_url, data=payload)
    root = etree.HTML(result.text)
    logging.debug(result.text)
    data['symbol'] = parse_symbol(root)
    try:
        data['q'] = parse_qmax(root)
    except ValueError:
        logging.warning("Qbeta parse error: z={}, a={}".format(z, a))
        raise ImportError
    data['hl'] = parse_half_life(root)
    # try:
    #     data['gamma'] = parse_gamma(result.text)
    # except ValueError:
    #     logging.warning("Gamma parse error: z={}, a={}".format(z, a))
    data['z'] = z
    data['a'] = a
    return data


if __name__ == "__main__":
    data = get_data_by_element(39, 96)
    print(data)
