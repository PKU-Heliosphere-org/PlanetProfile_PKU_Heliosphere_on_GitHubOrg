import numpy as np
import logging as log
from scipy.interpolate import NearestNDInterpolator, RectBivariateSpline
from scipy.optimize import root_scalar as GetZero
from scipy.io import loadmat
from seafreeze import seafreeze as SeaFreeze
from seafreeze import whichphase as WhichPhase
from Utilities.defineStructs import Constants, EOSlist
from Thermodynamics.MgSO4.MgSO4Props import MgSO4Props, MgSO4Phase, MgSO4Seismic, MgSO4Conduct
from Thermodynamics.Seawater.SwProps import SwProps, SwPhase, SwSeismic, SwConduct
from Thermodynamics.Clathrates.ClathrateProps import ClathProps, ClathStableSloan1998, TclathDissocLower_K, \
    TclathDissocUpper_K, ClathSeismic
from Thermodynamics.FromLiterature.InnerEOS import GetphiFunc

def GetOceanEOS(compstr, wOcean_ppt, P_MPa, T_K, elecType, rhoType=None, scalingType=None):
    oceanEOS = OceanEOSStruct(compstr, wOcean_ppt, P_MPa, T_K, elecType, rhoType=rhoType,
                              scalingType=scalingType)
    if oceanEOS.ALREADY_LOADED:
        log.debug(f'{wOcean_ppt} ppt {compstr} EOS already loaded. Reusing existing EOS.')
        oceanEOS = EOSlist.loaded[oceanEOS.EOSlabel]

    return oceanEOS

