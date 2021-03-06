import numpy as np
from . import elements
from .refractiveindex import calculate_n, calculate_mu, calculate_mass_coefficient
from . import stoichiometry
from . import icru44

class Material:
    """
    Representation of materials for purpose of calculating xray absorption and refractive index.
    
    A material is essentially a dict of atomic symbols and mass densities.
    """
    
    def __init__(self, symbols, density_g_cc):
        """
        Create material by specifying elements and densities.
        
        Consider creating new Material instances using the class functions:
        
        Material.from_element()
        Material.from_compound()
        Material.from_vector()
        Material.from_dict()
        
        Args:
            symbols (array-like): List of symbols (e.g. "H") or atomic numbers
            density_g_cc (array-like): List of corresponding densities for each element, in grams per cc.
        """
        self.z = []
        self.g_cc = []
        for s, density in zip(symbols, density_g_cc):
            self.z.append(elements.ELEMENTS[s].number)
            self.g_cc.append(density)
        
    def delta(self, energy_keV):
        """
        Calculate refractive index decrement at given energies.
        The xray refractive index is given by n = 1 - delta - 1j*beta.
        
        energy_keV: photon energies of interest, in keV
        
        Returns: delta corresponding to each energy
        """
        delta, _, _ = calculate_n(self.z, elem_g_cc=self.g_cc, energy_keV=energy_keV)
        return delta
    
    def beta(self, energy_keV):
        """
        Calculate imaginary part of refractive index at given energies.
        The xray refractive index is given by n = 1 - delta - 1j*beta.
        
        energy_keV: photon energies of interest, in keV
        
        Returns: beta corresponding to each energy
        """
        _, beta, _ = calculate_n(self.z, elem_g_cc=self.g_cc, energy_keV=energy_keV)
        return beta
    
    def mu(self, energy_keV):
        """
        Calculate total absorption coefficient at given energies.  (Units: 1/cm)
        The total absorption includes photoelectric and Compton components.
        
        energy_keV: photon energies of interest, in keV
        
        Returns: mu corresponding to each energy
        """
        mu, _ = calculate_mu(self.z, elem_g_cc=self.g_cc, energy_keV=energy_keV)
        return mu
    
    def mu_pe(self, energy_keV):
        """
        Calculate photoelectric part of absorption coefficient at given energies.  (Units: 1/cm)
        
        energy_keV: photon energies of interest, in keV
        
        Returns: mu_pe corresponding to each energy
        """
        mu_pe, _ = calculate_mass_coefficient(self.z, self.g_cc, "mu_rho_pe_cm2_g", energy_keV)
        return mu_pe
    
    def mu_pe_k(self, energy_keV):
        """
        Calculate K-shell component of photoelectric part of absorption coefficient at given energies.  (Units: 1/cm)
        
        energy_keV: photon energies of interest, in keV
        
        Returns: mu_pe_k corresponding to each energy
        """
        mu_pe_k, _ = calculate_mass_coefficient(self.z, self.g_cc, "mu_rho_K_cm2_g", energy_keV)
        return mu_pe_k
    
    def sigma(self, energy_keV):
        """
        Calculate total scattering cross-section at given energies.  (Units: 1/cm)
        
        energy_keV: photon energies of interest, in keV
        
        Returns: sigma corresponding to each energy
        """
        sigma, _ = calculate_mass_coefficient(self.z, self.g_cc, "sigma_rho_cm2_g", energy_keV)
        return sigma
    
    def __add__(self, rhs):
        """
        Add materials by mass density.
        """
        
        # my_n_cc = stoichiometry.number_density(self.z, self.g_cc)
        # rhs_n_cc = stoichiometry.number_density(rhs.z, rhs.g_cc)

        # sum_n_cc = Material._to_array(self.z, my_n_cc) + Material._to_array(rhs.z, rhs_n_cc)
        # sum_z = np.where(sum_n_cc)[0] + 1
        # sum_n_cc = sum_n_cc[sum_z-1]

        # sum_g_cc = stoichiometry.mass_density(sum_z, sum_n_cc)

        # return Material(sum_z, sum_g_cc)

        x = self.to_array()
        y = rhs.to_array()
        z = x+y

        return Material.from_array(z)

    def __getitem__(self, key):
        if isinstance(key, str) or isinstance(key, int):
            return self[ [key] ]

        indices = [elements.ELEMENTS[k].number-1 for k in key]

        x = self.to_array()
        y = np.zeros_like(x)
        y[indices] = x[indices]

        return Material.from_array(y)
        
    def to_dict(self):
        """
        Convert to dictionary.
        
        Returns: dict(zip(z, density_g_cc))
        """
        return dict(zip(self.z, self.g_cc))
    
    @staticmethod
    def _to_array(z, values):
        new_array = np.zeros(99)
        new_array[np.array(z, dtype=int) - 1] = values
        return new_array
    
    def to_array(self):
        """
        Convert to array.  Length of array is 99.  Nth element corresponds to atomic number N+1.
        
        Returns: array of densities of component elements [g/cc]
        """
        
        return Material._to_array(self.z, self.g_cc)
    
    @property
    def density(self):
        """
        Total density of material [g/cc]
        """
        return np.sum(self.g_cc)
    
    @density.setter
    def density(self, value):
        multiplier = value / self.density
        self.g_cc = np.multiply(self.g_cc, multiplier)
    
    def as_density(self, new_density_g_cc):
        """
        Return Material with density changed to new value.
        """
        new_material = Material(self.z, self.g_cc)
        new_material.density = new_density_g_cc
        return new_material

    def number_densities(self):
        """
        Return array of element number densities
        """

        n_cc = stoichiometry.number_density(self.z, self.g_cc)
        return Material._to_array(self.z, n_cc)
    
    @classmethod
    def from_element(cls, symbol, density_g_cc=None):
        """
        Create Material from a pure element.
        
        If density_g_cc is not provided, a default density will be taken from the elements library.
        
        symbol:       atomic number or symbol of element, e.g. "H"
        density_g_cc: (optional) density of material [g/cc]
        """
        if density_g_cc is None:
            density_g_cc = elements.ELEMENTS[symbol].density
        return cls([symbol], [density_g_cc])
    
    @classmethod
    def from_compound(cls, formula, density_g_cc=None):
        """
        Create Material from a chemical formula.
        
        formula:       chemical formula e.g. "H2O"
        density_g_cc:  (optional) total density of compound.  Default is 1.0.
        """
        if density_g_cc is None:
            density_g_cc = 1.0
        symbols, elem_n_cc = stoichiometry.compound_number_densities(formula, density_g_cc)
        elem_g_cc = stoichiometry.mass_density(symbols, elem_n_cc)
        return cls(symbols, elem_g_cc)

    @classmethod
    def from_icru44(cls, icru44_name):
        """
        Create Material from an ICRU-44 material.

        icru44_name:  valid ICRU-44 material name e.g. "Water, Liquid"

        For full list of valid ICRU-44 material names, call xraymaterials.icru44.list().
        """
        return icru44.load(icru44_name)

    @classmethod
    def from_array(cls, density_g_cc):
        """
        Create Material from an array of element densities.
        
        The Nth element of density_g_cc corresponds to atomic number N+1.
        
        density_g_cc: array of densities
        """
        z = np.where(density_g_cc)[0] + 1
        return cls(z, density_g_cc[z-1])
    
    @classmethod
    def from_dict(cls, z_density):
        """
        Create Material from dict of symbols or atomic numbers and densities.
        
        z_density: dict, keys are symbols e.g. "H" or atomic numbers e.g. 1
                   values are densities [g/cc]
        """
        return cls(z_density.keys(), z_density.values())
        
    def __repr__(self):
        keys = [elements.ELEMENTS[z].symbol for z in self.z]
        d = dict(zip(keys, self.g_cc))
        return repr(d)
    
    def __str__(self):
        return repr(self)
    
    @staticmethod
    def add_by_volume(mat1, vol1, mat2, vol2, final_density_g_cc=None):
        """
        Add two materials with given parts-per-volume.  Assumes conservation of volume.

        The final mixture's element densities are the volume-weighted average of the
        input mixtures' element densities.
        
        If final_density is given, the density of the resulting mixture will be
        coerced to this value.
        
        mat1:               first Material
        vol1:               part-by-volume of first material
        mat2:               second Material
        vol2:               part-by-volume of second material
        final_density_g_cc: (optional) density of resulting material [g/cc]
        
        Returns: Material representing mixture of two materials.
        
        Example: unseasoned biscuit mix.  Add 2 cups of flour to 1 tablespoon of
        baking powder (1 tablespoon = 1/16 cup).  We expect to get 2.0625 cups
        of unflavorful biscuit mix, i.e. volume is conserved, so we use add_by_volume().
        
        mixture = add_by_volume(flour, 2.0, baking_powder, 1./16)
        
        mixture.density is the elemental density of the resulting biscuit mix.
        """
        
        return Material.sum_by_volume([mat1, mat2], [vol1, vol2], final_density_g_cc)
        

    @staticmethod
    def add_by_mass(mat1, m1, mat2, m2, final_density_g_cc=None):
        """
        Add two materials with given parts-per-mass.  Assumes conservation of volume.
        
        If final_density is given, the density of the resulting mixture will be
        coerced to this value.
        
        mat1:               first Material
        m1:                 part-by-mass of first material
        mat2:               second Material
        m2:                 part-by-mass of second material
        final_density_g_cc: (optional) density of resulting material [g/cc]
        
        Returns: Material representing mixture of two materials.
        """
        
        return Material.sum_by_mass([mat1, mat2], [m1, m2], final_density_g_cc)

    @staticmethod
    def sum_by_volume(materials, volumes, final_density_g_cc=None):
        """
        Sum multiple materials with given parts-per-volume.  Volume is conserved.
        
        materials:          list of Materials
        volumes:            list of parts-by-volume
        final_density_g_cc: (optional) density of resulting material [g/cc]
        
        Returns: Material representing mixture of materials
        """
        masses = [m.to_array() * v for (m,v) in zip(materials, volumes)]
        mass_total = np.sum(masses, 0)
        v_total = np.sum(volumes)
        
        new_material = Material.from_array(mass_total / v_total)
        
        if final_density_g_cc is not None:
            new_material.density = final_density_g_cc
        
        return new_material

    @staticmethod
    def sum_by_mass(materials, masses, final_density_g_cc=None):
        """
        Sum multiple materials with given parts-per-mass.  Volume is conserved.
        
        materials:          list of Materials
        masses:             list of parts-by-mass
        final_density_g_cc: (optional) density of resulting material [g/cc]
        
        Returns: Material representing mixture of materials
        """
        
        volumes = np.divide(masses, [m.density for m in materials])
        return Material.sum_by_volume(materials, volumes, final_density_g_cc)
    
    # An idea.
    # def _repr_markdown_(self):
    #     # total_density = np.sum(self.g_cc)

    #     keys = [elements.ELEMENTS[z].symbol for z in self.z]
    #     d = dict(zip(keys, self.g_cc))

    #     s = "$"
    #     for z, g_cc in zip(self.z, self.g_cc):
    #         s += elements.ELEMENTS[z].symbol + f"_{{{g_cc:0.3f}}}"
    #     s += "$"
    #     return s
