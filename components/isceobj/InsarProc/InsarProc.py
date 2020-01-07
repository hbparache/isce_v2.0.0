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
import os
import logging
import logging.config
from iscesys.Component.Component import Component
from iscesys.DateTimeUtil.DateTimeUtil import DateTimeUtil as DTU
from iscesys.Compatibility import Compatibility
from isceobj.Scene.Frame import FrameMixin

## Master Slave Hash Table
MASTER_SLAVE = {0:'master', 1:'slave', 'master':'master', 'slave':'slave'}

RESAMP_IMAGE_NAME_BASE = Component.Parameter('_resampImageName',
    public_name='resamp image name base',
    default='resampImage',
    type='str',
    mandatory=False,
    doc=('Base name for output interferogram and amplitude files, '+
         'with fixed extensions .int and .amp added')
)

class InsarProc(Component, FrameMixin):
    """
    This class holds the properties, along with methods (setters and getters)
    to modify and return their values.
    """

    parameter_list = (RESAMP_IMAGE_NAME_BASE,)

    _masterFrame = None
    _slaveFrame = None
    _masterOrbit = None
    _slaveOrbit = None
    _masterDoppler = None
    _slaveDoppler = None
    _peg = None
    _pegH1 = None
    _pegH2 = None
    _fdH1 = None
    _fdH2 = None
    _pegV1 = None
    _pegV2 = None
    is_mocomp = None
    _masterRawImage = None
    _slaveRawImage = None
    _masterSlcImage = None
    _slaveSlcImage = None
    _offsetAzimuthImage = None
    _offsetRangeImage = None
    _resampAmpImage = None
    _resampIntImage = None
    _resampOnlyImage = None
    _resampOnlyAmp = None
    _topoIntImage = None
    _heightTopoImage = None
    _rgImageName = 'rgImage'
    _rgImage = None
    _simAmpImageName = 'simamp.rdr'
    _simAmpImage = None
