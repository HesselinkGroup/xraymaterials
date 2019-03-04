import os
import json
import numpy as np
from . import loaddata
from .material import Material

def list():
    """
    Return a list of known ICRU-44 material names.

    Valid ICRU-44 names can be input to load().
    """

    with open(os.path.join(loaddata.pwd, "mixtures", "material_composition.txt")) as fh:
        s = json.load(fh)
        names = [entry["material"] for entry in s]

    return names


    # return loaddata.list_files(loaddata.icru44_dir)

def load(material_name):
    """
    Load ICRU-44 material as a Material object.
    """
    try:
        mat_df = loaddata.load_composition(material_name)
    except KeyError as exc:
        raise Exception(f"Material name '{material_name}' is not in ICRU-44 database")
    elem_g_cc = mat_df["density_g_cc"] * np.array(mat_df["fraction"])
    mat = Material(mat_df["z"], elem_g_cc)
    return mat