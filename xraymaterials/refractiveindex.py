import re
import numpy as np
import scipy.constants
import pandas

from . import elements
from . import loadcsv
from . import stoichiometry

def _energy_to_wavelength_m(energy_eV):
    energy_J = energy_eV * scipy.constants.electron_volt
    angular_frequency = energy_J / scipy.constants.hbar
    lambda_m = 2*np.pi*scipy.constants.c/angular_frequency
    return lambda_m

_electron_radius_cm = scipy.constants.physical_constants["classical electron radius"][0] * 1e2
def _calculate_refractive_index(energy_keV, number_density_cc, f1, f2):
    lambda_cm = _energy_to_wavelength_m(energy_keV * 1e3) * 1e2
    beta = (_electron_radius_cm/(2*np.pi)) * lambda_cm**2 * number_density_cc * f2
    delta = (_electron_radius_cm/(2*np.pi)) * lambda_cm**2 * number_density_cc * f1
    return beta, delta

def calculate_stoichiometry(formula):
    """
    Calculate the atomic composition of a molecule.

    Parameters:
        formula: chemical formula, capitalization-sensitive, e.g. "H2O"

    Returns:
        element_symbols:   list of chemical symbols e.g. ["H", "O"]
        element_count:     list of numbers of atoms of each element, e.g. [2, 1]
        element_mass:      list of atomic masses of each element, e.g. [1.00794, 15.9994]
    """
    element_pattern = re.compile(r"([A-Z][a-z]?)([0-9]*)")
    tokens = element_pattern.findall(formula)
    
    element_symbols = []
    element_mass_total = []
    element_count = []
    element_mass = []
    
    for (elem_name, elem_number) in tokens:
        
        if elem_name not in elements.ELEMENTS:
            raise Exception(f"Cannot find element '{elem_name}'.  Check capitalization?")
        elem_record = elements.ELEMENTS[elem_name]
        
        element_symbols.append(elem_name)
        if elem_number:
            elem_number = int(elem_number)
        else:
            elem_number = 1
            
        element_count.append(elem_number)
        
        element_mass_total.append(elem_record.mass * elem_number)
        element_mass.append(elem_record.mass)
    
    return element_symbols, element_count, element_mass


def calculate_mu(symbols, element_density_g_cc, energy_keV=None):
    """
    Calculate the refractive index and total attenuation coefficient for a mixture
    of elements.

    Parameters:
        z: array-like
            Atomic numbers or symbols of constituent elements
        element_density_g_cc: array-like
            Densities of constituent elements, in g/cm^3
        energy_keV: array-like
            Energies at which to calculate n and mu, in keV

    Returns:
        mu: array-like
            Attenuation coefficient, 1/cm
        energy_keV: array-like
            Energies at which refractive index is provided
    """
    if energy_keV is not None:
        energy_keV = np.asarray(energy_keV)
        
    total_mu = None
    
    for (elem_name, elem_density) in zip(symbols, element_density_g_cc):
        if isinstance(elem_name, int):
            elem_name = elements.ELEMENTS[elem_name].symbol
        
        df = loadcsv.load_element(elem_name)

        if energy_keV is None:
            energy_keV = df.energy_keV.values
            mu_rho = df.mu_rho_tot_cm2_g.values
        else:
            mu_rho = np.interp(energy_keV, df.energy_keV.values, df.mu_rho_tot_cm2_g.values)
        
        if total_mu is None:
            total_mu = mu_rho * elem_density
        else:
            total_mu += mu_rho * elem_density
    
    return total_mu, energy_keV


def calculate_n(symbols, element_number_density_cc, energy_keV=None):
    """
    Calculate the refractive index for a mixture of elements.

    Parameters:
        z: array-like
            Atomic numbers or symbols of constituent elements
        elem_number_density_cc: array-like
            Number densities of constituent elements, in 1/cm^3
        energy_keV: array-like
            Energies at which to calculate n, in keV

    Returns:
        delta: array-like
            Refraction index decrement such that n = 1 - delta - 1j*beta
        beta: array-like
            Imaginary part of refractive index such that n = 1 - delta - 1j*beta
        energy_keV: array-like
            Energies at which refractive index is provided
    """
    beta = None
    delta = None

    if energy_keV is not None:
        energy_keV = np.asarray(energy_keV)
    
    for (elem_name, n_cc) in zip(symbols, element_number_density_cc):
        if isinstance(elem_name, int):
            elem_name = elements.ELEMENTS[elem_name].symbol
        
        df = loadcsv.load_element(elem_name)
        
        if energy_keV is None:
            energy_keV = df.energy_keV.values
            f1 = df.f1_e_atom.values
            f2 = df.f2_e_atom.values
        else:
            f1 = np.interp(energy_keV, df.energy_keV.values, df.f1_e_atom.values)
            f2 = np.interp(energy_keV, df.energy_keV.values, df.f2_e_atom.values)
        
        b, d = _calculate_refractive_index(energy_keV, n_cc, f1, f2)
        
        if beta is not None:
            beta += b
            delta += d
        else:
            beta = b
            delta = d
    
    return delta, beta, energy_keV