class OceanEOSStruct:
    def __init__(self, compstr, wOcean_ppt, P_MPa, T_K, elecType, rhoType=None, scalingType=None):
        self.EOSlabel = f'{compstr}{wOcean_ppt}{elecType}{rhoType}{scalingType}'
        self.ALREADY_LOADED, self.rangeLabel, self.P_MPa, self.T_K = CheckIfEOSLoaded(self.EOSlabel,
                                                                                      P_MPa, T_K)
        if not self.ALREADY_LOADED:
            self.comp = compstr
            self.w_ppt = wOcean_ppt
            if elecType is None:
                self.elecType = 'Vance2018'

            self.Pmin = np.min(self.P_MPa)
            self.Pmax = np.max(self.P_MPa)
            self.Tmin = np.min(self.T_K)
            self.Tmax = np.max(self.T_K)
            self.deltaP = np.mean(np.diff(self.P_MPa))
            self.deltaT = np.mean(np.diff(self.T_K))
            log.debug(f'Loading EOS for {wOcean_ppt} ppt {compstr} with ' +
                      f'P_MPa = [{self.Pmin:.1f}, {self.Pmax:.1f}, {self.deltaP:.2f}], ' +
                      f'T_K = [{self.Tmin:.1f}, {self.Tmax:.1f}, {self.deltaT:.2f}], ' +
                      f'for [min, max, step].')

            # Get tabular data from the appropriate source for the specified ocean composition
            if compstr == 'none':
                self.fn_phase = lambda P,T: np.zeros_like(P, dtype=np.int_)
                self.type = 'No H2O'
                self.m_gmol = 0.0
                self.rho_kgm3 = np.zeros((np.size(self.P_MPa), np.size(self.T_K)))
                self.Cp_JkgK = self.rho_kgm3
                self.alpha_pK = self.rho_kgm3
                self.kTherm_WmK = self.rho_kgm3
                self.fn_Seismic = lambda P,T: (np.zeros_like(P), np.zeros_like(P))
                self.fn_sigma_Sm = lambda P,T: np.zeros_like(P)
            elif wOcean_ppt == 0 or compstr == 'PureH2O':
                self.type = 'SeaFreeze'
                self.m_gmol = Constants.mH2O_gmol

                PTgrid = np.array([self.P_MPa, self.T_K], dtype=object)
                seaOut = SeaFreeze(PTgrid, 'water1')
                self.rho_kgm3 = seaOut.rho
                self.Cp_JkgK = seaOut.Cp
                self.alpha_pK = seaOut.alpha
                self.kTherm_WmK = np.zeros_like(self.alpha_pK) + Constants.kThermWater_WmK  # Placeholder until we implement a self-consistent calculation

                self.phase = WhichPhase(PTgrid)
                # Create phase finder -- note that the results from this function must be cast to int after retrieval
                Plin_MPa = np.array([P for P in self.P_MPa for _ in self.T_K])
                Tlin_K = np.array([T for _ in self.P_MPa for T in self.T_K])
                PTpairs = list(zip(Plin_MPa, Tlin_K))
                phase1D = np.reshape(self.phase, (-1))
                # Create phase finder -- note that the results from this function must be cast to int after retrieval
                self.fn_phase = NearestNDInterpolator(PTpairs, phase1D)

                self.fn_Seismic = H2OSeismic(compstr, self.w_ppt)
                self.fn_sigma_Sm = H2Osigma_Sm()
            elif compstr == 'Seawater':
                self.type = 'GSW'
                self.m_gmol = Constants.mH2O_gmol
                if((self.T_K[0] <= 250) or (self.P_MPa[-1] > 250)):
                    log.warning('GSW handles only ice Ih for determining phases in the ocean. At ' +
                                'low temperatures or high pressures, this model will be wrong as no ' +
                                'high-pressure ice phases will be found.')

                self.fn_phase = SwPhase(self.w_ppt)
                self.rho_kgm3, self.Cp_JkgK, self.alpha_pK, self.kTherm_WmK = SwProps(self.P_MPa, self.T_K, self.w_ppt)
                self.fn_Seismic = SwSeismic(self.w_ppt)
                self.fn_sigma_Sm = SwConduct(self.w_ppt)
            elif compstr == 'NH3':
                self.m_gmol = Constants.mNH3_gmol
                self.type = 'PlanetProfile'
                raise ValueError('Unable to load ocean EOS. NH3 is not implemented yet.')
            elif compstr == 'MgSO4':
                if elecType == 'Pan2020' and round(self.w_ppt) == 100:
                    self.elecType = elecType
                elif elecType == 'Pan2020' and round(self.w_ppt) != 100:
                    log.warning('elecType "Pan2020" behavior is defined only for Ocean.wOcean_ppt = 100. ' +
                                'Defaulting to elecType "Vance2018".')
                    self.elecType = 'Vance2018'
                else:
                    self.elecType = elecType
                self.type = 'ChoukronGrasset2010'
                self.m_gmol = Constants.mMgSO4_gmol

                self.rho_kgm3, self.Cp_JkgK, self.alpha_pK, self.kTherm_WmK = MgSO4Props(self.P_MPa, self.T_K, self.w_ppt)
                phaseFunc = MgSO4Phase(self.w_ppt)
                self.fn_phase = phaseFunc.arrays
                self.fn_Seismic = MgSO4Seismic(self.w_ppt)
                self.fn_sigma_Sm = MgSO4Conduct(self.w_ppt, self.elecType, rhoType=rhoType, scalingType=scalingType)
            elif compstr == 'NaCl':
                self.type = 'PlanetProfile'
                self.m_gmol = Constants.mNaCl_gmol
                raise ValueError('Unable to load ocean EOS. NaCl is not implemented yet.')
            else:
                raise ValueError(f'Unable to load ocean EOS. compstr="{compstr}" but options are "Seawater", "NH3", "MgSO4", ' +
                                 '"NaCl", and "none" (for waterless bodies).')

            self.fn_rho_kgm3 = RectBivariateSpline(self.P_MPa, self.T_K, self.rho_kgm3)
            self.fn_Cp_JkgK = RectBivariateSpline(self.P_MPa, self.T_K, self.Cp_JkgK)
            self.fn_alpha_pK = RectBivariateSpline(self.P_MPa, self.T_K, self.alpha_pK)
            self.fn_kTherm_WmK = RectBivariateSpline(self.P_MPa, self.T_K, self.kTherm_WmK)

            # Store complete EOSStruct in global list of loaded EOSs
            EOSlist.loaded[self.EOSlabel] = self
            EOSlist.ranges[self.EOSlabel] = self.rangeLabel


