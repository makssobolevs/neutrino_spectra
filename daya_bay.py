from main import init_energy_cells
from calculation.summation import get_ibd_cross_section
import api.resources_access as resources

# Plan:
# 1) Get Full spectrum with fuel coefficients
# 2) Parse daya bay results, get integration bins
# 3) Integrate spectrum
# 4) Contract result with IBD cross-section

percentage = {
    'u235': 0.561,
    'u238': 0.076,
    'pu239': 0.307,
    'pu241': 0.056
}


def get_spectra_for_nuclide(main_nuclide_name):
    postfix = 'timeCFY_gamma'
    filepath = resources.get_dat_export_filepath(main_nuclide_name, postfix)
    data = []
    with open(filepath, 'r') as file:
        for line in file:
            e, s = map(lambda v: float(v), line.split())
            data.append({
                'e': e,
                's': s
            })

    return data


def add_element_spectrum_value(full_value, nuclide_value, abudance):
    for i in range(len(full_value)):
        full_value[i]['s'] += abudance * nuclide_value[i]['s']
    return full_value


def get_full_spectrum():
    full_spectrum = init_energy_cells()
    for nuclide, abudance in percentage.items():
        add_element_spectrum_value(full_spectrum, get_spectra_for_nuclide(nuclide), abudance)
    return contract_spectrum_with_ibd(full_spectrum)


def contract_spectrum_with_ibd(full_spectrum):
    for i in range(len(full_spectrum)):
        full_spectrum[i]['s'] *= get_ibd_cross_section(full_spectrum[i]['e'])
    return full_spectrum


def get_daya_bay_bins():
    filepath = resources.get_daya_bay_filepath()
    bins = []
    with open(filepath, 'r') as file:
        for line in file:
            binstr = line.split()[0]
            a1, a2 = binstr.split('–')
            bins.append((float(a1), float(a2)))
    return bins


def integrate_bin(bin, full_spectrum):
    from scipy.interpolate import UnivariateSpline
    # segment = []
    # for el in full_spectrum:
    #     if bin[0] < el['e'] < bin[1]:
    #         segment.append(el)

    x = [el['e'] for el in full_spectrum]
    y = [el['s'] for el in full_spectrum]
    s = UnivariateSpline(x, y, k=5, s=0)
    return s.integral(bin[0], bin[1])


def integrate_bin_rectangles(bin, full_spectrum):
    import sys

    x = 0
    x_index = 0
    x_abs = sys.maxsize
    dx = full_spectrum[1]['e'] - full_spectrum[0]['e']
    for i in range(len(full_spectrum)):
        if abs(full_spectrum[i]['e'] - bin[0]) < x_abs:
            x = full_spectrum[i]['e']
            x_abs = abs(x - bin[0])
            x_index = i

    s = 0.0
    while x < bin[1] and x_index < len(full_spectrum):
        s += full_spectrum[x_index]['s']
        x_index += 1
    return s * dx


def export_calculated_bins(data):
    exportfn = resources.get_export_daya_bay_filepath()
    with open(exportfn, 'w') as file:
        for bin in data:
            file.write("{} {}\n".format(bin['e'], bin['s']))


def main():
    full_spectrum = get_full_spectrum()
    bins = get_daya_bay_bins()
    result = []
    for bin in bins:
        # value = integrate_bin(bin, full_spectrum)
        value = integrate_bin_rectangles(bin, full_spectrum) / 1.0E-46
        print(value)
        result.append({
            'e': "{}-{}".format(str(bin[0]), str(bin[1])),
            's': value / 1.0E-46
        })
    export_calculated_bins(result)


if __name__ == '__main__':
    main()
