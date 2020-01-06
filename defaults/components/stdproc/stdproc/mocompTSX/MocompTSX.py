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
from iscesys.Component.Component import Component, Port
from iscesys.Compatibility import Compatibility
from isceobj.Image.Image import Image
from stdproc.stdproc.mocompTSX import mocompTSX
from iscesys.ImageUtil.ImageUtil import ImageUtil as IU

class MocompTSX(Component):

    def mocomptsx(self):
        for port in self.inputPorts:
            port()

        try:
            self.inAccessor = self.slcInImage.getImagePointer()
        except AttributeError:
            self.logger.error("Error in accessing image pointers")
            raise AttributeError("Error in accessing image pointers")

        if self.stdWriter is None:
            self.createStdWriter()

        self.createOutSlcImage()
        self.outAccessor = self.slcOutImage.getImagePointer()
        self.allocateArrays()
        self.setState()
        mocompTSX.mocompTSX_Py(self.inAccessor, self.outAccessor)
        self.mocompPositionSize = mocompTSX.getMocompPositionSize_Py()
        self.dim1_mocompPosition = 2
        self.dim2_mocompPosition = self.mocompPositionSize
        self.dim1_mocompIndex = self.mocompPositionSize
        self.getState()
        self.deallocateArrays()
        self.slcOutImage.renderHdr()
        self.slcOutImage.finalizeImage()

        return self.slcOutImage


    def createStdWriter(self):
        from iscesys.StdOEL.StdOELPy import create_writer
        self._stdWriter = create_writer(
        "log", "",True,"insar.log"
        ).set_file_tags("formslcTSX", "log", "err", "out")
        return None
        
    ## TODO: use slcInImage's method to make new image.
    def createOutSlcImage(self):
        """
        Create the output SCL image based on the input image information.
        If self.slcOutImageName is not set that the default is the input image name
        preceded by 'mocomp'. 
        """
        import isceobj
        self.slcOutImage = isceobj.createSlcImage()
        IU.copyAttributes(self.slcInImage, self.slcOutImage)
        if self.slcOutImageName:
            name = self.slcOutImageName
        else:
            name = 'mocomp' + self.slcInImage.getFilename().capitalize()
            self.slcOutImage.setFilename(name)

        self.slcOutImage.setAccessMode('write')
        self.slcOutImage.createImage()
        return None
        

    def setState(self):
        mocompTSX.setStdWriter_Py(int(self.stdWriter))
        mocompTSX.setNumberRangeBins_Py(int(self.numberRangeBins))
        mocompTSX.setNumberAzLines_Py(int(self.numberAzLines))
        mocompTSX.setDopplerCentroidCoefficients_Py(self.dopplerCentroidCoefficients, self.dim1_dopplerCentroidCoefficients)
        mocompTSX.setTime_Py(self.time, self.dim1_time)
        mocompTSX.setPosition_Py(self.position, self.dim1_position, self.dim2_position)
        mocompTSX.setPlanetLocalRadius_Py(float(self.planetLocalRadius))
        mocompTSX.setBodyFixedVelocity_Py(float(self.bodyFixedVelocity))
        mocompTSX.setSpacecraftHeight_Py(float(self.spacecraftHeight))
        mocompTSX.setPRF_Py(float(self.prf))
        mocompTSX.setRangeSamplingRate_Py(float(self.rangeSamplingRate))
        mocompTSX.setRadarWavelength_Py(float(self.radarWavelength))
        mocompTSX.setRangeFisrtSample_Py(float(self.rangeFirstSample))
        mocompTSX.setLookSide_Py(int(self.lookSide))

        return None


    def setSlcInImage(self,img):
        self.slcInImage = img

    def setSlcOutImageName(self,name):
        self.slcOutImageName = name

    def setNumberRangeBins(self,var):
        self.numberRangeBins = int(var)
        return

    def setNumberAzLines(self,var):
        self.numberAzLines = int(var)
        return

    def setLookSide(self,var):
        self.lookSide = int(var)
        return

    def setDopplerCentroidCoefficients(self,var):
        self.dopplerCentroidCoefficients = var
        return

    def setTime(self,var):
        self.time = var
        return

    def setPosition(self,var):
        self.position = var
        return

    def setPlanetLocalRadius(self,var):
        self.planetLocalRadius = float(var)
        return

    def setBodyFixedVelocity(self,var):
        self.bodyFixedVelocity = float(var)
        return

    def setSpacecraftHeight(self,var):
        self.spacecraftHeight = float(var)
        return

    def setPRF(self,var):
        self.prf = float(var)
        return

    def setRangeSamplingRate(self,var):
        self.rangeSamplingRate = float(var)
        return

    def setRadarWavelength(self,var):
        self.radarWavelength = float(var)
        return

    def setRangeFisrtSample(self,var):
        self.rangeFirstSample = float(var)
        return

    def getState(self):
        self.mocompIndex = mocompTSX.getMocompIndex_Py(self.dim1_mocompIndex)
        self.mocompPosition = mocompTSX.getMocompPosition_Py(self.dim1_mocompPosition, self.dim2_mocompPosition)
        self.startingRange = mocompTSX.getStartingRange_Py()
        return None

    def getMocompIndex(self):
        return self.mocompIndex

    def getMocompPosition(self, index=None):
        return self.mocompPosition[index] if index else self.mocompPosition

    def getMocompPositionSize(self):
        return self.mocompPositionSize

    def getMocompImage(self):
        return self.slcOutImage

    def allocateArrays(self):
        if (self.dim1_dopplerCentroidCoefficients == None):
            self.dim1_dopplerCentroidCoefficients = len(self.dopplerCentroidCoefficients)

        if (not self.dim1_dopplerCentroidCoefficients):
            print("Error. Trying to allocate zero size array")

            raise Exception

        mocompTSX.allocate_dopplerCentroidCoefficients_Py(self.dim1_dopplerCentroidCoefficients)

        if (self.dim1_time == None):
            self.dim1_time = len(self.time)

        if (not self.dim1_time):
            print("Error. Trying to allocate zero size array")

            raise Exception

        mocompTSX.allocate_time_Py(self.dim1_time)

        if (self.dim1_position == None):
            self.dim1_position = len(self.position)
            self.dim2_position = len(self.position[0])

        if (not self.dim1_position) or (not self.dim2_position):
            print("Error. Trying to allocate zero size array")

            raise Exception

        mocompTSX.allocate_sch_Py(self.dim1_position, self.dim2_position)
        return None

    def deallocateArrays(self):
        mocompTSX.deallocate_dopplerCentroidCoefficients_Py()
        mocompTSX.deallocate_time_Py()
        mocompTSX.deallocate_sch_Py()
        return None
    
    def addOrbit(self):
        orbit = self._inputPorts.getPort('orbit').getObject()
        if (orbit):
            try:
                (time,position,velocity,offset) = orbit._unpackOrbit()
                self.time = time
                self.position = position
            except AttributeError:
                self.logger.error("Object %s requires an _unpackOrbit() method" % (orbit.__class__))
                raise AttributeError
    def addDoppler(self):
        doppler = self._inputPorts.getPort('doppler').getObject()
        if (doppler):
            try:
                self.dopplerCentroidCoefficients = doppler.getDopplerCoefficients(inHz=False)
                self.dim1_dopplerCentroidCoefficients = len(self.dopplerCentroidCoefficients)
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError

    def addSlcInImage(self):
        image = self._inputPorts.getPort('slcInImage').getObject()
        #check only if it is an instance of Image which is the base class
        if (image):
            if (isinstance(image,Image)):
                self.slcInImage = image
                self.numberRangeBins = self.slcInImage.getWidth()
                self.numberAzLines = self.slcInImage.getLength()
            else:
                self.logger.error("Object %s must be an instance of Image" %(image))
    
    
    def addFrame(self):
        frame = self._inputPorts.getPort('frame').getObject()
        if (frame):
            try:
                self.rangeFirstSample = frame.getStartingRange()            
                instrument = frame.getInstrument()
                self.rangeSamplingRate = instrument.getRangeSamplingRate()
                self.radarWavelength = instrument.getRadarWavelength()
                self.prf = instrument.getPulseRepetitionFrequency()                
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError
    def addPeg(self):
        peg = self._inputPorts.getPort('peg').getObject()
        if (peg):
            try:
                self.planetLocalRadius = peg.getRadiusOfCurvature()
            except AttributeError as strerr:
                self.logger.error(strerr)
                raise AttributeError
            pass
        return None

    logging_name = 'isce.mocompTSX'

    def __init__(self):
        super(MocompTSX,self).__init__()
        self.inAccessor = None
        self.outAccessor = None
        self.numberRangeBins = None
        self.numberAzLines = None
        self.dopplerCentroidCoefficients = []
        self.dim1_dopplerCentroidCoefficients = None
        self.time = []
        self.dim1_time = None
        self.position = []
        self.dim1_position = None
        self.dim2_position = None
        self.planetLocalRadius = None
        self.bodyFixedVelocity = None
        self.spacecraftHeight = None
        self.prf = None
        self.rangeSamplingRate = None
        self.radarWavelength = None
        self.rangeFirstSample = None
        self.startingRange = None
        self.mocompIndex = []
        self.dim1_mocompIndex = None
        self.mocompPositionSize = None
        self.slcOutImageName = ""
        self.slcInImage = None
        self.slcOutImage = None
        self.lookSide = -1    #Right looking by default
        
