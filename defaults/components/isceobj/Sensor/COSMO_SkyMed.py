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

try:
    import h5py
except ImportError:
    raise ImportError(
        "Python module h5py is required to process COSMO-SkyMed data"
        )

import isceobj
from isceobj.Orbit.Orbit import StateVector
from isceobj.Planet.AstronomicalHandbook import Const
from isceobj.Planet.Planet import Planet
from isceobj.Scene.Frame import Frame
from iscesys.DateTimeUtil.DateTimeUtil import DateTimeUtil as DTUtil
from isceobj.Sensor import tkfunc,createAuxFile
from iscesys.Component.Component import Component
from .Sensor import Sensor

class COSMO_SkyMed(Sensor):
    """
        A class to parse COSMO-SkyMed metadata
    """
    logging_name = "isce.sensor.COSMO_SkyMed"

    def __init__(self):
        super(COSMO_SkyMed,self).__init__()
        self.hdf5 = None
        self.hdf5FileList = None
        #used to allow refactoring on tkfunc
        self._imageFileList = None

        ###Specific doppler functions for CSK
        self.dopplerRangeTime = []
        self.dopplerAzimuthTime = []
        self.azimuthRefTime = None
        self.rangeRefTime = None
        self.rangeFirstTime = None
        self.rangeLastTime = None

        self.dictionaryOfVariables = {
            'HDF5': ['hdf5FileList','str','mandatory'],
            'OUTPUT': ['output','str','optional']
            }

        ## make this a class attribute, and a Sensor.Constant--not a dictionary.
        self.constants = {'iBias': 127.5,
                          'qBias': 127.5}
        return None

    ## Note: this breaks the ISCE convention of getters.
    def getFrame(self):
        return self.frame


    #jng  parse or parse_context never used
    def parse(self):
        try:
            fp = h5py.File(self.hdf5, 'r')
        except Exception as strerror:
            self.logger.error("IOError: %s\n" % strerror)
            return None

        self.populateMetadata(file=fp)
        fp.close()

    ## Use h5's context management-- TODO: debug and install as 'parse'
    def parse_context(self):
        try:
            with h5py.File(self.hdf5, 'r') as fp:
                self.populateMetadata(file=fp)
        except Exception as strerror:
            self.logger.error("IOError: %s\n" % strerror)

        return None


    def _populatePlatform(self, file=None):
        platform = self.frame.getInstrument().getPlatform()

        platform.setMission(file.attrs['Satellite ID']) # Could use Mission ID as well
        platform.setPlanet(Planet("Earth"))
        platform.setPointingDirection(self.lookMap[file.attrs['Look Side'].decode('utf-8')])
        platform.setAntennaLength(file.attrs['Antenna Length'])

    def _populateInstrument(self,file):
        instrument = self.frame.getInstrument()

        rangePixelSize = Const.c/(2*file['S01'].attrs['Sampling Rate'])

        instrument.setRadarWavelength(file.attrs['Radar Wavelength'])
        instrument.setPulseRepetitionFrequency(file['S01'].attrs['PRF'])
        instrument.setRangePixelSize(rangePixelSize)
        instrument.setPulseLength(file['S01'].attrs['Range Chirp Length'])
        instrument.setChirpSlope(file['S01'].attrs['Range Chirp Rate'])
        instrument.setRangeSamplingRate(file['S01'].attrs['Sampling Rate'])
        instrument.setInPhaseValue(self.constants['iBias'])
        instrument.setQuadratureValue(self.constants['qBias'])
        instrument.setBeamNumber(file.attrs['Multi-Beam ID'])

    def _populateFrame(self,file):
        rft = file['S01']['B001'].attrs['Range First Times'][0]
        slantRange = rft*Const.c/2.0
        sensingStart = self._parseNanoSecondTimeStamp(file.attrs['Scene Sensing Start UTC'])
        sensingStop = self._parseNanoSecondTimeStamp(file.attrs['Scene Sensing Stop UTC'])
        centerTime = DTUtil.timeDeltaToSeconds(sensingStop - sensingStart)/2.0
        sensingMid = sensingStart + datetime.timedelta(microseconds=int(centerTime*1e6))

        self.frame.setStartingRange(slantRange)
        self.frame.setPassDirection(file.attrs['Orbit Direction'])
        self.frame.setOrbitNumber(file.attrs['Orbit Number'])
        self.frame.setProcessingFacility(file.attrs['Processing Centre'])
        self.frame.setProcessingSoftwareVersion(file.attrs['L0 Software Version'])
        self.frame.setPolarization(file['S01'].attrs['Polarisation'])
        self.frame.setNumberOfLines(file['S01']['B001'].shape[0])
        self.frame.setNumberOfSamples(file['S01']['B001'].shape[1])
        self.frame.setSensingStart(sensingStart)
        self.frame.setSensingMid(sensingMid)
        self.frame.setSensingStop(sensingStop)

        rangePixelSize = self.frame.getInstrument().getRangePixelSize()
        #Spurious factor of 2 removed - PSA
        farRange = slantRange +  self.frame.getNumberOfSamples()*rangePixelSize
        self.frame.setFarRange(farRange)


    def _populateOrbit(self,file):
        orbit = self.frame.getOrbit()

        orbit.setReferenceFrame('ECR')
        orbit.setOrbitSource('Header')
        t0 = datetime.datetime.strptime(file.attrs['Reference UTC'].decode('utf-8'),'%Y-%m-%d %H:%M:%S.%f000')
        t = file.attrs['State Vectors Times']
        position = file.attrs['ECEF Satellite Position']
        velocity = file.attrs['ECEF Satellite Velocity']

        for i in range(len(position)):
            vec = StateVector()
            dt = t0 + datetime.timedelta(seconds=t[i])
            vec.setTime(dt)
            vec.setPosition([position[i,0],position[i,1],position[i,2]])
            vec.setVelocity([velocity[i,0],velocity[i,1],velocity[i,2]])
            orbit.addStateVector(vec)

    def populateImage(self,filename):
        rawImage = isceobj.createRawImage()
        rawImage.setByteOrder('l')
        rawImage.setFilename(filename)
        rawImage.setAccessMode('read')
        rawImage.setWidth(2*self.frame.getNumberOfSamples())
        rawImage.setXmax(2*self.frame.getNumberOfSamples())
        rawImage.setXmin(0)
        self.getFrame().setImage(rawImage)

    def _populateExtras(self, file):
        """
        Populate some extra fields.
        """

        self.dopplerRangeTime = file.attrs['Centroid vs Range Time Polynomial']
        self.dopplerAzimuthTime = file.attrs['Centroid vs Azimuth Time Polynomial']
        self.rangeRefTime = file.attrs['Range Polynomial Reference Time']
        self.azimuthRefTime = file.attrs['Azimuth Polynomial Reference Time']
        ####Lazy fix for testing - PSA
        self.rangeFirstTime = self.rangeRefTime
        self.rangeLastTime = self.rangeRefTime


    def extractImage(self):
        """Extract the raw image data"""
        import os
        from ctypes import cdll, c_char_p
        extract_csk = cdll.LoadLibrary(os.path.dirname(__file__)+'/csk.so')
        # Prepare and run the C-based extractor

        #check if the input is a string. if so put it into one element list
        if(isinstance(self.hdf5FileList,str)):
            self.hdf5FileList = [self.hdf5FileList]

        for i in range(len(self.hdf5FileList)):
            #need to create a new instance every time
            self.frame = Frame()
            self.frame.configure()
            appendStr = '_' + str(i)
            # if more than one file to contatenate that create different outputs
            # but suffixing _i
            if(len(self.hdf5FileList) == 1):
                appendStr = ''
            outputNow = self.output + appendStr
            self.hdf5 = self.hdf5FileList[i]
            inFile_c = c_char_p(bytes(self.hdf5,'utf-8'))
            outFile_c = c_char_p(bytes(outputNow,'utf-8'))

            extract_csk.extract_csk(inFile_c,outFile_c)
            # Now, populate the metadata
            try:
                fp = h5py.File(self.hdf5,'r')
            except Exception as strerror:
                self.logger.error("IOError: %s\n" % strerror)
                return
            self.populateMetadata(file=fp)
            self.populateImage(outputNow)
            self._populateExtras(fp)

            fp.close()
            self.frameList.append(self.frame)
            createAuxFile(self.frame,outputNow + '.aux')
        self._imageFileList = self.hdf5FileList
        return tkfunc(self)


    def _parseNanoSecondTimeStamp(self,timestamp):
        """Parse a date-time string with nanosecond precision and return a
        datetime object
        """
        dateTime,nanoSeconds = timestamp.decode('utf-8').split('.')
        microsec = float(nanoSeconds)*1e-3
        dt = datetime.datetime.strptime(dateTime,'%Y-%m-%d %H:%M:%S')
        dt = dt + datetime.timedelta(microseconds=microsec)
        return dt

    def extractDoppler(self):
        """
        Return the doppler centroid as defined in the HDF5 file.
        """
        quadratic = {}
        midtime = (self.rangeLastTime + self.rangeFirstTime)*0.5 - self.rangeRefTime
        fd_mid = self.dopplerRangeTime[0] + self.dopplerRangeTime[1]*midtime + self.dopplerRangeTime[2]*midtime*midtime

        quadratic['a'] = fd_mid/self.frame.getInstrument().getPulseRepetitionFrequency()
        quadratic['b'] = 0.
        quadratic['c'] = 0.
        return quadratic
