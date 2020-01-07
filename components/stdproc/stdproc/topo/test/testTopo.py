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
from stdproc.stdproc.topo.Topo import Topo

def main():
    #need actual or soft link to alos.int and dem.la
    referenceOrbit = sys.argv[1] #look for reference_orbit.txt
    fin1 = open(referenceOrbit)
    allLines = fin1.readlines()
    s_mocomp = []
    for line in allLines:
        lineS = line.split()
        s_mocomp.append(float(lineS[2]))
    fin1.close()
    from  isceobj import Image as IF
    
    demNameXml = 'la.dem.xml'
    from iscesys.Parsers.FileParserFactory import createFileParser
    parser = createFileParser('xml')
    #get the properties from the file init file
    prop = parser.parse(demNameXml)[0]
    objDem  = IF.createDemImage()
    objDem.initProperties(prop)
    objDem.createImage()
    obj = Topo()
    obj.setReferenceOrbit(s_mocomp)
    intImage = IF.createIntImage()
    width = 1328
    filename = 'alos.int'
    intImage.initImage(filename,'read',width)
    intImage.createImage()       
    obj.wireInputPort(name='interferogram',object=intImage)    
    obj.wireInputPort(name='dem',object=objDem)
    obj.pegLatitude = 0.58936848339144254
    obj.pegLongitude = -2.1172133973559606
    obj.pegHeading = -0.22703294510994310
    obj.planetLocalRadius = 6356638.1714100000
    # Frame information
    obj.slantRangePixelSpacing =  9.3685142500000005
    obj.prf = 1930.502000000000
    obj.radarWavelength =  0.23605699999999999 
    obj.rangeFirstSample =   750933.00000000000
    # Doppler information
    # Make_raw information
    obj.spacecraftHeight = 698594.96239000000
    obj.bodyFixedVelocity = 7595.2060428100003
    obj.isMocomp = 3072
    obj.numberRangeLooks = 1
    obj.numberAzimuthLooks = 4 
    obj.dopplerCentroidConstantTerm = .0690595
    obj.topo()
    minLat = obj.getMinimumLatitude()
    maxLat = obj.getMaximumLatitude()
    minLon = obj.getMinimumLongitude()
    maxLon = obj.getMaximumLongitude()
    azspace = obj.getAzimuthSpacing()
    s0 = obj.getSCoordinateFirstLine()
    print(minLat,maxLat,minLon,maxLon,azspace,s0)
    #squintShift = obj.getSquintShift()
    #for el in squintShift:
        #print(el)
    intImage.finalizeImage()
    objDem.finalizeImage()

if __name__ == "__main__":
    sys.exit(main())
