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

from iscesys.ImageUtil.ImageUtil import ImageUtil as IU

logger = logging.getLogger('isce.self._insar.runResamp_only')

def runResamp_only(self):
    imageInt = self._insar.getResampIntImage()
    imageAmp = self._insar.getResampAmpImage()
    
    objInt = isceobj.createIntImage()
    objIntOut = isceobj.createIntImage()
    IU.copyAttributes(imageInt, objInt)
    IU.copyAttributes(imageInt, objIntOut)
    outIntFilename = self._insar.getResampOnlyImageName()
    objInt.setAccessMode('read')
    objIntOut.setFilename(outIntFilename)
    
    self._insar.setResampOnlyImage(objIntOut)
    
    objIntOut.setAccessMode('write')
    objInt.createImage()
    objIntOut.createImage()

    objAmp = isceobj.createAmpImage()
    objAmpOut = isceobj.createAmpImage()
    IU.copyAttributes(imageAmp, objAmp)
    IU.copyAttributes(imageAmp, objAmpOut)
    outAmpFilename = outIntFilename.replace('int','amp')
    objAmp.setAccessMode('read')
    objAmpOut.setFilename(outAmpFilename)
    
    self._insar.setResampOnlyAmp(objAmpOut)
    
    objAmpOut.setAccessMode('write')
    objAmp.createImage()
    objAmpOut.createImage()
    
    numRangeBin = objInt.getWidth() 
    lines = objInt.getLength() 
    instrument = self._insar.getMasterFrame().getInstrument()
    
    offsetField = self._insar.getRefinedOffsetField()                
    
    
    dopplerCoeff = self._insar.getDopplerCentroid().getDopplerCoefficients(inHz=False)
    numFitCoeff = self._insar.getNumberFitCoefficients() 
    
    pixelSpacing = self._insar.getSlantRangePixelSpacing()

    objResamp = stdproc.createResamp_only()

    objResamp.setNumberLines(lines) 
    objResamp.setNumberFitCoefficients(numFitCoeff)
    objResamp.setSlantRangePixelSpacing(pixelSpacing)
    objResamp.setNumberRangeBin(numRangeBin)
    objResamp.setDopplerCentroidCoefficients(dopplerCoeff)
    
    objResamp.wireInputPort(name='offsets', object=offsetField)
    objResamp.wireInputPort(name='instrument', object=instrument)
    #set the tag used in the outfile. each message is precided by this tag
    #is the writer is not of "file" type the call has no effect
    self._stdWriter.setFileTag("resamp_only", "log")
    self._stdWriter.setFileTag("resamp_only", "err")
    self._stdWriter.setFileTag("resamp_only", "out")
    objResamp.setStdWriter(self._stdWriter)

    objResamp.resamp_only(objInt, objIntOut, objAmp, objAmpOut)

    # Record the inputs and outputs
    from isceobj.Catalog import recordInputsAndOutputs
    recordInputsAndOutputs(self._insar.procDoc, objResamp, "runResamp_only", \
                  logger, "runResamp_only")
    objInt.finalizeImage()
    objIntOut.finalizeImage()
    objAmp.finalizeImage()
    objAmpOut.finalizeImage()
