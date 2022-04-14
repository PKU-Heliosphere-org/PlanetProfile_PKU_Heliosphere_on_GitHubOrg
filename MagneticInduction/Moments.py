""" Classes for keeping track of excitation and induced magnetic moments """

class InductionStruct:
    def __init__(self):
        self.bodyname = None  # Name of body modeled.
        self.yName = None  # Name of variable along y axis. Options are "Tb", "phi", "rho", "sigma", where the first 3 are vs. salinity, and sigma is vs. thickness.
        self.Texc_hr = None  # Dict of excitation periods modeled.
        self.Amp = None  # Amplitude of dipole response (modulus of complex dipole response).
        self.phase = None  # (Positive) phase delay in degrees.
        self.Bix_nT = None  # Induced Bx dipole moments relative to body surface in nT for each excitation.
        self.Biy_nT = None  # Induced By dipole moments relative to body surface in nT for each excitation.
        self.Biz_nT = None  # Induced Bz dipole moments relative to body surface in nT for each excitation.
        self.w_ppt = None  # Values of salinity used.
        self.oceanComp = None  # Ocean composition used.
        self.Tb_K = None  # Values of Bulk.Tb_K used.
        self.rhoSilMean_kgm3 = None  # Values of Sil.rhoMean_kgm3 resulted (also equal to those set for all but phi inductOtype).
        self.phiSilMax_frac = None  # Values of Sil.phiRockMax_frac set.
        self.Tb_K = None  # Values of Bulk.Tb_K used.
        self.sigmaMean_Sm = None  # Mean ocean conductivity. Used to map plots vs. salinity onto D/σ plots.
        self.sigmaTop_Sm = None  # Ocean top conductivity. Used to map plots vs. salinity onto D/σ plots.
        self.D_km = None  # Ocean layer thickness in km. Used to map plots vs. salinity onto D/σ plots.
        self.zb_km = None  # Upper ice shell thickness in km.
        self.R_m = None  # Body radius in m, used to scale amplitudes.
        self.rBds_m = None  # Conducting layer upper boundaries in m.
        self.sigmaLayers_Sm = None  # Conductivities below each boundary in S/m.


class ExcitationsList:
    def __init__(self):
        self.nprmMax = 1
        Texc_hr = {}
        # Approximate (.2f) periods to select from excitation spectrum for each body in hr
        Texc_hr['Europa'] = {'synodic':11.23, 'orbital':85.15, 'true anomaly':84.63, 'synodic harmonic':5.62}
        self.Texc_hr = Texc_hr

    def __call__(self, bodyname):
        return self.Texc_hr[bodyname]


Excitations = ExcitationsList()
InductionResults = InductionStruct()
