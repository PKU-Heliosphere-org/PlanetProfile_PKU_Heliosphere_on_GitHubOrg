"""
PPEuropa
Contains all body-specific parameters and information for PlanetProfile models of this body.
Import as a module and access information assigned to the attributes of the Planet and Params structs.
Note that this file expects to be imported from the directory above.
"""
import numpy as np
from Utilities.dataStructs import *
from config import Params

Planet = PlanetStruct("Europa")

# if Params.HOLD:
#     clrAllProfiles()
#     clrAllLayered(Planet.name)

""" Bulk planetary settings """
Planet.rho_kgm3 = 2989
Planet.R_m = 1561.0e3
Planet.M_kg = 4.7991e22
Planet.gsurf_ms2 = 1.428
Planet.Tsurf_K = 110
Planet.Psurf_MPa = 0
Planet.Cmeasured = 0.346
Planet.Cuncertainty = 0.005
Planet.phi_surface = 0
Planet.Tb_K = 269.8

""" Layer step settings """
Planet.Pseafloor_MPa = 350
Planet.nsteps_iceI = 200
Planet.nsteps_ocean = 350
Planet.nsteps_ref_rho = 30
Planet.nsteps_mantle = 500
Planet.nsteps_core = 10

""" Hydrosphere assumptions """
Planet.Ocean.comp = 'MgSO4'
Planet.Ocean.w_ocean_ppt = 100

""" Mantle heat """
Planet.Silicate.kr_mantle = 4
# cold case
Planet.Silicate.Qmantle_Wm2 = 2.2e11/4/np.pi/Planet.R_m**2
Planet.Silicate.QHmantle = 0
Planet.Silicate.EQUIL_Q = False
# hot case
# Planet.Silicate.Qmantle = 1.3e11
# Planet.Silicate.QHmantle = 8.5e11
# Rock porosity
Planet.Silicate.POROUS_ROCK = False
Planet.Silicate.PEFF = False
# Mantle equation of state model
# Planet.Silicate.mantleEOS = 'chon_678_1.tab' # (3500)
# Planet.Silicate.mantleEOS = 'pyrohp_sat_678_1.tab' # (2820)
# Planet.Silicate.mantleEOS = 'epyro_678_1.tab' # (3450)
# Planet.Silicate.mantleEOS = 'echon_hp_sat_PX678_14GPa.tab' # (3100)
# Planet.Silicate.mantleEOS = 'pyrohy_678v2_1.tab' # (3420)
# Planet.Silicate.mantleEOS = 'echonhy1wt_678_1.tab' # (3459)
# Planet.Silicate.mantleEOS = 'pyrohy_1wt_14GPa.tab' # (3300) this uses the procedure implemented by F. Cammarano
# Planet.Silicate.mantleEOS = 'echonhp_1wt_6GPa.tab' # too dense (3400) this uses the procedure implemented by F. Cammarano
# Planet.Silicate.mantleEOS = 'epyro_1.tab' # too dense (3400) this uses the procedure implemented by F. Cammarano
# Planet.Silicate.mantleEOS = 'echon_1.tab' # too dense (3500) this uses the procedure implemented by F. Cammarano
# Planet.Silicate.mantleEOS = 'chon_1.tab' # too dense (3500) this uses the procedure implemented by F. Cammarano
Planet.Silicate.mantleEOS = 'CV3hy1wt_678_1.tab' # (2900 for Q= 100 GW, 3240 for Q= 220 GW)
Planet.Silicate.rho_sil_withcore_kgm3 = 3539
# Planet.Silicate.mantleEOS = 'Simple_CI_HS_green_PP.tab' # CI chondrite material minus Fe core, computed with Green et al. 2016 (JMG) solution model and Lodders and Fegley 1998
# Planet.Silicate.rho_sil_withcore_kgm3 = 2975
# Planet.Silicate.mantleEOS = 'Simple_CM_HS_green_PP.tab' # CM chondrite material minus Fe core, computed with Green et al. 2016 (JMG) solution model and Lodders and Fegley 1998
# Planet.Silicate.rho_sil_withcore_kgm3 = 2975
# Planet.Silicate.mantleEOS = 'Simple_CV_HS_green_PP.tab' # CV chondrite material minus Fe core, computed with Green et al. 2016 (JMG) solution model and Lodders and Fegley 1998
# Planet.Silicate.rho_sil_withcore_kgm3 = 2975

