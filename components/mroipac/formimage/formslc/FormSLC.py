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
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
from mroipac.formimage import formslc
from iscesys.Component.Component import Component

##
# This class allows the creation of a SLC (Single Look Complex) image from a Raw image. The parameters that need to be set are
#\verbatim
#PLANET_RADIUS: radius of curvarture of the planet. Mandatory.
#LINEAR_RESAMPLING_COEFFICIENTS: Optional. Default [0,0,0,0].
#LINEAR_RESAMPLING_DELTAS: Optional. Default [0,0,0,0].
#DOPPLER_CENTROID_COEFFICIENTS: Mandatory.
#PLANET_GM: Planet gravitational constant times mass. Optional. Default 398600448073000x10^6 m^3/s^2, i.e Earth value.
#BODY_FIXED_VELOCITY: Mandatory.
#SPACECRAFT_HEIGHT: Spacecraft height. Mandatory.
#POINTING_DIRECTION: Mandatory. (check this one. I think is not used)
#ANTENNA_SCH_VELOCITY: Mandatory.
#ANTENNA_SCH_ACCELERATION: Mandatory.
#PRF: pulse repetition frequency. Mandatory.
#RANGE_SAMPLING_RATE: range sampling rate. Mandatory.
#CHIRP_SLOPE: chirp slope .Mandatory.
#RANGE_PULSE_DURATION: range pulse duration. Mandatory.
#RANGE_CHIRP_EXTENSION_POINTS: Mandatory
#RADAR_WAVELENGTH: radar wavelength. Mandatory.
#RANGE_SPECTRAL_WEIGHTING: Optional. Default 1.
#SPECTRAL_SHIFT_FRACTIONS: Optional. Default [1,1]
#NUMBER_GOOD_BYTES:  number of bytes in the raw image considered good for the computation. Must be less or equal to the width of the raw image. Optional. Default raw iamge width.
#NUMBER_BYTES_PER_LINE: number of bytes per line in the raw image. Optional. Default raw image width.
#DEBUG_FLAG: debug flag. Optional. Default 'n'.
#DESKEW_FLAG: deskew flag. Optional. Default 'n'.
#SECONDARY_RANGE_MIGRATION_FLAG: secondary range migration flag. Optional. Default 'n'.
#FIRST_LINE: first line in the raw image to be read. Mandatory.
#NUMBER_PATCHES: number of patches in which the image is divided in order to reduce memory usage. Mandatory.
#FIRST_SAMPLE: first sample to be used in the raw image. Mandatory.
#AZIMUTH_PATCH_SIZE: azimuth patch size. Mandatory.
#NUMBER_VALID_PULSES: number of valid pulses. Mandatory.
#CALTONE_LOCATION: caltone location. Optional. Default 0.
#START_RANGE_BIN: start range bin. Optional. Default 1.
#NUMBER_RANGE_BIN: number of range bin. Optional. Default SLC image width.
#RANGE_FIRST_SAMPLE': range first sample. Mandatory.
#INPHASE_VALUE: in phase value. Mandatory.
#QUADRATURE_VALUE: quadrature value. Mandatory.
#IQ_FLIP: IQ flip flag. Optional. Default 'n'.
#AZIMUTH_RESOLUTION: azimuth resolution. Mandatory.
#NUMBER_AZIMUTH_LOOKS: number of azimuth looks. Mandatory.
#\endverbatim
#In addition isceobj.RawImage and isceobj.SlcImage objects need to be created and the pointers to the underlying  LineAccessor.LineAccessor objects need to be passed (see isceobj.RawImage.getImagePointer() and isceobj.SlcImage.getImagePointer()) to the formSLCImage() method.
#Since the FormSLC class inherits the iscesys.Component.Component, the methods of initialization described in the Component package can be used.
#Moreover each parameter can be set with the corresponding accessor method setParameter() (see the class member methods).
#@see LineAccessor.LineAccessor.
#@see iscesys.Component.Component.
#@see isceobj.RawImage
#@see isceobj.SlcImage
#@see isceobj.RawImage.getImagePointer()
#@see isceobj.SlcImage.getImagePointer()

class FormSLC(Component):