def calculate_n_mu(z, elem_g_cc=None, elem_n_cc=None, energy_keV=None):
    """
    Calculate the refractive index and total attenuation coefficient for a mixture
    of elements.

    Either of elem_g_cc (element mass density in g/cc) or elem_n_cc (element number
    density in 1/cc) may be given.

    Parameters:
        z: array-like
            Atomic numbers or symbols of constituent elements
        elem_g_cc: array-like
            Densities of constituent elements, in g/cm^3
        elem_n_cc: array-like
            Number densities of constituent elements, in 1/cm^3
        energy_keV: array-like
            Energies at which to calculate n and mu, in keV

    Returns:
        delta: array-like
            Refraction index decrement such that n = 1 - delta - 1j*beta
        beta: array-like
            Imaginary part of refractive index such that n = 1 - delta - 1j*beta
        mu: array-like
            Attenuation coefficient, 1/cm
        energy_keV: array-like
            Energies at which refractive index is provided
    """
    if elem_n_cc is not None:
        if elem_g_cc is not None:
            raise Exception("Only one of elem_g_cc and elem_n_cc may be provided")
        elem_g_cc = stoichiometry.density(z, elem_n_cc)
    elif elem_g_cc is not None:
        elem_n_cc = stoichiometry.number_density(z, elem_g_cc)
    
    mu, energy_keV = calculate_mu(z, elem_g_cc, energy_keV)
    delta, beta, _ = calculate_n(z, elem_n_cc, energy_keV)
    
    return delta, beta, mu, energy_keV


# def calculate_element(elem_name, energy_keV=None):

#     elem = elements.ELEMENTS[elem_name]
#     return calculate_compound(elem_name, elem.density, energy_keV)


# def calculate_compound(formula, density_g_cc, energy_keV=None):
    
#     symbols, numbers, atomic_masses = calculate_stoichiometry(formula)

#     element_mass_g = np.multiply(numbers, atomic_masses) * scipy.constants.atomic_mass / scipy.constants.gram
#     total_mass_g = element_mass_g.sum()
#     total_number = np.asarray(numbers).sum()
#     total_number_density_cc = density_g_cc / total_mass_g
    
#     beta = None
#     delta = None

#     if energy_keV is not None:
#         energy_keV = np.asarray(energy_keV)
    
#     for (elem_name, elem_count) in zip(symbols, numbers):
#         df = loadcsv.load_element(elem_name)
        
#         n_cc = total_number_density_cc * elem_count

#         if energy_keV is None:
#             energy_keV = df.energy_keV.values
#             f1 = df.f1_e_atom.values
#             f2 = df.f2_e_atom.values
#         else:
#             f1 = np.interp(energy_keV, df.energy_keV.values, df.f1_e_atom.values)
#             f2 = np.interp(energy_keV, df.energy_keV.values, df.f2_e_atom.values)
        
#         b, d = calculate_refractive_index(energy_keV, n_cc, f1, f2)
        
#         if beta is not None:
#             beta += b
#             delta += d
#         else:
#             beta = b
#             delta = d
    
#     return beta, delta, energy_keV


# def calculate_icru44(name, density_g_cc, energy_keV=None):

#     df = loadcsv.load_icru44(name)

#     if energy_keV is not None:
#         energy_keV = np.asarray(energy_keV)
#         mu = np.interp(energy_keV*1e-3, df.energy_MeV.values, df.mu_rho_cm2_g.values * density_g_cc)
#     else:
#         energy_keV = df.energy_MeV.values * 1000.0
#         mu = df.mu_rho_cm2_g.values * density_g_cc

#     lambda_cm = _energy_to_wavelength_m(energy_keV*1000.0) * 100
#     beta = mu * lambda_cm / 2.0 / np.pi / 2.0

#     return beta, energy_keV




