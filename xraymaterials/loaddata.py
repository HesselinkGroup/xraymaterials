import os
import pandas
import glob
import json

pwd = os.path.dirname(os.path.abspath(__file__))
icru44_dir = os.path.join(pwd, "icru44")
elements_dir = os.path.join(pwd, "elements")
mixtures_dir = os.path.join(pwd, "mixtures")

def _list_files(dir):
    files = glob.glob(os.path.join(dir, "*.txt"))
    return [os.path.splitext(os.path.basename(file))[0] for file in files]

def _load_csv_file(dir, file_name):
    ext = os.path.splitext(file_name)
    if len(ext[1]) == 0:
        fname = file_name + ".txt"
    else:
        fname = file_name
    
    df = pandas.read_csv(os.path.join(dir, fname))
    return df


def list_icru44():
    """
    Return a list of known ICRU-44 material names.

    Valid ICRU-44 names can be input to load_icru44.
    """
    return _list_files(icru44_dir)

def list_elements():
    """
    Return a list of supported elements for load_element.

    Valid element names can be input to load_element.
    """
    return _list_files(elements_dir)

def load_element(element_name):
    """
    Return element xray properties in Pandas dataframe.

    xraymaterials knows f1, f2 and several absorption coefficients for a range
    of energies from about 2 keV to 430 keV.
    """
    return _load_csv_file(elements_dir, element_name)

def load_icru44_absorption(material_name):
    """
    Return ICRU-44 material xray properties in Pandas dataframe.

    xraymaterials knows the absorption coefficient for ICRU-44 materials for a
    range of energies from about 1 keV to 20 meV.  The fractional composition by
    mass of ICRU-44 materials is available from load_icru44_composition.
    """
    return _load_csv_file(icru44_dir, material_name)

def load_icru44_composition(material_name):
    """
    Return ICRU-44 material fractional composition by mass.

    Returns a dict with the following fields:
        material: name of ICRU-44 material
        density_g_cc: mass density of material
        z: atomic numbers of elements in the mixture
        fraction: fraction by mass of each constituent element
    """
    with open(os.path.join(pwd, "mixtures", "material_composition.txt")) as fh:
        s = json.load(fh)
        kvs = [(entry["material"], entry) for entry in s]
        s_dict = dict(kvs)
    entry = s_dict[material_name]
    return entry