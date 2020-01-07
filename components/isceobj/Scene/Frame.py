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
# Author: Walter Szeliga
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import datetime

from isceobj.Attitude.Attitude import Attitude
from iscesys.Component.Component import Component
from isceobj.Image.Image import Image
from isceobj.Orbit.Orbit import Orbit
from isceobj.Radar.Radar import Radar
from isceobj.Util.decorators import type_check

SCHHEIGHT = Component.Parameter('_schHeight',
        public_name='SCHHEIGHT',
        default=None,
        type=float,
        mandatory=True,
        doc = 'SCH HEIGHT')

SCHVELOCITY = Component.Parameter('_schVelocity',
        public_name = 'SCHVELOCITY',
        default = None,
        type = float,
        mandatory=True,
        doc = 'SCH VELOCITY')

POLARIZATION = Component.Parameter('_polarization',
        public_name = 'POLARIZATION',
        default=None,
        type=str,
        mandatory=False,
        doc = 'Polarization.')

NUMBER_OF_SAMPLES = Component.Parameter('_numberOfSamples',
        public_name = 'NUMBER_OF_SAMPLES',
        default = None,
        type=int,
        mandatory=False,
        doc = 'Number of samples in a range line.')

NUMBER_OF_LINES = Component.Parameter('_numberOfLines',
        public_name = 'NUMBER_OF_LINES',
        default=None,
        type=int,
        mandatory=False,
        doc = 'Number of lines in the image')

STARTING_RANGE = Component.Parameter('_startingRange',
        public_name = 'STARTING_RANGE',
        default=None,
        type=int,
        mandatory=False,
        doc = 'Range to the first valid sample in the image')

SENSING_START = Component.Parameter('_sensingStart',
        public_name = 'SENSING_START',
        default = None,
        type = datetime.datetime,
        mandatory=False,
        doc = 'Date time object for UTC of first line')

SENSING_MID = Component.Parameter('_sensingMid',
        public_name = 'SENSING_MID',
        default = None,
        type = datetime.datetime,
        mandatory=False,
        doc = 'Date time object for UTC of middle of image')

SENSING_STOP = Component.Parameter('_sensingStop',
        public_name = 'SENSING_STOP',
        default = None,
        type = datetime.datetime,
        mandatory = False,
        doc = 'Date time object for UTC of last line of image')

TRACK_NUMBER = Component.Parameter('_trackNumber',
        public_name = 'TRACK_NUMBER',
        default=None,
        type = int,
        mandatory=False,
        doc = 'Track number for the acquisition')

ORBIT_NUMBER = Component.Parameter('orbitNumber',
        public_name='ORBIT_NUMBER',
        default=None,
        type = int,
        mandatory = False,
        doc = 'Orbit number for the acquisition')

PASS_DIRECTION = Component.Parameter('_passDirection',
    public_name='PASS_DIRECTION',
    default=None,
    type = str,
    mandatory = False,
    doc = 'Ascending or Descending direction of orbit')

PROCESSING_FACILITY = Component.Parameter('_processingFacility',
    public_name='PROCESSING_FACILITY',
    default=None,
    type = str,
    mandatory = False,
    doc = 'Processing facility information')

PROCESSING_SYSTEM = Component.Parameter('_processingSystem',
    public_name='PROCESSING_SYSTEM',
    default=None,
    type = str,
    mandatory = False,
    doc = 'Processing system information')

PROCESSING_LEVEL = Component.Parameter('_processingLevel',
    public_name='PROCESSING_LEVEL',
    default=None,
    type = str,
    mandatory = False,
    doc = 'Processing level of the product')

PROCESSING_SYSTEM_VERSION = Component.Parameter('_processingSoftwareVersion',
    public_name='PROCESSING_SYSTEM_VERSION',
    default=None,
    type = str,
    mandatory = False,
    doc = 'Processing system software version')

AUX_FILE = Component.Parameter('_auxFile',
    public_name='AUX_FILE',
    default=None,
    type = str,
    mandatory = False,
    doc = 'Auxiliary file for the acquisition')

