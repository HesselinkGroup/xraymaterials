from ..material import Material as Material
from .compounds import *
from .elements import *

__all__ = [
    "cotton_clothes_packed",
    "live_oak", "white_oak", "sugar_maple", "jack_pine",
    "naval_brass", "phosphor_bronze", "stainless_steel"]

# Density of textile fibers can be done with a gradient column:
# http://fashion2apparel.blogspot.com/2016/12/important-textile-fibers-densities.html
# These values range from 1.55 g/cc for cotton, down to 0.9 g/cc for polypropylene (Meraklon).
# (Meraklon is for diapers and other hygiene products.  tmyk)
# These densities are unhelpful for clothing in suitcases, sadly.

# A bale of cotton is around 450 kg/m^3 or 0.45 g/cc.

# https://cerasis.com/calculate-freight-class/ referring to the NMFC book about freight classes
# 4-6 lbs/cubic foot
clothing_density_NMFC_g_cc = 0.096
clothing_density_Bill_g_cc = 0.25 # I think Bill said 0.25 g/cc was about right for clothes

# Detection of explosive materials using nuclear radiation, a critical review, Hussein 1992 cites
# W.J.Rof,J.R.Scot,J.Paciti,HandbokofComonPolymers:Fibres,Films,PlasticsandRubers,CRC Pres,Cleveland,1971.
# Mass density of silk/wool cloths: 200 kg/m3 = 0.2 g/cc
# 

cotton_clothes_packed = cellulose.as_density(0.25)

96.1107802 *1e3 * 1e-6

# ==== Woods

live_oak_g_cc = 0.977
white_oak_g_cc = 0.710
sugar_maple_g_cc = 0.676
jack_pine_g_cc = 0.461
wood = Material.sum_by_mass([carbon, oxygen, hydrogen, nitrogen], [50, 42, 6, 1])

live_oak = wood.as_density(live_oak_g_cc)
white_oak = wood.as_density(white_oak_g_cc)
sugar_maple = wood.as_density(sugar_maple_g_cc)
jack_pine = wood.as_density(jack_pine_g_cc)

# ==== Metal alloys

# https://www.makeitfrom.com/material-properties/As-Forged-and-Air-Cooled-M10-C46400-Brass
naval_brass = Material.sum_by_mass([lead, tin, zinc, copper], [0.5, 0.5, 38, 61], final_density_g_cc=8.0)

# https://www.makeitfrom.com/material-properties/EN-CC481K-CuSn11P-C-Phosphor-Bronze
phosphor_bronze = Material.sum_by_mass([tin, phosphorus, copper], [11.0, 1.0, 88.0], final_density_g_cc=8.7)

# https://www.makeitfrom.com/material-properties/Half-Hard-201-Stainless-Steel
stainless_steel = Material.sum_by_mass([silicon, nickel, manganese, chromium, iron], [0.5, 4.5, 6.5, 17, 71.5], final_density_g_cc=7.7)


