import json
import os

dir = os.path.dirname(__file__)
filename = os.path.join(dir, 'parsing/dumps/yields_symbols_qmax.json')


class Element:

    def __init__(self, *initial_data, **kwargs):
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, "_" + key, dictionary[key])
        for key in kwargs:
            setattr(self, "_" + key, kwargs[key])

    def get_export_dict(self):
        s = {}
        for key in self.__dict__.keys():
            k = key[1:]
            s[k] = self.__dict__[key]
        if hasattr(self, "_parent"):
            s['parent'] = self._parent.symbol
        if hasattr(self, "_child"):
            s['child'] = self._child.symbol
        return s

    def __str__(self):
        d = self.get_export_dict()
        return str(d)

    @property
    def decay(self):
        if hasattr(self, "_decay"):
            return self._decay
        else:
            return None

    @decay.setter
    def decay(self, decay):
        self._decay = decay

    @property
    def symbol(self):
        if hasattr(self, "_symbol"):
            return self._symbol
        else:
            return None

    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol

    @property
    def child(self):
        if hasattr(self, "_child"):
            return self._child
        else:
            return None

    @child.setter
    def child(self, child):
        self._child = child

    @property
    def parent(self):
        if hasattr(self, "_parent"):
            return self._parent
        else:
            return None

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def qmax(self):
        if hasattr(self, "_qmax"):
            return self._qmax
        else:
            return None

    @qmax.setter
    def qmax(self, qmax):
        self._qmax = qmax

    @property
    def hl(self):
        if hasattr(self, "_hl"):
            return self._hl
        else:
            return None

    @hl.setter
    def hl(self, hl):
        self._hl = hl

    @property
    def a(self):
        if hasattr(self, "_a"):
            return self._a
        else:
            return None

    @a.setter
    def a(self, a):
        self._a = a

    @property
    def z(self):
        if hasattr(self, "_z"):
            return self._z
        else:
            return None

    @z.setter
    def z(self, z):
        self._z = z


def filter_yields(yields):
    for y in yields:
        if 'qmax' not in y.keys():
            yields.remove(y)
            continue
        if y['qmax'] < 0:
            yields.remove(y)
            continue
        if '%' in str(y['hl']):
            yields.remove(y)
            continue
    return yields

with open(filename) as file:
    yields = json.load(file)
    yields = filter_yields(yields)
    with open("file.json", "w") as f:
        json.dump(yields, f)


elements = []

for y in yields:
    element = Element(y)
    elements.append(element)
