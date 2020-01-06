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
from iscesys.Component import Component,Port
from iscesys.Compatibility import Compatibility
from Sensor.readOrbitPulseERS import readOrbitPulseERS
from iscesys.Component.Component import Component, Port

class ReadOrbitPulseERS(Component):

    def readOrbitPulseERS(self):
        for port in self._inputPorts:
            method = port.getMethod()
            method()                                
        self.setState()
        readOrbitPulseERS.readOrbitPulseERS_Py()
        self.getState()
        return None

    def setState(self):
        readOrbitPulseERS.setWidth_Py(int(self.width))
        readOrbitPulseERS.setICUoffset_Py(int(self.ICU_OFFSET))
        readOrbitPulseERS.setNumberLines_Py(int(self.NUMBER_LINES))
        readOrbitPulseERS.setSatelliteUTC_Py(float(self.satelliteUTC))
        readOrbitPulseERS.setPRF_Py(float(self.PRF))
        readOrbitPulseERS.setDeltaClock_Py(float(self.DELTA_CLOCK))
        readOrbitPulseERS.setEncodedBinaryTimeCode_Py(float(self.DELTA_CLOCK))
        return None

    def setWidth(self,var):
        self.width = int(var)
        return

    def setICUoffset(self,var):
        self.icuOffset = int(var)
        return

    def setNumberLines(self,var):
        self.numberLines = int(var)
        return

    def setSatelliteUTC(self,var):
        self.satelliteUTC = float(var)
        return

    def setPRF(self,var):
        self.prf = float(var)
        return

    def setDeltaClock(self,var):
        self.deltaClock = float(var)
        return
    
    def setEncodedBinaryTimeCode(self,var):
        self.encodedBinaryTimeCode = int(var)
        return

    def setRawImage(self,var):
        self.rawImage = var
        return



    def getState(self):
        self.startingTime = readOrbitPulseERS.getStartingTime_Py()

        return


    def getStartingTime(self):
        return self.startingTime

    def addRawImage(self):
        image = self._inputPorts.getPort('rawImage').getObject()
        if (image):
            if (isinstance(image,Image)):
                self.rawImage = image
                self.width = self.rawImage.getWidth()
            else:
                self.logger.error("Object %s must be an instance of Image" % (image))
                raise TypeError
    
    def addInstrument(self):
        instrument = self._inputPorts.getPort('instrument').getObject()
        if(instrument):
            try:
                self.prf = instrument.getPulseRepetitionFrequency()
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError("Unable to wire instrument port")


    def addMetadata(self):
        metadata = self._inputPorts.getPort('metadata').getObject()
        if(metadata):
            try:
            	self.satelliteUTC = datetime.datetime.strptime(metadata['Satellite clock time'],"%Y%m%d%H%M%S%f")
                self.encodedBinaryTimeCode = metadata['Satellite encoded binary time code']
                self.deltaClock = metadata['Satellite clock step length']*10**-9
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError("Unable to wire instrument port")


    logging_name = 'isceobj.Sensor.ReadOrbitPulseERS'
    
    def __init__(self):
        super(ReadOrbitPulseERS, self).__init__()
        self.encodedBinaryTimeCode = None
        self.rawImage = None
        self.width = None
        self.icuOffset = None
        self.numberLines = None
        self.satelliteUTC = None
        self.prf = None
        self.deltaClock = None
        self.startingTime = None
        self.dictionaryOfVariables = { 
            'ENCODED_BINARY_TIME_CODE' : ['encodedBinaryTimeCode',
                                          'int',
                                          'optional'], 
            'WIDTH' : ['width', 'int','optional'], 
            'ICU_OFFSET' : ['icuOffset', 'int','optional'], 
            'NUMBER_LINES' : ['numberLines', 'int','optional'], 
            'SATELLITE_UTC' : ['satelliteUTC', 'float','mandatory'], 
            'PRF' : ['prf', 'float','mandatory'], 
            'DELTA_CLOCK' : ['deltaClock', 'float','mandatory'] 
            }

        self.dictionaryOfOutputVariables = { 
            'STARTING_TIME' : 'startingTime' 
            }
        self.descriptionOfVariables = {}
        self.mandatoryVariables = []
        self.optionalVariables = []
        self.initOptionalAndMandatoryLists()
        return None


    def createPorts(self):
        rawImagePort = Port(name='rawImage',method=self.addRawImage)
        instrumentPort = Port(name='instrument',method=self.addInstrument)
        metaPort = Port(name='metadata',method=self.addMetadata)
        self._inputPorts.add(rawImagePort)
        self._inputPorts.add(instrumentPort)
        self._inputPorts.add(metaPort)
        return None
