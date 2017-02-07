import scipy.constants as const
from enum import Enum

# ALPHA = const.alpha
# ELECTRON_MASS = const.physical_constants['electron mass energy equivalent in MeV'][0]
# HBAR = const.hbar
ALPHA = const.alpha
ELECTRON_MASS = 1
HBAR = 1


class Database(Enum):
    JENDL = 1
    ENDF = 2
    ROSFOND = 3
    AME2012 = 4
