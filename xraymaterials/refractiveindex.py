import re
import numpy as np
import scipy.constants
import pandas

from . import elements
from . import loaddata
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


def calculate_mass_coefficient(symbols, element_density_g_cc, property_name, energy_keV=None):
    """
    Calculate one of the density-normalized properties for a mixture of elements:
        mu_rho_pe_cm2_g:    mass photoelectric attenuation coefficient
        sigma_rho_cm2_g:    total scattering cross-section
        mu_rho_tot_cm2_g:   mass attenuation coefficient
        mu_rho_K_cm2_g:     mass K-shell attenuation coefficient (part of PE)

    Parameters:
        symbols: array-like
            Atomic numbers or symbols of constituent elements
        element_density_g_cc: array-like
            Densities of constituent elements, in g/cm^3
        property_name: str
            One of the properties listed above
        energy_keV: array-like
            Energies at which to calculate n and mu, in keV

    Returns:
        property_value: array-like
            Attenuation or other desired coefficient
        energy_keV: array-like
            Energies at which property is provided
    """
    if energy_keV is not None:
        energy_keV = np.asarray(energy_keV)

    valid_property_names = ["mu_rho_pe_cm2_g", "sigma_rho_cm2_g", "mu_rho_tot_cm2_g", "mu_rho_K_cm2_g"]
    if property_name not in valid_property_names:
        raise Exception('Invalid property name {}, should be one of {}'.format(property_name, valid_property_names))

    total_mu = None
    
    for (elem_name, elem_density) in zip(symbols, element_density_g_cc):
        if isinstance(elem_name, int):
            elem_name = elements.ELEMENTS[elem_name].symbol
        
        df = loaddata.load_element(elem_name)

        if energy_keV is None:
            energy_keV = df.energy_keV.values
            mu_rho = df[property_name].values
        else:
            mu_rho = np.interp(energy_keV, df.energy_keV.values, df[property_name].values)
        
        if total_mu is None:
            total_mu = mu_rho * elem_density
        else:
            total_mu += mu_rho * elem_density
    
    return total_mu, energy_keV



def calculate_mu(symbols, elem_g_cc=None, elem_n_cc=None, energy_keV=None):
    """
    Calculate the total attenuation coefficient for a mixture of elements.

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
        mu: array-like
            Attenuation coefficient, 1/cm
        energy_keV: array-like
            Energies at which mu is provided
    """
    if elem_n_cc is not None:
        if elem_g_cc is not None:
            raise Exception("Only one of elem_g_cc and elem_n_cc can be given")
        elem_g_cc = stoichiometry.mass_density(z, elem_n_cc)

    return calculate_mass_coefficient(symbols, elem_g_cc, "mu_rho_tot_cm2_g", energy_keV)


def calculate_n(symbols, elem_g_cc=None, elem_n_cc=None, energy_keV=None):
    """
    Calculate the refractive index for a mixture of elements.

    Parameters:
        z: array-like
            Atomic numbers or symbols of constituent elements
        elem_g_cc: array-like
            Densities of constituent elements, in g/cm^3
        elem_n_cc: array-like
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

    if elem_g_cc is not None:
        if elem_n_cc is not None:
            raise Exception("Only one of elem_g_cc and elem_n_cc can be given")
        elem_n_cc = stoichiometry.number_density(symbols, elem_g_cc)
    
    for (elem_name, n_cc) in zip(symbols, elem_n_cc):
        if isinstance(elem_name, int):
            elem_name = elements.ELEMENTS[elem_name].symbol
        
        df = loaddata.load_element(elem_name)
        
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
        elem_g_cc = stoichiometry.mass_density(z, elem_n_cc)
    elif elem_g_cc is not None:
        elem_n_cc = stoichiometry.number_density(z, elem_g_cc)
    
    mu, energy_keV = calculate_mu(z, elem_g_cc, energy_keV)
    delta, beta, _ = calculate_n(z, elem_n_cc=elem_n_cc, energy_keV=energy_keV)
    
    return delta, beta, mu, energy_keV


