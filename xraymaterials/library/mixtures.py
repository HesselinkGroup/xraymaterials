
_g = dict()

def _init():
    from ..material import Material as Material
    from .elements import carbon, oxygen, hydrogen, nitrogen, lead, tin, nickel, manganese, chromium, iron, silicon, zinc, copper, phosphorus
    from .compounds import cellulose, water, fructose, glucose, sucrose, maltose, gluconic_acid, water, acetic_acid

    global _g
    g = _g

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

    # From Bill:
    #   I think .25 is pretty good.
    #   If you think about the weight of a fully packed suitcase and divide by the volume, I think you will find it's close.
    #   I have no source for this, but I have picked up a hell of a lot of suitcases.  (literally thousands)

    g["cotton_clothes_packed"] = cellulose.as_density(0.25)

    # ==== Woods

    live_oak_g_cc = 0.977
    white_oak_g_cc = 0.710
    sugar_maple_g_cc = 0.676
    jack_pine_g_cc = 0.461
    wood = Material.sum_by_mass([carbon, oxygen, hydrogen, nitrogen], [50, 42, 6, 1])

    g["live_oak"] = wood.as_density(live_oak_g_cc)
    g["white_oak"] = wood.as_density(white_oak_g_cc)
    g["sugar_maple"] = wood.as_density(sugar_maple_g_cc)
    g["jack_pine"] = wood.as_density(jack_pine_g_cc)

    # ==== Metal alloys

    # https://www.makeitfrom.com/material-properties/As-Forged-and-Air-Cooled-M10-C46400-Brass
    g["naval_brass"] = Material.sum_by_mass([lead, tin, zinc, copper], [0.5, 0.5, 38, 61], final_density_g_cc=8.0)

    # https://www.makeitfrom.com/material-properties/EN-CC481K-CuSn11P-C-Phosphor-Bronze
    g["phosphor_bronze"] = Material.sum_by_mass([tin, phosphorus, copper], [11.0, 1.0, 88.0], final_density_g_cc=8.7)

    # https://www.makeitfrom.com/material-properties/Half-Hard-201-Stainless-Steel
    g["stainless_steel"] = Material.sum_by_mass([silicon, nickel, manganese, chromium, iron], [0.5, 4.5, 6.5, 17, 71.5], final_density_g_cc=7.7)


    # ==== Foodstuffs

    # From Ball 2007, I will take the water and monosaccharide components and then
    # just replace the other disaccharides with glucose.  Maltose for instance can
    # be a big component of honey and has effects on its crystallization.

    honey_g_cc = 1.415 # 0.5*(1.38 + 1.45) per wikipedia
    g["honey"] = Material.sum_by_mass([water, fructose, glucose, sucrose, maltose, gluconic_acid],
                        [17.2, 38.4, 30.3, 1.3, 8.7, 0.57],
                        honey_g_cc)

    # Generic vinegar: FDA regulations state minimum of 5% acidity (http://www.chem.latech.edu/~deddy/chem122m/L04U00Vinegar122.htm)
    g["vinegar"] = Material.sum_by_mass([water, acetic_acid], [0.95, 0.05], 1.05) # density: google

    # https://www.simplyrecipes.com/a_guide_to_balsamic_vinegar/
    # To qualify for official recognition, Balsamic Vinegar of Modena can only be made with the following ingredients:
    # - Boiled or concentrated grape must (at least 20% by volume) 
    # - Wine vinegar (at least 10%)
    # - Natural caramel (made by cooking sugar) for color (up to 2%)
    # - Aged balsamic vinegar (aged at least 10 years), an unspecified amount, usually negligible



    # ==== Explosives

    # C4 with RDX:
    # 91% RDX
    # 5.3% DOS
    # 2.1% PIB
    # 1.6% motor oil
    # Nominal density 1.72658 g/cc
    # (Wikipedia)

    from .compounds import rdx, dioctyl_sebacate, polyisobutylene, cyclohexene
    g["c4_rdx"] = Material.sum_by_mass([rdx, dioctyl_sebacate, polyisobutylene, cyclohexene], 
                                       [91.0, 5.3, 2.1, 1.6], 1.72658)


    globals().update(g)


def list():
    return [k for k in _g.keys()]

_init()
