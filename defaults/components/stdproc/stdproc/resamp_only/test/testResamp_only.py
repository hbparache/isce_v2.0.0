#!/usr/bin/env python3

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2010 to the present, California Institute of Technology.
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
# Author: Giangi Sacco
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





from __future__ import print_function
import sys
import os
import math
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
from isceobj.Image.AmpImageBase import AmpImage
from iscesys.Component.InitFromXmlFile import InitFromXmlFile
from iscesys.Component.InitFromDictionary import InitFromDictionary
from stdproc.stdproc.resamp_only.Resamp_only import Resamp_only

def main():
    filename = sys.argv[1] #rgoffset.out
    fin = open(filename)
    allLines = fin.readlines()
    locationAc = []
    locationAcOffset = []
    locationDn = []
    locationDnOffset = []
    snr = []
    for line in allLines:
        lineS = line.split()
        locationAc.append(float(lineS[0]))
        locationAcOffset.append(float(lineS[1]))
        locationDn.append(float(lineS[2]))
        locationDnOffset.append(float(lineS[3]))
        snr.append(float(lineS[4]))
    dict = {}
    dict['LOCATION_ACROSS1'] = locationAc
    dict['LOCATION_ACROSS_OFFSET1'] = locationAcOffset
    dict['LOCATION_DOWN1'] = locationDn
    dict['LOCATION_DOWN_OFFSET1'] = locationDnOffset
    dict['SNR1'] = snr
    objAmpIn = AmpImage()
    # only sets the parameter
    # it actually creates the C++ object
    objAmpIn.initImage('alos.int','read',2053)
    objAmpIn.createImage()
    

    objAmpOut = AmpImage()
    objAmpOut.initImage('resampImageOnly.int','write',2053)
    objAmpOut.createImage()
    # only sets the parameter
    # it actually creates the C++ object
    objAmpOut.createImage()
    obj = Resamp_only()
    obj.setLocationAcross1(locationAc) 
    obj.setLocationAcrossOffset1(locationAcOffset) 
    obj.setLocationDown1(locationDn) 
    obj.setLocationDownOffset1(locationDnOffset) 
    obj.setSNR1(snr)
    obj.setNumberLines(2816) 
    obj.setNumberFitCoefficients(6)
    obj.setNumberRangeBin(2053)
    obj.setDopplerCentroidCoefficients([-0.224691,0,0,0])
    obj.radarWavelength = 0.0562356424
    obj.setSlantRangePixelSpacing(0)
    obj.resamp_only(objAmpIn,objAmpOut)

    azCarrier = obj.getAzimuthCarrier()
    raCarrier = obj.getRangeCarrier()
    #for i in range(len(azCarrier)):
    #    print(azCarrier[i],raCarrier[i])
    objAmpIn.finalizeImage()
    objAmpOut.finalizeImage()
    print('goodbye')
if __name__ == "__main__":
    sys.exit(main())
