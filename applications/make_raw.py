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

import isce
from iscesys.Compatibility import Compatibility
from iscesys.Component.Component import Component, Port
from isceobj.Planet.Ellipsoid import Ellipsoid
from isceobj.Doppler.Doppler import Doppler
from isceobj.Orbit.Orbit import Orbit
#from iscesys.DateTimeUtil.DateTimeUtil import DateTimeUtil as DTU
from iscesys import DateTimeUtil as DTU

from iscesys.Component.Application import Application
from isce.applications.insarApp import SENSOR_NAME, DOPPLER_METHOD
from isceobj.Scene.Frame import FrameMixin

from isceobj.Util.decorators import port

SENSOR = Application.Facility('sensor',
                              public_name='sensor',
                              module='isceobj.Sensor',
                              factory='createSensor',
                              args=('sensorName', ),
                              mandatory=True,
                              doc="Master raw data component"
                              )
DOPPLER = Application.Facility('doppler',
                               public_name='doppler',
                               module='isceobj.Doppler',
                               factory='createDoppler',
                               args=('dopplerMethod', ),
                               mandatory=False,
                               doc="Master Doppler calculation method"
                                 )

class makeRawApp(Application):

    parameter_list = (SENSOR_NAME, DOPPLER_METHOD)
    facility_list = (SENSOR, DOPPLER)


    def _facilities(self):
        """
        Define the user configurable facilities for this application.
        """
        self.sensor = self.facility(
            'sensor',
            public_name='sensor',
            module='isceobj.Sensor',
            factory='createSensor',
            args=(self.sensorName, ),
            mandatory=True,
            doc="Sensor raw data component"
        )
        self.doppler = self.facility(
            'doppler',
            public_name='doppler',
            module='isceobj.Doppler',
            factory='createDoppler',
            args=(self.dopplerMethod, ),
            mandatory=False,
            doc="Doppler calculation method"
        )

    def main(self):
        self.make_raw.wireInputPort(name='doppler', object=self.doppler)
        self.make_raw.wireInputPort(name='sensor', object=self.sensor)
        self.make_raw.make_raw()
        self.printInfo()

    def printInfo(self):
        print(self.make_raw.frame)
        print(self.make_raw)

    def __init__(self):
        Application.__init__(self, "makeraw")
        self.sensor = None
        self.doppler = None
        self.make_raw = make_raw()

    def initFromArglist(self, arglist):
        self.initFactory(arglist)
        self.sensor = self.getComponent('Sensor')
        self.doppler = self.getComponent('Doppler')


