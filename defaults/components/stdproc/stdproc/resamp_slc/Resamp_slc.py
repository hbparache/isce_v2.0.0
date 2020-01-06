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
import logging
from iscesys.Component.Component import Component,Port
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
from stdproc.stdproc.resamp_slc import resamp_slc

class Resamp_slc(Component):

    def resamp_slc(self,imageIn,imageOut):
        for port in self._inputPorts:
            method = port.getMethod()
            method()                                
        if not (imageIn == None):
            self.imageIn = imageIn
        
        if (self.imageIn == None):
            self.logger.error("Input slc image not set.")
            raise Exception
        if not (imageOut == None):
            self.imageOut = imageOut
        if (self.imageOut == None):
            self.logger.error("Output slc image not set.")
            raise Exception
        
        self.setDefaults()
        #preallocate the two arrays that are returned
        self.azimuthCarrier = [0]*self.numberRangeBin
        self.rangeCarrier = [0]*self.numberRangeBin

        self.imageInAccessor = self.imageIn.getImagePointer()
        self.imageOutAccessor = self.imageOut.getImagePointer()
        self.computeSecondLocation()    
        self.allocateArrays()
        self.setState()
        resamp_slc.resamp_slc_Py(self.imageInAccessor,self.imageOutAccessor)
        self.getState()
        self.deallocateArrays()

        return

    def setDefaults(self):
        if (self.numberLines == None):
            self.numberLines = self.imageIn.getLength()
            self.logger.warning('The variable NUMBER_LINES has been set to the default value %d which is the number of lines in the slc image.' % (self.numberLines)) 
       
        if (self.numberRangeBin == None):
            self.numberRangeBin = self.imageIn.getWidth()
            self.logger.warning('The variable NUMBER_RANGE_BIN has been set to the default value %d which is the width of the slc image.' % (self.numberRangeBin))

        if (self.numberFitCoefficients == None):
            self.numberFitCoefficients = 6
            self.logger.warning('The variable NUMBER_FIT_COEFFICIENTS has been set to the default value %s' % (self.numberFitCoefficients)) 
        
        if (self.firstLineOffset == None):
            self.firstLineOffset = 1
            self.logger.warning('The variable FIRST_LINE_OFFSET has been set to the default value %s' % (self.firstLineOffset)) 
        

    def computeSecondLocation(self):
