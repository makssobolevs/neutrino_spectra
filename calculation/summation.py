import math
import scipy.integrate as integrate
from phys_functions import fermi_function
import calculation.settings as settings


def get_normalization_for_chain(element, spectrum_values):
    if not element['chain']:
        n = 1
    else:
        n = len(element['chain'])
    integral_value = 0
    dE = spectrum_values[1]['e'] - spectrum_values[0]['e']
    for cell in spectrum_values:
        integral_value += cell['s']
    integral_value *= dE
    if integral_value != 0:
        return element['y'] * n / integral_value
    else:
        return 0

cache = {}


def get_normalization_for_distribution(element):
    result = 0.0
    key = str(element['a']) + str(element['z'])
    if key in cache:
        result = cache[key]
    else:
        def func(e):
            if settings.WITH_GAMMA:
                return distribution_with_gamma(element, e)
            else:
                return distribution(element, e)
        # integral_result = integrate.quad(func, 0, 15)
        integral_result = custom_integrate(func, 0, 15)
        if integral_result[0] != 0:
            result = 1 / integral_result[0]
        cache.update({key: result})
    return result


def custom_integrate(f, x0, x1):
    n = 1000
    dx = (x1 - x0) / n
    x = 0.0
    s = 0.0
    while x < x1:
        s += f((x + dx) / 2.0)
        x += dx
    return s * dx, 0


def distribution(element, energy):
    qbeta = element['qmax'] * 1E-3
    return distribution_for_q(element, energy, qbeta)


def distribution_for_q(element, energy, qbeta):
    m_e = 0.511
    if energy > qbeta:
        return 0.0
    elif qbeta - energy > m_e:
        mult1 = energy * energy * (qbeta - energy)
        mult2 = math.sqrt(math.pow(qbeta - energy, 2) - m_e * m_e)
        return mult1 * mult2  # * fermi_function(element['z'], element['a'], qbeta - energy)
    else:
        return 0.0


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


def get_spectrum_value_for_element(element, energy, time):
    chain = [element]
    chain += element['chain']

    s1 = 0
    for i in range(0, len(chain) - 1):
        if settings.WITH_GAMMA:
            coef = distribution_with_gamma(chain[i], energy)
        else:
            coef = distribution(chain[i], energy)
        k = get_normalization_for_distribution(chain[i])
        coef *= k
        if 'ratio' in chain[i]:
            coef *= chain[i]['ratio']

        s1 += (chain[0]['y'] - bateman_solving(chain, i, time)) * coef
    return s1


def get_spectrum_value(data, energy, time):
    s = 0
    for element in data:
        s1 = get_spectrum_value_for_element(element, energy, time)
        s += s1

    return s


def get_spectrum_value_for_element_cfy(element, energy):
    if settings.WITH_GAMMA:
        coeff = distribution_with_gamma(element, energy)
    else:
        coeff = distribution(element, energy)
    k = get_normalization_for_distribution(element)
    coeff *= k
    if 'ratio' in element:
        coeff *= element['ratio']
    return element['y'] * coeff


def get_spectrum_for_cfy(data, energy):
    s = 0
    for element in data:
        if settings.WITH_GAMMA:
            coeff = distribution_with_gamma(element, energy)
        else:
            coeff = distribution(element, energy)
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
