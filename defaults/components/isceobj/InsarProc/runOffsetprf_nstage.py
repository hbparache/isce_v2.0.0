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
# Author: Gaiangi Sacco
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import logging
import isceobj
import mroipac
import numpy
from iscesys.ImageUtil.ImageUtil import ImageUtil as IU
from isceobj import Constants as CN
from mroipac.ampcor.NStage import NStage

logger = logging.getLogger('isce.insar.runOffsetprf')

def runOffsetprf(self):
    from isceobj.Catalog import recordInputs, recordOutputs

    masterFrame = self._insar.getMasterFrame()
    slaveFrame = self._insar.getSlaveFrame()
    masterOrbit = self._insar.getMasterOrbit()
    slaveOrbit = self._insar.getSlaveOrbit()
    prf1 = masterFrame.getInstrument().getPulseRepetitionFrequency()
    prf2 = slaveFrame.getInstrument().getPulseRepetitionFrequency()
    nearRange1 = self.insar.formSLC1.startingRange
    nearRange2 = self.insar.formSLC2.startingRange
    fs1 = masterFrame.getInstrument().getRangeSamplingRate()
    fs2 = slaveFrame.getInstrument().getRangeSamplingRate()

    ###There seems to be no other way of determining image length - Piyush
    patchSize = self._insar.getPatchSize()
    numPatches = self._insar.getNumberPatches()
    valid_az_samples =  self._insar.getNumberValidPulses()
    firstAc =  self._insar.getFirstSampleAcrossPrf()
    firstDown =  self._insar.getFirstSampleDownPrf()
    numLocationAcross =  self._insar.getNumberLocationAcrossPrf()
    numLocationDown =  self._insar.getNumberLocationDownPrf()

    delRg1 = CN.SPEED_OF_LIGHT / (2*fs1)
    delRg2 = CN.SPEED_OF_LIGHT / (2*fs2)

    coarseRange = (nearRange1 - nearRange2) / delRg2
    coarseAcross = int(coarseRange + 0.5)
    if(coarseRange <= 0):
        coarseAcross = int(coarseRange - 0.5)
        pass

    print("*****************   runOffsetprf_nstage  **********************")
    print()
    print("self.grossRg, self.grossAz = ", self.grossRg, self.grossAz)
    print()
    print("*****************   runOffsetprf_nstage  **********************")
    if self.grossRg is not None:
        coarseAcross = self.grossRg
        pass

    s1 = self.insar.formSLC1.mocompPosition[1][0]
    s1_2 = self.insar.formSLC1.mocompPosition[1][1]
    s2 = self.insar.formSLC2.mocompPosition[1][0]
    s2_2 = self.insar.formSLC2.mocompPosition[1][1]

    coarseAz = int(
        (s1 - s2)/(s2_2 - s2) + prf2*(1/prf1 - 1/prf2)*(patchSize - valid_az_samples)/2)

    coarseDown = int(coarseAz + 0.5)
    if(coarseAz <= 0):
        coarseDown = int(coarseAz - 0.5)
        pass

    if self.grossAz is not None:
        coarseDown = self.grossAz
        pass

    coarseAcross = 0 + coarseAcross
    coarseDown = 0 + coarseDown

    mSlcImage = self._insar.getMasterSlcImage()
    mSlc = isceobj.createSlcImage()
    IU.copyAttributes(mSlcImage, mSlc)
    accessMode = 'read'
    mSlc.setAccessMode(accessMode)
    mSlc.createImage()
    masterWidth = mSlc.getWidth()
    masterLength = mSlc.getLength()

    sSlcImage = self._insar.getSlaveSlcImage()
    sSlc = isceobj.createSlcImage()
    IU.copyAttributes(sSlcImage, sSlc)
    accessMode = 'read'
    sSlc.setAccessMode(accessMode)
    sSlc.createImage()
    slaveWidth = sSlc.getWidth()
    slaveLength = sSlc.getLength()


    nStageObj = NStage(name='insarapp_slcs_nstage')
    nStageObj.configure()
    nStageObj.setImageDataType1('complex')
    nStageObj.setImageDataType2('complex')
    nStageObj.setFirstPRF(prf1)
    nStageObj.setSecondPRF(prf2)
    nStageObj.setFirstRangeSpacing(delRg1)
    nStageObj.setSecondRangeSpacing(delRg2)

    if nStageObj.acrossGrossOffset is None:
        nStageObj.setAcrossGrossOffset(coarseAcross)

    if nStageObj.downGrossOffset is None:
        nStageObj.setDownGrossOffset(coarseDown)

    recordInputs(self._insar.procDoc,
                    nStageObj,
                    "runOffsetprf",
                    logger,
                    "runOffsetprf")

    nStageObj.nstage(slcImage1=mSlc, slcImage2=sSlc)


    recordOutputs(self._insar.procDoc,
                    nStageObj,
                    "runOffsetprf",
                    logger,
                    "runOffsetprf")
    offField = nStageObj.getOffsetField()
    # save the input offset field for the record
    self._insar.setOffsetField(offField)
    self._insar.setRefinedOffsetField(offField)
