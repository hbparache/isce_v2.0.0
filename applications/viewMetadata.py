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
import logging
import logging.config
logging.config.fileConfig(os.path.join(os.environ['ISCE_HOME'], 'defaults',
    'logging', 'logging.conf'))
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
from iscesys.Component.FactoryInit import FactoryInit
from isceobj.Renderer.XmlRenderer import XmlRenderer

class viewMetadataApp(FactoryInit):

    def main(self):
        self.logger.info('Parsing Metadata')
        self.sensorObj.extractImage()
        frame = self.sensorObj.getFrame()
        instrument = frame.getInstrument()
        platform = instrument.getPlatform()
        orbit = frame.getOrbit()
        attitude = frame.getAttitude()
        print(platform)
        print(instrument)
        print(frame)
        print(orbit)
        for sv in orbit:
            print(sv)

        print(attitude)
        for sv in attitude:
            print(sv)

        self.logger.info('Rendering Metadata')
        self.renderer.setComponent(frame)
        self.renderer.render()

    def __init__(self,arglist):
        FactoryInit.__init__(self)
        self.initFactory(arglist)
        self.logger = logging.getLogger('isce.viewMetadata')
        self.sensorObj = self.getComponent('Sensor')
        self.renderer = self.getComponent('XmlRenderer')


if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("Usage:%s <xml-parameter file>" % sys.argv[0])
        sys.exit(1)
    runObj = viewMetadataApp(sys.argv[1:])
    runObj.main()
