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
from iscesys.Component.Component import Component


class FormSLC(Component):

    def formSLCImage(self,rawImage,slcImage):
        
        self.setOptionalVariables(rawImage,slcImage)
        self.printComponent()

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
        self.dictionaryOfVariables = {'PLANET_RADIUS':['self.planetRadiusOfCurvature', 'float','mandatory'], \
         
         'LINEAR_RESAMPLING_COEFFICIENTS':['self.linearResamplingCoefficients', 'float','optional'], \
         'LINEAR_RESAMPLING_DELTAS':['self.linearResamplingDeltas', 'float','optional'], \
         'DOPPLER_CENTROID_COEFFICIENTS':['self.dopplerCentroidCoefficients', 'float','mandatory'], \
         'PLANET_GM':['self.planetGravitationalConstant', 'float','optional'], \
         'BODY_FIXED_VELOCITY':['self.bodyFixedVelocity', 'float','mandatory'], \
         'SPACECRAFT_HEIGHT':['self.spacecraftHeight', 'float','mandatory'], \
         'POINTING_DIRECTION':['self.pointingDirection', 'int','mandatory'], \
         'ANTENNA_SCH_VELOCITY':['self.antennaSCHVelocity','float','mandatory'],\
         'ANTENNA_SCH_ACCELERATION':['self.antennaSCHAcceleration','float','mandatory'],\
         'PRF':['self.PRF', 'float','mandatory'], \
         'RANGE_SAMPLING_RATE':['self.rangeSamplingRate', 'float','mandatory'], \
         'CHIRP_SLOPE':['self.chirpSlope', 'float','mandatory'], \
         'RANGE_PULSE_DURATION':['self.rangePulseDuration', 'float','mandatory'], \
         'RANGE_CHIRP_EXTENSION_POINTS':['self.rangeChirpExtensionPoints', 'int','mandatory'], \
         'RADAR_WAVELENGTH':['self.radarWavelength', 'float','mandatory'], \
         'RANGE_SPECTRAL_WEIGHTING':['self.rangeSpectralWeighting', 'float','optional'],\
         'SPECTRAL_SHIFT_FRACTIONS':['self.spectralShiftFractions','float','optional'] ,\
         'NUMBER_GOOD_BYTES': ['self.numberGoodBytes', 'int','optional'], \
         'NUMBER_BYTES_PER_LINE': ['self.numberBytesPerLine', 'int','optional'], \
         'DEBUG_FLAG': ['self.debugFlag', 'str','optional'], \
         'DESKEW_FLAG': ['self.deskewFlag', 'str','optional'], \
         'SECONDARY_RANGE_MIGRATION_FLAG': ['self.secondaryRangeMigrationFlag', 'str','optional'], \
         'FIRST_LINE': ['self.firstLine', 'int','mandatory'], \
         'NUMBER_PATCHES': ['self.numberPatches', 'int','mandatory'], \
         'FIRST_SAMPLE' : ['self.firstSample', 'int','mandatory'], \
         'AZIMUTH_PATCH_SIZE' : ['self.azimuthPatchSize', 'int','mandatory'], \
         'NUMBER_VALID_PULSES': ['self.numberValidPulses', 'int','mandatory'], \
         'CALTONE_LOCATION': ['self.caltoneLocation', 'float','optional'], \
         'START_RANGE_BIN': ['self.startRangeBin', 'int','optional'], \
         'NUMBER_RANGE_BIN': ['self.numberRangeBin', 'int','optional'], \
         'RANGE_FIRST_SAMPLE': ['self.rangeFirstSample', 'float','mandatory'], \
         'INPHASE_VALUE': ['self.inPhaseValue', 'float','mandatory'], \
         'QUADRATURE_VALUE': ['self.quadratureValue', 'float','mandatory'], \
         'IQ_FLIP': ['self.IQFlip', 'str','optional'], \
         'AZIMUTH_RESOLUTION' : ['self.azimuthResolution', 'float','mandatory'], \
         'NUMBER_AZIMUTH_LOOKS' : ['self.numberAzimuthLooks', 'int','mandatory']}
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
