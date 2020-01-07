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



from isceobj.Image.Image import Image
from iscesys.Component.Component import Component, Port
from stdproc.stdproc.formslc import formslc


NUMBER_GOOD_BYTES = Component.Parameter(
    'numberGoodBytes',
    public_name='NUMBER_GOOD_BYTES',
    default=None,
    type=int,
    mandatory=True,
    doc='Number of bytes used in a range line in the raw image'
)
NUMBER_BYTES_PER_LINE = Component.Parameter(
    'numberBytesPerLine',
    public_name='NUMBER_BYTES_PER_LINE',
    default=None,
    type=int,
    mandatory=True,
    doc='Number of bytes per line in the raw image'
)
FIRST_LINE = Component.Parameter(
    'firstLine',
    public_name='FIRST_LINE',
    default=0,
    type=int,
    mandatory=False,
    doc='First line processed in the raw image'
)
NUMBER_VALID_PULSES = Component.Parameter(
    'numberValidPulses',
    public_name='NUMBER_VALID_PULSES',
    default=None,
    type=int,
    mandatory=True,
    doc='Number of lines to be stored from each azimuth patch'
)
FIRST_SAMPLE = Component.Parameter(
    'firstSample',
    public_name='FIRST_SAMPLE',
    default=None,
    type=int,
    mandatory=True,
    doc='First valid sample in the raw image range line.'
)
NUMBER_PATCHES = Component.Parameter(
    'numberPatches',
    public_name='NUMBER_PATCHES',
    default=None,
    type=int,
    mandatory=True,
    doc='Number of patches used.'
)
START_RANGE_BIN = Component.Parameter(
    'startRangeBin',
    public_name='START_RANGE_BIN',
    default=1,
    type=int,
    mandatory=False,
    doc=('Starting range bin to read from the raw data. '+
         'Must have positive value.'
    )
)
NUMBER_RANGE_BIN = Component.Parameter(
    'numberRangeBin',
    public_name='NUMBER_RANGE_BIN',
    default=None,
    type=int,
    mandatory=True,
    doc=('Number of range bins in the input raw image. '+
         'Used in the computation of the slcWidth. '
    )
)
NUMBER_AZIMUTH_LOOKS = Component.Parameter(
    'numberAzimuthLooks',
    public_name='NUMBER_AZIMUTH_LOOKS',
    default=None,
    type=int,
    mandatory=True,
    doc='Number of looks in the azimuth direction'
)
RANGE_CHIRP_EXTENSION_POINTS = Component.Parameter(
    'rangeChirpExtensionPoints',
    public_name='RANGE_CHIRP_EXTENSION_POINTS',
    default=0,
    type=int,
    mandatory=False,
    doc=('Number of points to extend in range. Set negative for truncation.')
)
AZIMUTH_PATCH_SIZE = Component.Parameter(
    'azimuthPatchSize',
    public_name='AZIMUTH_PATCH_SIZE',
    default=None,
    type=int,
    mandatory=True,
    doc='Number of lines in an azimuth patch'
)
OVERLAP = Component.Parameter(
    'overlap',
    public_name='OVERLAP',
    default=0,
    type=int,
    mandatory=False,
    doc='Overlap between consecutive azimuth patches'
)
RAN_FFTOV = Component.Parameter(
    'ranfftov',
    public_name='RAN_FFTOV',
    default=65536,
    type=int,
    mandatory=False,
    doc='FFT size for offset video'
)
RAN_FFTIQ = Component.Parameter(
    'ranfftiq',
    public_name='RAN_FFTIQ',
    default=32768,
    type=int,
    mandatory=False,
    doc='FFT size for I/Q processing'
)
DEBUG_FLAG = Component.Parameter(
    'debugFlag',
    public_name='DEBUG_FLAG',
    default=0,
    type=int,
    mandatory=False,
    doc='Debug output flag'
)
CALTONE_LOCATION = Component.Parameter(
    'caltoneLocation',
    public_name='CALTONE_LOCATION',
    default=0,
    type=int,
    mandatory=False,
    doc='Location of the calibration tone'
)
PLANET_LOCAL_RADIUS = Component.Parameter(
    'planetLocalRadius',
    public_name='PLANET_LOCAL_RADIUS',
    default=None,
    type=float,
    mandatory=True,
    doc='Local radius of the planet'
)
BODY_FIXED_VELOCITY = Component.Parameter(
    'bodyFixedVelocity',
    public_name='BODY_FIXED_VELOCITY',
    default=None,
    type=float,
    mandatory=True,
    doc='Platform velocity'
)
SPACECRAFT_HEIGHT = Component.Parameter(
    'spacecraftHeight',
    public_name='SPACECRAFT_HEIGHT',
    default=None,
    type=float,
    mandatory=True,
    doc='Spacecraft height'
)
PRF = Component.Parameter(
    'prf',
    public_name='PRF',
    default=None,
    type=float,
    mandatory=True,
    doc='Pulse repetition frequency'
)
INPHASE_VALUE = Component.Parameter(
    'inPhaseValue',
    public_name='INPHASE_VALUE',
    default=None,
    type=float,
    mandatory=True,
    doc=''
)
QUADRATURE_VALUE = Component.Parameter(
    'quadratureValue',
    public_name='QUADRATURE_VALUE',
    default=None,
    type=float,
    mandatory=True,
    doc=''
)
AZIMUTH_RESOLUTION = Component.Parameter(
    'azimuthResolution',
    public_name='AZIMUTH_RESOLUTION',
    default=None,
    type=float,
    mandatory=True,
    doc='Desired azimuth resolution for determining azimuth B/W'
)
RANGE_SAMPLING_RATE = Component.Parameter(
    'rangeSamplingRate',
    public_name='RANGE_SAMPLING_RATE',
    default=None,
    type=float,
    mandatory=True,
    doc='Sampling frequency of the range pixels'
)
CHIRP_SLOPE = Component.Parameter(
    'chirpSlope',
    public_name='CHIRP_SLOPE',
    default=None,
    type=float,
    mandatory=True,
    doc='Frequency slope of the transmitted chirp'
)
RANGE_PULSE_DURATION = Component.Parameter(
    'rangePulseDuration',
    public_name='RANGE_PULSE_DURATION',
    default=None,
    type=float,
    mandatory=True,
    doc='Range pulse duration'
)
RADAR_WAVELENGTH = Component.Parameter(
    'radarWavelength',
    public_name='RADAR_WAVELENGTH',
    default=None,
    type=float,
    mandatory=True,
    doc='Radar wavelength'
)
RANGE_FIRST_SAMPLE = Component.Parameter(
    'rangeFirstSample',
    public_name='RANGE_FIRST_SAMPLE',
    default=None,
    type=float,
    mandatory=True,
    doc='Range of the first sample in meters'
)
RANGE_SPECTRAL_WEIGHTING = Component.Parameter(
    'rangeSpectralWeighting',
    public_name='RANGE_SPECTRAL_WEIGHTING',
    default=1,
    type=float,
    mandatory=False,
    doc='Spectral weights for range spectrum.'
)
SPECTRAL_SHIFT_FRACTION = Component.Parameter(
    'spectralShiftFraction',
    public_name='SPECTRAL_SHIFT_FRACTION',
    default=0,
    type=float,
    mandatory=False,
    doc='Spectral weights for azimuth spectrum.'
)
IQ_FLIP = Component.Parameter(
    'IQFlip',
    public_name='IQ_FLIP',
    default='n',
    type=str,
    mandatory=False,
    doc='If I/Q channels are flipped in the raw data file'
)
DESKEW_FLAG = Component.Parameter(
    'deskewFlag',
    public_name='DESKEW_FLAG',
    default='n',
    type=str,
    mandatory=False,
    doc='If deskewing is desired'
)
SECONDARY_RANGE_MIGRATION_FLAG = Component.Parameter(
    'secondaryRangeMigrationFlag',
    public_name='SECONDARY_RANGE_MIGRATION_FLAG',
    default='n',
    type=str,
    mandatory=False,
    doc='If secondary range migration is desired'
)
POSITION = Component.Parameter(
    'position',
    public_name='POSITION',
    default=[],
    type=list,
    mandatory=True,
    doc='Position vector'
)
TIME = Component.Parameter(
    'time',
    public_name='TIME',
    default=[],
    type=list,
    mandatory=True,
    doc='Time vector'
)
DOPPLER_CENTROID_COEFFICIENTS = Component.Parameter(
    'dopplerCentroidCoefficients',
    public_name='DOPPLER_CENTROID_COEFFICIENTS',
    default=[],
    type=list,
    mandatory=True,
    doc='Doppler centroid coefficients'
)
MOCOMP_POSITION = Component.Parameter(
    'mocompPosition',
    public_name='MOCOMP_POSITION',
    default=[],
    type=list,
    mandatory=None,
    doc='Motion compensated position'
)
MOCOMP_INDEX = Component.Parameter(
    'mocompIndx',
    public_name='MOCOMP_INDEX',
    default=[],
    type=list,
    mandatory=None,
    doc='Valid indexes of the motion compensated position'
)
STARTING_RANGE = Component.Parameter(
    'startingRange',
    public_name='STARTING_RANGE',
    default=None,
    mandatory=None,
    doc='Modified starting range for the SLC'
)

