import re
import numpy as np
import scipy.constants
import pandas

from . import elements
from . import loadcsv

def calculate_number_density_per_cc(element):
    amu_kg = scipy.constants.atomic_mass
    density_g_cc = element.density
    atomic_mass_g = element.mass * scipy.constants.atomic_mass / scipy.constants.gram
    number_density = density_g_cc / atomic_mass_g
    return number_density

def energy_to_wavelength_m(energy_eV):
    energy_J = energy_eV * scipy.constants.electron_volt
    angular_frequency = energy_J / scipy.constants.hbar
    lambda_m = 2*np.pi*scipy.constants.c/angular_frequency
    return lambda_m

_electron_radius_cm = scipy.constants.physical_constants["classical electron radius"][0] * 1e2
def calculate_refractive_index(energy_keV, number_density_cc, f1, f2):
    lambda_cm = energy_to_wavelength_m(energy_keV * 1e3) * 1e2
    beta = (_electron_radius_cm/(2*np.pi)) * lambda_cm**2 * number_density_cc * f2
    delta = (_electron_radius_cm/(2*np.pi)) * lambda_cm**2 * number_density_cc * f1
    return beta, delta

def calculate_atomic_masses(formula):
    element_pattern = re.compile(r"([A-Z][a-z]?)([0-9]*)")
    tokens = element_pattern.findall(formula)
    
    element_symbols = []
    element_mass_total = []
    element_count = []
    
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
    
    return element_symbols, element_mass_total, element_count

def calculate_element(elem_name, energy_keV=None):

    elem = elements.ELEMENTS[elem_name]
    return calculate_compound(elem_name, elem.density, energy_keV)


def calculate_compound(formula, density_g_cc, energy_keV=None):
    
    symbols, mol_weights, numbers = calculate_atomic_masses(formula)
    atomic_mass_g = np.asarray(mol_weights) * scipy.constants.atomic_mass / scipy.constants.gram
    total_mass_g = atomic_mass_g.sum()
    total_number = np.asarray(numbers).sum()
    total_number_density_cc = density_g_cc / total_mass_g
    
    beta = None
    delta = None

    if energy_keV is not None:
        energy_keV = np.asarray(energy_keV)
    
    for (elem_name, elem_count) in zip(symbols, numbers):
        df = loadcsv.load_element(elem_name)
        
        n_cc = total_number_density_cc * elem_count

        if energy_keV is None:
            energy_keV = df.energy_keV.values
            f1 = df.f1_e_atom.values
            f2 = df.f2_e_atom.values
        else:
            f1 = np.interp(energy_keV, df.energy_keV.values, df.f1_e_atom.values)
            f2 = np.interp(energy_keV, df.energy_keV.values, df.f2_e_atom.values)
        
        b, d = calculate_refractive_index(energy_keV, n_cc, f1, f2)
        
        if beta is not None:
            beta += b
            delta += d
        else:
            beta = b
            delta = d
    
    return beta, delta, energy_keV