#this part was previously done in the fortran code
        self.locationAcross2 = [0]*len(self.locationAcross1)
        self.locationAcrossOffset2 = [0]*len(self.locationAcross1)
        self.locationDown2 = [0]*len(self.locationAcross1)
        self.locationDownOffset2 = [0]*len(self.locationAcross1)
        self.snr2 = [0]*len(self.locationAcross1)
        for i in range(len(self.locationAcross1)):
            self.locationAcross2[i] = self.locationAcross1[i] + self.locationAcrossOffset1[i]
            self.locationAcrossOffset2[i] = self.locationAcrossOffset1[i]
            self.locationDown2[i] = self.locationDown1[i] + self.locationDownOffset1[i]
            self.locationDownOffset2[i] = self.locationDownOffset1[i]
            self.snr2[i] = self.snr1[i]

    def setState(self):
        resamp_slc.setStdWriter_Py(int(self._stdWriter.getWriter()))
        resamp_slc.setNumberFitCoefficients_Py(int(self.numberFitCoefficients))
        resamp_slc.setNumberRangeBin_Py(int(self.numberRangeBin))
        resamp_slc.setNumberLines_Py(int(self.numberLines))
        resamp_slc.setFirstLineOffset_Py(int(self.firstLineOffset))
        resamp_slc.setRadarWavelength_Py(float(self.radarWavelength))
        resamp_slc.setSlantRangePixelSpacing_Py(float(self.slantRangePixelSpacing))
        resamp_slc.setDopplerCentroidCoefficients_Py(self.dopplerCentroidCoefficients, self.dim1_dopplerCentroidCoefficients)
        resamp_slc.setLocationAcross1_Py(self.locationAcross1, self.dim1_locationAcross1)
        resamp_slc.setLocationAcrossOffset1_Py(self.locationAcrossOffset1, self.dim1_locationAcrossOffset1)
        resamp_slc.setLocationDown1_Py(self.locationDown1, self.dim1_locationDown1)
        resamp_slc.setLocationDownOffset1_Py(self.locationDownOffset1, self.dim1_locationDownOffset1)
        resamp_slc.setSNR1_Py(self.snr1, self.dim1_snr1)
        resamp_slc.setLocationAcross2_Py(self.locationAcross2, self.dim1_locationAcross2)
        resamp_slc.setLocationAcrossOffset2_Py(self.locationAcrossOffset2, self.dim1_locationAcrossOffset2)
        resamp_slc.setLocationDown2_Py(self.locationDown2, self.dim1_locationDown2)
        resamp_slc.setLocationDownOffset2_Py(self.locationDownOffset2, self.dim1_locationDownOffset2)
        resamp_slc.setSNR2_Py(self.snr2, self.dim1_snr2)

        return




    def setStdWriter(self,writer):
        self._stdWriter = writer

    def setNumberFitCoefficients(self,var):
        self.numberFitCoefficients = int(var)
        return

    def setNumberRangeBin(self,var):
        self.numberRangeBin = int(var)
        return

    def setNumberLines(self,var):
        self.numberLines = int(var)
        return

    def setFirstLineOffset(self,var):
        self.firstLineOffset = int(var)
        return

    def setRadarWavelength(self,var):
        self.radarWavelength = float(var)
        return

    def setSlantRangePixelSpacing(self,var):
        self.slantRangePixelSpacing = float(var)
        return

    def setDopplerCentroidCoefficients(self,var):
        self.dopplerCentroidCoefficients = var
        return

    def setLocationAcross1(self,var):
        self.locationAcross1 = var
        return

    def setLocationAcrossOffset1(self,var):
        self.locationAcrossOffset1 = var
        return

    def setLocationDown1(self,var):
        self.locationDown1 = var
        return

    def setLocationDownOffset1(self,var):
        self.locationDownOffset1 = var
        return

    def setSNR1(self,var):
        self.snr1 = var
        return

    def setLocationAcross2(self,var):
        self.locationAcross2 = var
        return

    def setLocationAcrossOffset2(self,var):
        self.locationAcrossOffset2 = var
        return

    def setLocationDown2(self,var):
        self.locationDown2 = var
        return

    def setLocationDownOffset2(self,var):
        self.locationDownOffset2 = var
        return

    def setSNR2(self,var):
        self.snr2 = var
        return






    def getState(self):
        self.azimuthCarrier = resamp_slc.getAzimuthCarrier_Py(self.dim1_azimuthCarrier)
        self.rangeCarrier = resamp_slc.getRangeCarrier_Py(self.dim1_rangeCarrier)

        return





    def getAzimuthCarrier(self):
        return self.azimuthCarrier

    def getRangeCarrier(self):
        return self.rangeCarrier






    def allocateArrays(self):
        if (self.dim1_dopplerCentroidCoefficients == None):
            self.dim1_dopplerCentroidCoefficients = len(self.dopplerCentroidCoefficients)

        if (not self.dim1_dopplerCentroidCoefficients):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_dopplerCoefficients_Py(self.dim1_dopplerCentroidCoefficients)

        if (self.dim1_locationAcross1 == None):
            self.dim1_locationAcross1 = len(self.locationAcross1)

        if (not self.dim1_locationAcross1):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_r_ranpos_Py(self.dim1_locationAcross1)

        if (self.dim1_locationAcrossOffset1 == None):
            self.dim1_locationAcrossOffset1 = len(self.locationAcrossOffset1)

        if (not self.dim1_locationAcrossOffset1):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_r_ranoff_Py(self.dim1_locationAcrossOffset1)

        if (self.dim1_locationDown1 == None):
            self.dim1_locationDown1 = len(self.locationDown1)

        if (not self.dim1_locationDown1):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_r_azpos_Py(self.dim1_locationDown1)

        if (self.dim1_locationDownOffset1 == None):
            self.dim1_locationDownOffset1 = len(self.locationDownOffset1)

        if (not self.dim1_locationDownOffset1):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_r_azoff_Py(self.dim1_locationDownOffset1)

        if (self.dim1_snr1 == None):
            self.dim1_snr1 = len(self.snr1)

        if (not self.dim1_snr1):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_r_sig_Py(self.dim1_snr1)

        if (self.dim1_locationAcross2 == None):
            self.dim1_locationAcross2 = len(self.locationAcross2)

        if (not self.dim1_locationAcross2):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_r_ranpos2_Py(self.dim1_locationAcross2)

        if (self.dim1_locationAcrossOffset2 == None):
            self.dim1_locationAcrossOffset2 = len(self.locationAcrossOffset2)

        if (not self.dim1_locationAcrossOffset2):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_r_ranoff2_Py(self.dim1_locationAcrossOffset2)

        if (self.dim1_locationDown2 == None):
            self.dim1_locationDown2 = len(self.locationDown2)

        if (not self.dim1_locationDown2):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_r_azpos2_Py(self.dim1_locationDown2)

        if (self.dim1_locationDownOffset2 == None):
            self.dim1_locationDownOffset2 = len(self.locationDownOffset2)

        if (not self.dim1_locationDownOffset2):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_r_azoff2_Py(self.dim1_locationDownOffset2)

        if (self.dim1_snr2 == None):
            self.dim1_snr2 = len(self.snr2)

        if (not self.dim1_snr2):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_r_sig2_Py(self.dim1_snr2)

        if (self.dim1_azimuthCarrier == None):
            self.dim1_azimuthCarrier = len(self.azimuthCarrier)

        if (not self.dim1_azimuthCarrier):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_azimuthCarrier_Py(self.dim1_azimuthCarrier)

        if (self.dim1_rangeCarrier == None):
            self.dim1_rangeCarrier = len(self.rangeCarrier)

        if (not self.dim1_rangeCarrier):
            print("Error. Trying to allocate zero size array")

            raise Exception

        resamp_slc.allocate_rangeCarrier_Py(self.dim1_rangeCarrier)


        return





    def deallocateArrays(self):
        resamp_slc.deallocate_dopplerCoefficients_Py()
        resamp_slc.deallocate_r_ranpos_Py()
        resamp_slc.deallocate_r_ranoff_Py()
        resamp_slc.deallocate_r_azpos_Py()
        resamp_slc.deallocate_r_azoff_Py()
        resamp_slc.deallocate_r_sig_Py()
        resamp_slc.deallocate_r_ranpos2_Py()
        resamp_slc.deallocate_r_ranoff2_Py()
        resamp_slc.deallocate_r_azpos2_Py()
        resamp_slc.deallocate_r_azoff2_Py()
        resamp_slc.deallocate_r_sig2_Py()
        resamp_slc.deallocate_azimuthCarrier_Py()
        resamp_slc.deallocate_rangeCarrier_Py()

        return

    def addInstrument(self):
        instrument = self._inputPorts.getPort('instrument').getObject()
        if(instrument):
            try:
                self.radarWavelength = instrument.getRadarWavelength()
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError("Unable to wire instrument port")




    def addOffsets(self):
        offsets = self._inputPorts.getPort('offsets').getObject()
        if(offsets):
            try:
                for offset in offsets:
                    (across,down) = offset.getCoordinate()
                    (acrossOffset,downOffset) = offset.getOffset()
                    snr = offset.getSignalToNoise()
                    self.locationAcross1.append(across)
                    self.locationDown1.append(down)                
                    self.locationAcrossOffset1.append(acrossOffset)
                    self.locationDownOffset1.append(downOffset)
                    self.snr1.append(snr)
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError("Unable to wire Offset port")



    def __getstate__(self):
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self,d):
        self.__dict__.update(d)
        self.logger = logging.getLogger('isce.stdproc.resamp_slc')
        return


    def __init__(self):
        Component.__init__(self)
        self._stdWriter = None
        self.numberFitCoefficients = None
        self.numberRangeBin = None
        self.numberLines = None
        self.firstLineOffset = None
        self.radarWavelength = None
        self.slantRangePixelSpacing = None
        self.dopplerCentroidCoefficients = []
        self.dim1_dopplerCentroidCoefficients = None
        self.locationAcross1 = []
        self.dim1_locationAcross1 = None
        self.locationAcrossOffset1 = []
        self.dim1_locationAcrossOffset1 = None
        self.locationDown1 = []
        self.dim1_locationDown1 = None
        self.locationDownOffset1 = []
        self.dim1_locationDownOffset1 = None
        self.snr1 = []
        self.dim1_snr1 = None
        self.locationAcross2 = []
        self.dim1_locationAcross2 = None
        self.locationAcrossOffset2 = []
        self.dim1_locationAcrossOffset2 = None
        self.locationDown2 = []
        self.dim1_locationDown2 = None
        self.locationDownOffset2 = []
        self.dim1_locationDownOffset2 = None
        self.snr2 = []
        self.dim1_snr2 = None
        self.azimuthCarrier = []
        self.dim1_azimuthCarrier = None
        self.rangeCarrier = []
        self.dim1_rangeCarrier = None
        self.logger = logging.getLogger('isce.stdproc.resamp_slc')
        
        offsetPort = Port(name='offsets',method=self.addOffsets)
        instrumentPort = Port(name='instrument',method=self.addInstrument)
        self._inputPorts.add(offsetPort)
        self._inputPorts.add(instrumentPort)
        
        self.dictionaryOfVariables = { \
                                      'NUMBER_FIT_COEFFICIENTS' : ['self.numberFitCoefficients', 'int','optional'], \
                                      'NUMBER_RANGE_BIN' : ['self.numberRangeBin', 'int','mandatory'], \
                                      'NUMBER_LINES' : ['self.numberLines', 'int','optional'], \
                                      'FIRST_LINE_OFFSET' : ['self.firstLineOffset', 'int','optional'], \
                                      'RADAR_WAVELENGTH' : ['self.radarWavelength', 'float','mandatory'], \
                                      'SLANT_RANGE_PIXEL_SPACING' : ['self.slantRangePixelSpacing', 'float','mandatory'], \
                                      'DOPPLER_CENTROID_COEFFICIENTS' : ['self.dopplerCentroidCoefficients', 'float','mandatory'], \
                                      'LOCATION_ACROSS1' : ['self.locationAcross1', 'float','mandatory'], \
                                      'LOCATION_ACROSS_OFFSET1' : ['self.locationAcrossOffset1', 'float','mandatory'], \
                                      'LOCATION_DOWN1' : ['self.locationDown1', 'float','mandatory'], \
                                      'LOCATION_DOWN_OFFSET1' : ['self.locationDownOffset1', 'float','mandatory'], \
                                      'SNR1' : ['self.snr1', 'float','mandatory'], \
                                      'LOCATION_ACROSS2' : ['self.locationAcross2', 'float','mandatory'], \
                                      'LOCATION_ACROSS_OFFSET2' : ['self.locationAcrossOffset2', 'float','mandatory'], \
                                      'LOCATION_DOWN2' : ['self.locationDown2', 'float','mandatory'], \
                                      'LOCATION_DOWN_OFFSET2' : ['self.locationDownOffset2', 'float','mandatory'], \
                                      'SNR2' : ['self.snr2', 'float','mandatory'] \
                                      }
        
        self.dictionaryOfOutputVariables = { \
                                      'AZIMUTH_CARRIER' : 'self.azimuthCarrier',\
                                      'RANGE_CARRIER' : 'self.rangeCarrier' \
                                     }

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
