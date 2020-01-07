#!usr/bin/env python

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2013 to the present, California Institute of Technology.
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
# Author: Piyush Agram
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



from __future__ import print_function
import sys
import numpy as np
from iscesys.Component.Component import Component, Port

class CskSlcDopp(Component):
   
    def calculateDoppler(self):
        self.activateInputPorts()

        #compute also the avd doppler which is the one used later on
        midtime = (self.lastRangeTime + self.firstRangeTime)*0.5 - self.refTime
        fd_mid = self.doppvsRangeTime[0] + self.doppvsRangeTime[1]*midtime + self.doppvsRangeTime[2]*midtime*midtime

        self.quadratic['a'] = fd_mid/self.prf 
        self.quadratic['b'] = 0.
        self.quadratic['c'] = 0.

    def fitDoppler(self):
        pass

    def addSensor(self):
        sensor = self._inputPorts.getPort('sensor').getObject()
        self._sensor =  sensor
        if (sensor):
            try:
                self.doppvsRangeTime = sensor.dopplerRangeTime
            except:
                self.doppvsRangeTime = sensor.dopplerCoeffs

            self.firstRangeTime = sensor.rangeFirstTime
            self.lastRangeTime = sensor.rangeLastTime
            self.refTime = sensor.rangeRefTime
            self.prf = sensor.frame.getInstrument().getPulseRepetitionFrequency()

    logging_name = 'CskSlcDopp'

    def __init__(self):
        super(CskSlcDopp, self).__init__()
        self._sensor = None
        self.quadratic = {}
        self.doppvsRangeTime = None
        self.firstRangeTime = None
        self.lastRangeTime = None
        self.refTime = None
        self.prf = None
        return None

    def createPorts(self):
        sensorPort = Port(name='sensor',method=self.addSensor)
        self._inputPorts.add(sensorPort)
        return None


if __name__ == '__main__':
    pass