class Frame(Component):
    """A class to represent a frame along a radar track"""

    family = 'frame'
    logging_name = 'isce.isceobj.scene.frame'

    parameter_list = (SCHHEIGHT,
                      SCHVELOCITY,
                      POLARIZATION,
                      NUMBER_OF_SAMPLES,
                      NUMBER_OF_LINES,
                      STARTING_RANGE,
                      SENSING_START,
                      SENSING_MID,
                      SENSING_STOP,
                      TRACK_NUMBER,
                      ORBIT_NUMBER,
                      PASS_DIRECTION,
                      PROCESSING_SYSTEM,
                      PROCESSING_LEVEL,
                      PROCESSING_SYSTEM_VERSION,
                      AUX_FILE)


    def _facilities(self):
        '''
        Defines all the user configurable facilities for this application.
        '''

        self._instrument = self.facility(
                '_instrument',
                public_name='INSTRUMENT',
                module='isceobj.Radar.Radar',
                factory='createRadar',
                args=(),
                mandatory=True,
                doc = "Radar information")

        self._orbit = self.facility(
                '_orbit',
                public_name='ORBIT',
                module = 'isceobj.Orbit.Orbit',
                factory = 'createOrbit',
                args=(),
                mandatory=True,
                doc = "Orbit information")

        self._attitude = self.facility(
                '_attitude',
                public_name='ATTITUDE',
                module='isceobj.Attitude.Attitude',
                factory='createAttitude',
                args=(),
                mandatory=True,
                doc = "Attitude Information")

       
    ## this init will be removed when super no longer overides the class's
    ## dictionaryOfVariables
    def __init__(self, name=''):
        super(Frame, self).__init__(family=self.__class__.family, name=name)