class make_raw(Component, FrameMixin):

    def __init__(self):
        Component.__init__(self)
        self.sensor = None
        self.doppler = None
        self.dopplerValues = None
        self.frame = None
        # Derived Values
        self.spacecraftHeight = 0.0
        self.heightDt = 0.0
        self.velocity = 0.0
        self.squint = 0.0

        sensorPort = Port(name='sensor', method=self.addSensor)
        dopplerPort = Port(name='doppler', method=self.addDoppler)

        self._inputPorts.add(sensorPort)
        self._inputPorts.add(dopplerPort)
        self.logger = logging.getLogger("isce.make_raw")
        return None

    def __getstate__(self):
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        self.__dict__.update(d)
        self.logger = logging.getLogger("isce.make_raw")
        return None

    @port('extractImage')
    def addSensor(self):
        return None

    @port('calculateDoppler')
    def addDoppler(self):
        return None

    def getFrame(self):
        return self.frame

    def getDopplerValues(self):
        return self.dopplerValues

    def getSpacecraftHeight(self):
        return self.spacecraftHeight

    def getHeightDT(self):
        return self.heightDt

    def getVelocity(self):
        return self.velocity

    def getSquint(self):
        return self.squint

    def calculateHeightDt(self):
        orbit = self.orbit
        ellipsoid = self.ellipsoid
        startTime = self.sensingStart
        midTime = self.sensingMid
        sv0 = orbit.interpolate(startTime)
        sv1 = orbit.interpolate(midTime)

        startHeight = sv0.calculateHeight(ellipsoid)
        midHeight = sv1.calculateHeight(ellipsoid)
        self.spacecraftHeight = startHeight
        self.heightDt = (
            (midHeight - startHeight)/
            DTU.timeDeltaToSeconds(midTime - startTime)
            )

    def calculateVelocity(self):
        import math
        orbit = self.orbit
        midTime = self.sensingMid

        sv = orbit.interpolateOrbit(midTime)
        vx1, vy1, vz1 = sv.velocity
        self.velocity = math.sqrt(vx1**2 + vy1**2 + vz1**2)

    def calculateSquint(self):
        """Calculate the squint angle
            R0 is the starting range
            h is the height at mid-swath
            v is the velocity at mid-swath
        """
        import math
        startingRange = self.startingRange
        prf = self.PRF
        wavelength = self.radarWavelength
        h = self.spacecraftHeight
        v = self.velocity

        if h > startingRange:
            raise ValueError("Spacecraft Height too large (%s>%s)" %
                             (h, startingRange))

        sinTheta = math.sqrt( 1 - (h/startingRange)**2 )
        fd = self.doppler.quadratic['a']*prf
        sinSquint = fd/(2.0*v*sinTheta)*wavelength
        if sinSquint**2 > 1:
            raise ValueError(
                "Error in One or More of the Squint Calculation Values\n"+
                "Doppler Centroid: %s\nVelocity: %s\nWavelength: %s\n" %
                (fd, v, wavelength)
                )
        self.squint = math.degrees(
            math.atan2(sinSquint, math.sqrt(1-sinSquint**2))
            )
        #jng squint is also used later on from the frame, just add it here
        self.frame.squintAngle = math.radians(self.squint)

    def make_raw(self):
        from  isceobj.Image import createRawImage, createSlcImage
        self.activateInputPorts()

        # Parse the image metadata and extract the image
        self.logger.info('Extracting image')
        try:
            self.sensor.extractImage()
        except NotImplementedError as strerr:
            self.logger.error("%s" % (strerr))
            self.logger.error(
                "make_raw not implemented for %s"  %  self.sensor.__class__
                )
            raise NotImplementedError
        self.frame = self.sensor.frame

        #jng NOTE if we pass just the sensor also in the case of raw image we
        ## can avoid the if
        if isinstance(self.frame.image, createRawImage().__class__):
            # Calculate the doppler fit
            self.logger.info("Calculating Doppler Centroid")

            try:
                self.doppler.wireInputPort(name='frame',
                                       object=self.frame)
            except:
                computeFlag = False
            else:
                computeFlag = True

            if computeFlag:
                self.doppler.wireInputPort(name='instrument',
                                       object=self.frame.instrument)
                self.doppler.wireInputPort(name='image',
                                       object=self.frame.image)
                self.doppler.calculateDoppler()
                inHz = False

            else:
                self.doppler.wireInputPort(name='sensor', object=self.sensor)
                self.doppler.calculateDoppler()
                inHz = False

            #new jng compute slc image size here
            rangeSamplingRate = self.instrument.rangeSamplingRate
            rangePulseDuration = self.instrument.pulseLength
            goodBytes = self.frame.image.xmax - self.frame.image.xmin
            try:
                #check if the instrument implements it, if not set it to zero
                chirpExtension = self.instrument.chirpExtension # Should probably be a percentage rather than a set number
            except AttributeError:
                chirpExtension = 0

            chirpSize = int(rangeSamplingRate * rangePulseDuration)
            self.frame.numberRangeBins = (int(goodBytes/2) -
                                          chirpSize + chirpExtension)


        elif isinstance(self.frame.image, createSlcImage().__class__):
            # jng changed in view of the new tsx preproc from Howard
            self.doppler.wireInputPort(name='sensor', object=self.sensor)
            self.doppler.calculateDoppler()
            inHz = False

            #new jng compute slc image size here
            self.frame.numberRangeBins = self.frame.image.width
        else:
            message = (
                "Unrecognized image type %s"  %
                str(self.frame.image.__class__)
                )
            self.logger.error(message)
            raise TypeError(message)

        # Fit a polynomial to the doppler values. in the tsx case or every
        # zero doppler case this function simple sets the a = fd b = 0, c = 0
        self.doppler.fitDoppler()

        # Create a doppler object
        prf = self.frame.instrument.PRF
        fit = self.doppler.quadratic
        coef = [fit['a'], fit['b'], fit['c'], 0.0]
        self.logger.debug("Doppler Coefficients %s" % (coef))
        self.dopplerValues = Doppler(prf=prf)
        self.dopplerValues.setDopplerCoefficients(coef, inHz=inHz)

        # Calculate the height, height_dt, and velocity
        self.logger.info("Calculating Spacecraft Velocity")
        self.calculateHeightDt()
        self.calculateVelocity()

        # Calculate squint angle
        self.logger.info("Calculating Squint Angle")
        self.calculateSquint()
        self.frame.image.coord1Start = self.frame.image.xmin
        self.frame.image.renderHdr()
        #just in case the Sensor does not compute the pulse timing
        try:
            self.adjustSensingStart()
        except:
            pass
        return None

    def adjustSensingStart(self, pulseTimingFilename=None, ext='.aux'):
        pulseTimingFilename  = (
            pulseTimingFilename or
            self.frame.image.filename + ext
            )
        import datetime as dt
        import math
        import struct

        with open(pulseTimingFilename) as fp:
            allF = fp.read()
            pass

        #use only a limited number of point from the first frame
        lines = min(len(allF)/16, 10000)
        allT = [0]*lines
        d0 = struct.unpack('<d', allF[0:8])[0]
        day0 =  dt.timedelta(d0).days
        sec = 0
        for i in range(lines):
            day, musec = struct.unpack('<dd', allF[i*16:(i+1)*16])
            # note the musec are relative to the day, not to the second i.e.
            # they are the total musec in the day
            td =  dt.timedelta(day, sec, musec)
            allT[i] = (
                (td.microseconds +
                 (td.seconds +
                  (td.days - day0) * 24 * 3600.0) * 10**6) / 10**6
                )
            pass
        prf = self.frame.instrument.PRF
        sumPart = [allT[i] - i/prf for i in xrange(len(allT))]
        sum = math.fsum(sumPart)
        sum /= len(allT)
        day = day0
        sec = math.floor(sum)
        musec = (sum - sec)*10**6
        sensingOld = self.frame.sensingStart
        #day-1 since we start from jan 1 and not jan 0
        newSensingStart = (
            dt.datetime(sensingOld.year, 1, 1) +
            dt.timedelta(day-1, sec, musec)
            )
        self.frame.setSensingStart(newSensingStart)
        self.logger.info("Changing sensing start from %s to %s" %
                         (str(sensingOld), str(newSensingStart)))

    def __str__(self):
        retstr = "Velocity: (%s)\n"
        retlst = (self.velocity, )
        retstr += "HeightDt: (%s)\n"
        retlst += (self.heightDt, )
        retstr += "Squint: (%s)\n"
        retlst += (self.squint, )
        retstr += "Height: (%s)\n"
        retlst += (self.spacecraftHeight, )
        return retstr % retlst

    pass

## JEB: added a main for script operation
def main():
    return makeRawApp().run()

if __name__ == "__main__":
    import sys
    if (len(sys.argv) < 2):
        print("Usage:%s <xml-parameter file>" % sys.argv[0])
        sys.exit(1)
    main()
