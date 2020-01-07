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
from iscesys.Component.Component import Component
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
#from mroipac.looks import powlooks

class Powlooks(Component):

    def looks(self):
        self.setState()
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #!!!!!!!!!!!!!!!!!!! ADD NECESSARY CODE !!!!!!!!!!!!!!!
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        looks.looks_Py()
        self.getState()

        return





    def setState(self):
        looks.setRangeLook_Py(int(self.rangeLook))
        looks.setAzimuthLook_Py(int(self.azimuthLook))
        looks.setWidth_Py(int(self.width))
        looks.setLength_Py(int(self.length))
        looks.setLookType_Py(self.lookType)
        looks.setInputImage_Py(self.inputImage)
        looks.setOutputImage_Py(self.outputImage)

        return





    def setRangeLook(self,var):
        self.rangeLook = int(var)
        return

    def setAzimuthLook(self,var):
        self.azimuthLook = int(var)
        return

    def setWidth(self,var):
        self.width = int(var)
        return

    def setLength(self,var):
        self.length = int(var)
        return

    def setLookType(self,var):
        self.lookType = str(var)
        return

    def setInputImage(self,var):
        self.inputImage = str(var)
        return

    def setOutputImage(self,var):
        self.outputImage = str(var)
        return






    def __init__(self):
        Component.__init__(self)
        self.lookInstance = None
        self.rangeLook = None
        self.azimuthLook = None
        self.width = None
        self.length = None
        self.lookType = ''
        self.inputImage = ''
        self.outputImage = ''
        self.dictionaryOfVariables = {'RANGE_LOOK' : ['self.rangeLook', 'int','mandatory'], \
                                      'AZIMUTH_LOOK' : ['self.azimuthLook', 'int','mandatory'], \
                                      'WIDTH' : ['self.width', 'int','mandatory'], \
                                      'LENGTH' : ['self.length', 'int','optional'], \
                                      'LOOK_TYPE' : ['self.lookType', 'str','mandatory'], \
                                      'INPUT_IMAGE' : ['self.inputImage', 'str','mandatory'], \
                                      'OUTPUT_IMAGE' : ['self.outputImage', 'str','mandatory']}
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
