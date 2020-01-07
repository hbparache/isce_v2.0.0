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


from isceobj.Constants import SPEED_OF_LIGHT

logger = logging.getLogger('isce.insar.runPrepareResamps')

def runPrepareResamps(self, rangeLooks=None, azLooks=None):
    import math
    slaveOrbit = self.insar.slaveOrbit
    masterFrame = self.insar.masterFrame
    peg = self.insar.peg
    masterSlcImage = self.insar.masterSlcImage
    time2, schPosition2, schVelocity2, offset2 = slaveOrbit._unpackOrbit()
    
    s2 = schPosition2[0][0]
    s2_2 = schPosition2[1][0]
    
    valid_az_samples =  self.insar.numberValidPulses
    numPatches = self.insar.numberPatches
    lines = numPatches * valid_az_samples 
    
    fs = masterFrame.getInstrument().getRangeSamplingRate()
    dr = (SPEED_OF_LIGHT / (2 * fs))
    
    self._insar.setSlantRangePixelSpacing(dr)
    
#    widthSlc = max(self._insar.getMasterSlcImage().getWidth(), self._insar.getSlaveSlcImage().getWidth())
    widthSlc = self._insar.getMasterSlcImage().getWidth()
    
    radarWavelength = masterFrame.getInstrument().getRadarWavelength()
    
    rc = peg.getRadiusOfCurvature()  
    ht = self._insar.getAverageHeight()
    r0 = masterFrame.getStartingRange()
    
    range = r0 + (widthSlc / 2 * dr)
    
    costheta = (2*rc*ht+ht*ht-range*range)/-2/rc/range
    sininc = math.sqrt(1 - (costheta * costheta))
    
    posting = self.posting
    grndpixel = dr / sininc
    
    if rangeLooks:
        looksrange=rangeLooks
    else:
        looksrange=int(posting/grndpixel+0.5)

    if azLooks:
        looksaz=azLooks
    else:
        looksaz=int(round(posting/(s2_2 - s2)))
    
    if (looksrange < 1):
        logger.warn("Number range looks less than zero, setting to 1")
        looksrange = 1
    if (looksaz < 1):
        logger.warn("Number azimuth looks less than zero, setting to 1")
        looksaz = 1

    self._insar.setNumberAzimuthLooks(looksaz) 
    self._insar.setNumberRangeLooks(looksrange) 
    self._insar.setNumberResampLines(lines) 
    

    #jng at one point this will go in the defaults of the self._insar calss
    numFitCoeff = 6
    self._insar.setNumberFitCoefficients(numFitCoeff) 