##
#This method invokes the actual fortran compute engine in formslc.F that creates the SLC image from the Raw image. 
#@param rawImage pointer to a  LineAccessor.LineAccessor object (see isceobj.RawImage.getImagePointer()).
#@param SlcImage pointer to a  LineAccessor.LineAccessor object (see isceobj.SlcImage.getImagePointer()).
#@see isceobj.RawImage.
#@see isceobj.SlcImage.
#@see isceobj.RawImage.getImagePointer()
#@see isceobj.SlcImage.getImagePointer()
    def formSLCImage(self,rawImage,slcImage):
        
        self.setOptionalVariables(rawImage,slcImage)
        self.checkInitialization()
        self.allocateArrays()
        if(self.debugFlag == 'n'): #some flags where defined 'y' or 'n' but this one 0 or 1. make the interface equal for all flags
            self.debugFlag = 0
        else:
            self.debugFlag = 1
        self.setState()
        slcImagePt = slcImage.getImagePointer()
        rawImagePt = rawImage.getImagePointer()
        formslc.formslc_Py(rawImagePt,slcImagePt)
        self.deallocateArrays()

    def setOptionalVariables(self,rawImage,slcImage):

        if self.numberGoodBytes == None:
            self.numberGoodBytes = rawImage.getWidth()
            print('Variable NUMBER_GOOD_BYTES set equal to the raw image width %i in FormSLC.py'%self.numberGoodBytes)

        if self.numberBytesPerLine == None:
            self.numberBytesPerLine = rawImage.getWidth()
            print('Variable NUMBER_BYTES_PER_LINE set equal to the raw image width %i in FormSLC.py'%self.numberBytesPerLine)

        if self.numberRangeBin == None:
            self.numberRangeBin = slcImage.getWidth()
            print('Variable NUMBER_RANGE_BIN set equal to the slc image width %i in FormSLC.py'%self.numberRangeBin)
