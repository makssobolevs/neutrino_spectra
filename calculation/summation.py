import math
import scipy.integrate as integrate
from phys_functions import fermi_function


def distribution(element, energy):
    qbeta = element['qmax'] * 1E-3
    return distribution_for_q(element, energy, qbeta)


def distribution_for_q(element, energy, qbeta):
    m_e = 0.511
    if energy > qbeta:
        return 0
    elif qbeta - energy > m_e:
        mult1 = energy * energy * (qbeta - energy)
        mult2 = math.sqrt(math.pow(qbeta - energy, 2) - m_e * m_e)
        return mult1 * mult2  # * fermi_function(element['z'], element['a'], qbeta - energy)
    else:
        return 0


def lmbd(element):
    hl = element['hl']
    l = math.log(2) / hl
    return l


def populate_lmdb(data):
    for el in data:
        el['l'] = lmbd(el)
        if 'chain' in el:
            for child in el['chain']:
                child['l'] = lmbd(child)


def bateman_solving(elements, n, t):
    mult1 = 1
    mult1 *= elements[0]['y']
    for j in range(0, n):
        mult1 *= lmbd(elements[j])
    sum1 = 0
    for j in range(0, n + 1):
        mult2 = 1
        for p in range(n + 1):
            if p != j:
                mult2 *= elements[p]['l'] - elements[j]['l']
        if mult2 != 0.0:
            sum1 += math.exp(- elements[j]['l'] * t) / mult2
    mult1 *= sum1
    return mult1


def coefficient(element, time, parent_coeff=1, parent_lambda=1):
    try:
        l = lmbd(element)
        result = parent_coeff * parent_lambda / l
        # coeff = math.exp(-l * time)
        # if 'y' in element:
        #     result = (1 - coeff) * element['y'] / 2
        # else:
        #     result = (1 - coeff) * parent_coeff
        if 'ratio' in element:
            result *= element['ratio']
        return result
    except TypeError as e:
        print(e)
        print(element)
        raise e


def get_spectrum_value(data, energy, time):
    s = 0
    for element in data:
        chain = [element]
        chain += element['chain']

        ii = 0
        for el in chain:
            ii += 1
            if el['hl'] == float("inf"):
                break

        # if (ii +1) != len(chain):
        #     print(chain)

        def f_last(t):
            return bateman_solving(chain, ii - 1, t)

        s1 = 0
        for i in range(0, len(chain) - 1):
            # coeff = distribution(chain[i], energy)
            coeff = distribution_with_gamma(chain[i], energy)
            if 'ratio' in chain[i]:
                coeff *= chain[i]['ratio']

            s1 += (chain[0]['y'] - bateman_solving(chain, i, time)) * coeff
        s += s1

    return s


def get_spectrum_for_cfy(data, energy):
    s = 0
    for element in data:
        # coeff = distribution(element, energy)
        coeff = distribution_with_gamma(element, energy)
        if 'ratio' in element:
             coeff *= element['ratio']
        s += element['y'] * coeff
    return s


def distribution_with_gamma(element, energy):
    s = 0
    p = 0
    if 'gamma' in element:
        for g in element['gamma']:
            pgamma = g['pgamma']
            s += distribution_for_q(element, energy, (element['qmax'] - g['qgamma']) * 1E-3 ) * pgamma
            p += pgamma
    s += distribution_for_q(element, energy, element['qmax'] * 1E-3) * (1 - p)
    return s


def get_ibd_cross_section(energy):
    delta = 0.939565 - 0.93827
    m_e = 0.511
    mult1 = energy - delta
    k = (energy - delta)*(energy - delta) - m_e * m_e
    if k > 0:
        mult2 = math.sqrt(k)
    else:
        mult2 = 1
    return mult2 * mult1
