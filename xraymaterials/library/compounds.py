"""Some materials specified by their chemical formulas.
"""

_g = dict()

def _init():
    from ..material import Material as Material

    global _g
    g = _g


    g["water"] = Material.from_compound("H2O", 1.0)
    g["acetic_acid"] = Material.from_compound("C2H4O2", 1.049) # density: wikipedia

    # Lipids
    g["triolein"] = Material.from_compound("C57H104O6")

    # Sugars
    g["sucrose"] = Material.from_compound("C12H22O11")
    g["fructose"] = Material.from_compound("C6H12O6")
    g["glucose"] = Material.from_compound("C6H12O6")
    g["maltose"] = Material.from_compound("C12H22O11")

    g["gluconic_acid"] = Material.from_compound("C6H12O7")

    # Amino acids
    g["arginine"] = Material.from_compound("C6H14N4O2")
    g["histidine"] = Material.from_compound("C6H9N3O2")

    # Polysaccharides
    g["cellulose"] = Material.from_compound("C6H10O5", 1.5) # density: Wikipedia

    # Polymers
    g["polyethylene_terephthalate"] = Material.from_compound("C10H8O4", 1.38) # density: Wikipedia

    globals().update(g)


def list():
    return [k for k in _g.keys()]

_init()

