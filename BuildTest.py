""" This is a test script meant to check that the current PlanetProfile
    build maintains all functionality across updates. Run this script
    as "python Testing.py" from the main PlanetProfile directory
    before committing any major updates. New major functionality added
    to PlanetProfile should be accompanied by a new PPTest#.py test
    body in the Test/ directory.
"""

from PlanetProfile import PlanetProfile
from config import Params
import logging as log
import importlib, os, fnmatch, sys

def full():
    # Include timestamps in messages and force debug level logging
    log.basicConfig(level=log.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')
    testBase = 'Test.PPTest'

    # Set general testing config atop standard config options
    Params.CALC_NEW =       True
    Params.CALC_NEW_REF =   True
    Params.CALC_NEW_INDUC = True
    Params.CALC_SEISMIC =   True
    Params.CALC_CONDUCT =   True

    # Get first test profile separately, as we will reuse it
    testPlanet1 = importlib.import_module(f'{testBase}{1}').Planet
    testPlanet1 = PlanetProfile(testPlanet1, Params)
    # Loop over remaining test profiles
    nTests = len(fnmatch.filter(os.listdir('Test'), 'PPTest*'))
    for i in range(1, nTests):
        testPlanetN = importlib.import_module(f'{testBase}{i}').Planet
        testPlanetN = PlanetProfile(testPlanetN, Params)

    # Test that we can successfully run things not including parallelization options
    Params.DO_PARALLEL = False
    testPlanet1 = PlanetProfile(testPlanet1, Params)

    # Make sure our auxiliary calculation flags work correctly
    Params.CALC_SEISMIC =   False
    Params.CALC_CONDUCT =   False
    testPlanet1 = PlanetProfile(testPlanet1, Params)

    # Check that skipping layers/portions work correctly
    Params.SKIP_INNER =  False
    testPlanet1 = PlanetProfile(testPlanet1, Params)

    # Verify that we can reload things as needed
    Params.CALC_NEW =       False
    Params.CALC_NEW_REF =   False
    Params.CALC_NEW_INDUC = False
    testPlanet1 = PlanetProfile(testPlanet1, Params)

    log.info('Testing complete!')
    return


def simple():
    # Include timestamps in messages and force debug level logging
    log.basicConfig(level=log.DEBUG, format='[%(levelname)s] %(asctime)s - %(message)s')
    testMod = 'Test.PPTest'

    # Set general testing config atop standard config options
    Params.CALC_NEW = True
    Params.CALC_NEW_REF = True
    Params.CALC_NEW_INDUC = True
    Params.CALC_SEISMIC = True
    Params.CALC_CONDUCT = True

    testPlanet = importlib.import_module('Test.PPTest3').Planet
    testPlanet = PlanetProfile(testPlanet, Params)
    log.info('Simple test complete!')
    return


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Test type was passed as command line argument
        testType = sys.argv[1]
    else:
        testType = 'full'

    if testType == 'simple':
        simple()
    else:
        full()