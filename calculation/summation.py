import math
import setup
from scipy import integrate

cache = {}


def get_normalization_natural(nuclide):
    qmax = nuclide['q']
    return nuclide['l'] * get_normalization_for_distribution(nuclide, qmax)


def get_normalization_for_distribution(element, qmax):
    result = 0.0
    key = str(element['a']) + str(element['s']) + str(qmax)
    if key in cache:
        result = cache[key]
    else:
        def func(e):
            return distribution_for_q(element, e, qmax)
        integral_result = integrate.quad(func, 0, qmax - 0.511)
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
    try:
        qbeta = element['q']
    except TypeError:
        qbeta = 1
    return distribution_for_q(element, energy, qbeta)


def distribution_for_q(element, energy, qbeta):
    from phys_functions import fermi_function

    m_e = 0.511
    if energy > qbeta:
        return 0.0
    elif qbeta - energy > m_e:
        mult1 = energy * energy * (qbeta - energy)
        mult2 = math.sqrt(math.pow(qbeta - energy, 2) - m_e * m_e)
        result = mult1 * mult2
        if setup.WITH_FERMI:
            return result * fermi_function(element['z'], element['a'], qbeta - energy)
        else:
            return result
    else:
        return 0.0


def lmbd(element):
    hl = element['hl']
    l = math.log(2) / hl
    return l


def populate_lmdb(data):
    for branch in data:
        for el in branch['branch']:
            el['l'] = lmbd(el)


def populate_lmdb_cfy(data):
    for element in data:
        nuclide = element['nuclide']
        nuclide['l'] = lmbd(nuclide)
        nuclide['z'] = element['z']


def bateman_solving(elements, n, t):
    mult1 = 1
    branch = elements['branch']
    mult1 *= elements['y']
    for j in range(0, n):
        mult1 *= lmbd(branch[j]) * branch[j]['ratio']
    sum1 = 0
    for j in range(0, n + 1):
        mult2 = 1
        for p in range(n + 1):
            if p != j:
                mult2 *= branch[p]['l'] - branch[j]['l']
        if mult2 != 0.0:
            sum1 += math.exp(- branch[j]['l'] * t) / mult2
    mult1 *= sum1
    return mult1


def bateman_solving_with_source(elements, n, t):
    mult1 = 1
    branch = elements['branch']
    power = 1200E6
    q0 = 3.244E-11
    source = elements['y']
    mult1
    for j in range(0, n):
        mult1 *= lmbd(branch[j])
    sum1 = 0
    for j in range(0, n + 1):
        mult2 = 1
        for p in range(n + 1):
            if p != j:
                mult2 *= branch[p]['l'] - branch[j]['l']
        if mult2 != 0.0:
            sum1 += elements['y'] * math.exp(- branch[j]['l'] * t) / mult2
            sum1 += source * (1 - math.exp(-branch[j]['l'] * t)) / (branch[j]['l'] * mult2)
    mult1 *= sum1
    return mult1


def get_spectrum_for_nuclide(nuclide, energy):
    s = distribution_for_q(nuclide, energy, nuclide['q'])
    k = get_normalization_for_distribution(nuclide, nuclide['q'])
    # k = get_normalization_natural(nuclide)
    s *= k
    if 'ratio' in nuclide:
        s *= nuclide['ratio']
    return s


def get_spectrum_for_nuclide_with_branches(nuclide, energy):
    qmax = nuclide['q']
    s = 0
    p = 0
    for b in nuclide['branches']:
        e = b['e']
        ib = b['ib']
        coeff = distribution_for_q(nuclide, energy, qmax - e)
        k = get_normalization_for_distribution(nuclide, qmax - e)
        coeff = coeff * k * ib
        s += coeff
        p += ib
    if p < nuclide['ratio']:
        ib = nuclide['ratio'] - p
        coeff = distribution_for_q(nuclide, energy, qmax)
        k = get_normalization_for_distribution(nuclide, qmax)
        coeff = coeff * k * ib
        s += coeff
    return s


def get_spectrum_value_for_branch(element, energy, time):
    branch = element['branch']

    s1 = 0
    for i in range(0, len(branch)):
        if setup.WITH_GAMMA:
            s = get_spectrum_for_nuclide_with_branches(branch[i], energy)
        else:
            s = get_spectrum_for_nuclide(branch[i], energy)
        s1 += (element['y'] - bateman_solving(element, i, time)) * s
    return s1


def get_spectrum_value_for_element_cfy(element, energy):
    """
    Cumulative fission yield present as for radioactive and stable
    nuclide and has yield which was received by summation of 
    the yield of all decay branches and direct product.
    There is no need to know full decay branch.    
    :param element: 
    :param energy: 
    :return: spectrum value
    """
    nuclide = element['nuclide']
    # setup.WITH_FERMI = True
    if setup.WITH_GAMMA:
        s = get_spectrum_for_nuclide_with_branches(nuclide, energy)
        return element['y'] * s
    else:
        s = get_spectrum_for_nuclide(nuclide, energy)
        return element['y'] * s


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
