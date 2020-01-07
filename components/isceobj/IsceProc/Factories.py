#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2013 to the present, California Institute of Technology.
# ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged.
# Any commercial use must be negotiated with the Office of Technology Transfer
# at the California Institute of Technology.
# 
# This software may be subject to U.S. export control laws. By accepting this
# software, the user agrees to comply with all applicable U.S. export laws and
# regulations. User has the responsibility to obtain export licenses,  or other
# export authority as may be required before exporting such information to
# foreign countries or providing access to foreign persons.
# 
# Installation and use of this software is restricted by a license agreement
# between the licensee and the California Institute of Technology. It is the
# User's responsibility to abide by the terms of the license agreement.
#
# Author: Kosal Khun
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Comment: Adapted from InsarProc/Factories.py
# Path to the _RunWrapper factories
_PATH = "isceobj.IsceProc."

__todo__ = "use 2.7's importlib"

## A factory to make _RunWrapper factories
def _factory(name, other_name=None):
    """create_run_wrapper = _factory(name)
    name is the module and class function name
    """
    other_name = other_name or name
    module = __import__(
        _PATH+name, fromlist=[""]
        )

    cls = getattr(module, other_name)
    def creater(other, *args, **kwargs):
        """_RunWrapper for object calling %s"""
        return _RunWrapper(other, cls)
    return creater

## Put in "_" to prevent import on "from Factories import *"
class _RunWrapper(object):
    """_RunWrapper(other, func)(*args, **kwargs)

    executes:

    func(other, *args, **kwargs)

    (like a method)
    """
    def __init__(self, other, func):
        self.method = func
        self.other = other
        return None

    def __call__(self, *args, **kwargs):
        return self.method(self.other, *args, **kwargs)

    pass

# we turned runFormSLC into a facility
def createFormSLC(other, do_formslc, sensor):
    if not do_formslc:
        return None
    if sensor.lower() in ["terrasarx","cosmo_skymed_slc"]:
        from runFormSLCTSX import runFormSLC
    else:
        from runFormSLC import runFormSLC
    return _RunWrapper(other, runFormSLC)


def createOffsetprf(other, do_offsetprf, coregisterMethod):
    if not do_offsetprf:
        return None
    if coregisterMethod.lower() == "ampcor":
        from runOffsetprf_ampcor import runOffsetprf
    else:
        from runOffsetprf import runOffsetprf
    return _RunWrapper(other, runOffsetprf)


createCreateDem = _factory("createDem")
createExtractInfo = _factory("extractInfo")
createPreprocessor = _factory("runPreprocessor")
createPulseTiming = _factory("runPulseTiming")
createEstimateHeights = _factory("runEstimateHeights")
createSetmocomppath = _factory("runSetmocomppath")
createOrbit2sch = _factory("runOrbit2sch")
createUpdatePreprocInfo = _factory("runUpdatePreprocInfo")
createOffoutliers = _factory("runOffoutliers")
createPrepareResamps = _factory("runPrepareResamps")
createResamp = _factory("runResamp")
createResamp_image = _factory("runResamp_image")
createISSI = _factory("runISSI")
createCrossmul = _factory("runCrossmul") #2013-11-26
createMocompbaseline = _factory("runMocompbaseline")
createTopo = _factory("runTopo")
createCorrect = _factory("runCorrect")
createShadecpx2rg = _factory("runShadecpx2rg")
createRgoffset = _factory("runRgoffset")
createResamp_only = _factory("runResamp_only")
createCoherence = _factory("runCoherence")
createFilter = _factory("runFilter")
createGrass = _factory("runGrass")
createGeocode = _factory("runGeocode")