def GetIceEOS(P_MPa, T_K, phaseStr, porosType=None, phiTop_frac=0, Pclosure_MPa=0, phiMin_frac=0):
    iceEOS = IceEOSStruct(P_MPa, T_K, phaseStr, porosType=porosType, phiTop_frac=phiTop_frac,
                          Pclosure_MPa=Pclosure_MPa, phiMin_frac=phiMin_frac)
    if iceEOS.ALREADY_LOADED:
        log.debug(f'Ice {phaseStr} EOS already loaded. Reusing existing EOS.')
        iceEOS = EOSlist.loaded[iceEOS.EOSlabel]

    return iceEOS

class IceEOSStruct:
    def __init__(self, P_MPa, T_K, phaseStr, porosType=None, phiTop_frac=0, Pclosure_MPa=0, phiMin_frac=0):
        self.EOSlabel = f'{phaseStr}{porosType}{phiTop_frac}{Pclosure_MPa}{phiMin_frac}'
        self.ALREADY_LOADED, self.rangeLabel, self.P_MPa, self.T_K = CheckIfEOSLoaded(self.EOSlabel,
                                                                                      P_MPa, T_K)
        if not self.ALREADY_LOADED:
            self.Pmin = np.min(self.P_MPa)
            self.Pmax = np.max(self.P_MPa)
            self.Tmin = np.min(self.T_K)
            self.Tmax = np.max(self.T_K)
            self.deltaP = np.mean(np.diff(self.P_MPa))
            self.deltaT = np.mean(np.diff(self.T_K))
            log.debug(f'Loading EOS for {phaseStr} with ' +
                      f'P_MPa = [{self.Pmin:.1f}, {self.Pmax:.1f}, {self.deltaP:.2f}], ' +
                      f'T_K = [{self.Tmin:.1f}, {self.Tmax:.1f}, {self.deltaT:.2f}], ' +
                      f'for [min, max, step].')

            # Make sure arrays are long enough to interpolate
            nPs = np.size(self.P_MPa)
            nTs = np.size(self.T_K)
            if(nPs <= 3):
                self.P_MPa = np.linspace(self.P_MPa[0], self.P_MPa[-1], nPs*3)
            if(nTs <= 3):
                self.T_K = np.linspace(self.T_K[0], self.T_K[-1], nTs*3)
            # If input arrays are equal length, repeat final T value due to a quirk of numpy arrays
            # combined with SeaFreeze's particular implementation that requires gridded P,T values
            # to have different array lengths
            if(nPs == nTs):
                self.T_K = np.append(self.T_K, self.T_K[-1]*1.00001)

            if phaseStr == 'Clath':
                # Special functions for clathrate properties
                self.rho_kgm3, self.Cp_JkgK, self.alpha_pK, self.kTherm_WmK \
                    = ClathProps(self.P_MPa, self.T_K)
                self.phase = ClathStableSloan1998(self.P_MPa, self.T_K)

                Plin_MPa = np.array([P for P in self.P_MPa for _ in self.T_K])
                Tlin_K = np.array([T for _ in self.P_MPa for T in self.T_K])
                PTpairs = list(zip(Plin_MPa, Tlin_K))
                phase1D = np.reshape(self.phase, (-1))
                # Create phase finder -- note that the results from this function must be cast to int after retrieval
                # Returns either Constants.phaseClath (stable) or 0 (not stable), making it compatible with GetTfreeze
                self.fn_phase = NearestNDInterpolator(PTpairs, phase1D)
                self.fn_Seismic = ClathSeismic()
            else:
                # Get tabular data from SeaFreeze for all other ice phases
                PTgrid = np.array([self.P_MPa, self.T_K], dtype=object)
                iceOut = SeaFreeze(PTgrid, phaseStr)
                self.rho_kgm3 = iceOut.rho
                self.Cp_JkgK = iceOut.Cp
                self.alpha_pK = iceOut.alpha
                self.kTherm_WmK = np.array([kThermIsobaricAnderssonIbari2005(self.T_K, PhaseInv(phaseStr)) for _ in self.P_MPa])
                self.fn_Seismic = IceSeismic(phaseStr)

            # Interpolate functions for this ice phase that can be queried for properties
            self.fn_rho_kgm3 = RectBivariateSpline(self.P_MPa, self.T_K, self.rho_kgm3)
            self.fn_Cp_JkgK = RectBivariateSpline(self.P_MPa, self.T_K, self.Cp_JkgK)
            self.fn_alpha_pK = RectBivariateSpline(self.P_MPa, self.T_K, self.alpha_pK)
            self.fn_kTherm_WmK = RectBivariateSpline(self.P_MPa, self.T_K, self.kTherm_WmK)
            # Assign phase ID and string for convenience in functions where iceEOS is passed
            self.phaseStr = phaseStr
            self.phaseID = PhaseInv(phaseStr)

            if porosType is None or porosType == 'none':
                self.fn_phi_frac = lambda P, T: np.zeros_like(P)
                self.POROUS = False
            else:
                self.fn_phi_frac = GetphiFunc(porosType, phiTop_frac, Pclosure_MPa, None, self.P_MPa, self.T_K, phiMin_frac)
                self.POROUS = True

            # Combine pore fluid properties with matrix properties in accordance with
            # Yu et al. (2016): http://dx.doi.org/10.1016/j.jrmge.2015.07.004
            self.fn_porosCorrect = lambda propBulk, propPore, phi, J: (propBulk**J * (1 - phi) + propPore**J * phi)**(1/J)

            # Store complete EOSStruct in global list of loaded EOSs
            EOSlist.loaded[self.EOSlabel] = self
            EOSlist.ranges[self.EOSlabel] = self.rangeLabel


