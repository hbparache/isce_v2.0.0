#!/usr/bin/env python3 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2014 to the present, California Institute of Technology.
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




from xml.etree.ElementTree import ElementTree
import datetime
import isceobj
from isceobj.Scene.Frame import Frame
from isceobj.Planet.Planet import Planet
from isceobj.Orbit.Orbit import StateVector, Orbit
from isceobj.Orbit.OrbitExtender import OrbitExtender
from isceobj.Planet.AstronomicalHandbook import Const
from iscesys.Component.Component import Component
from iscesys.DateTimeUtil.DateTimeUtil import DateTimeUtil as DTUtil
import os
import numpy as np

sep = "\n"
tab = "    "
lookMap = { 'RIGHT' : -1,
            'LEFT' : 1}

class Sentinel1A(Component):
    """
        A Class representing RadarSAT 2 data
    """
    def __init__(self):
        Component.__init__(self)        
        self.xml = None
        self.tiff = None
        self.output = None
        self.gdal_translate = None
        self.frame = Frame()
        self.frame.configure()
    
        self._xml_root=None
        self.descriptionOfVariables = {}
        self.dictionaryOfVariables = {'XML': ['self.xml','str','mandatory'],
                                      'TIFF': ['self.tiff','str','mandatory'],
                                      'OUTPUT': ['self.output','str','optional'],
                                      'GDAL_TRANSLATE': ['self.gdal_translate','str','optional']}                        
        
                                               
    def getFrame(self):
        return self.frame
    
    def parse(self):
        try:
            fp = open(self.xml,'r')
        except IOError as strerr:
            print("IOError: %s" % strerr)
            return
        self._xml_root = ElementTree(file=fp).getroot()                     
#        self.product.set_from_etnode(self._xml_root)
        self.populateMetadata()
        
        fp.close()

    def grab_from_xml(self, path):
        try:
            res = self._xml_root.find(path).text
        except:
            raise Exception('Tag= %s not found'%(path))

        if res is None:
            raise Exception('Tag = %s not found'%(path))

        return res

    def convertToDateTime(self, string):
        dt = datetime.datetime.strptime(string,"%Y-%m-%dT%H:%M:%S.%f")
        return dt

    
    def populateMetadata(self):
        """
            Create metadata objects from the metadata files
        """
        ####Set each parameter one - by - one
        mission = self.grab_from_xml('adsHeader/missionId')
        swath = self.grab_from_xml('adsHeader/swath')
        polarization = self.grab_from_xml('adsHeader/polarisation')

        frequency = float(self.grab_from_xml('generalAnnotation/productInformation/radarFrequency'))
        passDirection = self.grab_from_xml('generalAnnotation/productInformation/pass')

        rangePixelSize = float(self.grab_from_xml('imageAnnotation/imageInformation/rangePixelSpacing'))
        azimuthPixelSize = float(self.grab_from_xml('imageAnnotation/imageInformation/azimuthPixelSpacing'))
        rangeSamplingRate = Const.c/(2.0*rangePixelSize)
        prf = 1.0/float(self.grab_from_xml('imageAnnotation/imageInformation/azimuthTimeInterval'))

        lines = int(self.grab_from_xml('imageAnnotation/imageInformation/numberOfLines'))
        samples = int(self.grab_from_xml('imageAnnotation/imageInformation/numberOfSamples'))

        startingRange = float(self.grab_from_xml('imageAnnotation/imageInformation/slantRangeTime'))*Const.c/2.0
        incidenceAngle = float(self.grab_from_xml('imageAnnotation/imageInformation/incidenceAngleMidSwath'))
        dataStartTime = self.convertToDateTime(self.grab_from_xml('imageAnnotation/imageInformation/productFirstLineUtcTime'))
        dataStopTime = self.convertToDateTime(self.grab_from_xml('imageAnnotation/imageInformation/productLastLineUtcTime'))


        pulseLength = float(self.grab_from_xml('generalAnnotation/downlinkInformationList/downlinkInformation/downlinkValues/txPulseLength'))
        chirpSlope = float(self.grab_from_xml('generalAnnotation/downlinkInformationList/downlinkInformation/downlinkValues/txPulseRampRate'))
        pulseBandwidth = pulseLength * chirpSlope

        ####Sentinel is always right looking
        lookSide = -1
        facility = 'EU'
        version = '1.0'


