import constants as CONST
import math
import scipy.special as special


def lambda_var(z, electronEnergy):
    """Lambda convenient variable"""
    return CONST.ALPHA * z * electronEnergy / math.sqrt(math.pow(electronEnergy, 2) - math.pow(CONST.ELECTRON_MASS, 2))


def r_var(a):
    """Nuclei radius"""
    return CONST.ALPHA * math.pow(a, 1/3) / 2


def d_var(z):
    """fission constant"""
    return 1 - math.pow(CONST.ALPHA * z, 2)


def fermi_function(z, a, electronEnergy):
    """fermi function"""
    mult1 = 4 * (1 + d_var(z))
    try:
        mult2 = math.exp(math.pi * lambda_var(z, electronEnergy))
    except OverflowError:
        print("overflow")
        return 1
    p_e = math.sqrt(math.pow(electronEnergy, 2) - math.pow(CONST.ELECTRON_MASS, 2))
    mult3 = 2 * p_e * r_var(a)
    mult4 = math.pow(mult3 / CONST.HBAR, 2 * (d_var(z) - 1))
    mult5 = abs(special.gamma(complex(d_var(z), lambda_var(z, electronEnergy))))
    mult6 = abs(special.gamma(2 * d_var(z) + 1))
    return mult1 * mult2 * mult4 * (mult5 * mult5) / (mult6 * mult6)
