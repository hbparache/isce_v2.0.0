#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2012 to the present, California Institute of Technology.
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
# Author: Brett George
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import logging
import isceobj
import mroipac
from mroipac.baseline.Baseline import Baseline
logger = logging.getLogger('isce.insar.runPreprocessor')

def runPreprocessor(self):
     
    master = make_raw(self.master, self.masterdop)
    slave = make_raw(self.slave, self.slavedop)
    self._insar.numberRangeBins = master.frame.numberRangeBins
    #add raw images to main object
    masterRaw = initRawImage(master)
    self._insar.setMasterRawImage(masterRaw)
    slaveRaw = initRawImage(slave)
    self._insar.setSlaveRawImage(slaveRaw)
    
    #add frames to main  object
    self._insar.setMasterFrame(master.frame)
    self._insar.setSlaveFrame(slave.frame)
    
    #add doppler to main object
    self._insar.setMasterDoppler(master.getDopplerValues())
    self._insar.setSlaveDoppler(slave.getDopplerValues())
    
    #add squints to main object
    self._insar.setMasterSquint(master.getSquint())
    self._insar.setSlaveSquint(slave.getSquint())

    #add look direction
    self._insar.setLookSide(master.frame.getInstrument().getPlatform().pointingDirection)
    
    catalog = isceobj.Catalog.createCatalog(self._insar.procDoc.name)

    frame = self._insar.getMasterFrame()
    instrument = frame.getInstrument()
    platform = instrument.getPlatform()    

    planet = platform.getPlanet()
    catalog.addInputsFrom(planet, 'planet')
    catalog.addInputsFrom(planet.get_elp(), 'planet.ellipsoid')

    catalog.addInputsFrom(master.sensor, 'master.sensor')
    catalog.addItem('width', masterRaw.getWidth(), 'master')
    catalog.addItem('xmin', masterRaw.getXmin(), 'master')
    catalog.addItem('iBias', instrument.getInPhaseValue(), 'master')
    catalog.addItem('qBias', instrument.getQuadratureValue(), 'master')
    catalog.addItem('range_sampling_rate', instrument.getRangeSamplingRate(), 'master')
    catalog.addItem('prf', instrument.getPulseRepetitionFrequency(), 'master')
    catalog.addItem('pri', 1.0/instrument.getPulseRepetitionFrequency(), 'master')
    catalog.addItem('pulse_length', instrument.getPulseLength(), 'master')
    catalog.addItem('chirp_slope', instrument.getChirpSlope(), 'master')
    catalog.addItem('wavelength', instrument.getRadarWavelength(), 'master')
    catalog.addItem('lookSide', platform.pointingDirection, 'master')
    catalog.addInputsFrom(frame, 'master.frame')
    catalog.addInputsFrom(instrument, 'master.instrument')
    catalog.addInputsFrom(platform, 'master.platform')


    frame = self._insar.getSlaveFrame()
    instrument = frame.getInstrument()
    platform = instrument.getPlatform()    

    catalog.addInputsFrom(slave.sensor, 'slave.sensor')
    catalog.addItem('width', slaveRaw.getWidth(), 'slave')
    catalog.addItem('xmin', slaveRaw.getXmin(), 'slave')
    catalog.addItem('iBias', instrument.getInPhaseValue(), 'slave')
    catalog.addItem('qBias', instrument.getQuadratureValue(), 'slave')
    catalog.addItem('range_sampling_rate', instrument.getRangeSamplingRate(), 'slave')
    catalog.addItem('prf', instrument.getPulseRepetitionFrequency(), 'slave')
    catalog.addItem('pri', 1.0/instrument.getPulseRepetitionFrequency(), 'slave')
    catalog.addItem('pulse_length', instrument.getPulseLength(), 'slave')
    catalog.addItem('chirp_slope', instrument.getChirpSlope(), 'slave')
    catalog.addItem('wavelength', instrument.getRadarWavelength(), 'slave')
    catalog.addItem('lookSide', platform.pointingDirection, 'slave')
    catalog.addInputsFrom(frame, 'slave.frame')
    catalog.addInputsFrom(instrument, 'slave.instrument')
    catalog.addInputsFrom(platform, 'slave.platform')


    baseObj = Baseline()
    baseObj.wireInputPort(name='masterFrame',object=self._insar.getMasterFrame())
    baseObj.wireInputPort(name='slaveFrame',object=self._insar.getSlaveFrame())
    baseObj.baseline()

    catalog.addItem('horizontal_baseline_top', baseObj.hBaselineTop, 'baseline')
    catalog.addItem('horizontal_baseline_rate', baseObj.hBaselineRate, 'baseline')
    catalog.addItem('horizontal_baseline_acc', baseObj.hBaselineAcc, 'baseline')
    catalog.addItem('vertical_baseline_top', baseObj.vBaselineTop, 'baseline')
    catalog.addItem('vertical_baseline_rate', baseObj.vBaselineRate, 'baseline')
    catalog.addItem('vertical_baseline_acc', baseObj.vBaselineAcc, 'baseline')
    catalog.addItem('perp_baseline_top', baseObj.pBaselineTop, 'baseline')
    catalog.addItem('perp_baseline_bottom', baseObj.pBaselineBottom, 'baseline')

    catalog.printToLog(logger, "runPreprocessor")
    self._insar.procDoc.addAllFromCatalog(catalog)

def make_raw(sensor, doppler):
    from make_raw import make_raw
    objMakeRaw = make_raw()
    objMakeRaw(sensor=sensor, doppler=doppler)
    return objMakeRaw

def initRawImage(makeRawObj):
    from isceobj.Image import createSlcImage
    from isceobj.Image import createRawImage
    #the "raw" image in same case is an slc.
    #for now let's do it in this way. probably need to make this a factory
    #instantiated based on the sensor type
    imageType = makeRawObj.frame.getImage()
    if isinstance(imageType, createRawImage().__class__):
        filename = makeRawObj.frame.getImage().getFilename()
        bytesPerLine = makeRawObj.frame.getImage().getXmax()
        goodBytes = makeRawObj.frame.getImage().getXmax() - makeRawObj.frame.getImage().getXmin()
        logger.debug("bytes_per_line: %s" % (bytesPerLine))
        logger.debug("good_bytes_per_line: %s" % (goodBytes))
        objRaw = createRawImage()
        objRaw.setFilename(filename)
        
        objRaw.setNumberGoodBytes(goodBytes)
        objRaw.setWidth(bytesPerLine)
        objRaw.setXmin(makeRawObj.frame.getImage().getXmin())
        objRaw.setXmax(bytesPerLine)
    elif(isinstance(imageType,createSlcImage().__class__)):
        objRaw = createSlcImage()
        filename = makeRawObj.frame.getImage().getFilename()
        bytesPerLine = makeRawObj.frame.getImage().getXmax()
        objRaw.setFilename(filename)
        objRaw.setWidth(bytesPerLine)
        objRaw.setXmin(makeRawObj.frame.getImage().getXmin())
        objRaw.setXmax(bytesPerLine)
    return objRaw
