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
# Author: Walter Szeliga
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





import os
import math
import logging
import logging.config
logging.config.fileConfig(os.path.join(os.environ['ISCE_HOME'], 'defaults',
    'logging', 'logging.conf'))
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
from isceobj.Location.Peg import Peg
from iscesys.Component.FactoryInit import FactoryInit

class CalculatePegPoint(FactoryInit):

    def calculatePegPoint(self):
        self.logger.info("Parsing Raw Data")
        self.sensorObj.parse()
        frame = self.sensorObj.getFrame()
        # First, get the orbit nadir location at mid-swath and the end of the scene
        orbit = self.sensorObj.getFrame().getOrbit()
        midxyz = orbit.interpolateOrbit(frame.getSensingMid())
        endxyz = orbit.interpolateOrbit(frame.getSensingStop())
        # Next, calculate the satellite heading from the mid-point to the end of the scene
        ellipsoid = frame.getInstrument().getPlatform().getPlanet().get_elp()
        midllh = ellipsoid.xyz_to_llh(midxyz.getPosition())
        endllh = ellipsoid.xyz_to_llh(endxyz.getPosition())
        heading = ellipsoid.geo_hdg(midllh,endllh)
        # Then create a peg point from this data
        peg = Peg(latitude=midllh[0],longitude=midllh[1],heading=heading,ellipsoid=ellipsoid)
        self.logger.info("Peg Point:\n%s" % peg)

    def __init__(self,arglist):
        FactoryInit.__init__(self)
        self.initFactory(arglist)
        self.sensorObj = self.getComponent('Sensor')
        self.logger = logging.getLogger('isce.calculatePegPoint')

if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("Usage:%s <xml-parameter file>" % sys.argv[0])
        sys.exit(1)
    runObj = CalculatePegPoint(sys.argv[1:])
    runObj.calculatePegPoint()
