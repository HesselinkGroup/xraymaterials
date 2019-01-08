"""
Calculate properties of mixtures, compounds and elements of use for simulating
xray propagation through materials.

The most useful functions are imported into the xraymaterials namespace.

xraymaterials contains the excellent elements.py by Christoph Gohlke.
"""

from .refractiveindex import calculate_mu, calculate_n, calculate_n_mu
from .stoichiometry import calculate_stoichiometry, compound_number_densities
from .loaddata import list_icru44, list_elements, load_element, load_icru44_absorption, load_icru44_composition
from . import elements