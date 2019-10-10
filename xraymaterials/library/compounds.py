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

    g["polyoxymethylene"] = Material.from_compound("CH2O", 1.41) # density: wikipedia.  Delrin!
    g["delrin"] = g["polyoxymethylene"]


    # Components of C4
    g["rdx"] = Material.from_compound("C3H6N6O6", 1.858) # wikipedia
    g["dioctyl_sebacate"] = Material.from_compound("C26H50O4", 0.9) # wikipedia
    g["polyisobutylene"] = Material.from_compound("C4H8", 0.92) # wikipedia; density has a range

    # Liang et al.
    # Comprehensive chemical characterization of lubricating oils used in modern vehicular engines utilizing GC × GC-TOFMS
    # Fuel 220, 2018
    # This paper says that cyclohexene fragments are among the most common found
    # using gas chromatography of motor oils.  I need motor oil properties
    # for C4.
    g["cyclohexene"] = Material.from_compound("C6H10") # Density unknown!!!!

    globals().update(g)


def list():
    return [k for k in _g.keys()]

_init()