def CheckIfEOSLoaded(EOSlabel, P_MPa, T_K):
    """ Determine if we need to load a new EOS, or if we can reuse one that's already been
        loaded within this session.

        Args:
            EOSlabel (str): A unique identifier containing all the settings passed to the
                EOSStruct class instantiator.
            P_MPa (float, shape N): Pressures to desired for constructing the EOS in MPa.
            T_K (float, shape N): Temperatures to desired for constructing the EOS in K.
        Returns:
            ALREADY_LOADED (bool): Whether we can make use of an EOSStruct in EOSlist.loaded
                with a label matching the one we wish to load now.
            rangeLabel (str): A string identifying the min/max/step values for P and T.
            outP_MPa (float, shape N): Pressures to use for constructing the EOS in MPa.
            outT_K (float, shape N): Temperatures to use for constructing the EOS in K.
    """

    # Create label for identifying P, T arrays
    rangeLabel = f'{np.min(P_MPa)},{np.max(P_MPa)},{np.mean(np.diff(P_MPa))},' + \
                 f'{np.min(T_K)},{np.max(T_K)},{np.mean(np.diff(T_K))}'
    if EOSlabel in EOSlist.loaded.keys():
        if EOSlist.ranges[EOSlabel] == rangeLabel:
            # This exact EOS has been loaded already. Reuse the one in memory
            ALREADY_LOADED = True
            outP_MPa = None
            outT_K = None
        else:
            # Check if we can reuse an already-loaded EOS because the
            # P, T ranges are contained within the already-loaded EOS
            nopeP = np.min(P_MPa) < EOSlist.loaded[EOSlabel].Pmin or \
                    np.max(P_MPa) > EOSlist.loaded[EOSlabel].Pmax
            nopeT = np.min(T_K) < EOSlist.loaded[EOSlabel].Tmin or \
                    np.max(T_K) > EOSlist.loaded[EOSlabel].Tmax
            if nopeP or nopeT:
                # The new inputs have at least one min/max value outside the range
                # of the previously loaded EOS, so we have to load a new one.
                ALREADY_LOADED = False
                # Set P and T ranges to include the outer bounds from
                # the already-loaded EOS and the one we want now
                minPmin = np.minimum(np.min(P_MPa), EOSlist.loaded[EOSlabel].Pmin)
                maxPmax = np.maximum(np.max(P_MPa), EOSlist.loaded[EOSlabel].Pmax)
                minTmin = np.minimum(np.min(T_K), EOSlist.loaded[EOSlabel].Tmin)
                maxTmax = np.maximum(np.max(T_K), EOSlist.loaded[EOSlabel].Tmax)
                minDeltaP = np.minimum(np.mean(np.diff(P_MPa)), EOSlist.loaded[EOSlabel].deltaP)
                minDeltaT = np.minimum(np.mean(np.diff(T_K)), EOSlist.loaded[EOSlabel].deltaT)
                outP_MPa = np.arange(minPmin, maxPmax, minDeltaP)
                outT_K = np.arange(minTmin, maxTmax, minDeltaT)
                rangeLabel = f'{np.min(outP_MPa)},{np.max(outP_MPa)},{np.min(outT_K)},{np.max(outT_K)}'
            else:
                # A previous EOS has been loaded that has a wider P or T range than the inputs,
                # so we will use the previously loaded one.
                ALREADY_LOADED = True
                outP_MPa = None
                outT_K = None
    else:
        # This EOS has not been loaded, so we need to load it with the input parameters
        ALREADY_LOADED = False
        outP_MPa = P_MPa
        outT_K = T_K

    return ALREADY_LOADED, rangeLabel, outP_MPa, outT_K


