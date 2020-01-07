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

class DefaultDopp(Component):
   
    def calculateDoppler(self):
        print('Using default doppler values for sensor: %s'%(self._sensor.__class__.__name__))
        self.activateInputPorts()
        pass

    def fitDoppler(self):
        pass

    def addSensor(self):
        sensor = self._inputPorts.getPort('sensor').getObject()
        self._sensor =  sensor
        if (sensor):
            self.quadratic = sensor.extractDoppler()
            self.prf = sensor.frame.getInstrument().getPulseRepetitionFrequency()

    logging_name = 'DefaultDopp'

    def __init__(self):
        super(DefaultDopp, self).__init__()
        self._sensor = None
        self.quadratic = {}
        self.prf = None
        return None

    def createPorts(self):
        sensorPort = Port(name='sensor',method=self.addSensor)
        self._inputPorts.add(sensorPort)
        return None


if __name__ == '__main__':
    pass
