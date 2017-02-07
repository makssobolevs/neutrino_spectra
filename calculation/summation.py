import math


def distribution(element, energy):
    qbeta = element['qmax'] * 1E-3
    m_e = 0.511
    if energy > qbeta:
        return 0
    elif qbeta - energy > m_e:
        mult1 = energy * energy * (qbeta - energy)
        mult2 = math.sqrt(math.pow(qbeta - energy, 2) - m_e * m_e)
        return mult1 * mult2
    else:
        return 0


def coefficient(element, time, parent_coeff=0):
    try:
        hl = element['hl']
        l = math.log(2) / hl
        coeff = math.exp(-l * time)
        if 'y' in element:
            result = (1 - coeff) * element['y'] / 2
        else:
            result = (1 - coeff) * parent_coeff
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
        coeff = coefficient(element, time)
        s += coeff * distribution(element, energy)
        for child in element['chain']:
            coeff = coefficient(child, time, coeff)
            try:
                s += coeff * distribution(child, energy)
            except ValueError:
                print(child)
            except TypeError as e:
                print(e)
                print(child)
    return s