# Create a function that can pack up (P,T) pairs that are compatible with SeaFreeze
sfPTpairs = lambda P_MPa, T_K: np.array([(P, T) for P, T in zip(P_MPa, T_K)], dtype='f,f').astype(object)

class H2OSeismic:
    """ Creates a function call for returning seismic properties of depth profile for pure water. """
    def __init__(self, compstr, wOcean_ppt):
        self.compstr = compstr
        self.w_ppt = wOcean_ppt

    def __call__(self, P_MPa, T_K):
        seaOut = SeaFreeze(sfPTpairs(P_MPa, T_K), 'water1')
        return seaOut.vel * 1e-3, seaOut.Ks * 1e-3


class H2Osigma_Sm:
    def __call__(self, P_MPa, T_K):
        return np.zeros_like(P_MPa) + Constants.sigmaH2O_Sm


class IceSeismic:
    def __init__(self, phaseStr):
        self.phase = phaseStr

    def __call__(self, P_MPa, T_K):
        seaOut = SeaFreeze(sfPTpairs(P_MPa, T_K), self.phase)
        return seaOut.Vp * 1e-3, seaOut.Vs * 1e-3,  seaOut.Ks * 1e-3, seaOut.shear * 1e-3


def GetPfreeze(oceanEOS, phaseTop, Tb_K, PLower_MPa=0, PUpper_MPa=300, PRes_MPa=0.1, UNDERPLATE=None):
    """ Returns the pressure at which ice changes phase based on temperature, salinity, and composition

        Args:
            oceanEOS (OceanEOSStruct): Interpolator functions for evaluating the ocean EOS
            Tb_K (float): Temperature of the phase transition in K
        Returns:
            Pfreeze_MPa (float): Pressure at the phase change interface consistent with Tb_K
    """
    phaseChangeUnderplate = lambda P: 0.5 + (phaseTop - oceanEOS.fn_phase(P, Tb_K))
    if UNDERPLATE is None:
        TRY_BOTH = True
        UNDERPLATE = True
    else:
        TRY_BOTH = False
    if UNDERPLATE:
        phaseChange = phaseChangeUnderplate
    else:
        phaseChange = lambda P: 0.5 - (phaseTop - oceanEOS.fn_phase(P, Tb_K))

    try:
        Pfreeze_MPa = GetZero(phaseChange, bracket=[PLower_MPa, PUpper_MPa]).root + PRes_MPa/5
    except ValueError:
        if UNDERPLATE:
            raise ValueError(f'Tb_K of {Tb_K:.3f} is not consistent with underplating ice III.')
        elif TRY_BOTH:
            try:
                Pfreeze_MPa = GetZero(phaseChangeUnderplate, bracket=[PLower_MPa, PUpper_MPa]).root + PRes_MPa / 5
            except ValueError:
                raise ValueError(f'No transition pressure was found below {PUpper_MPa:.3f} MPa ' +
                                 f'for ice {PhaseConv(phaseTop)}. Increase PUpper_MPa until one is found.')
        else:
            log.warning(f'No transition pressure was found below {PUpper_MPa:.3f} MPa ' +
                        f'for ice {PhaseConv(phaseTop)} and UNDERPLATE is explicitly set to False.')
            Pfreeze_MPa = np.nan

    return Pfreeze_MPa


