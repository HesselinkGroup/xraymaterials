"""
Calculate properties of mixtures, compounds and elements of use for simulating
xray propagation through materials.

The most useful functions are imported into the xraymaterials namespace.

xraymaterials contains the excellent elements.py by Christoph Gohlke.

Columns of element tables:
    energy_keV:         photon energy
    f1_e_atom:          real part of atomic form factor in eu
    f2_e_atom:          imaginary part of atomic form factor in eu
    mu_rho_pe_cm2_g:    mass photoelectric attenuation coefficient
    sigma_rho_cm2_g:    estimate of coherent and incoherent scattering cross-section sum
    mu_rho_tot_cm2_g:   mass attenuation coefficient
    mu_rho_K_cm2_g:     component of mass PE attenuation coefficient relating to the
                        isolated K-shell orbital
    lambda_nm:          photon wavelength

Columns of ICRU-44 absorption tables:
    energy_MeV:         photon energy
    mu_rho_cm2_g:       mass attenuation coefficient
    muen_rho_cm2_g:     mass energy-absorption coefficient

Properties of ICRU-44 composition tables:
    material:           name of material (e.g. "Alanine")
    density_g_cc:       mass density
    fraction:           fraction by mass of constituent elements
    z:                  atomic numbers of constituent elements
"""

from .refractiveindex import calculate_mu, calculate_n, calculate_n_mu, calculate_mass_coefficient
from .stoichiometry import calculate_stoichiometry, compound_number_densities
from .loaddata import list_icru44, list_elements, load_element, load_icru44_absorption, load_icru44_composition
from . import elements
from .material import Material