"""
General runtime configuration parameters.
Overridden by any settings contained within PPBody.py files.
"""
from PlanetProfile.Utilities.defineStructs import ParamsStruct, ExploreParamsStruct, Constants

configVersion = 3  # Integer number for config file version. Increment when new settings are added to the default config file.

Params = ParamsStruct()
Params.VERBOSE =       True  # Provides extra runtime messages. Overrides QUIET below
Params.QUIET =         False  # Hides all log messages except warnings and errors
Params.QUIET_MOONMAG = True  # If True, sets MoonMag logging level to WARNING, otherwise uses the same as PlanetProfile.
Params.printFmt = '[%(levelname)s] %(message)s'  # Format for printing log messages
# The below flags allow or prevents extrapolation of EOS functions beyond the definition grid.
Params.EXTRAP_ICE = {'Ih':False, 'II':False, 'III':False, 'V':False, 'VI':False, 'Clath':False}
Params.EXTRAP_OCEAN = False
Params.EXTRAP_REF =   True  # Allow refprofile extrapolation separate from normal ocean
Params.EXTRAP_SIL =   False
Params.EXTRAP_Fe =    False
Params.lookupInterpMethod = 'nearest'  # Interpolation method to use for EOS lookup tables. Options are 'nearest', 'linear', 'cubic'.

Params.CALC_NEW =         True  # Recalculate profiles? If not, read data from disk and re-plot.
Params.CALC_NEW_REF =     True  # Recalculate reference melting curve densities?
Params.CALC_NEW_INDUCT =  True  # Recalculate magnetic induction responses?
Params.CALC_SEISMIC =     True  # Calculate sound speeds and elastic moduli?
Params.CALC_CONDUCT =     True  # Calculate electrical conductivity?
Params.RUN_ALL_PROFILES = False  # Whether to run all PPBody.py files for the named body and plot together
Params.SPEC_FILE =        False  # Whether we are running a specific file or files
Params.COMPARE =          False  # Whether to plot each new run against other runs from the same body
Params.DO_PARALLEL =      True  # Whether to use multiprocessing module for parallel computation where applicable
Params.threadLimit =      1000  # Upper limit to number of processors/threads for parallel computation
Params.FORCE_EOS_RECALC = False  # Whether to reuse previously loaded EOS functions for multi-profile runs
Params.SKIP_INNER =       False  # Whether to skip past everything but ocean calculations after MoI matching (for large induction studies)
Params.NO_SAVEFILE =      False  # Whether to prevent printing run outputs to disk. Saves time and disk space for large induction studies.
Params.DISP_LAYERS =      True  # Whether to display layer depths and heat fluxes for user
Params.DISP_TABLE =       True  # Whether to print latex-formatted table
Params.ALLOW_BROKEN_MODELS = False  # Whether to continue running models that don't match physical constraints (i.e. MoI), with many values set to nan. Currently only implemented for CONSTANT_INNER_DENSITY = True and only allows broken MoI matching. Broken Tb_K matching is also intended.
Params.DEPRECATED =       False  # Whether to allow deprecated code to run. Will often cause errors.

# Plot Settings
Params.SKIP_PLOTS =       False  # Whether to skip creation of all plots
Params.PLOT_GRAVITY =     True  # Whether to plot Gravity and Pressure
Params.PLOT_HYDROSPHERE = True  # Whether to plot Conductivity with Interior Properties (Hydrosphere)
Params.PLOT_REF =         True  # Whether to plot reference melting curve densities on hydrosphere plot
Params.PLOT_SIGS =        True  # Whether to plot conductivities as a function of radius on hydrosphere plot if they have been calculated
Params.PLOT_SOUNDS =      True  # Whether to plot sound speeds as a function of radius on hydrosphere plot if they have been calculated
Params.PLOT_TRADEOFF =    True  # Whether to plot mantle properties tradeoff
Params.PLOT_POROSITY =    True  # Whether to plot porosities in rock and/or ice for bodies that have it modeled
Params.PLOT_SEISMIC =     True  # Whether to plot seismic quantities if they have been calculated
Params.PLOT_WEDGE =       True  # Whether to plot interior wedge diagram
Params.LEGEND =           True  # Whether to include legends

# Magnetic induction plot settings
Params.DO_INDUCTOGRAM =          False  # Whether to evaluate and/or plot an inductogram for the body in question
Params.PLOT_FFT =                True  # Whether to show plots of fourier space
Params.INDUCTOGRAM_IN_PROGRESS = False  # Whether we are currently working on constructing an inductogram
Params.COMBINE_BCOMPS =          False  # Whether to plot Bx, By, Bz with phase all in one plot, or separate for each comp

# Parameter exploration plot settings
Params.DO_EXPLOREOGRAM = False  # Whether to evaluate and/or plot an exploreogram for the body in question
Params.SKIP_INDUCTION = False  # Whether to skip past induction calculations. Primarily intended to avoid duplicate calculations in exploreOgrams
# Options for x/y variables: "xFeS", "rhoSilInput_kgm3", "wOcean_ppt", "Tb_K", "ionosTop_km", "sigmaIonos_Sm",
# "silPhi_frac", "silPclosure_MPa", "icePhi_frac", "icePclosure_MPa", "Htidal_Wm3", "Qrad_Wkg", "qSurf_Wm2" (Do.NO_H2O only)
ExploreParams = ExploreParamsStruct()
ExploreParams.xName = 'xFeS'  # x variable over which to iterate for exploreograms. Options are as above.
ExploreParams.yName = 'rhoSilInput_kgm3'  # y variable over which to iterate for exploreograms. Options are as above.
ExploreParams.zName = 'Rcore_km'  # heatmap/colorbar/z variable to plot for exploreograms. Options are "Rcore_km", "qSurf_Wm2" (only if Do.NO_H2O is False).
ExploreParams.xRange = [0, 1]  # [min, max] values for the x variable above
ExploreParams.yRange = [2000, 4500]  # Same as above for y variable
ExploreParams.nx = 50  # Number of points to use in linspace with above x range
ExploreParams.ny = 50  # Same as above for y

# Reference profile settings
# Salinities of reference melting curves in ppt
Params.wRef_ppt = {'none':[0], 'PureH2O':[0],
                   'Seawater':[0, 0.5*Constants.stdSeawater_ppt, Constants.stdSeawater_ppt, 1.5*Constants.stdSeawater_ppt],
                   'MgSO4':[0, 33.3, 66.7, 100],
                   'NH3':[0, 10, 20],
                   'NaCl':[0, 17.5, 35]}

# SPICE kernels to use
Params.spiceTLS = 'naif0012.tls'  # Leap-seconds kernel
Params.spicePCK = 'pck00010.tpc'  # Planetary Constants Kernel from SPICE in order to get body radii
Params.spiceJupiter = 'jup365.bsp'  # Generic kernel for Jupiter + Galilean moons
Params.spiceSaturn = 'sat427.bsp'  # Generic kernel for Saturn + large moons
Params.spiceUranus = 'ura111.bsp'  # Generic kernel for Uranus + large moons
Params.spiceNeptune = 'nep095.bsp'  # Generic kernel for Neptune + large moons