def GetTfreeze(oceanEOS, P_MPa, T_K, TfreezeRange_K=50, TRes_K=0.05):
    """ Returns the temperature at which a solid layer melts based on temperature, salinity, and composition

        Args:
            oceanEOS (OceanEOSStruct): Interpolator functions for evaluating the ocean EOS
            P_MPa (float): Pressure of the fluid in MPa
            T_K (float): Temperature of the fluid in K
        Returns:
            Tfreeze_K (float): Temperature of nearest higher-temperature phase transition between
                liquid and ice at this pressure
    """
    topPhase = oceanEOS.fn_phase(P_MPa, T_K)
    phaseChange = lambda T: 0.5 - (topPhase - oceanEOS.fn_phase(P_MPa, T))

    try:
        Tfreeze_K = GetZero(phaseChange, bracket=[T_K, T_K+TfreezeRange_K]).root + TRes_K/5
    except ValueError:
        raise ValueError(f'No melting temperature was found above {T_K:.3f} K ' +
                         f'for ice {PhaseConv(topPhase)} at pressure {P_MPa:.3f} MPa. ' +
                          'Check to see if T_K is close to default Ocean.THydroMax_K value. ' +
                          'If so, increase Ocean.THydroMax_K. Otherwise, increase TfreezeRange_K ' +
                          'until a melting temperature is found.')

    return Tfreeze_K


def PhaseConv(phase):
    """ Convert phase integers into strings compatible with SeaFreeze

        Arguments:
            phase (int): ID of phase for each layer
        Returns:
            phaseStr (string): Corresponding string for each phase ID
    """
    if phase == 0:
        phaseStr = 'water1'
    elif abs(phase) == 1:
        phaseStr = 'Ih'
    elif abs(phase) == 2:
        phaseStr = 'II'
    elif abs(phase) == 3:
        phaseStr = 'III'
    elif abs(phase) == 5:
        phaseStr = 'V'
    elif abs(phase) == 6:
        phaseStr = 'VI'
    elif abs(phase) == Constants.phaseClath:
        phaseStr = 'Clath'
    elif phase >= Constants.phaseSil and phase < Constants.phaseSil+10:
        phaseStr = 'Sil'
    elif phase >= Constants.phaseFe:
        phaseStr = 'Fe'
    else:
        raise ValueError(f'PhaseConv does not have a definition for phase ID {phase:d}.')

    return phaseStr


