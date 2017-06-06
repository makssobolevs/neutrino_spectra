import os
import fnmatch
import re
import sys
import parse.jendl_wesite_parser as jendl
import parse.endf_decay_data as endf

scriptdir = os.path.dirname(__file__)
xzy_pattern = "\+[XYZVUW]+"


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
    pattern = re.compile("^\s{,2}\d{1,3}[A-Z]{2}\s{2,}" + parent_id + " B-")
    cards = []
    inCard = False
    for line in lines:
        if pattern.match(line) and 'MIXED SOURCE' not in line:
            cards.append([line.strip()])
            inCard = True
        if inCard and not line.isspace():
            cards[len(cards) - 1].append(line)
        if inCard and line.isspace():
            inCard = False
    return cards


def get_parent_line(card, parent_id):
    header = "{}  P".format(parent_id)
    for line in card:
        if header in line[:9]:
            return line
    return None


def get_parent_energy(card, parent_id):
    line = get_parent_line(card, parent_id)
    try:
        after_sub = re.sub(xzy_pattern, '', line[9:19]).strip()
        value = float(after_sub)
    except ValueError:
        print("Parent energy value error: \"{}\"".format(line.strip()))
        value = 0.0
    except TypeError:
        print("TypeError parent energy: \"{}\"".format(line.strip()))
        value = 0.0
    return value


def filter_card_by_fps(cards, parent_id, fps):
    for card in cards:
        line = get_parent_line(card, parent_id)
        energy = get_parent_energy(card, parent_id)
        if fps != 0.0 and (energy != 0.0 or re.match("[XYZUVW]", line[9:19])):
            return [card]
        elif fps == 0.0 and energy == 0.0:
            return [card]
    return []


def get_q_value(card, parent_id):
    line = get_parent_line(card, parent_id)
    energy = get_parent_energy(card, parent_id)
    q = float(line[64:74].strip())
    return q + energy


def get_half_life(card, parent_id):
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


def get_child(line):
    search = re.match("(^\s{,2}\d{1,3}[A-Z]{2})", line)
    return search.group(1).strip()


def get_normalization(card):
    nline = ''
    for line in card:
        if check_record_type(line, 'N'):
            nline = line
            break
    nb = nline[41:49]
    if nb.isspace() or nb == "":
        return 1
    else:
        return float(nb)


def get_branching(card):
    nlines = list(filter(lambda l: check_record_type(l, 'N'), card))
    if len(nlines) == 0:
        return 1.0
    nline = nlines[0]
    if nline[31:39].isspace():
        branching = 1.0
    else:
        branching = float(nline[31:39])
    return branching


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
        try:
            ib = float(beta_decay_line[21:29]) * norm / 100
        except ValueError:
            ib = "?"

        level_line = beta_decay_dict['level']
        try:
            level_energy = float(re.sub(xzy_pattern, '', level_line[9:19]).strip())
        except ValueError:
            print("Warning level energy: \"{}\"".format(level_line))
            level_energy = 0.0

        return {
            'e': level_energy * 1E-3,
            'ib': ib
        }

    beta_decays = list(map(beta_decay_data, beta_decays))
    return list(filter(lambda b: '?' not in str(b['ib']), beta_decays))


def check_ib(element):
    branches = element['branches']
    s = 0
    for b in branches:
        s += b['ib']
    print(s)
    if s > element['ratio']:
        return False
    return True


def get_data_for_nucid(nucid, fps, z):
    a = int(nucid[:len(nucid) - 2])
    lines = load_ensdf_file(a)

    cards = get_beta_decay_cards(lines, nucid)

    actual_cards = filter_card_by_fps(cards, nucid, fps)

    symbol = nucid
    if fps != 0.0:
        symbol += 'm'

    if len(actual_cards) > 1:
        print("Warning, two actual cards for {}".format(symbol))
        [print(c) for c in actual_cards]
    if len(actual_cards) == 0:
        raise ImportError('No beta decay card:{}, z:{}'.format(nucid, z))

    actual_card = actual_cards[0]
    q = get_q_value(actual_card, nucid) * 1E-3  # Mev
    hl = get_half_life(actual_card, nucid)
    br = get_branching(actual_card)
    child = get_child(actual_card[0])

    branches = get_beta_decay_branches(actual_card)

    child = {
        'z': z + 1,
        'a': a,
        'fps': 0.0
    }

    return {'q': q,
            'hl': hl,
            'a': a,
            'z': z,
            'fps': fps,
            'ratio': br,
            'child': child,
            's': symbol,
            'branches': branches,
            'isStable': False
            }


def get_endf_data(z, a, fps):
    s = get_symbol_for_z_a(z, a)
    endf_s = s[0].upper() + s[1].lower()
    return endf.get_data_for_z_a(z, a, endf_s, fps)


def get_jendl_website(z, a):
    print("Fallback JENDL website")
    jendl_data = jendl.get_data_by_element(z, a)
    jendl_data['ratio'] = 1.0
    jendl_data['isStable'] = False if jendl_data['q'] > 0 and '%' not in str(jendl_data['hl']) else True
    if not jendl_data['isStable']:
        jendl_data['child'] = {
            'z': z + 1,
            'a': a,
            'fps': 0.0
        }
    return jendl_data


def get_data_for_z_a(z, a, fps):
    try:
        symbol = get_symbol_for_z_a(z, a).upper()
        parent_id = str(a) + symbol
        data = get_data_for_nucid(parent_id, fps, z)
    except (ImportError, AttributeError):
        print('Fallback ENDF, z:{}, a:{}'.format(z, a))
        try:
            data = get_endf_data(z, a, fps)
        except (ValueError, TypeError) as e:
            print(e)
            data = get_jendl_website(z, a)
        except FileNotFoundError as e:
            print(e)
            data = get_jendl_website(z, a)
        except ImportError as e:
            print(e)
            data = get_jendl_website(z, a)
    return data


def get_decay_branch(z, a, fps):
    nuclide = get_data_for_z_a(z, a, fps)
    if nuclide is None:
        return []
    branch = []
    while nuclide is not None and not nuclide['isStable']:
        print(nuclide)
        branch.append(nuclide)
        nuclide = get_data_for_z_a(nuclide['child']['z'], nuclide['child']['a'],
                                   nuclide['child']['fps'])
    return branch


if __name__ == '__main__':
    # get_decay_branch(54, 139)
    element = get_data_for_z_a(27, 68, 1.0)
    print(element)
    # element = get_data_for_z_a(52, 133, metaStable=False)
    # element1 = get_data_for_z_a(52, 133, metaStable=True)
    # print(element)
    # print(element1)
    # print(check_ib(element))
    # print(check_ib(element1))




