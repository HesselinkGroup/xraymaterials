from ..material import Material as _Material
from ..elements import ELEMENTS as _ELEMENTS
from .compounds import *

def _create_elements():
    g = globals()
    for elem in _ELEMENTS:
        g[elem.name.lower()] = _Material.from_element(elem.symbol)

_create_elements()

def list():
    return [elem.name.lower() for elem in _ELEMENTS]