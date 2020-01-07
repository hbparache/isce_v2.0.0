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
# Author: Brett George
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import datetime
import logging

from isceobj.Orbit.Orbit import Orbit

logger = logging.getLogger('isce.insar.runPulseTiming')

def runPulseTiming(self):
    master = self.insar.masterFrame
    slave = self.insar.slaveFrame
    # add orbits to main object -law of demeter pls.
    self.insar.masterOrbit = pulseTiming(master, self.insar.procDoc, 'master')
    self.insar.slaveOrbit = pulseTiming(slave, self.insar.procDoc, 'slave')
    return None

def pulseTiming(frame, catalog, which):
    logger.info("Pulse Timing")
    numberOfLines = frame.getNumberOfLines()
    prf = frame.getInstrument().getPulseRepetitionFrequency()
    pri = 1.0 / prf
    startTime = frame.getSensingStart()
    orbit = frame.getOrbit()
    pulseOrbit = Orbit()
    startTimeUTC0 = (startTime -
                     datetime.datetime(startTime.year,
                                       startTime.month,startTime.day)
                     )
    timeVec = [pri*i +
               startTimeUTC0.seconds +
               10**-6*startTimeUTC0.microseconds for i in range(numberOfLines)
               ]
    catalog.addItem("timeVector", timeVec, "runPulseTiming.%s" % which)
    for i in range(numberOfLines):
        dt = i * pri
        time = startTime + datetime.timedelta(seconds=dt)
        sv = orbit.interpolateOrbit(time, method='hermite')
        pulseOrbit.addStateVector(sv)
        
    return pulseOrbit