""" Core assumptions """
Planet.Core.FeCore = True
Planet.Core.rhoFe = 8000
Planet.Core.rhoFeS = 5150
Planet.Core.rhoPoFeFCC = 5455
Planet.Core.QScore = 1e4
Planet.Core.coreEOS = 'sulfur_core_partition_SE15_1pctSulfur.tab'
Planet.Core.xFeS_meteoritic = 0.0405
Planet.Core.xFeS = 0.55
Planet.Core.xFe_core = 0.0279
Planet.Core.XH2O = 0.0035

""" Seismic properties of solids """
Planet.Seismic.low_ice_Q = 1
# Attenuation Parameters Based on those Described in Cammarano et al. 2006
# ice I
Planet.Seismic.B_aniso_iceI = 0.56
Planet.Seismic.gamma_aniso_iceI = 0.2
Planet.Seismic.g_aniso_iceI = 22 # C2006
# ice II
Planet.Seismic.B_aniso_iceII = 0.56
Planet.Seismic.gamma_aniso_iceII = 0.2
Planet.Seismic.g_aniso_iceII = 30
# ice III
Planet.Seismic.B_aniso_iceIII = 0.56
Planet.Seismic.gamma_aniso_iceIII = 0.2
Planet.Seismic.g_aniso_iceIII = 25
# ice V
Planet.Seismic.B_aniso_iceV = 0.56
Planet.Seismic.gamma_aniso_iceI = 0.2
Planet.Seismic.g_aniso_iceV = 27
# ice VI
Planet.Seismic.B_aniso_iceVI = 0.56
Planet.Seismic.gamma_aniso_iceVI = 0.2
Planet.Seismic.g_aniso_iceVI = 28
# mantle
Planet.Seismic.B_aniso_mantle = 0.56
Planet.Seismic.gamma_aniso_mantle = 0.2
Planet.Seismic.g_aniso_mantle = 30 # C2006

""" Magnetic induction """
Planet.Magnetic.peaks_Hz = np.array([4.946e-5, 2.473e-5, 3.259e-6])
Planet.Magnetic.f_orb = 2*np.pi/3.55/86400
Planet.Magnetic.ionos_bounds = 100e3
Planet.Magnetic.ionosPedersen_sig = 30/100e3
Planet.Magnetic.ionos_only = None
Planet.Magnetic.ADD_TRANSITION_BOUNDS = False

""" Other parameter options """
Params.PLOT_SIGS = True
Params.wlims = [np.log10(0.001), np.log10(1000)]
Params.FOURSUBPLOTS = True
Params.LEGEND = True
Params.LegendPosition = 'North'
Params.ylim = [910, 1230]
Params.LineStyle = Params.LS_Mg
Params.wrefLine = '--'
Params.wref = [0, 5, 10, 15]

# The block below should be made into one single function that returns the FTdata struct if the file is found, and warns the user/downloads if not.
# try:
#     load(['FTdata' Planet.name],'FTdata')
# catch:
#     dlNow = FTdataMissingWarning()
#     if dlNow; load(['FTdata' Planet.name],'FTdata'); end

""" Interior constraints imposed in Vance et al. 2014 """
Planet.Silicate.mSi = 28.0855
Planet.Silicate.mS = 32.065
Planet.Silicate.mFe = 55.845
Planet.Silicate.mMg = 24.305
Planet.Silicate.xOl = 0.44 # percentage of olivine - Javoy (1995) - Fe/Si = 0.909 Mg/Si = 0.531, Mg# = 0.369
Planet.Silicate.xSi = (Planet.Silicate.xOl+2*(1-Planet.Silicate.xOl))*Planet.Silicate.mSi/(Planet.Silicate.xOl*184.295+(1-Planet.Silicate.xOl)*244.3805) # mass fraction of sulfur in silicates
Planet.Silicate.M_Earth_kg = 5.97e24
Planet.Silicate.xSiEarth = 0.1923 # Javoy in kg/kg in Exoplanets paper20052006-xSiSolar only in mole
Planet.Silicate.xK = 1 # enrichment in K