def PhaseInv(phaseStr):
    """ Convert phase strings compatible with SeaFreeze into integers

        Arguments:
            phaseStr (string): String for each phase ID
        Returns:
            phase (int): Corresponding ID of phase for each layer
    """
    if phaseStr == 'water1':
        phase = 0
    elif phaseStr == 'Ih':
        phase = 1
    elif phaseStr == 'II':
        phase = 2
    elif phaseStr == 'III':
        phase = 3
    elif phaseStr == 'V':
        phase = 5
    elif phaseStr == 'VI':
        phase = 6
    elif phaseStr == 'Clath':
        phase = Constants.phaseClath
    elif phaseStr == 'Sil':
        phase = Constants.phaseSil
    elif phaseStr == 'Fe':
        phase = Constants.phaseFe
    else:
        raise ValueError(f'PhaseInv does not have a definition for phase string "{phaseStr}".')

    return phase


def GetPhaseIndices(phase):
    """ Get indices for each phase of ice/liquid

        Args:
            phase (int, shape N)
        Returns:
            indsLiquid, indsIceI, ... indsFe (int, shape 0-M): lists of indices corresponding to each phase.
                Variable length.
    """
    # Avoid an annoying problem where np.where returns an empty array for a length-1 list,
    # by making sure the input value(s) are a numpy array:
    phase = np.array(phase)

    indsLiquid = np.where(phase==0)[0]
    indsIceI = np.where(phase==-1)[0]
    indsIceIwet = np.where(phase==-1)[0]
    indsIceII = np.where(phase==2)[0]
    indsIceIIund = np.where(phase==-2)[0]
    indsIceIII = np.where(phase==3)[0]
    indsIceIIIund = np.where(phase==-3)[0]
    indsIceV = np.where(phase==5)[0]
    indsIceVund = np.where(phase==-5)[0]
    indsIceVI = np.where(phase==6)[0]
    indsIceVIund = np.where(phase==-6)[0]
    indsClath = np.where(phase==Constants.phaseClath)[0]
    indsClathWet = np.where(phase==-Constants.phaseClath)[0]
    indsSil = np.where(np.logical_and(phase>=Constants.phaseSil, phase<Constants.phaseSil+10))[0]
    indsSilLiq = np.where(phase==Constants.phaseSil)[0]
    indsSilI = np.where(phase==Constants.phaseSil+1)[0]
    indsSilII = np.where(phase==Constants.phaseSil+2)[0]
    indsSilIII = np.where(phase==Constants.phaseSil+3)[0]
    indsSilV = np.where(phase==Constants.phaseSil+5)[0]
    indsSilVI = np.where(phase==Constants.phaseSil+6)[0]
    indsFe = np.where(phase>=Constants.phaseFe)[0]

    return indsLiquid, indsIceI, indsIceIwet, indsIceII, indsIceIIund, indsIceIII, indsIceIIIund, indsIceV, indsIceVund, \
               indsIceVI, indsIceVIund, indsClath, indsClathWet, indsSil, indsSilLiq, indsSilI, indsSilII, indsSilIII, \
               indsSilV, indsSilVI, indsFe


def kThermIsobaricAnderssonIbari2005(T_K, phase):
    """ Calculate thermal conductivity of ice at a fixed pressure according to
        Andersson and Ibari (2005) as a function of temperature.
        Range of validity is as follows:
        Phase:  P (MPa):    T range (K):
        Ih      0.1         40-180*
        II      240         120-240
        III     240         180-250
        V       530         240-270
        VI      1000        135-250
        *Andersson and Ibari give an alternate equation that accounts for the range 180-273 K
        for ice Ih at 0.1 MPa, but as this was not included in the Matlab version, it's
        skipped here too. This implementation does not apply at the relevant T and P values
        for icy moon shells except at specific points, so a more versatile and accurate
        model should be found and used to replace this.

        Args:
            T_K (float, shape N): Temperatures to evaluate in K
            phase (int): Phase ID
        Returns:
            kTherm_WmK (float, shape N): Thermal conductivity of desired phase at specified temperatures
                in W/(m K)
    """
    D = np.array([np.nan, 630, 695, 93.2, np.nan, 38.0, 50.9])
    X = np.array([np.nan, 0.995, 1.097, 0.822, np.nan, 0.612, 0.612])

    kTherm_WmK = D[abs(phase)] * T_K**(-X[abs(phase)])

    return kTherm_WmK


