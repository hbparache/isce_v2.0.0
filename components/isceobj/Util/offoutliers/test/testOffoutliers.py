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
from isceobj.Util.Offoutliers import Offoutliers

def main():

#############################
#be careful that the lists are passed by reference and changed during the computation. If need the old one do a  deep copy
############################
    filename = sys.argv[1]
    fin = open(filename)
    allLines = fin.readlines()
    locationAc = []
    locationAcOffset = []
    locationDn = []
    locationDnOffset = []
    snr = []
    distance = 10
    for line in allLines:
        lineS = line.split()
        locationAc.append(float(lineS[0]))
        locationAcOffset.append(float(lineS[1]))
        locationDn.append(float(lineS[2]))
        locationDnOffset.append(float(lineS[3]))
        snr.append(float(lineS[4]))
    obj = Offoutliers()
    obj.setLocationAcross(locationAc)
    obj.setLocationAcrossOffset(locationAcOffset)
    obj.setLocationDown(locationDn)
    obj.setLocationDownOffset(locationDnOffset)
    obj.setSNR(snr)
    sign = [1]*len(snr)
    obj.setSign(sign)
    obj.setDistance(distance)
    obj.offoutliers()
    indxA = obj.getIndexArray()
    '''
    for el in indxA:
        print(el,locationAc[el],locationAcOffset[el],locationDn[el],locationDnOffset[el],snr[el])
    '''
if __name__ == "__main__":
    sys.exit(main())
