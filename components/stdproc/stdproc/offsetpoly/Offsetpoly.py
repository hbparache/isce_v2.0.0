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
# Author: Piyush Agram
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



from __future__ import print_function
from iscesys.Component.Component import Component,Port
from iscesys.Compatibility import Compatibility
from stdproc.stdproc.offsetpoly import offsetpoly

class Offsetpoly(Component):
    
    def offsetpoly(self):
        self.numberOffsets = len(self.offset)
        self.allocateArrays()
        self.setState()
        offsetpoly.offsetpoly_Py()
        self.getState()
        self.deallocateArrays()

        return

    def setState(self):
        offsetpoly.setLocationAcross_Py(self.locationAcross,
                                     self.numberOffsets)
        offsetpoly.setOffset_Py(self.offset,
                                           self.numberOffsets)
        offsetpoly.setLocationDown_Py(self.locationDown, self.numberOffsets)
        offsetpoly.setSNR_Py(self.snr, self.numberOffsets)
        return

    def setNumberFitCoefficients(self, var):
        self.numberFitCoefficients = int(var)
        return


    def setLocationAcross(self, var):
        self.locationAcross = var
        return

    def setOffset(self, var):
        self.offset = var
        return

    def setLocationDown(self, var):
        self.locationDown = var
        return

    def setSNR(self, var):
        self.snr = var
        return

    def getState(self):
        self.offsetPoly = offsetpoly.getOffsetPoly_Py(
            self.numberFitCoefficients
            )
        return

    def allocateArrays(self):
        offsetpoly.allocateFieldArrays_Py(self.numberOffsets)
        offsetpoly.allocatePolyArray_Py(self.numberFitCoefficients)
        return

    def deallocateArrays(self):
        offsetpoly.deallocateFieldArrays_Py()
        offsetpoly.deallocatePolyArray_Py()
        return

    logging_name = 'isce.stdproc.offsetpoly'
    def __init__(self):
        super(Offsetpoly, self).__init__()
        self.numberFitCoefficients = 6
        self.numberOffsets = None 
        self.locationAcross = []
        self.offset=[]
        self.locationDown = []
        self.snr = []
        self.offsetPoly = []
        self.downOffsetPoly = []
        self.dictionaryOfVariables = { 
            'NUMBER_FIT_COEFFICIENTS' : ['self.numberFitCoefficients', 'int','optional'],
            'NUMBER_OFFSETS' : ['self.numberOffsets', 'int', 'mandatory'],
            }
        self.dictionaryOfOutputVariables = { 
            'OFFSET_POLYNOMIAL' : 'self.offsetPoly',
            }
        self.descriptionOfVariables = {}
        self.mandatoryVariables = []
        self.optionalVariables = []
        return