def kThermIsothermalAnderssonIbari2005(P_MPa, phase):
    """ Calculate thermal conductivity of ice at a fixed temperature according to
        Andersson and Ibari (2005) as a function of pressure.
        Range of validity is as follows:
        Phase:  P range (GPa):  T (K):
        Ih      0-0.5           130
        II      0-0.24          120
        III     0.2-0.35        240
        V       0.35-0.6        246
        VI      0.7-2.0         246
        This implementation does not apply at the relevant T and P values for icy moon
        shells except at specific points, so a more versatile and accurate model should
        be found and used to replace this.

        Args:
            P_MPa (float, shape N): Pressure to evaluate in MPa
            phase (int, shape N): Phase index
        Returns:
            kTherm_WmK (float, shape N): Thermal conductivity of desired phase at specified pressures
                in W/(m K)
    """
    E = np.array([np.nan, 1.60, 1.25, -0.02, np.nan, 0.16, 0.37])
    F = np.array([np.nan, -0.44, 0.2, 0.2, np.nan, 0.2, 0.16])

    # Note the 1e-3 factor because F has units of 1/GPa
    kTherm_WmK = np.exp(E[abs(phase)] + F[abs(phase)] * P_MPa * 1e-3)

    return kTherm_WmK


def kThermMelinder2007(T_K, Tmelt_K, ko_WmK=2.21, dkdT_WmK2=-0.012):
    """ Calculate thermal conductivity of ice Ih according to Melinder (2007).

        Args:
            T_K (float, shape N): Temperature in K
            Tmelt_K (float, shape N): Melting temperature at the evaluated pressure in K
            ko_WmK = 2.21 (float): Thermal conductivity at the melting temperature in W/(m K)
            dkdT_WmK2 = -0.012 (float): Constant temperature derivative of k in W/(mK^2)
        Returns:
            kTherm_WmK (float, shape N): Thermal conductivity of ice Ih at specified temperature
                in W/(m K)
    """

    kTherm_WmK = ko_WmK + dkdT_WmK2 * (T_K - Tmelt_K)
    return kTherm_WmK


def kThermHobbs1974(T_K):
    """ Calculate thermal conductivity of ice Ih according to Hobbs (1974), as
        reported by Ojakangas and Stevenson (1989).

        Args:
            T_K (float, shape N): Temperature value(s) in K
        Returns:
            kTherm_WmK (float, shape N): Thermal conductivities in W/(m K)
    """
    a0 = 4.68e4  # Units of ergs/(K cm s)
    a1 = 4.88e7  # Units of ergs/(cm s)
    a0_SI = a0 * Constants.erg2J * 1e2
    a1_SI = a1 * Constants.erg2J * 1e2
    kTherm_WmK = a1_SI/T_K + a0_SI

    return kTherm_WmK


def GetPbClath(Tb_K):
    """ Calculate the pressure consistent with Tb_K when clathrates are assumed
        to be in contact with the ocean, i.e. for Bulk.clathType = 'bottom' or 'whole'.

        Args:
            Tb_K (float): Clathrate layer bottom temperature in K
        Returns:
            PbClath_MPa (float): Bottom temperature consistent with dissociation curve
                pressure at Tb_K
    """
    if Tb_K < 273:
        TbZero_K = lambda P_MPa: Tb_K - TclathDissocLower_K(P_MPa)
        Pends_MPa = [0.0, 2.567]
    else:
        TbZero_K = lambda P_MPa: Tb_K - TclathDissocUpper_K(P_MPa)
        Pends_MPa = [2.567, Constants.PmaxLiquid_MPa]

    PbClath_MPa = GetZero(TbZero_K, bracket=Pends_MPa).root

    return PbClath_MPa
