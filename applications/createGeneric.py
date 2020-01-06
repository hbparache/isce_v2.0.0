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
import isceobj
from iscesys.Component.FactoryInit import FactoryInit

class ToGeneric(object):
# Convert from a satellite-specific format, to a generic HDF5-based format.

    def __init__(self,rawObj=None):
        self.rawObj = rawObj
        self.logger = logging.getLogger('isce.toGeneric')

    def convert(self):
        from isceobj.Sensor.Generic import Generic
        doppler = isceobj.Doppler.useDOPIQ()
        hhRaw = self.make_raw(self.rawObj,doppler)
        hhRaw.getFrame().getImage().createImage()

        writer = Generic()
        writer.frame = hhRaw.getFrame()
        writer.write('test.h5',compression='gzip')

    def make_raw(self,sensor,doppler):
        """
        Extract the unfocused SAR image and associated data

        @param sensor (\a isceobj.Sensor) the sensor object
        @param doppler (\a isceobj.Doppler) the doppler object
        @return (\a make_raw) a make_raw instance
        """
        from make_raw import make_raw
        import stdproc
        import isceobj

        # Extract raw image
        self.logger.info("Creating Raw Image")
        mr = make_raw()
        mr.wireInputPort(name='sensor',object=sensor)
        mr.wireInputPort(name='doppler',object=doppler)
        mr.make_raw()

        return mr

def main():
    import sys
    import isceobj

    fi = FactoryInit()
    fi.fileInit = sys.argv[1]
    fi.defaultInitModule = 'InitFromXmlFile'
    fi.initComponentFromFile()

    master = fi.getComponent('Master')

    toGeneric = ToGeneric(rawObj=master)
    toGeneric.convert()

if __name__ == "__main__":
    main()
