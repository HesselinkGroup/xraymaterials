from .material import Material as _Material
from .elements import ELEMENTS as _ELEMENTS

def _create_elements():
    g = globals()
    for elem in _ELEMENTS:
        g[elem.name.lower()] = _Material.from_element(elem.symbol)

_create_elements()

