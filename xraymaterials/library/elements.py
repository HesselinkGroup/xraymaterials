from ..material import Material as _Material
from ..elements import ELEMENTS as _ELEMENTS
from .compounds import *

def _create_elements():
    g = globals()
    for z in range(1,93):
        elem = _ELEMENTS[z]
        g[elem.name.lower()] = _Material.from_element(elem.symbol)

_create_elements()

def list():
    return [_ELEMENTS[z].name.lower() for z in range(1,93)]