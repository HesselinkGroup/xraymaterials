"""Some materials specified by their chemical formulas.
"""

from ..material import Material as Material

__all__ = ["triolein",
    "sucrose", "fructose", "glucose", "maltose", "gluconic_acid",
    "arginine", "histidine",
    "cellulose", "polyethylene_terephthalate"]

# Lipids
triolein = Material.from_compound("C57H104O6")

# Sugars
sucrose = Material.from_compound("C12H22O11")
fructose = Material.from_compound("C6H12O6")
glucose = Material.from_compound("C6H12O6")
maltose = Material.from_compound("C12H22O11")

gluconic_acid = Material.from_compound("C6H12O7")

# Amino acids
arginine = Material.from_compound("C6H14N4O2")
histidine = Material.from_compound("C6H9N3O2")

# Polysaccharides
cellulose = Material.from_compound("C6H10O5", 1.5) # density: Wikipedia

# Polymers
polyethylene_terephthalate = Material.from_compound("C10H8O4", 1.38) # density: Wikipedia


