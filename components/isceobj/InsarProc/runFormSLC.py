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
import stdproc
import isceobj

logger = logging.getLogger('isce.insar.runFormSLC')

#Run FormSLC for master
def master(self, deltaf=None):
    from isceobj.Catalog import recordInputsAndOutputs
    from iscesys.ImageUtil.ImageUtil import ImageUtil as IU

    v,h = self.insar.vh()

    objRaw = self.insar.masterRawImage.copy(access_mode='read')
    objFormSlc = stdproc.createFormSLC(name='insarapp_formslc_master')
    objFormSlc.setBodyFixedVelocity(v)
    objFormSlc.setSpacecraftHeight(h)
    objFormSlc.setAzimuthPatchSize(self.patchSize)
    objFormSlc.setNumberValidPulses(self.goodLines)
    objFormSlc.setNumberPatches(self.numPatches)
    objFormSlc.setLookSide(self.insar._lookSide)
    objFormSlc.setNumberAzimuthLooks(self.insar.numberAzimuthLooks)
    logger.info("Focusing Master image")
    objFormSlc.stdWriter = self.stdWriter

    if (deltaf is not None) and (objFormSlc.azimuthResolution is None):
        ins = self.insar.masterFrame.getInstrument()
        prf = ins.getPulseRepetitionFrequency()
        res = ins.getPlatform().getAntennaLength() / 2.0
        azbw = min(v/res, prf)
        factor = 1.0 - (abs(deltaf)/azbw)
        logger.info('MASTER AZIMUTH BANDWIDTH FACTOR = %f'%(factor))
        azres = res / factor
        objFormSlc.setAzimuthResolution(azres)
    

    objSlc = objFormSlc(rawImage=objRaw,
                orbit=self.insar.masterOrbit,
                frame=self.insar.masterFrame,
                planet=self.insar.masterFrame.instrument.platform.planet,
                doppler=self.insar.dopplerCentroid,
                peg=self.insar.peg)

    imageSlc = isceobj.createSlcImage()
    IU.copyAttributes(objSlc, imageSlc)
    imageSlc.setAccessMode('read')
    objSlc.finalizeImage()
    objRaw.finalizeImage()
    recordInputsAndOutputs(self.insar.procDoc, objFormSlc,
        "runFormSLC.master", logger, "runFormSLC.master")

    logger.info('New Width = %d'%(imageSlc.getWidth()))
    self.insar.masterSlcImage = imageSlc
    self.insar.formSLC1 = objFormSlc
    return objFormSlc.numberPatches

#Run FormSLC on slave
def slave(self, deltaf=None):
    from isceobj.Catalog import recordInputsAndOutputs
    from iscesys.ImageUtil.ImageUtil import ImageUtil as IU

    v,h = self.insar.vh()

    objRaw = self.insar.slaveRawImage.copy(access_mode='read')
    objFormSlc = stdproc.createFormSLC(name='insarapp_formslc_slave')
    objFormSlc.setBodyFixedVelocity(v)
    objFormSlc.setSpacecraftHeight(h)
    objFormSlc.setAzimuthPatchSize(self.patchSize)
    objFormSlc.setNumberValidPulses(self.goodLines)
    objFormSlc.setNumberPatches(self.numPatches)
    objFormSlc.setNumberAzimuthLooks(self.insar.numberAzimuthLooks)
    objFormSlc.setLookSide(self.insar._lookSide)
    logger.info("Focusing Master image")
    objFormSlc.stdWriter = self.stdWriter

    if (deltaf is not None) and (objFormSlc.azimuthResolution is None):
        ins = self.insar.slaveFrame.getInstrument()
        prf = ins.getPulseRepetitionFrequency()
        res = ins.getPlatform().getAntennaLength()/2.0
        azbw = min(v / res, prf)
        factor = 1.0 - (abs(deltaf) / azbw)
        logger.info('SLAVE AZIMUTH BANDWIDTH FACTOR = %f'%(factor))
        azres = res/factor
        objFormSlc.setAzimuthResolution(azres)

    objSlc = objFormSlc(rawImage=objRaw,
                orbit=self.insar.slaveOrbit,
                frame=self.insar.slaveFrame,
                planet=self.insar.slaveFrame.instrument.platform.planet,
                doppler=self.insar.dopplerCentroid,
                peg=self.insar.peg)

    imageSlc = isceobj.createSlcImage()
    IU.copyAttributes(objSlc, imageSlc)
    imageSlc.setAccessMode('read')
    objSlc.finalizeImage()
    objRaw.finalizeImage()
    recordInputsAndOutputs(self.insar.procDoc, objFormSlc,
        "runFormSLC.slave", logger, "runFormSLC.slave")

    logger.info('New Width = %d'%(imageSlc.getWidth()))
    self.insar.slaveSlcImage = imageSlc
    self.insar.formSLC2 = objFormSlc
    return objFormSlc.numberPatches

def runFormSLC(self):

    mDoppler = self.insar.masterDoppler.getDopplerCoefficients(inHz=True)
    sDoppler = self.insar.slaveDoppler.getDopplerCoefficients(inHz=True)
    deltaf = abs(mDoppler[0] - sDoppler[0])
    n_master = master(self, deltaf=deltaf)
    n_slave = slave(self, deltaf=deltaf)
    self.insar.setNumberPatches(min(n_master, n_slave))
    self.is_mocomp = int(
        (self.insar.formSLC1.azimuthPatchSize -
         self.insar.formSLC1.numberValidPulses)/2
        )
    self.insar.is_mocomp = self.is_mocomp
    self.insar.patchSize = self.insar.formSLC1.azimuthPatchSize
    self.insar.numberValidPulses = self.insar.formSLC1.numberValidPulses
    logger.info('Number of Valid Pulses = %d'%(self.insar.numberValidPulses))

    return None