#        self._instrument.configure()
        return None

    @property
    def platform(self):
        return self.instrument.platform
    @property
    def planet(self):
        return self.platform.planet
    @property
    def ellipsoid(self):
        return self.planet.ellipsoid
    @property
    def PRF(self):
        return self.instrument.PRF
    @property
    def radarWavelegth(self):
        return self.instrument.radarWavelength
    @property
    def rangeSamplingRate(self):
        return self.instrument.rangeSamplingRate
    @property
    def pulseLength(self):
        return self.instrument.pulseLength
    

    def setSchHeight(self, h):
        self._schHeight = h
        
    def getSchHeight(self):
        return self._schHeight
    
    def setNumberRangeBins(self, nrb):
        self._numberRangeBins = nrb

    def getNumberRangeBins(self):
        return self._numberRangeBins
    
    def setSchVelocity(self, v):
        self._schVelocity = v
        
    def getSchVelocity(self):
        return self._schVelocity

    def setSquintAngle(self, angle):
        self._squintAngle = angle

    def getSquintAngle(self):
        return self._squintAngle
    
    def setStartingRange(self, range):
        self._startingRange = range
        
    def getStartingRange(self):
        """The Starting Range, in km"""
        return self._startingRange
    
    def setFarRange(self, range):
        self._farRange = range
    
    def getFarRange(self):
        """The Far Range, in km"""
        return self._farRange


    @type_check(datetime.datetime)
    def setSensingStart(self, time):        
        self._sensingStart = time
        pass
            
    def getSensingStart(self):
        """The UTC date and time of the first azimuth line"""
        return self._sensingStart

    @type_check(datetime.datetime)
    def setSensingMid(self, time):        
        self._sensingMid = time
        pass

    def getSensingMid(self):
        """The UTC date and time of the azimuth line at the center of the
        scene"""
        return self._sensingMid
        
    @type_check(datetime.datetime)
    def setSensingStop(self, time):
        self._sensingStop = time
        pass
            
    def getSensingStop(self):
        """The UTC date and time of the last azimuth line"""
        return self._sensingStop
        
    @type_check(Radar)
    def setInstrument(self, instrument):
        self._instrument = instrument
        pass
            
    def getInstrument(self):
        return self._instrument
        
    def setOrbit(self, orbit):
        self._orbit = orbit
            
    def getOrbit(self):
        return self._orbit
    
    
    @type_check(Attitude)
    def setAttitude(self, attitude):
        self._attitude = attitude
        pass
    
    def getAttitude(self):
        return self._attitude
    
    @type_check(Image)
    def setImage(self, image):
        self._image = image
        pass
        
    def getImage(self):
        return self._image
     
    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, image):
        return self.setImage(image)

    def getAuxFile(self):
        return self._auxFile
    
    def setAuxFile(self,aux):
        self._auxFile = aux
    
    def setPolarization(self, polarization):
        self._polarization = polarization
            
    def getPolarization(self):
        """The polarization of the scene"""
        return self._polarization
        
    def setNumberOfSamples(self, samples):
        self._numberOfSamples = samples
            
    def getNumberOfSamples(self):
        """The number of samples in range"""
        return self._numberOfSamples
        
    def setNumberOfLines(self, lines):
        self._numberOfLines = lines
            
    def getNumberOfLines(self):
        """The number of azimuth lines"""
        return self._numberOfLines
        
    def setTrackNumber(self, track):
        self._trackNumber = track
            
    def getTrackNumber(self):
        """The Track number of the scene"""
        return self._trackNumber
        
    def setOrbitNumber(self, orbit):
        self._orbitNumber = orbit
            
    def getOrbitNumber(self):
        """The orbit number of the scene"""
        return self._orbitNumber
        
    def setFrameNumber(self, frame):
        self._frameNumber = frame
            
    def getFrameNumber(self):
        """The frame number of the scene"""
        return self._frameNumber
    
    def setPassDirection(self, dir):
        self._passDirection = dir
        
    def getPassDirection(self):
        """The pass direction of the satellite, either ascending or descending
        """
        return self._passDirection
        
    def setProcessingFacility(self, facility):
        self._processingFacility = facility
            
    def getProcessingFacility(self):
        """The facility that processed the raw data"""
        return self._processingFacility
    
    def setProcessingSystem(self, system):
        self._processingSystem = system
        
    def getProcessingSystem(self):
        """The software used to process the raw data"""
        return self._processingSystem
        
    def setProcessingLevel(self, level):
        self._processingLevel = level
            
    def getProcessingLevel(self):
        """The level to which the raw data was processed"""
        return self._processingLevel
    
    def setProcessingSoftwareVersion(self, ver):
        self._processingSoftwareVersion = ver
        
    def getProcessingSoftwareVersion(self):
        """The software version of the processing software"""
        return self._processingSoftwareVersion
    
    def __str__(self):
        retstr = "Sensing Start Time: (%s)\n"
        retlst = (self._sensingStart, )
        retstr += "Sensing Mid Time: (%s)\n"
        retlst += (self._sensingMid, )
        retstr += "Sensing Stop Time: (%s)\n"
        retlst += (self._sensingStop, )
        retstr += "Orbit Number: (%s)\n"
        retlst += (self._orbitNumber, )
        retstr += "Frame Number: (%s)\n"
        retlst += (self._frameNumber, )
        retstr += "Track Number: (%s)\n"
        retlst += (self._trackNumber, )
        retstr += "Number of Lines: (%s)\n"
        retlst += (self._numberOfLines, )
        retstr += "Number of Samples: (%s)\n"
        retlst += (self._numberOfSamples, )
        retstr += "Starting Range: (%s)\n"
        retlst += (self._startingRange, )
        retstr += "Polarization: (%s)\n"
        retlst += (self._polarization, )
        retstr += "Processing Facility: (%s)\n"
        retlst += (self._processingFacility, )
        retstr += "Processing Software: (%s)\n"
        retlst += (self._processingSystem, )
        retstr += "Processing Software Version: (%s)\n"
        retlst += (self._processingSoftwareVersion, )
                        
        return retstr % retlst
    

    frameNumber = property(getFrameNumber, setFrameNumber)
    instrument = property(getInstrument, setInstrument)
    numberOfLines = property(getNumberOfLines, setNumberOfLines)
    numberOfSamples = property(getNumberOfSamples, setNumberOfSamples)
    numberRangeBins = property(getNumberRangeBins, setNumberRangeBins)
    orbit = property(getOrbit, setOrbit)
    attitude = property(getAttitude, setAttitude)
    orbitNumber = property(getOrbitNumber, setOrbitNumber)
    passDirection = property(getPassDirection, setPassDirection)
    polarization = property(getPolarization, setPolarization)
    processingFacility = property(getProcessingFacility, setProcessingFacility)
    processingLevel = property(getProcessingLevel, setProcessingLevel)
    processingSoftwareVersion = property(getProcessingSoftwareVersion, setProcessingSoftwareVersion)
    processingSystem = property(getProcessingSystem, setProcessingSystem)    
    sensingMid = property(getSensingMid, setSensingMid)
    sensingStart = property(getSensingStart, setSensingStart)
    sensingStop = property(getSensingStop, setSensingStop)
    squintAngle = property(getSquintAngle, setSquintAngle)
    startingRange = property(getStartingRange, setStartingRange)
    trackNumber = property(getTrackNumber, setTrackNumber)
    schHeight = property(getSchHeight, setSchHeight)
    schVelocity = property(getSchVelocity, setSchVelocity)
    auxFile = property(getAuxFile, setAuxFile)

    pass



## A mixin for objects with a Frame() that they need to look through-via
## read-only attributes.
class FrameMixin(object):
    """Mixin flattens frame's attributes"""


    @property
    def instrument(self):
        return self.frame.instrument

    @property
    def platform(self):
        return self.frame.platform

    @property
    def planet(self):
        return self.frame.planet

    @property
    def ellipsoid(self):
        return self.frame.ellipsoid
    
    @property
    def orbit(self):
        return self.frame.orbit

    @property
    def sensingStart(self):
        return self.frame.sensingStart
    
    @property
    def sensingMid(self):
        return self.frame.sensingMid
    
    @property
    def startingRange(self):
        return self.frame.startingRange

    @property
    def PRF(self):
        return self.frame.PRF

    @property
    def radarWavelength(self):
        return self.instrument.radarWavelength

    @property
    def squintAngle(self):
        return self.frame.squintAngle

    @squintAngle.setter
    def squintAngle(self, value):
        self.frame.squintAngle = value

    @property
    def rangeSamplingRate(self):
        return self.frame.rangeSamplingRate
    @property
    def pulseLength(self):
        return self.frame.pulseLength
    
    pass

        