#        self.logger = logging.getLogger('isce.mocompTSX')
#        self.createPorts()

        self.dictionaryOfVariables = {
            'STD_WRITER' : ['stdWriter', 'int','optional'], 
            'NUMBER_RANGE_BINS' : ['numberRangeBins', 'int','optional'], 
            'NUMBER_AZ_LINES' : ['numberAzLines', 'int','optional'], 
            'DOPPLER_CENTROID_COEFFICIENTS' : ['dopplerCentroidCoefficients', 'float','mandatory'], 
            'TIME' : ['time', 'float','mandatory'], 
            'POSITION' : ['position', '','mandatory'], 
            'PLANET_LOCAL_RADIUS' : ['planetLocalRadius', 'float','mandatory'], 
            'BODY_FIXED_VELOCITY' : ['bodyFixedVelocity', 'float','mandatory'], 
            'SPACECRAFT_HEIGHT' : ['spacecraftHeight', 'float','mandatory'], 
            'PRF' : ['prf', 'float','mandatory'], 
            'RANGE_SAMPLING_RATE' : ['rangeSamplingRate', 'float','mandatory'], 
            'RADAR_WAVELENGTH' : ['radarWavelength', 'float','mandatory'], 
            'RANGE_FIRST_SAMPLE' : ['rangeFirstSample', 'float','mandatory'] 
            }
        self.dictionaryOfOutputVariables = {
            'MOCOMP_INDEX' : 'mocompIndex', 
            'MOCOMP_POSITION' : 'mocompPosition', 
            'MOCOMP_POSITION_SIZE' : 'mocompPositionSize' 
            }
        
        self.descriptionOfVariables = {}
        self.mandatoryVariables = []
        self.optionalVariables = []
        self.initOptionalAndMandatoryLists()
        return None

    def createPorts(self):
        slcInImagePort = Port(name='slcInImage',method=self.addSlcInImage)
        pegPort = Port(name='peg',method=self.addPeg)
        framePort = Port(name='frame',method=self.addFrame)
        dopplerPort = Port(name='doppler',method=self.addDoppler)
        orbitPort = Port(name='orbit',method=self.addOrbit)

        self._inputPorts.add(slcInImagePort)
        self._inputPorts.add(pegPort)
        self._inputPorts.add(dopplerPort)
        self._inputPorts.add(framePort)
        self._inputPorts.add(orbitPort)

        return None





#end class



