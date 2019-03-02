import re
import numpy as np
import scipy.constants
from . import elements
from . import loaddata


# TODO: consider whether this function is necessary and/or should be renamed
def compound_number_densities(formula, total_density_g_cc):
    """
    Calculate the number densities of elements in a compound

    Parameters:
        formula: chemical formula, capitalization-sensitive, e.g. "H2O"
        total_density_g_cc: mass density of the compound, e.g. 0.997

    Returns:
        elements: list of element symbols, e.g. ["H", "O"]
        number_density_cc: list of number densities in units of 1/cc
    """
    elements, numbers, atomic_masses = calculate_stoichiometry(formula)
    element_mass_g = np.multiply(numbers, atomic_masses) * scipy.constants.atomic_mass / scipy.constants.gram
    mol_mass_g = element_mass_g.sum()
    mol_number_density_cc = total_density_g_cc / mol_mass_g
    
    return elements, np.multiply(numbers, mol_number_density_cc)


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



def number_density(symbols, density_g_cc):
    """
    Convert mass density to number density for a list of elements.

    Parameters:
        symbols: array-like
            Atomic symbols or atomic numbers, e.g.
                ['He', 'Li', 'U'] or [2, 3, 92]
        density_g_cc: array-like
            Mass densities of given elements in units of g/cc

    Returns:
        number_density_cc: array-like
            Number densities of given elements in units of 1/cc 
    """
    if len(symbols) != len(density_g_cc):
        raise Exception("Number of symbols does not match number of densities")

    density_g_cc = np.asarray(density_g_cc)
    number_density_cc = np.empty_like(density_g_cc)
    
    for ii,(elem_name,elem_density_g_cc) in enumerate(zip(symbols, density_g_cc)):
        if isinstance(elem_name, int):
            elem_name = elements.ELEMENTS[elem_name].symbol
        
        elem_mass_g = elements.ELEMENTS[elem_name].mass * scipy.constants.atomic_mass / scipy.constants.gram
        
        n_cc = elem_density_g_cc / elem_mass_g
        number_density_cc[ii] = n_cc
    
    return number_density_cc
        

def mass_density(symbols, number_density_cc):
    """
    Convert number density to mass density for a list of elements.

    Parameters:
        symbols: array-like
            Atomic symbols or atomic numbers, e.g.
                ['He', 'Li', 'U'] or [2, 3, 92]
        number_density_cc: array-like
            Number densities of given elements in units of 1/cc 

    Returns:
        density_g_cc: array-like
            Mass densities of given elements in units of g/cc
    """
    if len(symbols) != len(number_density_cc):
        raise Exception("Number of symbols does not match number of densities")

    number_density_cc = np.asarray(number_density_cc)
    density_g_cc = np.empty_like(number_density_cc)
    
    for ii,(elem_name,elem_n_cc) in enumerate(zip(symbols, number_density_cc)):
        if isinstance(elem_name, int):
            elem_name = elements.ELEMENTS[elem_name].symbol
        
        elem_mass_g = elements.ELEMENTS[elem_name].mass * scipy.constants.atomic_mass / scipy.constants.gram
        elem_density_g_cc = elem_n_cc * elem_mass_g
        density_g_cc[ii] = elem_density_g_cc
    
    return density_g_cc


def _test_density():
    rho_in = [1.0, 2.0]
    n = number_density(["H", "O"], rho_in)
    rho_out = mass_density([1, 8], n)
    np.testing.assert_array_almost_equal(rho_in, rho_out)