##
# Set the data in the fortran data module.

    def setState(self):
        formslc.setNumberGoodBytes_Py(int(self.numberGoodBytes))
        formslc.setNumberBytesPerLine_Py(int(self.numberBytesPerLine))
        formslc.setDebugFlag_Py(int(self.debugFlag))
        formslc.setDeskewFlag_Py(self.deskewFlag)
        formslc.setSecondaryRangeMigrationFlag_Py(self.secondaryRangeMigrationFlag)
        formslc.setFirstLine_Py(int(self.firstLine))
        formslc.setNumberPatches_Py(int(self.numberPatches))
        formslc.setFirstSample_Py(int(self.firstSample))
        formslc.setAzimuthPatchSize_Py(int(self.azimuthPatchSize))
        formslc.setNumberValidPulses_Py(int(self.numberValidPulses))
        formslc.setCaltoneLocation_Py(float(self.caltoneLocation))
        formslc.setStartRangeBin_Py(int(self.startRangeBin))
        formslc.setNumberRangeBin_Py(int(self.numberRangeBin))
        formslc.setDopplerCentroidCoefficients_Py(self.dopplerCentroidCoefficients, self.dim1_dopplerCentroidCoefficients)
        formslc.setPlanetRadiusOfCurvature_Py(float(self.planetRadiusOfCurvature))
        formslc.setBodyFixedVelocity_Py(float(self.bodyFixedVelocity))
        formslc.setSpacecraftHeight_Py(float(self.spacecraftHeight))
        formslc.setPlanetGravitationalConstant_Py(float(self.planetGravitationalConstant))
        formslc.setPointingDirection_Py(int(self.pointingDirection))
        formslc.setAntennaSCHVelocity_Py(self.antennaSCHVelocity, self.dim1_antennaSCHVelocity)
        formslc.setAntennaSCHAcceleration_Py(self.antennaSCHAcceleration, self.dim1_antennaSCHAcceleration)
        formslc.setRangeFirstSample_Py(float(self.rangeFirstSample))
        formslc.setPRF_Py(float(self.PRF))
        formslc.setInPhaseValue_Py(float(self.inPhaseValue))
        formslc.setQuadratureValue_Py(float(self.quadratureValue))
        formslc.setIQFlip_Py(self.IQFlip)
        formslc.setAzimuthResolution_Py(float(self.azimuthResolution))
        formslc.setNumberAzimuthLooks_Py(int(self.numberAzimuthLooks))
        formslc.setRangeSamplingRate_Py(float(self.rangeSamplingRate))
        formslc.setChirpSlope_Py(float(self.chirpSlope))
        formslc.setRangePulseDuration_Py(float(self.rangePulseDuration))
        formslc.setRangeChirpExtensionPoints_Py(int(self.rangeChirpExtensionPoints))
        formslc.setRadarWavelength_Py(float(self.radarWavelength))
        formslc.setRangeSpectralWeighting_Py(float(self.rangeSpectralWeighting))
        formslc.setSpectralShiftFractions_Py(self.spectralShiftFractions, self.dim1_spectralShiftFractions)
        formslc.setLinearResamplingCoefficiets_Py(self.linearResamplingCoefficients, self.dim1_linearResamplingCoefficients)
        formslc.setLinearResamplingDeltas_Py(self.linearResamplingDeltas, self.dim1_linearResamplingDeltas)

        return





    def setNumberGoodBytes(self,var):
        self.numberGoodBytes = int(var)
        return

    def setNumberBytesPerLine(self,var):
        self.numberBytesPerLine = int(var)
        return

    def setDebugFlag(self,var):
        self.debugFlag = str(var)
        return

    def setDeskewFlag(self,var):
        self.deskewFlag = str(var)
        return

    def setSecondaryRangeMigrationFlag(self,var):
        self.secondaryRangeMigrationFlag = str(var)
        return

    def setFirstLine(self,var):
        self.firstLine = int(var)
        return

    def setNumberPatches(self,var):
        self.numberPatches = int(var)
        return

    def setFirstSample(self,var):
        self.firstSample = int(var)
        return

    def setAzimuthPatchSize(self,var):
        self.azimuthPatchSize = int(var)
        return

    def setNumberValidPulses(self,var):
        self.numberValidPulses = int(var)
        return

    def setCaltoneLocation(self,var):
        self.caltoneLocation = float(var)
        return

    def setStartRangeBin(self,var):
        self.startRangeBin = int(var)
        return

    def setNumberRangeBin(self,var):
        self.numberRangeBin = int(var)
        return

    def setDopplerCentroidCoefficients(self,var):
        self.dopplerCentroidCoefficients = var
        return

    def setPlanetRadiusOfCurvature(self,var):
        self.planetRadiusOfCurvature = float(var)
        return

    def setBodyFixedVelocity(self,var):
        self.bodyFixedVelocity = float(var)
        return

    def setSpacecraftHeight(self,var):
        self.spacecraftHeight = float(var)
        return

    def setPlanetGravitationalConstant(self,var):
        self.planetGravitationalConstant = float(var)
        return

    def setPointingDirection(self,var):
        self.pointingDirection = int(var)
        return

    def setAntennaSCHVelocity(self,var):
        self.antennaSCHVelocity = var
        return

    def setAntennaSCHAcceleration(self,var):
        self.antennaSCHAcceleration = var
        return

    def setRangeFirstSample(self,var):
        self.rangeFirstSample = float(var)
        return

    def setPRF(self,var):
        self.PRF = float(var)
        return

    def setInPhaseValue(self,var):
        self.inPhaseValue = float(var)
        return

    def setQuadratureValue(self,var):
        self.quadratureValue = float(var)
        return

    def setIQFlip(self,var):
        self.IQFlip = str(var)
        return

    def setAzimuthResolution(self,var):
        self.azimuthResolution = float(var)
        return

    def setNumberAzimuthLooks(self,var):
        self.numberAzimuthLooks = int(var)
        return

    def setRangeSamplingRate(self,var):
        self.rangeSamplingRate = float(var)
        return

    def setChirpSlope(self,var):
        self.chirpSlope = float(var)
        return

    def setRangePulseDuration(self,var):
        self.rangePulseDuration = float(var)
        return

    def setRangeChirpExtensionPoints(self,var):
        self.rangeChirpExtensionPoints = int(var)
        return

    def setRadarWavelength(self,var):
        self.radarWavelength = float(var)
        return

    def setRangeSpectralWeighting(self,var):
        self.rangeSpectralWeighting = float(var)
        return

    def setSpectralShiftFractions(self,var):
        self.spectralShiftFractions = var
        return

    def setLinearResamplingCoefficients(self,var):
        self.linearResamplingCoefficients = var
        return

    def setLinearResamplingDeltas(self,var):
        self.linearResamplingDeltas = var
        return






    def allocateArrays(self):
        if (self.dim1_dopplerCentroidCoefficients == None):
            self.dim1_dopplerCentroidCoefficients = len(self.dopplerCentroidCoefficients)

        if (not self.dim1_dopplerCentroidCoefficients):
            print("Error. Trying to allocate zero size array")
            raise Exception
        formslc.allocate_dopplerCoefficients_Py(self.dim1_dopplerCentroidCoefficients)

        if (self.dim1_antennaSCHVelocity == None):
            self.dim1_antennaSCHVelocity = len(self.antennaSCHVelocity)

        if (not self.dim1_antennaSCHVelocity):
            print("Error. Trying to allocate zero size array")
            raise Exception

        formslc.allocate_r_platvel1_Py(self.dim1_antennaSCHVelocity)

        if (self.dim1_antennaSCHAcceleration == None):
            self.dim1_antennaSCHAcceleration = len(self.antennaSCHAcceleration)

        if (not self.dim1_antennaSCHAcceleration):
            print("Error. Trying to allocate zero size array")
            raise Exception

        formslc.allocate_r_platacc1_Py(self.dim1_antennaSCHAcceleration)

        if (self.dim1_spectralShiftFractions == None):
            self.dim1_spectralShiftFractions = len(self.spectralShiftFractions)

        if (not self.dim1_spectralShiftFractions):
            print("Error. Trying to allocate zero size array")
            raise Exception

        formslc.allocate_spectralShiftFrac_Py(self.dim1_spectralShiftFractions)

        if (self.dim1_linearResamplingCoefficients == None):
            self.dim1_linearResamplingCoefficients = len(self.linearResamplingCoefficients)

        if (not self.dim1_linearResamplingCoefficients):
            print("Error. Trying to allocate zero size array")
            raise Exception

        formslc.allocate_linearResampCoeff_Py(self.dim1_linearResamplingCoefficients)

        if (self.dim1_linearResamplingDeltas == None):
            self.dim1_linearResamplingDeltas = len(self.linearResamplingDeltas)

        if (not self.dim1_linearResamplingDeltas):
            print("Error. Trying to allocate zero size array")
            raise Exception

        formslc.allocate_linearResampDeltas_Py(self.dim1_linearResamplingDeltas)


        return





    def deallocateArrays(self):
        formslc.deallocate_dopplerCoefficients_Py()
        formslc.deallocate_r_platvel1_Py()
        formslc.deallocate_r_platacc1_Py()
        formslc.deallocate_spectralShiftFrac_Py()
        formslc.deallocate_linearResampCoeff_Py()
        formslc.deallocate_linearResampDeltas_Py()

        return

    



    def __init__(self):
        
        Component.__init__(self)
        
        #optional variables
        self.debugFlag = 'n' 
        self.deskewFlag = 'n'
        self.secondaryRangeMigrationFlag = 'n'
        self.planetGravitationalConstant =  398600448073000
        self.numberGoodBytes = None
        self.numberBytesPerLine = None
        self.numberRangeBin = None
        self.caltoneLocation = 0
        self.startRangeBin = 1
        self.IQFlip = 'n'
        self.rangeSpectralWeighting = 1
        self.spectralShiftFractions = [0 , 0]
        self.linearResamplingCoefficients = [0,0,0,0]
        self.linearResamplingDeltas = [0,0,0,0]
        
        #mandatory variables
        self.firstLine = None
        self.numberPatches = None
        self.firstSample = None
        self.azimuthPatchSize = None
        self.numberValidPulses = None
        self.dopplerCentroidCoefficients = []
        self.planetRadiusOfCurvature = None
        self.bodyFixedVelocity = None
        self.spacecraftHeight = None
        self.pointingDirection = None
        self.antennaSCHVelocity = []
        self.antennaSCHAcceleration = []
        self.rangeFirstSample = None
        self.PRF = None
        self.inPhaseValue = None
        self.quadratureValue = None
        self.azimuthResolution = None
        self.numberAzimuthLooks = None
        self.rangeSamplingRate = None
        self.chirpSlope = None
        self.rangePulseDuration = None
        self.rangeChirpExtensionPoints = None
        self.radarWavelength = None
        self.dim1_spectralShiftFractions = None
        self.dopplerCentroidCoefficients = []
        
        
        self.dim1_dopplerCentroidCoefficients = None
        self.dim1_linearResamplingCoefficients = None
        self.dim1_linearResamplingDeltas = None
        self.dim1_antennaSCHVelocity = None
        self.dim1_antennaSCHAcceleration = None
        
        
        self.descriptionOfVariables = {}
        self.dictionaryOfVariables = { \
         'ANTENNA_SCH_ACCELERATION':['self.antennaSCHAcceleration','float','mandatory'],\
         'ANTENNA_SCH_VELOCITY':['self.antennaSCHVelocity','float','mandatory'],\
         'AZIMUTH_PATCH_SIZE' : ['self.azimuthPatchSize', 'int','mandatory'], \
         'AZIMUTH_RESOLUTION' : ['self.azimuthResolution', 'float','mandatory'], \
         'BODY_FIXED_VELOCITY':['self.bodyFixedVelocity', 'float','mandatory'], \
         'CALTONE_LOCATION': ['self.caltoneLocation', 'float','optional'], \
         'CHIRP_SLOPE':['self.chirpSlope', 'float','mandatory'], \
         'DEBUG_FLAG': ['self.debugFlag', 'str','optional'], \
         'DESKEW_FLAG': ['self.deskewFlag', 'str','optional'], \
         'DOPPLER_CENTROID_COEFFICIENTS':['self.dopplerCentroidCoefficients', 'float','mandatory'], \
         'FIRST_LINE': ['self.firstLine', 'int','mandatory'], \
         'FIRST_SAMPLE' : ['self.firstSample', 'int','mandatory'], \
         'INPHASE_VALUE': ['self.inPhaseValue', 'float','mandatory'], \
         'IQ_FLIP': ['self.IQFlip', 'str','optional'], \
         'LINEAR_RESAMPLING_COEFFICIENTS':['self.linearResamplingCoefficients', 'float','optional'], \
         'LINEAR_RESAMPLING_DELTAS':['self.linearResamplingDeltas', 'float','optional'], \
         'NUMBER_AZIMUTH_LOOKS' : ['self.numberAzimuthLooks', 'int','mandatory'],\
         'NUMBER_BYTES_PER_LINE': ['self.numberBytesPerLine', 'int','optional'], \
         'NUMBER_GOOD_BYTES': ['self.numberGoodBytes', 'int','optional'], \
         'NUMBER_PATCHES': ['self.numberPatches', 'int','mandatory'], \
         'NUMBER_RANGE_BIN': ['self.numberRangeBin', 'int','optional'], \
         'NUMBER_VALID_PULSES': ['self.numberValidPulses', 'int','mandatory'], \
         'PLANET_GM':['self.planetGravitationalConstant', 'float','optional'], \
         'PLANET_RADIUS':['self.planetRadiusOfCurvature', 'float','mandatory'], \
         'POINTING_DIRECTION':['self.pointingDirection', 'int','mandatory'], \
         'PRF':['self.PRF', 'float','mandatory'], \
         'QUADRATURE_VALUE': ['self.quadratureValue', 'float','mandatory'], \
         'RADAR_WAVELENGTH':['self.radarWavelength', 'float','mandatory'], \
         'RANGE_CHIRP_EXTENSION_POINTS':['self.rangeChirpExtensionPoints', 'int','mandatory'], \
         'RANGE_FIRST_SAMPLE': ['self.rangeFirstSample', 'float','mandatory'], \
         'RANGE_PULSE_DURATION':['self.rangePulseDuration', 'float','mandatory'], \
         'RANGE_SAMPLING_RATE':['self.rangeSamplingRate', 'float','mandatory'], \
         'RANGE_SPECTRAL_WEIGHTING':['self.rangeSpectralWeighting', 'float','optional'],\
         'SECONDARY_RANGE_MIGRATION_FLAG': ['self.secondaryRangeMigrationFlag', 'str','optional'], \
         'SPACECRAFT_HEIGHT':['self.spacecraftHeight', 'float','mandatory'], \
         'SPECTRAL_SHIFT_FRACTIONS':['self.spectralShiftFractions','float','optional'] ,\
         'START_RANGE_BIN': ['self.startRangeBin', 'int','optional'], \
         }
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