#    _resampImageName = 'resampImage'
    _resampOnlyImageName = 'resampOnlyImage.int'
    _offsetImageName = 'Offset.mht'
    _demImage = None
    _demInitFile =  'DemImage.xml'
    _firstSampleAcrossPrf = 50
    _firstSampleDownPrf = 50
    _numberLocationAcrossPrf = 40
    _numberLocationDownPrf = 50
    _numberRangeBins = None
    _firstSampleAcross = 50
    _firstSampleDown = 50
    _numberLocationAcross = 40
    _numberLocationDown = 40
    _topocorrectFlatImage = None
    _offsetField = None
    _refinedOffsetField = None
    _offsetField1 = None
    _refinedOffsetField1 = None
    _topophaseIterations = 25
    _coherenceFilename = 'topophase.cor'
    _unwrappedIntFilename = 'filt_topophase.unw'
    _phsigFilename = 'phsig.cor'
    _topophaseMphFilename = 'topophase.mph'
    _topophaseFlatFilename = 'topophase.flat'
    _filt_topophaseFlatFilename = 'filt_' + _topophaseFlatFilename
    _heightFilename = 'z.rdr'
    _heightSchFilename = 'zsch.rdr'
    _geocodeFilename = 'topophase.geo'
    _losFilename = 'los.rdr'
    _latFilename = 'lat.rdr'
    _lonFilename = 'lon.rdr'
    _demCropFilename = 'dem.crop'
    # The strength of the Goldstein-Werner filter
    _filterStrength = 0.7
    # This is hard-coded from the original script
    _numberValidPulses = 2048
    _numberPatches = None
    _patchSize = 8192
    _machineEndianness = 'l'
    _secondaryRangeMigrationFlag = None
    _chirpExtension = 0
    _slantRangePixelSpacing = None
    _dopplerCentroid = None
    _posting = 15
    _numberFitCoefficients = 6
    _numberLooks = 4
    _numberAzimuthLooks = 1
    _numberRangeLooks = None
    _numberResampLines = None
    _shadeFactor = 3
    _processingDirectory = None
    _checkPointer =  None
    _formSLC1 = None
    _formSLC2 = None
    _mocompBaseline = None
    _topocorrect = None
    _topo = None
    _masterSquint = 0
    _slaveSquint = 0
    _lookSide = -1    #Right looking by default.
    _geocode_list = [
                        _coherenceFilename,
                        _unwrappedIntFilename,
                        _phsigFilename,
                        _losFilename,
                        _topophaseFlatFilename,
                        _filt_topophaseFlatFilename,
                        _resampOnlyImageName.replace('.int', '.amp')
                       ]

    family='insarProc_conf'

    def __init__(self, name='', procDoc=None):
        self.name = name
        super(InsarProc, self).__init__(family=self.__class__.family,
            name=name)
        self.configure()
        self.procDoc = procDoc
        self._workingDirectory = os.getcwd()
        self._dataDirectory = os.getcwd()
        return None

    def get_is_mocomp(self):
        self.is_mocomp =  int((
                self.getPatchSize() - self.getNumberValidPulses()
                )/2)
        return self.is_mocomp

    # Getters

    def getLookSide(self):
        return self._lookSide

    def getMasterSquint(self):
        return self._masterSquint

    def getSlaveSquint(self):
        return self._slaveSquint

    def getFormSLC1(self):
        return self._formSLC1

    def getFormSLC2(self):
        return self._formSLC2

    def getMocompBaseline(self):
        return self._mocompBaseline

    def getTopocorrect(self):
        return self._topocorrect

    def getTopo(self):
        return self._topo

    ## to be deprecated
    def getAverageHeight(self):
        return self.averageHeight
    @property
    def averageHeight(self):
        return (self._pegH1 + self._pegH2)/2.0

    def getFirstAverageHeight(self):
        return self._pegH1

    def getSecondAverageHeight(self):
        return self._pegH2

    def getFirstFdHeight(self):
        return self._fdH1

    def getSecondFdHeight(self):
        return self._fdH2

    ## deprecate ASAP
    def getProcVelocity(self):
        return self.procVelocity
    @property
    def procVelocity(self):
        return (self._pegV1 + self._pegV2)/2.0

    # <v>, <h>
    def vh(self):
        return self.procVelocity, self.averageHeight

    def getFirstProcVelocity(self):
        return self._pegV1

    def getSecondProcVelocity(self):
        return self._pegV2

    def getMasterFrame(self):
        return self._masterFrame

    def getSlaveFrame(self):
        return self._slaveFrame

    def getMasterOrbit(self):
        return self._masterOrbit

    def getSlaveOrbit(self):
        return self._slaveOrbit

    def getMasterDoppler(self):
        return self._masterDoppler

    def getSlaveDoppler(self):
        return self._slaveDoppler

    def getPeg(self):
        return self._peg

    def getMasterRawImage(self):
        return self._masterRawImage

    def getSlaveRawImage(self):
        return self._slaveRawImage

    def getMasterSlcImage(self):
        return self._masterSlcImage

    def getSlaveSlcImage(self):
        return self._slaveSlcImage

    def getSimAmpImage(self):
        return self._simAmpImage

    def getRgImage(self):
        return self._rgImage

    def getResampAmpImage(self):
        return self._resampAmpImage

    def getResampIntImage(self):
        return self._resampIntImage

    def getResampOnlyImage(self):
        return self._resampOnlyImage

    def getResampOnlyAmp(self):
        return self._resampOnlyAmp

    def getTopoIntImage(self):
        return self._topoIntImage

    def getHeightTopoImage(self):
        return self._heightTopoImage

    def getOffsetAzimuthImage(self):
        return self._offsetAzimuthImage

    def getOffsetRangeImage(self):
        return self._offsetRangeImage

    def getSLC1ImageName(self):
        return self._slc1ImageName

    def getSLC2ImageName(self):
        return self._slc2ImageName

    def getSimAmpImageName(self):
        return self._simAmpImageName

    def getRgImageName(self):
        return self._rgImageName

    def getDemInitFile(self):
        return self._demInitFile

    def getDemImage(self):
        return self._demImage

    def getOffsetImageName(self):
        return self._offsetImageName

    def getResampImageName(self):
        return self._resampImageName

    def getResampOnlyImageName(self):
        return self._resampOnlyImageName
    def getTopocorrectFlatImage(self):
        return self._topocorrectFlatImage

    def getFirstSampleAcrossPrf(self):
        return self._firstSampleAcrossPrf

    def getFirstSampleDownPrf(self):
        return self._firstSampleDownPrf

    def getNumberRangeBins(self):
        return self._numberRangeBins

    def getNumberLocationAcrossPrf(self):
        return self._numberLocationAcrossPrf

    def getNumberLocationDownPrf(self):
        return self._numberLocationDownPrf

    def getFirstSampleAcross(self):
        return self._firstSampleAcross

    def getFirstSampleDown(self):
        return self._firstSampleDown

    def getNumberLocationAcross(self):
        return self._numberLocationAcross

    def getNumberLocationDown(self):
        return self._numberLocationDown

    def getOffsetField(self):
        return self._offsetField

    def getRefinedOffsetField(self):
        return self._refinedOffsetField

    def getOffsetField1(self):
        return self._offsetField1

    def getRefinedOffsetField1(self):
        return self._refinedOffsetField1

    def getNumberValidPulses(self):
        return self._numberValidPulses

    def getNumberPatches(self):
        return self._numberPatches

    def getPatchSize(self):
        return self._patchSize

    def getMachineEndianness(self):
        return self._machineEndianness

    def getSecondaryRangeMigrationFlag(self):
        return self._secondaryRangeMigrationFlag

    def getChirpExtension(self):
        return self._chirpExtension

    def getSlantRangePixelSpacing(self):
        return self._slantRangePixelSpacing

    def getDopplerCentroid(self):
        return self._dopplerCentroid

    def getPosting(self):
        return self._posting

    def getNumberFitCoefficients(self):
        return self._numberFitCoefficients

    def getNumberLooks(self):
        return self._numberLooks

    def getNumberAzimuthLooks(self):
        return self._numberAzimuthLooks

    def getNumberRangeLooks(self):
        return self._numberRangeLooks

    def getNumberResampLines(self):
        return self._numberResampLines

    def getShadeFactor(self):
        return self._shadeFactor

    def getTopophaseFlatFilename(self):
        return self._topophaseFlatFilename

    def getFiltTopophaseFlatFilename(self):
        return self._filt_topophaseFlatFilename

    def getCoherenceFilename(self):
        return self._coherenceFilename

    def getUnwrappedIntFilename(self):
        return self._unwrappedIntFilename

    def getPhsigFilename(self):
        return self._phsigFilename

    def getTopophaseMphFilename(self):
        return self._topophaseMphFilename

    def getHeightFilename(self):
        return self._heightFilename

    def getHeightSchFilename(self):
        return self._heightSchFilename

    def getGeocodeFilename(self):
        return self._geocodeFilename

    def getLosFilename(self):
        return self._losFilename

    def getLatFilename(self):
        return self._latFilename

    def getLonFilename(self):
        return self._lonFilename

    def getDemCropFilename(self):
        return self._demCropFilename

    def getTopophaseIterations(self):
        return self._topophaseIterations

    def getProcessingDirectory(self):
        return self._processingDirectory

    def getWorkingDirectory(self):
        return self._workingDirectory

    def getDataDirectory(self):
        return self._dataDirectory

    def getFilterStrength(self):
        return self._filterStrength

    def getCheckPointer(self):
        return self._checkPointer

    def getGeocodeList(self):
        return self._geocode_list

    # Setters
    def setLookSide(self, lookSide):
        self._lookSide = lookSide

    def setMasterSquint(self, squint):
        self._masterSquint = squint

    def setSlaveSquint(self, squint):
        self._slaveSquint = squint

    def setFormSLC1(self, fslc):
        self._formSLC1 = fslc

    def setFormSLC2(self, fslc):
        self._formSLC2 = fslc

    def setMocompBaseline(self, mocompbl):
        self._mocompBaseline = mocompbl

    def setTopo(self, topo):
        self._topo = topo

    def setTopocorrect(self, topo):
        self._topocorrect = topo

    def setFirstAverageHeight(self, h1):
        self._pegH1 = h1

    def setSecondAverageHeight(self, h2):
        self._pegH2 = h2

    def setFirstFdHeight(self, h1):
        self._fdH1 = h1

    def setSecondFdHeight(self, h2):
        self._fdH2 = h2

    def setFirstProcVelocity(self, v1):
        self._pegV1 = v1

    def setSecondProcVelocity(self, v2):
        self._pegV2 = v2


    def setMasterFrame(self, frame):
        self._masterFrame = frame

    def setSlaveFrame(self, frame):
        self._slaveFrame = frame

    def setMasterOrbit(self, orbit):
        self._masterOrbit = orbit

    def setSlaveOrbit(self, orbit):
        self._slaveOrbit = orbit

    def setMasterDoppler(self, doppler):
        self._masterDoppler = doppler

    def setSlaveDoppler(self, doppler):
        self._slaveDoppler = doppler

    def setPeg(self, peg):
        self._peg = peg

    def setMasterRawImage(self, image):
        self._masterRawImage = image

    def setSlaveRawImage(self, image):
        self._slaveRawImage = image

    def setMasterSlcImage(self, image):
        self._masterSlcImage = image

    def setSlaveSlcImage(self, image):
        self._slaveSlcImage = image

    def setSimAmpImage(self, image):
        self._simAmpImage = image

    def setRgImage(self, image):
        self._rgImage = image

    def setOffsetAzimuthImage(self, image):
        self._offsetAzimuthImage = image

    def setOffsetRangeImage(self, image):
        self._offsetRangeImage = image

    def setResampAmpImage(self, image):
        self._resampAmpImage = image

    def setResampIntImage(self, image):
        self._resampIntImage = image

    def setResampOnlyImage(self, image):
        self._resampOnlyImage = image

    def setResampOnlyAmp(self, image):
        self._resampOnlyAmp = image

    def setTopoIntImage(self, image):
        self._topoIntImage = image

    def setHeightTopoImage(self, image):
        self._heightTopoImage = image

    def setSimAmpImageName(self, name):
        self._simAmpImageName = name

    def setSLC1ImageName(self, name):
        self._slc1ImageName = name

    def setSLC2ImageName(self, name):
        self._slc2ImageName = name

    def setRgImageName(self, name):
        self._rgImageName = name

    def setOffsetImageName(self, name):
        self._offsetImageName = name

    def setResampImageName(self, name):
        self._resampImageName = name

    def setResampOnlyImageName(self, name):
        self._resampOnlyImageName = name

    def setDemImage(self, image):
        self._demImage = image

    def setDemInitFile(self, init):
        self._demInitFile = init

    def setTopocorrectFlatImage(self, image):
        self._topocorrectFlatImage = image

    def setFirstSampleAcrossPrf(self, x):
        self._firstSampleAcrossPrf = x

    def setFirstSampleDownPrf(self, x):
        self._firstSampleDownPrf = x

    def setNumberRangeBins(self, x):
        self._numberRangeBins = x

    def setNumberLocationAcrossPrf(self, x):
        self._numberLocationAcrossPrf = x

    def setNumberLocationDownPrf(self, x):
        self._numberLocationDownPrf = x

    def setFirstSampleAcross(self, x):
        self._firstSampleAcross = x

    def setFirstSampleDown(self, x):
        self._firstSampleDown = x

    def setNumberLocationAcross(self, x):
        self._numberLocationAcross = x

    def setNumberLocationDown(self, x):
        self._numberLocationDown = x

    def setOffsetField(self, offsets):
        self._offsetField = offsets

    def setRefinedOffsetField(self, offsets):
        self._refinedOffsetField = offsets

    def setOffsetField1(self, offsets):
        self._offsetField1 = offsets

    def setRefinedOffsetField1(self, offsets):
        self._refinedOffsetField1 = offsets


    def setNumberValidPulses(self, x):
        self._numberValidPulses = x

    def setNumberPatches(self, x):
        self._numberPatches = x

    def setPatchSize(self, x):
        self._patchSize = x

    def setMachineEndianness(self, x):
        self._machineEndianness = x

    def setSecondaryRangeMigrationFlag(self, yorn):
        """Should be 'y' or 'n'"""
        self._secondaryRangeMigrationFlag = yorn

    def setChirpExtension(self, ext):
        """Should probably be a percentage rather than value"""
        self._chirpExtension = int(ext)
        return None

    @property
    def chirpExtensionPercentage(self):
        return NotImplemented
    @chirpExtensionPercentage.setter
    def chirpExtensionPercentage(self, value):
        raise AttributeError("Can only set chirpExtension")

    def setSlantRangePixelSpacing(self, x):
        self._slantRangePixelSpacing = x

    def setDopplerCentroid(self, x):
        self._dopplerCentroid = x

    def setPosting(self, x):
        self._posting = x

    def setNumberFitCoefficients(self, x):
        self._numberFitCoefficients = x

    def setNumberLooks(self, x):
        self._numberLooks = int(x)

    def setNumberAzimuthLooks(self, x):
        self._numberAzimuthLooks = int(x)

    def setNumberRangeLooks(self, x):
        self._numberRangeLooks = int(x)

    def setNumberResampLines(self, x):
        self._numberResampLines = int(x)

    def setShadeFactor(self, x):
        self._shadeFactor = x

    def setTopophaseFlatFilename(self, filename):
        self._topophaseFlatFilename = filename

    def setFiltTopophaseFlatFilename(self, filename):
        self._filt_topophaseFlatFilename = filename

    def setCoherenceFilename(self, filename):
        self._coherenceFilename = filename

    def setUnwrappedIntFilename(self, filename):
        self._unwrappedIntFilename = filename

    def setPhsigFilename(self, filename):
        self._phsigFilename = filename

    def setTopophaseMphFilename(self, filename):
        self._topophaseMphFilename = filename

    def setHeightFilename(self, filename):
        self._heightFilename = filename

    def setHeightSchFilename(self, filename):
        self._heightSchFilename = filename

    def setGeocodeFilename(self, filename):
        self._geocodeFilename = filename

    def setLosFilename(self, filename):
        self._losFilename = filename

    def setLatFilename(self, filename):
        self._latFilename = filename

    def setLonFilename(self, filename):
        self._lonFilename = filename

    def setDemCropFilename(self, filename):
        self._demCropFilename = filename

    def setTopophaseIterations(self, iter):
        self._topophaseIterations = iter

    def setProcessingDirectory(self, pdir):
        self._processingDirectory = pdir

    def setWorkingDirectory(self, wdir):
        self._workingDirectory = wdir

    def setDataDirectory(self, ddir):
        self._dataDirectory = ddir

    def setFilterStrength(self, alpha):
        self._filterStrength = alpha

    def setCheckPointer(self, cp):
        self._checkPointer = cp

    def setGeocodeList(self,prd):
        self._geocode_list = prd

    ## folowing are tbd to split formSLC.
    def _hasher(self, index, Attr):
        return getattr(self, MASTER_SLAVE[index] + Attr)

    def select_frame(self, index): return self._hasher(index, 'Frame')
    def select_orbit(self, index): return self._hasher(index, 'Orbit')
    def select_doppler(self, index): return self._hasher(index, 'Doppler')
    def select_rawimage(self, index): return self._hasher(index, 'RawImage')
    def select_slcimage(self, index): return self._hasher(index, 'SlcImage')
    def select_squint(self, index): return self._hasher(index, 'SquintImage')

    def iter_orbits(self):
        return (self.select_orbit(n) for n in range(2))

    def select_swath(self, index):
        return RadarSwath(frame=self.select_frame(index),
                          orbit=self.select_orbit(index),
                          doppler=self.select_doppler(index),
                          rawimage=self.select_rawimage(index),
                          slcimage=self.select_slcimage(index),
                          squint=self.select_squint(index))

    ## This overides the _FrameMixin.frame
    @property
    def frame(self):
        return self.masterFrame

    # Some line violate PEP008 in order to facilitate using "grep"
    # for development
    refinedOffsetField = property(getRefinedOffsetField, setRefinedOffsetField)
    offsetField = property(getOffsetField, setOffsetField)
    demCropFilename = property(getDemCropFilename, setDemCropFilename)
    masterFrame = property(getMasterFrame, setMasterFrame)
    slaveFrame = property(getSlaveFrame, setSlaveFrame)
    masterOrbit = property(getMasterOrbit, setMasterOrbit)
    slaveOrbit = property(getSlaveOrbit, setSlaveOrbit)
    masterDoppler = property(getMasterDoppler, setMasterDoppler)
    slaveDoppler = property(getSlaveDoppler, setSlaveDoppler)
    peg = property(getPeg, setPeg)
    pegH1 = property(getFirstAverageHeight, setFirstAverageHeight)
    pegH2 = property(getSecondAverageHeight, setSecondAverageHeight)
    fdH1 = property(getFirstFdHeight, setFirstFdHeight)
    fdH2 = property(getSecondFdHeight, setSecondFdHeight)
    pegV1 = property(getFirstProcVelocity, setFirstProcVelocity)
    pegV2 = property(getSecondProcVelocity, setSecondProcVelocity)
    masterRawImage = property(getMasterRawImage, setMasterRawImage)
    slaveRawImage = property(getSlaveRawImage, setSlaveRawImage)
    masterSlcImage = property(getMasterSlcImage, setMasterSlcImage)
    slaveSlcImage = property(getSlaveSlcImage, setSlaveSlcImage)
    simAmpImage = property(getSimAmpImage, setSimAmpImage)
    demImage = property(getDemImage, setDemImage)
    demInitFile = property(getDemInitFile, setDemInitFile)
    rgImage = property(getRgImage, setRgImage)
    topocorrectFlatImage = property(getTopocorrectFlatImage, setTopocorrectFlatImage)
    resampAmpImage = property(getResampAmpImage, setResampAmpImage)
    resampIntImage = property(getResampIntImage, setResampIntImage)
    resampOnlyImage = property(getResampOnlyImage, setResampOnlyImage)
    topoIntImage = property(getTopoIntImage, setTopoIntImage)
    heightTopoImage = property(getHeightTopoImage, setHeightTopoImage)
    offsetAzimuthImage = property(getOffsetAzimuthImage, setOffsetAzimuthImage)
    offsetRangeImage = property(getOffsetRangeImage, setOffsetRangeImage)
    slc1ImageName = property(getSLC1ImageName, setSLC1ImageName)
    slc2ImageName = property(getSLC2ImageName, setSLC2ImageName)
    rgImageName = property(getRgImageName, setRgImageName)
    resampOnlyImageName = property(getResampOnlyImageName, setResampOnlyImageName)
    resampImageName = property(getResampImageName, setResampImageName)
    offsetImageName = property(getOffsetImageName, setOffsetImageName)
    chirpExtension = property(getChirpExtension, setChirpExtension)
    firstSampleAcrossPrf = property(getFirstSampleAcrossPrf, setFirstSampleAcrossPrf)
    firstSampleDownPrf = property(getFirstSampleDownPrf, setFirstSampleDownPrf)
    numberLocationAcrossPrf = property(getNumberLocationAcrossPrf, setNumberLocationAcrossPrf)
    numberLocationDownPrf = property(getNumberLocationDownPrf, setNumberLocationDownPrf)
    firstSampleAcross = property(getFirstSampleAcross, setFirstSampleAcross)
    firstSampleDown = property(getFirstSampleDown, setFirstSampleDown)
    numberLocationAcross = property(getNumberLocationAcross, setNumberLocationAcross)
    numberLocationDown = property(getNumberLocationDown, setNumberLocationDown)
    numberAzimuthLooks = property(getNumberAzimuthLooks, setNumberAzimuthLooks)
    numberValidPulses = property(getNumberValidPulses, setNumberValidPulses)
    numberPatches = property(getNumberPatches, setNumberPatches)
    patchSize = property(getPatchSize, setPatchSize)
    machineEndianness = property(getMachineEndianness, setMachineEndianness)
    secondaryRangeMigrationFlag = property(getSecondaryRangeMigrationFlag, setSecondaryRangeMigrationFlag)
    coherenceFilename = property(getCoherenceFilename, setCoherenceFilename)
    unwrappedIntFilename = property(getUnwrappedIntFilename, setUnwrappedIntFilename)
    phsigFilename = property(getPhsigFilename, setPhsigFilename)
    topophaseMphFilename = property(getTopophaseMphFilename, setTopophaseMphFilename)
    topophaseFlatFilename = property(getTopophaseFlatFilename, setTopophaseFlatFilename)
    filt_topophaseFlatFilename = property(getFiltTopophaseFlatFilename, setFiltTopophaseFlatFilename)
    heightFilename = property(getHeightFilename, setHeightFilename)
    heightSchFilename = property(getHeightSchFilename, setHeightSchFilename)
    geocodeFilename = property(getGeocodeFilename, setGeocodeFilename)
    losFilename = property(getLosFilename, setLosFilename)
    latFilename = property(getLatFilename, setLatFilename)
    lonFilename = property(getLonFilename, setLonFilename)
    topophaseIterations = property(getTopophaseIterations, setTopophaseIterations)
    slantRangePixelSpacing = property(getSlantRangePixelSpacing, setSlantRangePixelSpacing)
    dopplerCentroid = property(getDopplerCentroid, setDopplerCentroid)
    posting = property(getPosting, setPosting)
    numberLooks = property(getNumberLooks, setNumberLooks)
    numberFitCoefficients = property(getNumberFitCoefficients, setNumberFitCoefficients)
    numberAzimuthLooks = property(getNumberAzimuthLooks, setNumberAzimuthLooks)
    numberRangeLooks = property(getNumberRangeLooks, setNumberRangeLooks)
    numberResampLines = property(getNumberResampLines, setNumberResampLines)
    numberRangeBins = property(getNumberRangeBins, setNumberRangeBins)
    shadeFactor = property(getShadeFactor, setShadeFactor)
    processingDirectory = property(getProcessingDirectory, setProcessingDirectory)
    workingDirectory = property(getWorkingDirectory, setWorkingDirectory)
    dataDirectory = property(getDataDirectory, setDataDirectory)
    filterStrength = property(getFilterStrength, setFilterStrength)
    checkPointer = property(getCheckPointer, setCheckPointer)
    formSLC1 = property(getFormSLC1, setFormSLC1)
    formSLC2 = property(getFormSLC2, setFormSLC2)
    mocompBaseline = property(getMocompBaseline, setMocompBaseline)
    topocorrect = property(getTopocorrect, setTopocorrect)
    topo = property(getTopo, setTopo)
    masterSquint = property(getMasterSquint, setMasterSquint)
    slaveSquint = property(getSlaveSquint, setSlaveSquint)
    geocode_list = property(getGeocodeList, setGeocodeList)

    pass


## Why this: the code bloat with master this and slave that indicates the
## design princple does not use composition, this is an attempt to
## fix that
class RadarSwath(object):
    def __init__(self,
                 frame=None,
                 orbit=None,
                 doppler=None,
                 rawimgae=None,
                 slcimage=None,
                 squint=None):
        self.frame = frame
        self.orbit = orbit
        self.doppler = doppler
        self.rawimage = rawimage
        self.slcimage = slcimage
        self.squint = squint
        return None
    pass