#        height = self.product.imageGenerationParameters.sarProcessingInformation._satelliteHeight

        ####Populate platform
        platform = self.frame.getInstrument().getPlatform()
        platform.setPlanet(Planet("Earth"))
        platform.setMission(mission)
        platform.setPointingDirection(lookSide)
        platform.setAntennaLength(2*azimuthPixelSize)

        ####Populate instrument
        instrument = self.frame.getInstrument()
        instrument.setRadarFrequency(frequency)
        instrument.setPulseRepetitionFrequency(prf)
        instrument.setPulseLength(pulseLength)
        instrument.setChirpSlope(pulseBandwidth/pulseLength)
        instrument.setIncidenceAngle(incidenceAngle)
        #self.frame.getInstrument().setRangeBias(0)
        instrument.setRangePixelSize(rangePixelSize)
        instrument.setRangeSamplingRate(rangeSamplingRate)
        instrument.setBeamNumber(swath)
        instrument.setPulseLength(pulseLength)


        #Populate Frame
        #self.frame.setSatelliteHeight(height)
        self.frame.setSensingStart(dataStartTime)
        self.frame.setSensingStop(dataStopTime)
        diffTime = DTUtil.timeDeltaToSeconds(dataStopTime - dataStartTime)/2.0
        sensingMid = dataStartTime + datetime.timedelta(microseconds=int(diffTime*1e6))
        self.frame.setSensingMid(sensingMid)
        self.frame.setPassDirection(passDirection)
        self.frame.setPolarization(polarization) 
        self.frame.setStartingRange(startingRange)
        self.frame.setFarRange(startingRange + (samples-1)*rangePixelSize)
        self.frame.setNumberOfLines(lines)
        self.frame.setNumberOfSamples(samples)
        self.frame.setProcessingFacility(facility)
        self.frame.setProcessingSoftwareVersion(version)
        
        self.frame.setPassDirection(passDirection)
        self.extractOrbit()

        
    def extractOrbit(self):
        '''
        Extract orbit information from xml node.
        '''
        node = self._xml_root.find('generalAnnotation/orbitList')
        frameOrbit = self.frame.getOrbit()
        frameOrbit.setOrbitSource('Header')

        for child in node.getchildren():
            timestamp = self.convertToDateTime(child.find('time').text)
            pos = []
            vel = []
            posnode = child.find('position')
            velnode = child.find('velocity')
            for tag in ['x','y','z']:
                pos.append(float(posnode.find(tag).text))

            for tag in ['x','y','z']:
                vel.append(float(velnode.find(tag).text))

            vec = StateVector()
            vec.setTime(timestamp)
            vec.setPosition(pos)
            vec.setVelocity(vel)
            frameOrbit.addStateVector(vec)


    def extractImage(self):
        """
           Use gdal_translate to extract the slc
        """
        import tempfile
        import subprocess        

        if (not self.gdal_translate):
            raise TypeError("The path to executable gdal_translate was not specified")
        if (not os.path.exists(self.gdal_translate)):
            raise OSError("Could not find gdal_translate in directory %s" % os.path.dirname(self.gdal_translate))

        self.parse()
        # Use GDAL to convert the geoTIFF file to an raster image
        # There should be a way to do this using the GDAL python api
        curdir = os.getcwd()
        tempdir = tempfile.mkdtemp(dir=curdir)
#        os.rmdir(tempdir) # Wasteful, but if the directory exists, gdal_translate freaks out
        #instring = 'RADARSAT_2_CALIB:UNCALIB:%s' % self.xml
        #process = subprocess.Popen([self.gdal_translate,'-of','MFF2','-ot','CFloat32',instring,tempdir])
        if (self.tiff is None) or (not os.path.exists(self.tiff)):
            raise Exception('Path to input tiff file: %s is wrong or file doesnt exist.'%(self.tiff))

        process = subprocess.Popen([self.gdal_translate, self.tiff.strip(), '-of', 'ENVI', '-ot', 'CFloat32', '-co', 'INTERLEAVE=BIP',os.path.join(tempdir, 'image_data')])
        process.wait()
   
        # Move the output of the gdal_translate call to a reasonable file name

        width = self.frame.getNumberOfSamples()
        lgth = self.frame.getNumberOfLines()

        os.rename(os.path.join(tempdir,'image_data'), self.output)

#       os.unlink(os.path.join(tempdir,'attrib'))
        os.unlink(os.path.join(tempdir,'image_data.hdr'))
        os.rmdir(tempdir)


        ####
        slcImage = isceobj.createSlcImage()
        slcImage.setByteOrder('l')
        slcImage.setFilename(self.output)
        slcImage.setAccessMode('read')
        slcImage.setWidth(self.frame.getNumberOfSamples())
        slcImage.setLength(self.frame.getNumberOfLines())
        slcImage.setXmin(0)
        slcImage.setXmax(self.frame.getNumberOfSamples())
        self.frame.setImage(slcImage)

    def extractDoppler(self):
        '''
        self.parse()
        Extract doppler information as needed by mocomp
        '''
#        ins = self.frame.getInstrument()
#        dc = self.product.imageGenerationParameters.dopplerCentroid
        quadratic = {}

#        r0 = self.frame.startingRange
#        fs = ins.getRangeSamplingRate()
#        tNear = 2*r0/Const.c

#        tMid = tNear + 0.5*self.frame.getNumberOfSamples()/fs
#        t0 = dc.dopplerCentroidReferenceTime
#        poly = dc.dopplerCentroidCoefficients
       
#        fd_mid = 0.0
#        for kk in range(len(poly)):
#            fd_mid += poly[kk] * (tMid - t0)**kk
        
#        quadratic['a'] = fd_mid / ins.getPulseRepetitionFrequency()
        quadratic['a'] = 0.
        quadratic['b'] = 0.
        quadratic['c'] = 0.
        return quadratic

