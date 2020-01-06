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
from isceobj.Image.MhtImage import MhtImage
from iscesys.Component.InitFromXmlFile import InitFromXmlFile
from iscesys.Component.InitFromDictionary import InitFromDictionary
from stdproc.stdproc.resamp_image.Resamp_image import Resamp_image

def main():
    
    filename = sys.argv[1] # rgoffset.out
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
    initDict = InitFromDictionary(dict)
    initfileResamp_image = 'Resamp_image.xml'

    initResamp_image = InitFromXmlFile(initfileResamp_image)

    initfileRangeIm = 'RangeOffsetImage.xml'
    initRangeIm = InitFromXmlFile(initfileRangeIm)
    
    objRangeIm = MhtImage()
    # only sets the parameter
    objRangeIm.initComponent(initRangeIm)
    # it actually creates the C++ object
    objRangeIm.createImage()
    obj = Resamp_image()
    obj.initComponent(initResamp_image)
    obj.initComponent(initDict)
    obj.resamp_image(objRangeIm)

    objRangeIm.finalizeImage()
if __name__ == "__main__":
    sys.exit(main())
