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
import math
from isceobj import Constants as CN
from iscesys.Component.Component import Component,Port
from iscesys.Compatibility import Compatibility
import isceobj.Image as IF #load image factories
from stdproc.stdproc.correct import correct

class Correct(Component):

    logging_name = "isce.stdproc.topo"

    def __init__(self):
        super(Correct, self).__init__()
        self.referenceOrbit = []
        self.dim1_referenceOrbit = None
        self.mocompBaseline = []
        self.dim1_mocompBaseline = None
        self.dim2_mocompBaseline = None
        self.isMocomp = None
        self.ellipsoidMajorSemiAxis = None
        self.ellipsoidEccentricitySquared = None
        self.length = None
        self.width = None
        self.slantRangePixelSpacing = None
        self.rangeFirstSample = None
        self.spacecraftHeight = None
        self.planetLocalRadius = None
        self.bodyFixedVelocity = None
        self.numberRangeLooks = None
        self.numberAzimuthLooks = None
        self.pegLatitude = None
        self.pegLongitude = None
        self.pegHeading = None
        self.prf = None
        self.radarWavelength = None
        self.midpoint = []
        self.dim1_midpoint = None
        self.dim2_midpoint = None
        self.s1sch = []
        self.dim1_s1sch = None
        self.dim2_s1sch = None
        self.s2sch = []
        self.dim1_s2sch = None
        self.dim2_s2sch = None
        self.sc = []
        self.dim1_sc = None
        self.dim2_sc = None
        self.lookSide = -1    #Set to right side by default
        self.dopplerCentroidCoeffs = None
        
        self.heightSchFilename = ''
        self.heightSchCreatedHere = False
        self.heightSchImage = None
        self.heightSchAccessor = None
        self.intFilename = ''
        self.intCreatedHere = False
        self.intImage = None
        self.intAccessor = None
        self.topophaseMphFilename = ''
        self.topophaseMphCreatedHere = False
        self.topophaseMphImage = None
        self.topophaseMphAccessor = None
        self.topophaseFlatFilename = ''
        self.topophaseFlatCreatedHere = False
        self.topophaseFlatImage = None
        self.topophaseFlatAccessor = None
        
        self.dictionaryOfVariables = { 
            'REFERENCE_ORBIT' : ['referenceOrbit', 'float','mandatory'], 
            'MOCOMP_BASELINE' : ['mocompBaseline', '','mandatory'], 
            'IS_MOCOMP' : ['isMocomp', 'int','optional'], 
            'ELLIPSOID_MAJOR_SEMIAXIS' : ['ellipsoidMajorSemiAxis', 'float','optional'], 
            'ELLIPSOID_ECCENTRICITY_SQUARED' : ['ellipsoidEccentricitySquared', 'float','optional'], 
            'LENGTH' : ['length', 'int','mandatory'], 
            'WIDTH' : ['width', 'int','mandatory'], 
            'SLANT_RANGE_PIXEL_SPACING' : ['slantRangePixelSpacing', 'float','mandatory'], 
            'RANGE_FIRST_SAMPLE' : ['rangeFirstSample', 'float','mandatory'], 
            'SPACECRAFT_HEIGHT' : ['spacecraftHeight', 'float','mandatory'], 
            'PLANET_LOCAL_RADIUS' : ['planetLocalRadius', 'float','mandatory'], 
            'BODY_FIXED_VELOCITY' : ['bodyFixedVelocity', 'float','mandatory'], 
            'NUMBER_RANGE_LOOKS' : ['numberRangeLooks', 'int','mandatory'], 
            'NUMBER_AZIMUTH_LOOKS' : ['numberAzimuthLooks', 'int','mandatory'], 
            'PEG_LATITUDE' : ['pegLatitude', 'float','mandatory'], 
            'PEG_LONGITUDE' : ['pegLongitude', 'float','mandatory'], 
            'PEG_HEADING' : ['pegHeading', 'float','mandatory'], 
            'DOPPLER_CENTROID' : ['dopplerCentroidCoeffs', 'float','mandatory'], 
            'PRF' : ['prf', 'float','mandatory'], 
            'RADAR_WAVELENGTH' : ['radarWavelength', 'float','mandatory'], 
            'MIDPOINT' : ['midpoint', '','mandatory'], 
            'S1SCH' : ['s1sch', '','mandatory'], 
            'S2SCH' : ['s2sch', '','mandatory'], 
            'SC' : ['sc', '','mandatory'] 
            }
        self.dictionaryOfOutputVariables = {}
        self.descriptionOfVariables = {}
        self.mandatoryVariables = []
        self.optionalVariables = []
        self.initOptionalAndMandatoryLists()
        return None
    
    def createPorts(self):
        pegPort = Port(name="peg",method=self.addPeg)
        planetPort = Port(name='planet',method=self.addPlanet)        
        framePort = Port(name='frame',method=self.addFrame)
        ifgPort = Port(name='interferogram',method=self.addInterferogram)
        slcPort = Port(name='masterslc',method=self.addMasterSlc) #Piyush
        
        self._inputPorts.add(pegPort)
        self._inputPorts.add(planetPort)        
        self._inputPorts.add(framePort)
        self._inputPorts.add(ifgPort)
        self._inputPorts.add(slcPort)  #Piyush
        return None

    # assume that for the images passed no createImage has been called  

    def correct(self, intImage=None,heightSchImage=None,topoMphImage=None,
                topoFlatImage=None):
        for port in self.inputPorts:
            port()
        if not heightSchImage is None:
            self.heightSchImage = heightSchImage
        
        # another way of passing width and length if not using the ports
        if intImage is not None:
            self.intImage = intImage
        
            #if width or length not defined get 'em  from intImage since they 
            #are needed to create the output images
            if self.width is None:
                self.width = self.intImage.getWidth()
            if self.length is None:
                self.length = self.intImage.getLength()
        
        if not topoMphImage is None:
            self.topophaseMphImage = topoMphImage
        if topoFlatImage is not None:
            self.topophaseFlatImage = topoFlatImage
        self.setDefaults() 
        #creates images if not set and call the createImage() (also for the intImage)
        self.createImages()

        self.heightSchAccessor = self.heightSchImage.getImagePointer()
        self.intAccessor = self.intImage.getImagePointer()
        self.topophaseMphAccessor = self.topophaseMphImage.getImagePointer()
        self.topophaseFlatAccessor = self.topophaseFlatImage.getImagePointer()
        self.allocateArrays()
        self.setState()
        correct.correct_Py(self.intAccessor,
                           self.heightSchAccessor,
                           self.topophaseMphAccessor,
                           self.topophaseFlatAccessor)
        self.topophaseMphImage.trueDataType = self.topophaseMphImage.getDataType()
        self.topophaseFlatImage.trueDataType = self.topophaseFlatImage.getDataType()
        self.topophaseMphImage.renderHdr()
        self.topophaseFlatImage.renderHdr()
        self.deallocateArrays()
        #call the finalizeImage() on all the images
        self.destroyImages()

        return


    def setDefaults(self):
        if self.ellipsoidMajorSemiAxis is None:
            self.ellipsoidMajorSemiAxis = CN.EarthMajorSemiAxis

        if self.ellipsoidEccentricitySquared is None:
            self.ellipsoidEccentricitySquared = CN.EarthEccentricitySquared

        if self.isMocomp is None:
            self.isMocomp = (8192-2048)/2 
        
        if self.topophaseFlatFilename == '':
            self.topophaseFlatFilename = 'topophase.flat'
            self.logger.warning(
                'The topophase flat file has been given the default name %s' %
                (self.topophaseFlatFilename)
                )
        if self.topophaseMphFilename == '':
            self.topophaseMphFilename = 'topophase.mph'
            self.logger.warning(
            'The topophase mph file has been given the default name %s' %
            (self.topophaseMphFilename)
            )

    def destroyImages(self):
        self.intImage.finalizeImage()
        self.heightSchImage.finalizeImage()
        self.topophaseMphImage.finalizeImage()
        self.topophaseFlatImage.finalizeImage()

    def createImages(self):
        
        if self.heightSchImage is None and not self.heightSchFilename == '':
            self.heightSchImage = IF.createImage()
            accessMode = 'read'
            dataType = 'FLOAT'
            width = self.width
            self.heightSchImage.initImage(
                self.heightSchFilename, accessMode, width, dataType
            )
        elif self.heightSchImage is None:
            # this should never happen, atleast when using the  
            # correct method. same for other images
            self.logger.error(
            'Must either pass the heightSchImage in the call or set self.heightSchFilename.'
            )
            raise Exception
        
        if (
            self.topophaseFlatImage is None and
            not self.topophaseFlatFilename == ''
            ):
            self.topophaseFlatImage = IF.createIntImage()
            accessMode = 'write'
            width = self.width
            self.topophaseFlatImage.initImage(self.topophaseFlatFilename,
                                              accessMode,
                                              width)
        elif self.topophaseFlatImage is None:
            self.logger.error(
                'Must either pass the topophaseFlatImage in the call or set self.topophaseMphFilename.'
                )
        
        if (
            self.topophaseMphImage is None and
            not self.topophaseMphFilename == ''
            ):
            self.topophaseMphImage = IF.createIntImage()
            accessMode = 'write'
            width = self.width
            self.topophaseMphImage.initImage(self.topophaseMphFilename,
                                             accessMode,
                                             width)
        elif self.topophaseMphImage is None:
            self.logger.error(
                'Must either pass the topophaseMphImage in the call or set self.topophaseMphFilename.'
                )
            #one way or another when it gets here the images better be defined
        self.intImage.createImage()#this is passed but call createImage and finalizeImage from here
        self.heightSchImage.createImage()
        self.topophaseFlatImage.createImage()
        self.topophaseMphImage.createImage()

    def setState(self):
        correct.setReferenceOrbit_Py(self.referenceOrbit,
                                     self.dim1_referenceOrbit)
        correct.setMocompBaseline_Py(self.mocompBaseline,
                                     self.dim1_mocompBaseline,
                                     self.dim2_mocompBaseline)
        correct.setISMocomp_Py(int(self.isMocomp))
        correct.setEllipsoidMajorSemiAxis_Py(
            float(self.ellipsoidMajorSemiAxis)
            )
        correct.setEllipsoidEccentricitySquared_Py(
            float(self.ellipsoidEccentricitySquared)
            )
        correct.setLength_Py(int(self.length))
        correct.setWidth_Py(int(self.width))
        correct.setRangePixelSpacing_Py(float(self.slantRangePixelSpacing))
        correct.setRangeFirstSample_Py(float(self.rangeFirstSample))
        correct.setSpacecraftHeight_Py(float(self.spacecraftHeight))
        correct.setPlanetLocalRadius_Py(float(self.planetLocalRadius))
        correct.setBodyFixedVelocity_Py(float(self.bodyFixedVelocity))
        correct.setNumberRangeLooks_Py(int(self.numberRangeLooks))
        correct.setNumberAzimuthLooks_Py(int(self.numberAzimuthLooks))
        correct.setPegLatitude_Py(float(self.pegLatitude))
        correct.setPegLongitude_Py(float(self.pegLongitude))
        correct.setPegHeading_Py(float(self.pegHeading))
        correct.setDopCoeff_Py(self.dopplerCentroidCoeffs)
        correct.setPRF_Py(float(self.prf))
        correct.setRadarWavelength_Py(float(self.radarWavelength))
        correct.setMidpoint_Py(self.midpoint,
                               self.dim1_midpoint,
                               self.dim2_midpoint)
        correct.setSch1_Py(self.s1sch, self.dim1_s1sch, self.dim2_s1sch)
        correct.setSch2_Py(self.s2sch, self.dim1_s2sch, self.dim2_s2sch)
        correct.setSc_Py(self.sc, self.dim1_sc, self.dim2_sc)
        correct.setLookSide_Py(int(self.lookSide))

        return None

    def setLookSide(self, var):
        self.lookSide = int(var)
        return

    def setReferenceOrbit(self, var):
        self.referenceOrbit = var
        return

    def setMocompBaseline(self, var):
        self.mocompBaseline = var
        return

    def setISMocomp(self, var):
        self.isMocomp = int(var)
        return

    def setEllipsoidMajorSemiAxis(self, var):
        self.ellipsoidMajorSemiAxis = float(var)
        return

    def setEllipsoidEccentricitySquared(self, var):
        self.ellipsoidEccentricitySquared = float(var)
        return

    def setLength(self, var):
        self.length = int(var)
        return

    def setWidth(self, var):
        self.width = int(var)
        return

    def setRangePixelSpacing(self, var):
        self.slantRangePixelSpacing = float(var)
        return

    def setRangeFirstSample(self, var):
        self.rangeFirstSample = float(var)
        return

    def setSpacecraftHeight(self, var):
        self.spacecraftHeight = float(var)
        return

    def setPlanetLocalRadius(self, var):
        self.planetLocalRadius = float(var)
        return

    def setBodyFixedVelocity(self, var):
        self.bodyFixedVelocity = float(var)
        return

    def setNumberRangeLooks(self, var):
        self.numberRangeLooks = int(var)
        return

    def setNumberAzimuthLooks(self, var):
        self.numberAzimuthLooks = int(var)
        return

    def setPegLatitude(self, var):
        self.pegLatitude = float(var)
        return

    def setPegLongitude(self, var):
        self.pegLongitude = float(var)
        return

    def setPegHeading(self, var):
        self.pegHeading = float(var)
        return

    def setDopplerCentroidCoeffs(self, var):
        self.dopplerCentroidCoeffs = var
        return

    def setPRF(self, var):
        self.prf = float(var)
        return

    def setRadarWavelength(self, var):
        self.radarWavelength = float(var)
        return

    def setMidpoint(self, var):
        self.midpoint = var
        return

    def setSch1(self, var):
        self.s1sch = var
        return

    def setSch2(self, var):
        self.s2sch = var
        return

    def setSc(self, var):
        self.sc = var
        return

    def setHeightSchFilename(self, var):
        self.heightSchFilename = var
    
    def setInterferogramFilename(self, var):
        self.intFilename = var
    
    def setTopophaseMphFilename(self, var):
        self.topophaseMphFilename = var
    
    def setTopophaseFlatFilename(self, var):
        self.topophaseFlatFilename = var

    def setHeightSchImageImage(self, img):
        self.heightSchImage = img

    def setInterferogramImage(self, img):
        self.intImage = img

    def setTopophaseMphImage(self, img):
        self.topophaseMphImage = img

    def setImageTopophaseFlat(self, img):
        self.topophaseFlatImage = img
    
    def allocateArrays(self):
        if self.dim1_referenceOrbit is None:
            self.dim1_referenceOrbit = len(self.referenceOrbit)

        if not self.dim1_referenceOrbit:
            print("Error. Trying to allocate zero size array")
            raise Exception

        correct.allocate_s_mocompArray_Py(self.dim1_referenceOrbit)

        if self.dim1_mocompBaseline is None:
            self.dim1_mocompBaseline = len(self.mocompBaseline)
            self.dim2_mocompBaseline = len(self.mocompBaseline[0])

        if (not self.dim1_mocompBaseline) or (not self.dim2_mocompBaseline):
            print("Error. Trying to allocate zero size array")
            raise Exception

        #Recompute length in azimuth to be the minimum of its current value
        #(set from the ifg length in the interferogram port) and the computed
        #maximum value it can have in correct.f to prevent array out of bounds
        #condition in accessing the mocompBaseline.
        self.length = min(self.length,
            int((self.dim1_mocompBaseline - self.isMocomp -
                 self.numberAzimuthLooks/2)/self.numberAzimuthLooks))
        print("Recomputed length = ", self.length)

        correct.allocate_mocbaseArray_Py(self.dim1_mocompBaseline,
                                         self.dim2_mocompBaseline)

        if self.dim1_midpoint is None:
            self.dim1_midpoint = len(self.midpoint)
            self.dim2_midpoint = len(self.midpoint[0])

        if (not self.dim1_midpoint) or (not self.dim2_midpoint):
            print("Error. Trying to allocate zero size array")
            raise Exception

        correct.allocate_midpoint_Py(self.dim1_midpoint, self.dim2_midpoint)

        if self.dim1_s1sch is None:
            self.dim1_s1sch = len(self.s1sch)
            self.dim2_s1sch = len(self.s1sch[0])

        if (not self.dim1_s1sch) or (not self.dim2_s1sch):
            print("Error. Trying to allocate zero size array")
            raise Exception

        correct.allocate_s1sch_Py(self.dim1_s1sch, self.dim2_s1sch)

        if self.dim1_s2sch is None:
            self.dim1_s2sch = len(self.s2sch)
            self.dim2_s2sch = len(self.s2sch[0])

        if (not self.dim1_s2sch) or (not self.dim2_s2sch):
            print("Error. Trying to allocate zero size array")
            raise Exception

        correct.allocate_s2sch_Py(self.dim1_s2sch, self.dim2_s2sch)

        if self.dim1_sc is None:
            self.dim1_sc = len(self.sc)
            self.dim2_sc = len(self.sc[0])

        if (not self.dim1_sc) or (not self.dim2_sc):
            print("Error. Trying to allocate zero size array")
            raise Exception

        correct.allocate_smsch_Py(self.dim1_sc, self.dim2_sc)

        correct.allocate_dopcoeff_Py(len(self.dopplerCentroidCoeffs))
        return

    def deallocateArrays(self):
        correct.deallocate_s_mocompArray_Py()
        correct.deallocate_mocbaseArray_Py()
        correct.deallocate_midpoint_Py()
        correct.deallocate_s1sch_Py()
        correct.deallocate_s2sch_Py()
        correct.deallocate_smsch_Py()
        correct.deallocate_dopcoeff_Py()
        return

    def addPeg(self):
        peg = self._inputPorts.getPort(name='peg').getObject()
        if (peg):            
            try:
                self.planetLocalRadius = peg.getRadiusOfCurvature()
                self.pegLatitude = math.radians(peg.getLatitude())
                self.pegLongitude = math.radians(peg.getLongitude())
                self.pegHeading = math.radians(peg.getHeading())
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError
    
    def addPlanet(self):
        planet = self._inputPorts.getPort(name='planet').getObject()
        if (planet):            
            try:
                ellipsoid = planet.get_elp()
                self.ellipsoidMajorSemiAxis = ellipsoid.get_a()
                self.ellipsoidEccentricitySquared = ellipsoid.get_e2()
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError
        
    def addFrame(self):
        frame = self._inputPorts.getPort(name='frame').getObject()
        if (frame):            
            try:
                #                self.rangeFirstSample = frame.getStartingRange() - Piyush
                instrument = frame.getInstrument()
                self.slantRangePixelSpacing = instrument.getRangePixelSize()
                self.prf = instrument.getPulseRepetitionFrequency()
                self.radarWavelength = instrument.getRadarWavelength()
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError

    def addMasterSlc(self):    #Piyush
        formslc = self._inputPorts.getPort(name='masterslc').getObject()
        if (formslc):
            try:
                self.rangeFirstSample = formslc.startingRange
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError

            self.dopplerCentroidCoeffs = formslc.dopplerCentroidCoefficients

    def addInterferogram(self):
        ifg = self._inputPorts.getPort(name='interferogram').getObject()
        if (ifg):
            try:
                self.intImage = ifg
                self.width = ifg.getWidth()
                self.length = ifg.getLength()
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError




    pass
