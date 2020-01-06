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
# Author: Giangi Sacco
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import logging
import isceobj
import mroipac
import numpy
from iscesys.ImageUtil.ImageUtil import ImageUtil as IU
from isceobj import Constants as CN
from mroipac.ampcor.NStage import NStage
logger = logging.getLogger('isce.insar.runRgoffset')

def runRgoffset(self):
    from isceobj.Catalog import recordInputs,recordOutputs

    coarseAcross = 0
    coarseDown = 0
    numLocationAcross = self._insar.getNumberLocationAcross()
    numLocationDown = self._insar.getNumberLocationDown()
    firstAc = self._insar.getFirstSampleAcross()
    firstDn = self._insar.getFirstSampleDown()

    ampImage = self._insar.getResampAmpImage()
    slaveWidth = ampImage.getWidth()
    slaveLength = ampImage.getLength()
    objAmp = isceobj.createSlcImage()
    objAmp.dataType = 'CFLOAT'
    objAmp.bands = 1
    objAmp.setFilename(ampImage.getFilename())
    objAmp.setAccessMode('read')
    objAmp.setWidth(slaveWidth)
    objAmp.createImage()

    simImage = self._insar.getSimAmpImage()
    masterWidth = simImage.getWidth()
    objSim = isceobj.createImage()
    objSim.setFilename(simImage.getFilename())
    objSim.dataType = 'FLOAT'
    objSim.setWidth(masterWidth)
    objSim.setAccessMode('read')
    objSim.createImage()
    masterLength = simImage.getLength()


    nStageObj = NStage(name='insarapp_intsim_nstage')
    nStageObj.configure()
    nStageObj.setImageDataType1('real')
    nStageObj.setImageDataType2('complex')

    if nStageObj.acrossGrossOffset is None:
        nStageObj.setAcrossGrossOffset(0)

    if nStageObj.downGrossOffset is None:
        nStageObj.setDownGrossOffset(0)


    # Record the inputs
    recordInputs(self._insar.procDoc,
                nStageObj,
                "runRgoffset",
                logger,
                "runRgoffset")

    nStageObj.nstage(slcImage1=objSim,slcImage2=objAmp)

    recordOutputs(self._insar.procDoc,
                    nStageObj,
                    "runRgoffset",
                    logger,
                    "runRgoffset")

    offField = nStageObj.getOffsetField()

    # save the input offset field for the record
    self._insar.setOffsetField(offField)
    self._insar.setRefinedOffsetField(offField)
