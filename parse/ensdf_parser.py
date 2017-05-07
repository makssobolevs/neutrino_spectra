import os
import fnmatch
import re

scriptdir = os.path.dirname(__file__)


def get_symbol_for_z_a(z, a):
    jendl_dir = os.path.join(scriptdir, "..", "resources", "decay_data", "jendl2015")

    pattern = str(z).zfill(3) + "_([A-Za-z]{2})_" + str(a).zfill(3)  + ".jddf15"
    search = re.compile(pattern)

    for file in os.listdir(jendl_dir):
        result = search.match(file)
        if result:
            return result.group(1)

    return None


def load_ensdf_file(a):
    dir1 = os.path.join(scriptdir, "..", "resources", "decay_data", "ensdf")

    ensdf_dir_pattern = "ensdf_\d{6}[\._]"
    if a < 100:
        ensdf_dir_pattern += '099'
    elif 99 < a < 200:
        ensdf_dir_pattern += '199'
    elif a > 199:
        ensdf_dir_pattern += '299'

    for dir in os.listdir(dir1):
        result = re.match(ensdf_dir_pattern, dir)
        if result:
            dir1 = os.path.join(dir1, dir)

    filedir = os.path.join(dir1, "ensdf.{}".format(str(a).zfill(3)))

    with open(filedir, 'r') as file:
        return file.readlines()


def get_beta_decay_cards(lines, parent_id):
    header = " {} B-".format(parent_id)
    cards = []
    inCard = False
    for line in lines:
        if header in line:
            cards.append([line.strip()])
            inCard = True
        if inCard and not line.isspace():
            cards[len(cards) - 1].append(line)
        if inCard and line.isspace():
            inCard = False
    return cards

def get_parent_line(card, parent_id):
    header = "{}  P ".format(parent_id)
    for line in card:
        if header in line:
            return line
    return None


def get_parent_energy(card, parent_id):
    line = get_parent_line(card, parent_id)
    parent_energy = line[9:19].strip()
    return float(parent_energy)


def get_q_value(card, parent_id):
    line = get_parent_line(card, parent_id)
    energy = float(line[9:19].strip())
    q = float(line[64:74].strip())
    return q + energy


def get_halt_life(card, parent_id):
    line = get_parent_line(card, parent_id)
    hl = line[39:49]
    value = float(hl.split()[0].strip())
    unit = hl.split()[1].strip()
    if unit == 'Y':
        value *= 60*60*24*365
    elif unit == 'D':
        value *= 24*3600
    elif unit == 'H':
        value *= 3600
    elif unit == 'M':
        value *= 60
    elif unit == 'S':
        value *= 1
    elif unit == 'MS':
        value *= 1E-3
    elif unit == 'US':
        value *= 1E-6
    elif unit == 'NS':
        value *= 1E-9
    elif unit == 'PS':
        value *= 1E-12
    elif unit == 'FS':
        value *= 1E-15
    return value


def check_record_type(line, type):
    header = "  {} ".format(type)
    return True if header in line[:9] else False


def get_normalization(card):
    nline = ''
    for line in card:
        if check_record_type(line, 'N'):
            nline = line
            break
    nb = nline[41:49]
    return 1 if nb.isspace() else float(nb)


def get_beta_decay_branches(card):
    norm = get_normalization(card)
    beta_decays = []
    for i in range(len(card)):
        line = card[i]
        if check_record_type(line, 'B'):
            j = i
            while not check_record_type(card[j], 'L'):
                if j > 0:
                    j -= 1
            dict = {'beta': line, 'level': card[j]}
            beta_decays.append(dict)

    def beta_decay_data(beta_decay_dict):
        beta_decay_line = beta_decay_dict['beta']
        ib = float(beta_decay_line[21:29]) * norm / 100

        level_line = beta_decay_dict['level']
        level_energy = float(level_line[9:19])
        # print("level energy: {}, ib: {}".format(level_energy, ib))

        return {
            'e': level_energy,
            'ib': ib
        }

    return list(map(beta_decay_data, beta_decays))


def get_data_for_z_a(z, a, metaStable=False):
    symbol = get_symbol_for_z_a(z, a).upper()
    parent_id = str(a).zfill(3) + symbol

    lines = load_ensdf_file(a)

    cards = get_beta_decay_cards(lines, parent_id)

    if not metaStable:
        actual_cards = list(filter(lambda c: get_parent_energy(c, parent_id) == 0.0, cards))
    else:
        actual_cards = list(filter(lambda c: get_parent_energy(c, parent_id) != 0.0, cards))

    if len(actual_cards) > 1:
        print("Warning, two actual cards for {}".format(parent_id))
    if len(actual_cards) == 0:
        print("Warning, no beta decay card for {}".format(parent_id))

    actual_card = actual_cards[0]
    q = get_q_value(actual_card, parent_id)
    hl = get_halt_life(actual_card, parent_id)

    branches = get_beta_decay_branches(actual_card)

    if metaStable:
        parent_id += 'm'

    return {'q': q,
            'hl': hl,
            'z': z,
            'a': a,
            'symbol': parent_id,
            'branches': branches
            }


def check_ib(element):
    branches = element['branches']
    s = 0
    for b in branches:
        s += b['ib']
    print(s)
    if s > 1:
        return False
    return True



if __name__ == '__main__':
    element = get_data_for_z_a(52, 133, metaStable=False)
    element1 = get_data_for_z_a(52, 133, metaStable=True)
    print(element)
    print(element1)
    print(check_ib(element))
    print(check_ib(element1))




