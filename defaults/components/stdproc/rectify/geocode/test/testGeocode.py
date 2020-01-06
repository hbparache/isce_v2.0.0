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
from iscesys.Component.InitFromXmlFile import InitFromXmlFile
from isceobj.Image.DemImage import DemImage
from isceobj.Image.IntImage import IntImage
from stdproc.rectify.geocode.Geocode import Geocode

def main():
    referenceOrbit = sys.argv[1] #look for reference_orbit.txt
    fin1 = open(referenceOrbit)
    allLines = fin1.readlines()
    s_mocomp = []
    for line in allLines:
        lineS = line.split()
        s_mocomp.append(float(lineS[2]))
    fin1.close()
    initfileDem = 'DemImage.xml'
    initDem = InitFromXmlFile(initfileDem)
    objDem = DemImage()
    # only sets the parameter
    objDem.initComponent(initDem)
    # it actually creates the C++ object
    objDem.createImage()
    
    initfileTopo = 'TopoImage.xml'
    initTopo = InitFromXmlFile(initfileTopo)
    objTopo = IntImage()
    # only sets the parameter
    objTopo.initComponent(initTopo)
    # it actually creates the C++ object
    objTopo.createImage()
    initFile = 'Geocode.xml' 
    fileInit = InitFromXmlFile(initFile)

    obj = Geocode()
    obj.initComponent(fileInit)
    obj.setReferenceOrbit(s_mocomp)
    obj.geocode(objDem,objTopo)
    geoWidth= obj.getGeoWidth()
    geoLength  = obj.getGeoLength()
    latitudeSpacing = obj.getLatitudeSpacing()
    longitudeSpacing = obj.getLongitudeSpacing()
    minimumGeoLatitude = obj.getMinimumGeoLatitude()
    minimumGeoLongitude = obj.getMinimumGeoLongitude()
    maximumGeoLatitude = obj.getMaximumGeoLatitude()
    maximumGeoLongitude = obj.getMaxmumGeoLongitude()
    print(geoWidth,\
    geoLength,\
    latitudeSpacing,\
    longitudeSpacing,\
    minimumGeoLatitude,\
    minimumGeoLongitude,\
    maximumGeoLatitude,\
    maximumGeoLongitude)
    
    objDem.finalizeImage()
    objTopo.finalizeImage()
if __name__ == "__main__":
    sys.exit(main())
