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
from iscesys.Component.Component import Component, Port
from isceobj import Constants as CN
from iscesys.Compatibility import Compatibility
import isceobj.Image as IF #load image factories
from stdproc.stdproc.topo import topo

class Topo(Component):

    ## South, North, West, East boundaries
    ## see geocode and topo to much resued code.
    @property
    def snwe(self):
        return (self.minimumLatitude,
                self.maximumLatitude,
                self.minimumLongitude,
                self.maximumLongitude)

    @snwe.setter
    def snwe(self, snwe):
        (self.minimumLatitude, self.maximumLatitude,
        self.minimumLongitude, self.maximumLongitude) = snwe


    def topo(self, demImage=None, intImage=None):
        for port in self._inputPorts:
            port()

        if demImage is not None:
            self.demImage = demImage
            
        #another way of passing width and length if not using the ports
        if intImage is not None:
            self.intImage = intImage
            #if width or length not defined get 'em  from intImage ince they 
            # are needed to create the output images
            if self.width is None:
                self.width = self.intImage.getWidth()
            if self.length is None:
                self.length = self.intImage.getLength()

        self.setDefaults() 
        self.createImages()
        #not all the quantities could be set before. now that we have the 
        # images set the remaining defaults if necessary (such as width, length)
        self.updateDefaults()

        self.squintshift = [0]*self.width #preallocate
        self.demAccessor = self.demImage.getImagePointer()
        self.latAccessor = self.latImage.getImagePointer()
        self.lonAccessor = self.lonImage.getImagePointer()
        self.heightRAccessor = self.heightRImage.getImagePointer()
        self.heightSchAccessor = self.heightSchImage.getImagePointer()
        self.losAccessor = self.losImage.getImagePointer()

        self.allocateArrays()
        self.setState()
        topo.topo_Py(self.demAccessor)
        self.getState()
        self.deallocateArrays()
        self.destroyImages()

        return None

    def setDefaults(self):
        if self.ellipsoidMajorSemiAxis is None:
            self.ellipsoidMajorSemiAxis = CN.EarthMajorSemiAxis

        if self.ellipsoidEccentricitySquared is None:
            self.ellipsoidEccentricitySquared = CN.EarthEccentricitySquared

        if self.isMocomp is None:
            self.isMocomp = (8192-2048)/2 
        
        if self.numberIterations is None:
            self.numberIterations = 25
        
        if self.heightRFilename == '':
            self.heightRFilename = 'z.rdr'
            self.logger.warning('The real height file has been given the default name %s' % (self.heightRFilename))
        if self.heightSchFilename == '':
            self.heightSchFilename = 'zsch.rdr'
            self.logger.warning('The sch height file has been given the default name %s' % (self.heightSchFilename))
        if self.latFilename == '':
            self.latFilename = 'lat.rdr'
            self.logger.warning('The latitude file has been given the default name %s' % (self.latFilename))
        if self.lonFilename == '':
            self.lonFilename = 'lon.rdr'
            self.logger.warning('The longitude file has been given the default name %s' % (self.lonFilename))
        if self.losFilename == '':
            self.losFilename = 'los.rdr'
            self.logger.warning('The los file has been given the default name %s' % (self.losFilename))

    def updateDefaults(self):
        if self.demLength is None:
            self.demLength = self.demImage.getLength()
        
        if self.demWidth is None:
            self.demWidth = self.demImage.getWidth()

    def destroyImages(self):
        self.latImage.addDescription('Pixel-by-pixel latitude in degrees.')
        self.latImage.renderHdr()
        self.latImage.finalizeImage()
        
        self.lonImage.addDescription('Pixel-by-pixel longitude in degrees.')
        self.lonImage.renderHdr()
        self.lonImage.finalizeImage()
        
        
        self.heightRImage.addDescription('Pixel-by-pixel height in meters.')
        self.heightRImage.renderHdr()
        self.heightRImage.finalizeImage()
        self.heightSchImage.addDescription('Pixel-by-pixel height above local sphere in meters.')
        self.heightSchImage.renderHdr()
        self.heightSchImage.finalizeImage()
        
        descr = '''Two channel Line-Of-Sight geometry image (all angles in degrees). Represents vector drawn from target to platform. 
                Channel 1: Incidence angle measured from vertical at target (always +ve).
                Channel 2: Azimuth angle measured from North in Anti-clockwise direction.'''
        self.losImage.setImageType('bil')
        self.losImage.addDescription(descr)
        self.losImage.renderHdr()
        self.losImage.finalizeImage()
    
        #finalizing of the images handled here
        self.demImage.finalizeImage()
        #self.intImage.finalizeImage()


    def createImages(self):
       
        #assume that even if an image is passed, the createImage and finalizeImage are called here
        if self.demImage is None and not self.demFilename == '':
            self.demImage = IF.createDemImage()
            demAccessMode = 'read'
            demWidth = self.demWidth
            self.demImage.initImage(self.demFilename,demAccessMode,demWidth)
        elif self.demImage is None:#this should never happen, atleast when using the  correct method. same for other images

            self.logger.error('Must either pass the demImage in the call or set self.demFilename.')
            raise Exception
        
        if(self.latImage == None and not self.latFilename == ''):
            self.latImage = IF.createImage()
            accessMode = 'write'
            dataType = 'FLOAT'
            width = self.width
            self.latImage.initImage(self.latFilename,accessMode,width,dataType)
        elif(self.latImage == None):
            self.logger.error('Must either pass the latImage in the call or set self.latFilename.')
            raise Exception
        
        if(self.lonImage == None and not self.lonFilename == ''):
            self.lonImage = IF.createImage()
            accessMode = 'write'
            dataType = 'FLOAT'
            width = self.width
            self.lonImage.initImage(self.lonFilename,accessMode,width,dataType)
        elif(self.lonImage == None):
            self.logger.error('Must either pass the lonImage in the call or set self.lonFilename.')
            raise Exception

        if(self.heightRImage == None and not self.heightRFilename == ''):
            self.heightRImage = IF.createImage()
            accessMode = 'write'
            dataType = 'FLOAT'
            width = self.width
            self.heightRImage.initImage(self.heightRFilename,accessMode,width,dataType)
        elif(self.heightRImage == None):
            self.logger.error('Must either pass the heightRImage in the call or set self.heightRFilename.')
            raise Exception
        
        if(self.heightSchImage == None and not self.heightSchFilename == ''):
            self.heightSchImage = IF.createImage()
            accessMode = 'write'
            dataType = 'FLOAT'
            width = self.width
            self.heightSchImage.initImage(self.heightSchFilename,accessMode,width,dataType)
        elif(self.heightSchImage == None):
            self.logger.error('Must either pass the heightSchImage in the call or set self.heightSchFilename.')
            raise Exception

        if(self.losImage == None and not self.losFilename == ''):
            self.losImage = IF.createImage()
            accessMode = 'write'
            dataType ='FLOAT'
            bands = 2
            scheme = 'BIL'
            width = self.width
            self.losImage.initImage(self.losFilename,accessMode,width,dataType,bands=bands,scheme=scheme)
        
        #self.intImage.createImage()
        #the dem image could have different datatype so create a caster here
        #the short is the data type used in the fortran. 
        self.demImage.setCaster('read','FLOAT')
        self.demImage.createImage()
        self.latImage.createImage()
        self.lonImage.createImage()
        self.heightRImage.createImage()
        self.heightSchImage.createImage()
        self.losImage.createImage()
    
    def setState(self):
        topo.setNumberIterations_Py(int(self.numberIterations))
        topo.setDemWidth_Py(int(self.demWidth))
        topo.setDemLength_Py(int(self.demLength))
        topo.setReferenceOrbit_Py(self.referenceOrbit, self.dim1_referenceOrbit)
        topo.setFirstLatitude_Py(float(self.firstLatitude))
        topo.setFirstLongitude_Py(float(self.firstLongitude))
        topo.setDeltaLatitude_Py(float(self.deltaLatitude))
        topo.setDeltaLongitude_Py(float(self.deltaLongitude))
        topo.setISMocomp_Py(int(self.isMocomp))
        topo.setEllipsoidMajorSemiAxis_Py(float(self.ellipsoidMajorSemiAxis))
        topo.setEllipsoidEccentricitySquared_Py(float(self.ellipsoidEccentricitySquared))
        topo.setLength_Py(int(self.length))
        topo.setWidth_Py(int(self.width))
        topo.setRangePixelSpacing_Py(float(self.slantRangePixelSpacing))
        topo.setRangeFirstSample_Py(float(self.rangeFirstSample))
        topo.setSpacecraftHeight_Py(float(self.spacecraftHeight))
        topo.setPlanetLocalRadius_Py(float(self.planetLocalRadius))
        topo.setBodyFixedVelocity_Py(float(self.bodyFixedVelocity))
        topo.setNumberRangeLooks_Py(int(self.numberRangeLooks))
        topo.setNumberAzimuthLooks_Py(int(self.numberAzimuthLooks))
        topo.setPegLatitude_Py(float(self.pegLatitude))
        topo.setPegLongitude_Py(float(self.pegLongitude))
        topo.setPegHeading_Py(float(self.pegHeading))
        topo.setDopplerCentroidConstantTerm_Py(float(self.dopplerCentroidConstantTerm))
        topo.setPRF_Py(float(self.prf))
        topo.setRadarWavelength_Py(float(self.radarWavelength))
        topo.setLatitudePointer_Py(int(self.latAccessor))
        topo.setLongitudePointer_Py(int(self.lonAccessor))
        topo.setHeightRPointer_Py(int(self.heightRAccessor))
        topo.setHeightSchPointer_Py(int(self.heightSchAccessor))
        topo.setLosPointer_Py(int(self.losAccessor))
        topo.setLookSide_Py(int(self.lookSide))

        return None


    def setNumberIterations(self,var):
        self.numberIterations = int(var)
        return None

    def setDemWidth(self,var):
        self.demWidth = int(var)
        return None

    def setDemLength(self,var):
        self.demLength = int(var)
        return None

    def setReferenceOrbit(self,var):
        self.referenceOrbit = var
        return None

    def setFirstLatitude(self,var):
        self.firstLatitude = float(var)
        return None

    def setFirstLongitude(self,var):
        self.firstLongitude = float(var)
        return None

    def setDeltaLatitude(self,var):
        self.deltaLatitude = float(var)
        return None

    def setDeltaLongitude(self,var):
        self.deltaLongitude = float(var)
        return None

    def setISMocomp(self,var):
        self.isMocomp = int(var)
        return None

    def setEllipsoidMajorSemiAxis(self,var):
        self.ellipsoidMajorSemiAxis = float(var)
        return None

    def setEllipsoidEccentricitySquared(self,var):
        self.ellipsoidEccentricitySquared = float(var)
        return None

    def setLength(self,var):
        self.length = int(var)
        return None

    def setWidth(self,var):
        self.width = int(var)
        return None

    def setRangePixelSpacing(self,var):
        self.slantRangePixelSpacing = float(var)
        return None

    def setRangeFirstSample(self,var):
        self.rangeFirstSample = float(var)
        return None

    def setSpacecraftHeight(self,var):
        self.spacecraftHeight = float(var)
        return None

    def setPlanetLocalRadius(self,var):
        self.planetLocalRadius = float(var)
        return None

    def setBodyFixedVelocity(self,var):
        self.bodyFixedVelocity = float(var)
        return None

    def setNumberRangeLooks(self,var):
        self.numberRangeLooks = int(var)
        return None

    def setNumberAzimuthLooks(self,var):
        self.numberAzimuthLooks = int(var)
        return None

    def setPegLatitude(self,var):
        self.pegLatitude = float(var)
        return None

    def setPegLongitude(self,var):
        self.pegLongitude = float(var)
        return None

    def setPegHeading(self,var):
        self.pegHeading = float(var)
        return None

    def setDopplerCentroidConstantTerm(self,var):
        self.dopplerCentroidConstantTerm = float(var)
        return None

    def setPRF(self,var):
        self.prf = float(var)
        return None

    def setRadarWavelength(self,var):
        self.radarWavelength = float(var)
        return None

    def setLosFilename(self,var):
        self.losFilename = var
        return None
    
    def setLatFilename(self,var):
        self.latFilename = var
        return None

    def setLonFilename(self,var):
        self.lonFilename = var
        return None

    def setHeightRFilename(self,var):
        self.heightRFilename = var
        return None

    def setHeightSchFilename(self,var):
        self.heightSchFilename = var
        return None

    def setLookSide(self,var):
        self.lookSide = int(var)
        return None

    def getState(self):
        self.azimuthSpacing = topo.getAzimuthSpacing_Py()
        self.planetLocalRadius = topo.getPlanetLocalRadius_Py()
        self.sCoordinateFirstLine = topo.getSCoordinateFirstLine_Py()
        self.sCoordinateLastLine = topo.getSCoordinateLastLine_Py()
        self.minimumLatitude = topo.getMinimumLatitude_Py()
        self.minimumLongitude = topo.getMinimumLongitude_Py()
        self.maximumLatitude = topo.getMaximumLatitude_Py()
        self.maximumLongitude = topo.getMaximumLongitude_Py()
        self.squintshift = topo.getSquintShift_Py(self.dim1_squintshift)
        self.length = topo.getLength_Py()

        return None

    def getAzimuthSpacing(self):
        return self.azimuthSpacing

    def getPlanetLocalRadius(self):
        return self.planetLocalRadius

    def getSCoordinateFirstLine(self):
        return self.sCoordinateFirstLine

    def getSCoordinateLastLine(self):
        return self.sCoordinateLastLine

    def getMinimumLatitude(self):
        return self.minimumLatitude

    def getMinimumLongitude(self):
        return self.minimumLongitude

    def getMaximumLatitude(self):
        return self.maximumLatitude

    def getMaximumLongitude(self):
        return self.maximumLongitude

    def getSquintShift(self):
        return self.squintshift

    def allocateArrays(self):
        if (self.dim1_referenceOrbit == None):
            self.dim1_referenceOrbit = len(self.referenceOrbit)

        if (not self.dim1_referenceOrbit):
            print("Error. Trying to allocate zero size array")

            raise Exception

        topo.allocate_s_mocompArray_Py(self.dim1_referenceOrbit)

        if (self.dim1_squintshift == None):
            self.dim1_squintshift = len(self.squintshift)

        if (not self.dim1_squintshift):
            print("Error. Trying to allocate zero size array")

            raise Exception

        topo.allocate_squintshift_Py(self.dim1_squintshift)

        return None

    def deallocateArrays(self):
        topo.deallocate_s_mocompArray_Py()
        topo.deallocate_squintshift_Py()
        return None

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
                #self.rangeFirstSample = frame.getStartingRange() - Piyush
                instrument = frame.getInstrument()
                self.slantRangePixelSpacing = instrument.getRangePixelSize()
                self.prf = instrument.getPulseRepetitionFrequency()
                self.radarWavelength = instrument.getRadarWavelength()
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError

    def addMasterSlc(self):     #Piyush
        formslc = self._inputPorts.getPort(name='masterslc').getObject()

        if (formslc):
            try:
                self.rangeFirstSample = formslc.startingRange
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError
            
    def addDEM(self):
        dem = self._inputPorts.getPort(name='dem').getObject()
        if (dem):
            try:
                self.demImage = dem
                self.demWidth = dem.getWidth()
                self.demLength = dem.getLength()
                self.firstLatitude = dem.getFirstLatitude()
                self.firstLongitude = dem.getFirstLongitude()
                self.deltaLatitude = dem.getDeltaLatitude()
                self.deltaLongitude = dem.getDeltaLongitude()
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError

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

    logging_name = "isce.stdproc.topo"

    def __init__(self):
        super(Topo, self).__init__()
        self.numberIterations = None
        self.demWidth = None
        self.demLength = None
        self.referenceOrbit = []
        self.dim1_referenceOrbit = None
        self.firstLatitude = None
        self.firstLongitude = None
        self.deltaLatitude = None
        self.deltaLongitude = None
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
        self.dopplerCentroidConstantTerm = None
        self.prf = None
        self.radarWavelength = None
        self.demFilename = ''
        self.latFilename = ''
        self.lonFilename = ''
        self.heightRFilename = ''
        self.heightSchFilename = ''
        self.losFilename = ''
        self.demImage = None
        self.latImage = None
        self.lonImage = None
        self.heightRImage = None
        self.heightSchImage = None
        self.losImage = None
        self.demAccessor = None
        self.latAccessor = None
        self.lonAccessor = None
        self.heightRAccessor = None
        self.heightSchAccessor = None
        self.losAccessor = None
        self.azimuthSpacing = None
        self.sCoordinateFirstLine = None
        self.sCoordinateLastLine = None
        self.minimumLatitude = None
        self.minimumLongitude = None
        self.maximumLatitude = None
        self.maximumLongitude = None
        self.squintshift = []
        self.dim1_squintshift = None
        self.lookSide = -1     #Default set to right side
        self.dictionaryOfVariables = { 
            'NUMBER_ITERATIONS' : ['numberIterations', 'int','optional'], 
            'DEM_WIDTH' : ['demWidth', 'int','mandatory'], 
            'DEM_LENGTH' : ['demLength', 'int','mandatory'], 
            'REFERENCE_ORBIT' : ['referenceOrbit', 'float','mandatory'], 
            'FIRST_LATITUDE' : ['firstLatitude', 'float','mandatory'], 
            'FIRST_LONGITUDE' : ['firstLongitude', 'float','mandatory'], 
            'DELTA_LATITUDE' : ['deltaLatitude', 'float','mandatory'], 
            'DELTA_LONGITUDE' : ['deltaLongitude', 'float','mandatory'], 
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
            'DOPPLER_CENTROID_CONSTANT_TERM' : ['dopplerCentroidConstantTerm', 'float','mandatory'], 
            'PRF' : ['prf', 'float','mandatory'], 
            'RADAR_WAVELENGTH' : ['radarWavelength', 'float','mandatory'], 
            'LAT_ACCESSOR' : ['latAccessor', 'int','optional'], 
            'LON_ACCESSOR' : ['lonAccessor', 'int','optional'], 
            'HEIGHT_R_ACCESSOR' : ['heightRAccessor', 'int','optional'], 
            'HEIGHT_SCH_ACCESSOR' : ['heightSchAccessor', 'int','optional'] 
            }
        self.dictionaryOfOutputVariables = { 
            'AZIMUTH_SPACING' : 'azimuthSpacing', 
            'PLANET_LOCAL_RADIUS' : 'planetLocalRadius', 
            'S_COORDINATE_FIRST_LINE' : 'sCoordinateFirstLine', 
            'S_COORDINATE_LAST_LINE' : 'sCoordinateLastLine', 
            'MINIMUM_LATITUDE' : 'minimumLatitude', 
            'MINIMUM_LONGITUDE' : 'minimumLongitude', 
            'MAXIMUM_LATITUDE' : 'maximumLatitude', 
            'MAXIMUM_LONGITUDE' : 'maximumLongitude', 
            'SQUINT_SHIFT' : 'squintshift' 
            }
        self.descriptionOfVariables = {}
        self.mandatoryVariables = []
        self.optionalVariables = []
        self.initOptionalAndMandatoryLists()
        return None
    
    def createPorts(self):
        self.inputPorts['peg'] = self.addPeg
        self.inputPorts['frame'] = self.addFrame
        self.inputPorts['planet'] = self.addPlanet
        self.inputPorts['dem'] = self.addDEM
        self.inputPorts['interferogram'] = self.addInterferogram
        slcPort = Port(name='masterslc', method=self.addMasterSlc)  #Piyush
        self.inputPorts.add(slcPort)     #Piyush
        return None



    pass