##KK,ML 2013-07-15
SHIFT = Component.Parameter(
    'shift',
    public_name='azshiftpixels',
    default=-0.5,
    type=float,
    mandatory=None,
    doc='Number of pixels to shift in the azimuth direction'
)
##KK,ML


## This decorator takes a setter and only executes it if the argument is True
def set_if_true(func):
    """Decorate a setter to only set if the value is nonzero"""
    def new_func(self, var):
        if var:
            func(self, var)
    return new_func

class Formslc(Component):

    family = 'formslc'
    logging_name = 'isce.formslc'

    dont_pickle_me = ()

    parameter_list = (NUMBER_GOOD_BYTES,
                      NUMBER_BYTES_PER_LINE,
                      FIRST_LINE,
                      NUMBER_VALID_PULSES,
                      FIRST_SAMPLE,
                      NUMBER_PATCHES,
                      START_RANGE_BIN,
                      NUMBER_RANGE_BIN,
                      NUMBER_AZIMUTH_LOOKS,
                      RANGE_CHIRP_EXTENSION_POINTS,
                      AZIMUTH_PATCH_SIZE,
                      OVERLAP,
                      RAN_FFTOV,
                      RAN_FFTIQ,
                      DEBUG_FLAG,
                      CALTONE_LOCATION,
                      PLANET_LOCAL_RADIUS,
                      BODY_FIXED_VELOCITY,
                      SPACECRAFT_HEIGHT,
                      PRF,
                      INPHASE_VALUE,
                      QUADRATURE_VALUE,
                      AZIMUTH_RESOLUTION,
                      RANGE_SAMPLING_RATE,
                      CHIRP_SLOPE,
                      RANGE_PULSE_DURATION,
                      RADAR_WAVELENGTH,
                      RANGE_FIRST_SAMPLE,
                      RANGE_SPECTRAL_WEIGHTING,
                      SPECTRAL_SHIFT_FRACTION,
                      IQ_FLIP,
                      DESKEW_FLAG,
                      SECONDARY_RANGE_MIGRATION_FLAG,
                      POSITION,
                      TIME,
                      DOPPLER_CENTROID_COEFFICIENTS,
                      MOCOMP_POSITION,
                      MOCOMP_INDEX,
                      STARTING_RANGE,
                      SHIFT ##KK,ML 2013-07-15
                    )

    ## maxAzPatchSize is defined in case the user specifies an unusually
    ## large number of valid pulses to save but no patch size on input.
    maxAzPatchSize = 32768

    def formslc(self):
        for item in self.inputPorts:
            item()

        self.computeRangeParams()

        try:
            self.rawAccessor = self.rawImage.getImagePointer()
            self.slcAccessor = self.slcImage.getImagePointer()
        except AttributeError:
            self.logger.error("Error in accessing image pointers")
            raise AttributeError

        self.computePatchParams()
        self.allocateArrays()
        self.setState()
        formslc.formslc_Py(self.rawAccessor, self.slcAccessor)

        #the size of this vectors where unknown until the end of the run
        posSize = formslc.getMocompPositionSize_Py()
        self.dim1_mocompPosition = 2
        self.dim2_mocompPosition = posSize
        self.dim1_mocompIndx = posSize
        self.getState()
        self.deallocateArrays()
        self.slcImage.renderHdr()
        return self.slcImage

    @staticmethod
    def nxPower(num):
        power=0
        k=0
        while power < num:
            k+=1
            power=2**k
        return k

    def computeRangeParams(self):
        '''Ensure that the given range parameters are valid.'''
        from isceobj.Constants import SPEED_OF_LIGHT
        import isceobj

        chirpLength = int(self.rangeSamplingRate * self.rangePulseDuration)
        halfChirpLength = chirpLength // 2

        #Add a half-chirp to the user requested extension.
        #To decrease the extension relative to the halfChirpLength
        #the user would have to set rangeCHirpExtensionPoints to a negative
        #value; however, the resulting value must be greater than 0.
        self.logger.info('Default near range chirp extension '+
            '(half the chirp length): %d' % (halfChirpLength))
        self.logger.info('Extra Chirp Extension requested: '+
            '%d' % (self.rangeChirpExtensionPoints))

        self.rangeChirpExtensionPoints = (self.rangeChirpExtensionPoints +
            halfChirpLength)

        if self.rangeChirpExtensionPoints >= 0:
            self.logger.info('Extending range line by '+
                '%d pixels' % (self.rangeChirpExtensionPoints))
        elif self.rangeChirpExtensionPoints < 0:
            raise ValueError('Range Chirp Extension cannot be negative.')

        #startRangeBin must be positive.
        #It is an index into the raw data range line
        if self.startRangeBin <= 0:
            raise ValueError('startRangeBin must be positive ')

        self.logger.info('Number of Range Bins: %d'%self.numberRangeBin)
        self.slcWidth = (self.numberRangeBin + self.rangeChirpExtensionPoints +
            halfChirpLength + self.startRangeBin - 1)
        delr = self.rangeSamplingRate

        #Will be set here and passed on to Fortran. - Piyush
        self.startingRange = (self.rangeFirstSample + (self.startRangeBin - 1 -
            self.rangeChirpExtensionPoints) *
            SPEED_OF_LIGHT*0.5/self.rangeSamplingRate)

        self.logger.info('Raw Starting Range: %f'%(self.rangeFirstSample))
        self.logger.info('SLC Starting Range: %f'%(self.startingRange))
        self.logger.info('SLC width: %f'%(self.slcWidth))

        #Set width of the SLC image here .
        self.slcImage = isceobj.createSlcImage()
        self.logger.info('Debug fname : %s'%(self.rawImage.getFilename()))
        self.slcImage.setFilename(
            self.rawImage.getFilename().replace('.raw','.slc'))
        self.slcImage.setWidth(self.slcWidth)
        self.slcImage.setAccessMode('write')
        self.slcImage.createImage()


    ## set the patch size and number of valid pulses based on the computed
    ## synthetic aperture length
    def computePatchParams(self):

        from isceobj.Constants import SPEED_OF_LIGHT
        chunksize=1024
        rawFileSize = self.rawImage.getLength() * self.rawImage.getWidth()
        linelength = int(self.rawImage.getXmax())

        synthApertureSamps = (
            self.radarWavelength* (self.startingRange +
                self.slcWidth*SPEED_OF_LIGHT*0.5/self.rangeSamplingRate)*
                self.prf/(self.antennaLength*self.bodyFixedVelocity))
        nSAS = int((synthApertureSamps-1)/chunksize)+1
        chunkedSAS = chunksize*nSAS
        nxP = self.nxPower(nSAS)
        azP = chunksize*2*(2**nxP)      #Patchsize
        nV = azP-chunkedSAS             #Numbervalid
        if self.azimuthPatchSize:
            if self.azimuthPatchSize != 2**self.nxPower(self.azimuthPatchSize):
                self.azimuthPatchSize = 2**self.nxPower(self.azimuthPatchSize)
                self.logger.info(
                    "Patch size must equal power of 2. Resetting to %d" %
                    self.azimuthPatchSize
                    )

        if self.azimuthPatchSize and self.numberValidPulses:
            if (self.azimuthPatchSize < self.numberValidPulses or
                self.azimuthPatchSize < chunkedSAS+chunksize):
                self.azimuthPatchSize = azP
                self.numberValidPulses = nV
            elif self.numberValidPulses > self.azimuthPatchSize-chunkedSAS:
                msg = ("Number of valid pulses specified is too large "+
                       "for full linear convolution. ")
                msg += ("Should be less than %d" %
                        (self.azimuthPatchSize-chunkedSAS))
                self.logger.info(msg)
                self.logger.info(
                    "Continuing with specified value of %d" %
                    self.numberValidPulses
                    )

        elif self.azimuthPatchSize and not self.numberValidPulses:
            if self.azimuthPatchSize < chunkedSAS+chunksize:
                self.azimuthPatchSize = azP
                self.numberValidPulses = nV
            else:
                self.numberValidPulses = self.azimuthPatchSize-chunkedSAS
                if self.numberValidPulses > self.azimuthPatchSize-chunkedSAS:
                    msg = ("Number of valid pulses specified is too large "+
                           "for full linear convolution. ")
                    msg += ("Should be less than %d" %
                            (self.azimuthPatchSize-chunkedSAS))
                    self.logger.info(msg)
                    self.logger.info(
                        "Continuing with specified value of %d" %
                        self.numberValidPulses
                        )

        elif not self.azimuthPatchSize and self.numberValidPulses:
            self.azimuthPatchSize=2**self.nxPower(self.numberValidPulses+
                                                  synthApertureSamps)
            if self.azimuthPatchSize > self.maxAzPatchSize:
                msg = ("%d is a rather large patch size. " %
                         self.azimuthPatchSize)
                msg += ("Check that the number of valid pulses is in a "+
                        "reasonable range. Proceeding anyway...")
                self.logger.info(msg)

        elif not self.azimuthPatchSize and not self.numberValidPulses:
            self.azimuthPatchSize=azP
            self.numberValidPulses=nV

        overhead = self.azimuthPatchSize - self.numberValidPulses
        if not self.numberPatches:
            self.numberPatches = (
                1+int(
                    (rawFileSize/float(linelength)-overhead)/
                    self.numberValidPulses
                    )
                )

    def getState(self):
        self.mocompPosition = formslc.getMocompPosition_Py(
            self.dim1_mocompPosition, self.dim2_mocompPosition
            )
        self.mocompIndx = formslc.getMocompIndex_Py(self.dim1_mocompIndx)
        self.startingRange = formslc.getStartingRange_Py()

    def setState(self):
        formslc.setStdWriter_Py(int(self.stdWriter))
        formslc.setNumberGoodBytes_Py(int(self.numberGoodBytes))
        formslc.setNumberBytesPerLine_Py(int(self.numberBytesPerLine))
        formslc.setFirstLine_Py(int(self.firstLine))
        formslc.setNumberValidPulses_Py(int(self.numberValidPulses))
        formslc.setFirstSample_Py(int(self.firstSample))
        formslc.setNumberPatches_Py(int(self.numberPatches))
        formslc.setStartRangeBin_Py(int(self.startRangeBin))
        formslc.setNumberRangeBin_Py(int(self.numberRangeBin))
        formslc.setNumberAzimuthLooks_Py(int(self.numberAzimuthLooks))
        formslc.setRangeChirpExtensionPoints_Py(
            int(self.rangeChirpExtensionPoints)
            )
        formslc.setAzimuthPatchSize_Py(int(self.azimuthPatchSize))
        formslc.setOverlap_Py(int(self.overlap))
        formslc.setRanfftov_Py(int(self.ranfftov))
        formslc.setRanfftiq_Py(int(self.ranfftiq))
        formslc.setDebugFlag_Py(int(self.debugFlag))
        formslc.setCaltoneLocation_Py(float(self.caltoneLocation))
        formslc.setPlanetLocalRadius_Py(float(self.planetLocalRadius))
        formslc.setBodyFixedVelocity_Py(float(self.bodyFixedVelocity))
        formslc.setSpacecraftHeight_Py(float(self.spacecraftHeight))
        formslc.setPRF_Py(float(self.prf))
        formslc.setInPhaseValue_Py(float(self.inPhaseValue))
        formslc.setQuadratureValue_Py(float(self.quadratureValue))
        formslc.setAzimuthResolution_Py(float(self.azimuthResolution))
        formslc.setRangeSamplingRate_Py(float(self.rangeSamplingRate))
        formslc.setChirpSlope_Py(float(self.chirpSlope))
        formslc.setRangePulseDuration_Py(float(self.rangePulseDuration))
        formslc.setRadarWavelength_Py(float(self.radarWavelength))
        formslc.setRangeFirstSample_Py(float(self.rangeFirstSample))
        formslc.setRangeSpectralWeighting_Py(
            float(self.rangeSpectralWeighting))
        formslc.setSpectralShiftFraction_Py(float(self.spectralShiftFraction))
        formslc.setIMRC1_Py(int(self.imrc1Accessor))
        formslc.setIMMocomp_Py(int(self.immocompAccessor))
        formslc.setIMRCAS1_Py(int(self.imrcas1Accessor))
        formslc.setIMRCRM1_Py(int(self.imrcrm1Accessor))
        formslc.setTransDat_Py(int(self.transAccessor))
        formslc.setIQFlip_Py(self.IQFlip)
        formslc.setDeskewFlag_Py(self.deskewFlag)
        formslc.setSecondaryRangeMigrationFlag_Py(
            self.secondaryRangeMigrationFlag
            )
        formslc.setPosition_Py(self.position,
                               self.dim1_position,
                               self.dim2_position)
        formslc.setVelocity_Py(self.velocity,
                               self.dim1_velocity,
                               self.dim2_velocity)
        formslc.setTime_Py(self.time,
                           self.dim1_time)
        formslc.setDopplerCentroidCoefficients_Py(
            self.dopplerCentroidCoefficients,
            self.dim1_dopplerCentroidCoefficients
            )
        formslc.setPegPoint_Py(self.pegLatitude,
                               self.pegLongitude,
                               self.pegHeading)
        formslc.setPlanet_Py(self.spin, self.gm)
        formslc.setEllipsoid_Py(self.a, self.e2)
        formslc.setSlcWidth_Py(self.slcWidth)
        formslc.setStartingRange_Py(self.startingRange)
        formslc.setLookSide_Py(self.lookSide)
        formslc.setShift_Py(self.shift) ##KK,ML 2013-07-15

    def getMocompPosition(self, index=None):
        return self.mocompPosition[index] if index else self.mocompPosition

    def getMocompIndex(self):
        return self.mocompIndx

    def getStartingRange(self):
        return self.startingRange

    def setRawImage(self, raw):
        self.rawImage = raw

    def setSlcImage(self, slc):
        self.slcImage = slc

    def setNumberGoodBytes(self, var):
        self.numberGoodBytes = int(var)

    def setNumberBytesPerLine(self, var):
        self.numberBytesPerLine = int(var)

    def setFirstLine(self, var):
        self.firstLine = int(var)

    def setLookSide(self, var):
        self.lookSide = int(var)

    @set_if_true
    def setNumberValidPulses(self, var):
        self.numberValidPulses = int(var)

    def setFirstSample(self, var):
        self.firstSample = int(var)

    @set_if_true
    def setNumberPatches(self,var):
        self.numberPatches = int(var)

    def setStartRangeBin(self, var):
        self.startRangeBin = int(var)

    def setStartingRange(self, var):
        self.startingRange = float(var)

    def setNumberRangeBin(self, var):
        self.numberRangeBin = int(var)

    def setNumberAzimuthLooks(self, var):
        self.numberAzimuthLooks = int(var)

    def setRangeChirpExtensionPoints(self, var):
        self.rangeChirpExtensionPoints = int(var)

    @set_if_true
    def setAzimuthPatchSize(self, var):
        self.azimuthPatchSize = int(var)

    def setOverlap(self, var):
        self.overlap = int(var)

    def setRanfftov(self, var):
        self.ranfftov = int(var)

    def setRanfftiq(self, var):
        self.ranfftiq = int(var)

    def setDebugFlag(self, var):
        self.debugFlag = int(var)

    def setCaltoneLocation(self, var):
        self.caltoneLocation = float(var)

    def setPlanetLocalRadius(self, var):
        self.planetLocalRadius = float(var)

    def setBodyFixedVelocity(self, var):
        self.bodyFixedVelocity = float(var)

    def setSpacecraftHeight(self, var):
        self.spacecraftHeight = float(var)

    def setPRF(self, var):
        self.prf = float(var)

    def setInPhaseValue(self, var):
        self.inPhaseValue = float(var)

    def setQuadratureValue(self, var):
        self.quadratureValue = float(var)

    def setAzimuthResolution(self, var):
        self.azimuthResolution = float(var)

    def setRangeSamplingRate(self, var):
        self.rangeSamplingRate = float(var)

    def setChirpSlope(self, var):
        self.chirpSlope = float(var)

    def setRangePulseDuration(self, var):
        self.rangePulseDuration = float(var)

    def setRadarWavelength(self, var):
        self.radarWavelength = float(var)

    def setRangeFirstSample(self, var):
        self.rangeFirstSample = float(var)

    def setRangeSpectralWeighting(self, var):
        self.rangeSpectralWeighting = float(var)

    def setSpectralShiftFraction(self, var):
        self.spectralShiftFraction = float(var)

    def setIQFlip(self, var):
        self.IQFlip = str(var)

    def setDeskewFlag(self, var):
        self.deskewFlag = str(var)

    def setSecondaryRangeMigrationFlag(self, var):
        self.secondaryRangeMigrationFlag = str(var)

    def setPosition(self, var):
        self.position = var

    def setVelocity(self, var):
        self.velocity = var

    def setTime(self, var):
        self.time = var

    def setSlcWidth(self, var):
        self.slcWidth = var

    def setDopplerCentroidCoefficients(self, var):
        self.dopplerCentroidCoefficients = var

    ##KK,ML 2013-0-15
    def setShift(self, var):
        self.shift = var
    ##KK,ML


    def _testArraySize(self,*args):
        """Test for array dimesions that are zero or smaller"""
        for dimension in args:
            if (dimension <= 0):
                self.logger.error("Error, trying to allocate zero size array")
                raise ValueError

    def allocateArrays(self):
        # Set array sizes from their arrays
        try:
            self.dim1_position = len(self.position)
            self.dim2_position = len(self.position[0])
            self.dim1_velocity = len(self.velocity)
            self.dim2_velocity = len(self.velocity[0])
            self.dim1_time = len(self.time)
            self.dim1_dopplerCentroidCoefficients = len(
                self.dopplerCentroidCoefficients)
        except TypeError:
            self.logger.error("Some input arrays were not set")
            raise TypeError

        # Test that the arrays have a size greater than zero
        self._testArraySize(self.dim1_position,self.dim2_position)
        self._testArraySize(self.dim1_velocity,self.dim2_velocity)
        self._testArraySize(self.dim1_time)
        self._testArraySize(self.dim1_dopplerCentroidCoefficients)

        # Allocate the arrays
        formslc.allocate_sch_Py(self.dim1_position, self.dim2_position)
        formslc.allocate_vsch_Py(self.dim1_velocity, self.dim2_velocity)
        formslc.allocate_time_Py(self.dim1_time)
        formslc.allocate_dopplerCoefficients_Py(
            self.dim1_dopplerCentroidCoefficients)

    def deallocateArrays(self):
        formslc.deallocate_sch_Py()
        formslc.deallocate_vsch_Py()
        formslc.deallocate_time_Py()
        formslc.deallocate_dopplerCoefficients_Py()
        pass

    def addRawImage(self):
        image = self.inputPorts['rawImage']
        if image:
            if isinstance(image, Image):
                self.rawImage = image
                self.numberBytesPerLine = self.rawImage.getWidth()
                self.numberGoodBytes = self.rawImage.getNumberGoodBytes()
                self.firstSample = int(self.rawImage.getXmin()/2)
            else:
                self.logger.error(
                    "Object %s must be an instance of Image" % image
                    )
                raise TypeError


    def addOrbit(self):
        orbit = self.inputPorts['orbit']
        if orbit:
            try:
                time,position,velocity,offset = orbit._unpackOrbit()
                self.time = time
                self.position = position
                self.velocity = velocity
            except AttributeError:
                self.logger.error(
                    "Object %s requires an _unpackOrbit() method" %
                    orbit.__class__
                    )
                raise AttributeError

    def addFrame(self):
        frame = self.inputPorts['frame']
        if frame:
            try:
                self.rangeFirstSample = frame.getStartingRange()
                self.rangeLastSample = frame.getFarRange()
                instrument = frame.getInstrument()
                self.inPhaseValue = instrument.getInPhaseValue()
                self.quadratureValue = instrument.getQuadratureValue()
                self.rangeSamplingRate = instrument.getRangeSamplingRate()
                self.chirpSlope = instrument.getChirpSlope()
                self.rangePulseDuration = instrument.getPulseLength()
                self.radarWavelength = instrument.getRadarWavelength()
                self.prf = instrument.getPulseRepetitionFrequency()
                self.antennaLength = instrument.getPlatform().getAntennaLength()
                if self.azimuthResolution is None:
                    self.azimuthResolution = self.antennaLength/2.0
                self.numberRangeBin = frame.numberRangeBins
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError

    def addPlanet(self):
        planet = self.inputPorts['planet']
        if planet:
            try:
                self.spin = planet.spin
                self.gm = planet.GM
                ellipsoid = planet.ellipsoid
                self.a = ellipsoid.a
                self.e2 = ellipsoid.e2
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError

    def addPeg(self):
        peg = self.inputPorts['peg']
        if peg:
            try:
                self.pegLatitude = peg.getLatitude()
                self.pegLongitude = peg.getLongitude()
                self.pegHeading = peg.getHeading()
                self.planetLocalRadius = peg.getRadiusOfCurvature()
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError

    def addDoppler(self):
        doppler = self.inputPorts['doppler']
        if doppler:
            try:
                self.dopplerCentroidCoefficients = (
                    doppler.getDopplerCoefficients(inHz=True)
                    )

                for num in range(len(self.dopplerCentroidCoefficients)):
                    self.dopplerCentroidCoefficients[num] /= self.prf
                self.dim1_dopplerCentroidCoefficients = len(
                    self.dopplerCentroidCoefficients
                    )
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError

    def _facilities(self):
        self.slcImage = self.facility('slcImage',
            public_name='slcImage',
            module='isceobj.Image',
            factory='createSlcImage',
            mandatory='True',
            doc='Single Look Complex Image object'
        )
        self.rawImage = self.facility('rawImage',
            public_name='rawImage',
            module='isceobj.Image',
            factory='createRawImage',
            mandatory='True',
            doc='Raw Image object'
        )

    def createPorts(self):
        ## 2012/2/12: now using PortIterator.__setitem__
        self.inputPorts['rawImage'] = self.addRawImage
        self.inputPorts['orbit'] = self.addOrbit
        self.inputPorts['frame'] = self.addFrame
        self.inputPorts['peg'] = self.addPeg
        self.inputPorts['planet'] = self.addPlanet
        self.inputPorts['doppler'] = self.addDoppler
        return None

    def __init__(self, name=''):
        super(Formslc, self).__init__(self.__class__.family, name)
        self.configure()

        #Non-parameter defaults
        self.slcImage = None
        self.rawImage = None
        self.lookSide = -1    #By default right looking (to be consistent with old code)

        # Planet information
        # the code does not actually uses the ones set to -9999,
        ## but they are passed so they
        # need to be set
        self.a = -9999
        self.e2 = -9999
        self.spin = -9999
        self.gm = -9999

        # Peg Information
        self.pegLatitude = -9999#see comment above
        self.pegLongitude = -9999
        self.pegHeading = -9999

        # Orbit Information
        self.dim1_position = None
        self.dim2_position = None
        self.velocity = []
        self.dim1_velocity = None
        self.dim2_velocity = None
        self.dim1_time = None
        # Doppler Information
        self.dim1_dopplerCentroidCoefficients = None

        # Accessors
        self.imrc1Accessor = 0
        self.immocompAccessor = 0
        self.imrcas1Accessor = 0
        self.imrcrm1Accessor = 0
        self.transAccessor = 0
        self.rawAccessor = 0
        self.slcAccessor = 0
        self.slcWidth = 0

        self.createPorts()

        self.dictionaryOfOutputVariables = {
            'MOCOMP_POSITION' : 'mocompPosition' ,
            'MOCOMP_INDEX' : 'mocompIndx',
            'STARTING_RANGE' : 'startingRange',
            'SLC_WIDTH': 'slcWidth'
            }


        self.descriptionOfVariables = {}
        self.mandatoryVariables = []
        self.optionalVariables = []
        self.initOptionalAndMandatoryLists()
        return None
    pass
