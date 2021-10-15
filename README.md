# PlanetProfile v1.2.0
Matlab software for constructing 1D interior structure models based on planetary properties. Self-consistent thermodynamics are used for fluid, rock, and mineral phases. Sound speeds, attenuation, and electrical conductivities are computed as outputs. The main code is called from an input file containing all the planetary data. Ideally, no tweaks to the main code are needed in order to change the outputs of the model.

## Acknowledging PlanetProfile
We want to hear about your work with PlanetProfile! Please consider sending us a message alerting us to your work (svance@jpl.caltech.edu). Suggested acknowledgement in publications: "Data used in this work were generated using the open source PlanetProfile software hosted on GitHub."

## Prerequisites
* SeaFreeze -- see https://github.com/Bjournaux/SeaFreeze
* Matlab "Curve Fitting Toolbox"
* Matlab "Image Processing Toolbox"
* Matlab "Optimization Toolbox"
* Matlab "Parallel Computing Toolbox" (optional, for select applications)
* Refprop is required for NH3 solutions: https://www.nist.gov/refprop
  * Due to various complications it is not currently implemented.

## Setup
1. Install SeaFreeze by copying the contents of the Matlab folder at (https://github.com/Bjournaux/SeaFreeze) into the Thermodynamics/SeaFreeze folder of PlanetProfile.
1. Install magnetic field Fourier Transform (FT) data from C. Cochrane by copying the contents of ???????(pending) into the MagneticInduction/FieldData folder of PlanetProfile.
1. If TauP functionality is desired, download matTaup (https://github.com/g2e/seizmo/) and add mattaup, misc, and models to Utilities folder
1. Install magnetic induction data by downloading all .mat files from https://zenodo.org/record/5057572 into the MagneticInduction/FTdata folder.
1. Open a Terminal and navigate to the PlanetProfile directory.
1. Type "make install" (no quotes) and hit enter. Follow any directions you are given.
1. Open Matlab. In the Matlab Preferences menu, go to MATLAB -> General -> Toolbox path caching and click the "Update Toolbox Path Cache" button.
1. At the Matlab command prompt, run "startup" (no quotes), or close and relaunch.
1. Open the PP_____.m file for your selected body in the Matlab editor.
1. Check that your current directory is the PlanetProfile directory in Matlab.
   1. The last dir in the address bar just above the editor should say "PlanetProfile".
1. Run the PP_____.m file.
   1. In the ribbon at the top of the Matlab window, go to Editor -> Run.

## Contributing
PlanetProfile is open source software. Please see the [LICENSE](https://github.com/vancesteven/PlanetProfile/blob/master/LICENSE) file and read the guidelines for contrbuting in [CONTRIBUTING.md](https://github.com/vancesteven/PlanetProfile/blob/master/CONTRIBUTING.md) if you are interested in joining the project. Also see our community guidelines in [CODE_OF_CONDUCT.md](https://github.com/vancesteven/PlanetProfile/blob/master/CODE_OF_CONDUCT.md).

## Notes
* As of 2020-09-28, PlanetProfile v1.1.0 was released along with code for making calculations regarding magnetic induction. The development (master) branch of PlanetProfile is set up to generate profiles from minimal inputs. Output profiles that may be used along with the induction calculations may be found in the v1.1.0 release.
* The default settings include a recalculation of all parameters. It is recommended to recalculate all parameters whenever PlanetProfile is updated and any time a change in input parameters may affect layer thicknesses or other intermediate variables.
* To re-use data from past profiles, which dramatically speeds up runtime, set the CALC_NEW flags in the config.m input file to 0. If you are using git, use the following command to avoid editing the repository version of the config file:
> git update-index --assume-unchanged config.m

Some calculations use Matlab's Parallel Computing package.  If you don't have access to this package then parfor loops should be changed to for loops.  A future version will check and do this automatically.

Calculations with seawater solutions use the Gibbs Seawater package for Matlab: http://www.teos-10.org/software.htm#1

Calculations with NH3 solutions use REFPROP and require a compiled dynamic library based on the REFPROP source code (see below for placement of files).  The source can be obtained from the National Institute of Standards and Technology https://www.nist.gov/refprop
Access to REFPROP functions is through python 3 using librefprop.so: https://github.com/jowr/librefprop.so
Python capabilities are employed using the included matlab code refproppy.m
REFPROP version 10, expected in October 2017, will provide matlab functions and Mac modules, which may eliminate the need for the above workarounds.
Instructions for installing Python 3 on a Mac can be found at http://docs.python-guide.org/en/latest/starting/install3/osx/

Rock properties are from Perple_X: http://www.perplex.ethz.ch/
Input files were developed by Fabio Cammarano. Version 6.7.9 is currently being used.

Python 3 instructions (may be necessary in a future update):
  @ Find the path to the python3 executable (example command: which python3), and copy the full path
  @ In a fresh Matlab session, at the console type pyversion("/path/to/python3/executable")

## To-dos:
Modularization is not complete. 
Further equations of state are under development
Update to work with REFPROP V10

The source files and library for REFPROP should be placed in the top-level directory under /opt, as per below
$ls /opt
librefprop.dylib refprop/

$ls /opt/refprop
fluids   mixtures

$ls /opt/refprop/fluids
1BUTENE.FLD  C1CC6.FLD    COS.FLD      D6.FLD       ETHYLENE.FLD HYDROGEN.FLD MD3M.FLD     MOLEATE.FLD  NITROGEN.FLD PENTANE.FLD  R115.FLD     R124.FLD     R152A.FLD    R236FA.FLD   RE143A.FLD   WATER.FLD
ACETONE.FLD  C2BUTENE.FLD CYCLOHEX.FLD DECANE.FLD   FLUORINE.FLD IBUTENE.FLD  MD4M.FLD     MPALMITA.FLD NONANE.FLD   PROPANE.FLD  R116.FLD     R125.FLD     R161.FLD     R245CA.FLD   RE245CB2.FLD XENON.FLD
AMMONIA.FLD  C3CC6.FLD    CYCLOPEN.FLD DEE.FLD      H2S.FLD      IHEXANE.FLD  MDM.FLD      MSTEARAT.FLD NOVEC649.FLD PROPYLEN.FLD R12.FLD      R13.FLD      R21.FLD      R245FA.FLD   RE245FA2.FLD
ARGON.FLD    C4F10.FLD    CYCLOPRO.FLD DMC.FLD      HCL.FLD      IOCTANE.FLD  METHANE.FLD  MXYLENE.FLD  OCTANE.FLD   PROPYNE.FLD  R1216.FLD    R134A.FLD    R218.FLD     R32.FLD      RE347MCC.FLD
BENZENE.FLD  C5F12.FLD    D2.FLD       DME.FLD      HELIUM.FLD   IPENTANE.FLD METHANOL.FLD N2O.FLD      ORTHOHYD.FLD PXYLENE.FLD  R123.FLD     R14.FLD      R22.FLD      R365MFC.FLD  SF6.FLD
BUTANE.FLD   CF3I.FLD     D2O.FLD      EBENZENE.FLD HEPTANE.FLD  ISOBUTAN.FLD MLINOLEA.FLD NEON.FLD     OXYGEN.FLD   R11.FLD      R1233ZD.FLD  R141B.FLD    R227EA.FLD   R40.FLD      SO2.FLD
C11.FLD      CO.FLD       D4.FLD       ETHANE.FLD   HEXANE.FLD   KRYPTON.FLD  MLINOLEN.FLD NEOPENTN.FLD OXYLENE.FLD  R113.FLD     R1234YF.FLD  R142B.FLD    R23.FLD      R41.FLD      T2BUTENE.FLD
C12.FLD      CO2.FLD      D5.FLD       ETHANOL.FLD  HMX.BNC      MD2M.FLD     MM.FLD       NF3.FLD      PARAHYD.FLD  R114.FLD     R1234ZE.FLD  R143A.FLD    R236EA.FLD   RC318.FLD    TOLUENE.FLD

$ ls /opt/refprop/mixtures/
AIR.MIX      HIGHN2.MIX   R402A.MIX    R405A.MIX    R407D.MIX    R409B.MIX    R412A.MIX    R415B.MIX    R420A.MIX    R422C.MIX    R426A.MIX    R431A.mix    R436A.MIX    R442A.MIX    R502.MIX     R508B.MIX
AMARILLO.MIX NGSAMPLE.MIX R402B.MIX    R406A.MIX    R407E.MIX    R410A.MIX    R413A.MIX    R416A.MIX    R421A.MIX    R422D.MIX    R427A.MIX    R432A.mix    R436B.MIX    R443A.MIX    R503.MIX     R509A.MIX
EKOFISK.MIX  R401A.MIX    R403A.MIX    R407A.MIX    R407F.MIX    R410B.MIX    R414A.MIX    R417A.MIX    R421B.MIX    R423A.MIX    R428A.MIX    R433A.mix    R437A.MIX    R444A.MIX    R504.MIX     R510A.MIX
GLFCOAST.MIX R401B.MIX    R403B.MIX    R407B.MIX    R408A.MIX    R411A.MIX    R414B.MIX    R418A.MIX    R422A.MIX    R424A.MIX    R429A.mix    R434A.mix    R438A.mix    R500.MIX     R507A.MIX    R512A.MIX
HIGHCO2.MIX  R401C.MIX    R404A.MIX    R407C.MIX    R409A.MIX    R411B.MIX    R415A.MIX    R419A.MIX    R422B.MIX    R425A.MIX    R430A.mix    R435A.MIX    R441A.MIX    R501.MIX     R508A.MIX  
