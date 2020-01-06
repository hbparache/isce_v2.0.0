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
# Author: Giangi Sacco
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





from __future__ import print_function
import sys
import os
import math
from isceobj.Scene.Frame import Frame
from isceobj.RawImage.RawImage import RawImage
from isceobj.StreamImage.StreamImage import StreamImage
from isceobj.Initializer.Component import Component
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
from orbit import pulsetiming

class Pulsetiming(Component):

    def pulsetiming(self,rawImage = None,ledImage = None):
        rawCreatedHere = False
        ledCreatedHere = False
        if(rawImage == None):
            rawImage = self.createRawImage()
            rawCreatedHere = True
        if(ledImage == None):
            ledImage = self.createLeaderImage()
            ledCreatedHere = True
        numLines = rawImage.getFileLength()
        self.numberLines = numLines
        numCoord = 3
        self.dim1_position = numLines
        self.dim2_position = numCoord
        self.dim1_velocity = numLines
        self.dim2_velocity = numCoord
        self.dim1_time = numLines
        self.allocateArrays()
        self.setState()
        rawImagePt = rawImage.getImagePointer()
        ledImagePt = ledImage.getImagePointer()
        pulsetiming.pulsetiming_Py(ledImagePt,rawImagePt)
        self.getState()
        self.deallocateArrays()
        if(rawCreatedHere):
            rawImage.finalizeImage()
        if(ledCreatedHere):
            ledImage.finalizeImage()
        return


    def createLeaderImage(self):
        if(self.leaderFilename == ''):
            print('Error. The leader file name must be set.')
            raise Exception
        accessmode = 'read'
        width = 1
        objLed = StreamImage()
        datatype = 'BYTE'
        endian = 'l' #does not matter since single byte data
        objLed.initImage(self.leaderFilename,accessmode,datatype,endian)
        # it actually creates the C++ object
        objLed.createImage()
        return objLed

    def createRawImage(self):
        if(self.rawFilename == ''):
            print('Error. The raw image file name must be set.')
            raise Exception
        if(self.numberBytesPerLine == None):
            print('Error. The number of bytes per line must be set.')
            raise Exception
        accessmode = 'read'
        width = self.numberBytesPerLine
        objRaw = RawImage()
        endian = 'l' #does not matter synce single byte data
        objRaw.initImage(self.rawFilename,accessmode,endian,width)
        # it actually creates the C++ object
        objRaw.createImage()
        return objRaw


    def setState(self):
        pulsetiming.setNumberBitesPerLine_Py(int(self.numberBytesPerLine))
        pulsetiming.setNumberLines_Py(int(self.numberLines))

        return





    def setNumberBytesPerLine(self,var):
        self.numberBytesPerLine = int(var)
        return

    def setNumberLines(self,var):
        self.numberLines = int(var)
        return

    def setLeaderFilename(self,var):
        self.leaderFilename = var
        return

    def setRawFilename(self,var):
        self.rawFilename = var
        return

    def setRawImage(self,var):
        self.rawImage = var
        return

    def setLeaderImage(self,var):
        self.leaderImage = var
        return


    def getState(self):
        self.position = pulsetiming.getPositionVector_Py(self.dim1_position, self.dim2_position)
        self.velocity = pulsetiming.getVelocity_Py(self.dim1_velocity, self.dim2_velocity)
        self.time = pulsetiming.getOrbitTime_Py(self.dim1_time)

        return





    def getPosition(self):
        return self.position

    def getVelocity(self):
        return self.velocity

    def getOrbitTime(self):
        return self.time






    def allocateArrays(self):
        if (self.dim1_position == None):
            self.dim1_position = len(self.position)
            self.dim2_position = len(self.position[0])

        if (not self.dim1_position) or (not self.dim2_position):
            print("Error. Trying to allocate zero size array")

            raise Exception

        pulsetiming.allocate_position_Py(self.dim1_position, self.dim2_position)

        if (self.dim1_velocity == None):
            self.dim1_velocity = len(self.velocity)
            self.dim2_velocity = len(self.velocity[0])

        if (not self.dim1_velocity) or (not self.dim2_velocity):
            print("Error. Trying to allocate zero size array")

            raise Exception

        pulsetiming.allocate_velocity_Py(self.dim1_velocity, self.dim2_velocity)

        if (self.dim1_time == None):
            self.dim1_time = len(self.time)

        if (not self.dim1_time):
            print("Error. Trying to allocate zero size array")

            raise Exception

        pulsetiming.allocate_timeArray_Py(self.dim1_time)


        return





    def deallocateArrays(self):
        pulsetiming.deallocate_position_Py()
        pulsetiming.deallocate_velocity_Py()
        pulsetiming.deallocate_timeArray_Py()

        return

    def initFromObjects(self,frame=None):
        """Initialize a Pulsetiming object from a Frame object"""
        try:
            self.numberLines = frame.getNumberOfLines()
            self.numberBytesPerLine = frame.getNumberOfSamples()
        except AttributeError as (errno,strerr):
            print(strerr)

    def __init__(self):
        Component.__init__(self)
        self.rawImage = ''
        self.rawFilename = ''
        self.leaderFilename = ''
        self.numberBytesPerLine = None
        self.numberLines = None
        self.position = []
        self.dim1_position = None
        self.dim2_position = None
        self.velocity = []
        self.dim1_velocity = None
        self.dim2_velocity = None
        self.time = []
        self.dim1_time = None
        self.dictionaryOfVariables = {'NUMBER_BYTES_PER_LINE' : ['self.numberBytesPerLine', 'int','mandatory'], \
                                      'RAW_FILENAME' : ['self.rawFilename', 'str','optional'], \
                                      'LEADER_FILENAME' : ['self.leaderFilename', 'str','optional'], \
                                      'NUMBER_LINES' : ['self.numberLines', 'int','optional']}
        
        self.dictionaryOfOutputVariables = {'TIME' : 'self.time', \
                                            'POSITION': 'self.position', \
                                            'VELOCITY': 'self.velocity'}
        self.descriptionOfVariables = {}
        self.mandatoryVariables = []
        self.optionalVariables = []
        typePos = 2
        for key , val in self.dictionaryOfVariables.items():
            if val[typePos] == 'mandatory':
                self.mandatoryVariables.append(key)
            elif val[typePos] == 'optional':
                self.optionalVariables.append(key)
            else:
                print('Error. Variable can only be optional or mandatory')
                raise Exception
        return





#end class




if __name__ == "__main__":
    sys.exit(main())
