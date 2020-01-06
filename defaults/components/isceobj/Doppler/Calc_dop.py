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
import logging
import os
import math
from iscesys.Component.Component import Component, Port
from iscesys.Compatibility import Compatibility
from isceobj.Doppler import calc_dop
import isceobj
from isceobj.Util.decorators import pickled, logged, port

@pickled
class Calc_dop(Component):

    logging_name = 'isceobj.Doppler.Calc_dop'
    
    dictionaryOfVariables = {
        'RAW_FILENAME' : ['rawFilename', 'str','optional'],
        'HEADER' : ['header', 'int','mandatory'],
        'WIDTH' : ['width', 'int','mandatory'],
        'LAST_LINE' : ['lastLine', 'int','mandatory'],
        'FIRST_LINE' : ['firstLine', 'int','mandatory'],
        'IOFFSET' : ['Ioffset', 'float','mandatory'],
        'QOFFSET' : ['Qoffset', 'float','mandatory']
        }

    dictionaryOfOutputVariables = {
        'RNG_DOPPLER' : 'rngDoppler',
        'FD' : 'fd'
        }
    
    @logged
    def __init__(self):
        super(Calc_dop, self).__init__()
        self.rawFilename = ''
        self.header = None 
        self.width = None
        self.lastLine = None
        self.firstLine = None 
        self.Ioffset = None
        self.Qoffset = None
        self.rngDoppler = []
        self.dim1_rngDoppler = None
        self.fd = None
        self.quadratic = {}
        self.descriptionOfVariables = {}
        self.mandatoryVariables = []
        self.optionalVariables = []
        self.initOptionalAndMandatoryLists()
        self.createPorts()
        return None

    def createPorts(self):
        instrumentPort = Port(name="instrument",
                              method=self.addInstrument,
                              doc=(
                "An object that has getPulseRepetitionFrequency() and "+
                "getInPhaseValue() methods"
                ))
        framePort = Port(name="frame",
                         method=self.addFrame,
                         doc=(
                "An object that has getNumberOfSamples() and " +
                " etNumberOfLines() methods")
                         )
        imagePort = Port(name="image",
                         method=self.addImage,
                         doc=(
                "An object that has getXmin() and getXmax() methods"
                )
                         )
        self.inputPorts.add(instrumentPort)
        self.inputPorts.add(framePort)
        self.inputPorts.add(imagePort)
        return None

    def calculateDoppler(self, rawImage=None):
        self.activateInputPorts()

        rawCreatedHere = False
        if rawImage is None:
            self.rawImage = self.createRawImage()
            rawCreateHere = True
        else:
            self.rawImage = rawImage
            pass
        rawAccessor = self.rawImage.getImagePointer()
        self.setDefaults()
        self.rngDoppler = [0]*int((self.width - self.header)/2)
        self.allocateArrays()
        self.setState()
        calc_dop.calc_dop_Py(rawAccessor)
        self.getState()
        self.deallocateArrays()
        if rawCreatedHere:
            self.rawImage.finalizeImage()
            pass
        return None

    def createRawImage(self):
        # Check file name
        width = self.width        
        objRaw = isceobj.createRawImage()
        objRaw.initImage(self.rawFilename, 'read', width)
        objRaw.createImage()                
        return objRaw

    def fitDoppler(self):
#no fit is done. just keeping common interface with DopIQ
        self.quadratic['a'] = self.fd # for now use only zero order term 
        self.quadratic['b'] = 0  
        self.quadratic['c'] = 0
    
    def setDefaults(self):
        if self.firstLine is None:
            self.firstLine = 100
            self.logger.info('Variable  FIRST_LINE has been set  equal the defualt value %i' % (self.firstLine))
        if self.lastLine is None:
            self.lastLine = self.rawImage.getLength() - 200
            self.logger.info('Variable  LAST_LINE has been set  equal the default value imageLength - 200 = %i' % (self.lastLine))
        if self.header is None:
            self.header = 0
            self.logger.info('Variable  HEADER has been set  equal the default value %i' % (self.header))


    @port('__complex__')
    def addInstrument(self):
        z = complex(self.instrument)
        self.Ioffset, self.Qoffset = (z.real, z.imag)
        

    @port('numberOfLines')
    def addFrame(self):
        self.numberOfLines = self.frame.numberOfLines
        pass

    @port(None)
    def addImage(self):
        self.rawFilename = self.image.getFilename()
        self.header = self.image.getXmin()
        self.width = self.image.getXmax() - self.header
        return None


    def setState(self):
        calc_dop.setHeader_Py(int(self.header))
        calc_dop.setWidth_Py(int(self.width))
        calc_dop.setLastLine_Py(int(self.lastLine))
        calc_dop.setFirstLine_Py(int(self.firstLine))
        calc_dop.setIoffset_Py(float(self.Ioffset))
        calc_dop.setQoffset_Py(float(self.Qoffset))
        return None

    def setFilename(self, var):
        self.rawFilename = var

    def setHeader(self, var):
        self.header = int(var)
        return

    def setWidth(self, var):
        self.width = int(var)
        return

    def setLastLine(self, var):
        self.lastLine = int(var)
        return

    def setFirstLine(self, var):
        self.firstLine = int(var)
        return

    def setIoffset(self, var):
        self.Ioffset = float(var)
        return

    def setQoffset(self, var):
        self.Qoffset = float(var)
        return

    def getState(self):
        self.rngDoppler = calc_dop.getRngDoppler_Py(self.dim1_rngDoppler)
        self.fd = calc_dop.getDoppler_Py()
        return

    def getRngDoppler(self):
        return self.rngDoppler

    def getDoppler(self):
        return self.fd

    def allocateArrays(self):
        if self.dim1_rngDoppler is None:
            self.dim1_rngDoppler = len(self.rngDoppler)
            pass
        if not self.dim1_rngDoppler:
            print("Error. Trying to allocate zero size array")
            raise Exception

        calc_dop.allocate_rngDoppler_Py(self.dim1_rngDoppler)
        return 

    def deallocateArrays(self):
        calc_dop.deallocate_rngDoppler_Py()
        return 

    pass

        
                
        
                
        
                
        
                
