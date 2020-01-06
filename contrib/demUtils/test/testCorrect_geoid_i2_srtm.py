#!/usr/bin/env python3

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
# Author: Giangi Sacco
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





from __future__ import print_function
import sys
import os
import math
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
from contrib.demUtils.Correct_geoid_i2_srtm import Correct_geoid_i2_srtm

def main():
    
    from iscesys.StdOEL.StdOELPy import StdOEL as ST
    stdWriter = ST()
    stdWriter.createWriters()
    stdWriter.configWriter("log","",True,"insar.log")
    stdWriter.init()
    obj = Correct_geoid_i2_srtm()
    obj.setInputFilename(sys.argv[1])
    #if outputFilenmae not specified the input one is overwritten
    obj.setOutputFilename(sys.argv[1] + '.id')
   
    obj.setStdWriter(stdWriter)
    obj.setWidth(int(sys.argv[2]))
    obj.setStartLatitude(float(sys.argv[3]))
    obj.setStartLongitude(float(sys.argv[4]))
    obj.setDeltaLatitude(float(sys.argv[5]))
    obj.setDeltaLongitude(float(sys.argv[6]))
    # -1 EGM96 -> WGS84, 1 WGS84 -> EGM96
    obj.setConversionType(int(sys.argv[7]))
    obj.correct_geoid_i2_srtm()
    
if __name__ == "__main__":
    sys.exit(main())
