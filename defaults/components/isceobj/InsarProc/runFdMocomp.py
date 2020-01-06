#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2012 to the present, California Institute of Technology.
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
# Author: Brett George
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import logging
import stdproc
import sys
logger = logging.getLogger('isce.insar.runFdMocomp')

## Mapping from use_dop kewword to f(masterDop, slaveDrop)
USE_DOP = {'AVERAGE' : lambda x, y: (x+y)/2.,
           'MASTER': lambda x, y: x,
           'SLAVE': lambda x, y: y}

def runFdMocomp(self, use_dop="average"):
    """
    Calculate motion compenstation correction for Doppler centroid
    """
    H1 = self.insar.fdH1
    H2 = self.insar.fdH2
    peg = self.insar.peg
    lookSide = self.insar._lookSide
    masterOrbit = self.insar.masterOrbit
    slaveOrbit = self.insar.slaveOrbit
    rangeSamplingRate = (
        self.insar.getMasterFrame().instrument.rangeSamplingRate)
    rangePulseDuration = (
        self.insar.getSlaveFrame().instrument.pulseLength)
    chirpExtension = self.insar.chirpExtension
    chirpSize = int(rangeSamplingRate * rangePulseDuration)
   
    number_range_bins = self.insar.numberRangeBins
   
    masterCentroid = self.insar.masterDoppler.fractionalCentroid
    slaveCentroid = self.insar.slaveDoppler.fractionalCentroid
    logger.info("Correcting Doppler centroid for motion compensation")


    result = []
    for centroid, frame, orbit, H in zip((masterCentroid, slaveCentroid),
                                      (self.insar.masterFrame,
                                       self.insar.slaveFrame),
                                         (masterOrbit, slaveOrbit),
                                         (H1, H2)
                                      ):
        fdmocomp = stdproc.createFdMocomp()
        fdmocomp.wireInputPort(name='frame', object=frame)
        fdmocomp.wireInputPort(name='peg', object=peg)
        fdmocomp.wireInputPort(name='orbit', object=orbit)
        fdmocomp.setWidth(number_range_bins)
        fdmocomp.setSatelliteHeight(H)
        fdmocomp.setDopplerCoefficients([centroid, 0.0, 0.0, 0.0])
        fdmocomp.setLookSide(lookSide)
        fdmocomp.fdmocomp()
        result.append( fdmocomp.dopplerCentroid )
        pass

    masterDopplerCorrection, slaveDopplerCorrection = result

#    print masterDopplerCorrection, slaveDopplerCorrection
#    use_dop = "F"
    try:
        fd = USE_DOP[use_dop.upper()](masterDopplerCorrection,
                                      slaveDopplerCorrection)
    except KeyError:
        print("Unrecognized use_dop option.  use_dop = ",use_dop)
        print("Not found in dictionary:",USE_DOP.keys())
        sys.exit(1)
        pass
    
    logger.info("Updated Doppler Centroid: %s" % (fd))
    return fd



