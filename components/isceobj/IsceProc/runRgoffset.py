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
# Author: Kosal Khun
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Comment: Adapted from InsarProc/runRgoffset.py
import logging
import isceobj

from iscesys.ImageUtil.ImageUtil import ImageUtil as IU

logger = logging.getLogger('isce.isce.runRgoffset')

def runRgoffset(self):
    infos = {}
    for attribute in ['firstSampleAcross', 'firstSampleDown', 'numberLocationAcross', 'numberLocationDown']:
        infos[attribute] = getattr(self._isce, attribute)
    for attribute in ['sensorName', 'offsetSearchWindowSize']:
        infos[attribute] = getattr(self, attribute)

    stdWriter = self._stdWriter

    refPol = self._isce.refPol
    refScene = self._isce.refScene

    imageSim = self._isce.simAmpImage
    sceneid1, sceneid2 = self._isce.pairsToCoreg[0]
    if sceneid1 != refScene:
        sys.exit("runRgoffset: should have refScene here!")

    pair = (sceneid1, sceneid2)
    imageAmp = self._isce.resampAmpImages[pair][refPol]
    if not imageAmp:
        pair = (sceneid2, sceneid1)
        imageAmp = self._isce.resampAmpImages[pair][refPol]

    prf = self._isce.frames[refScene][refPol].getInstrument().getPulseRepetitionFrequency()
    sid = self._isce.formatname(refScene)
    infos['outputPath'] = self.getoutputdir(refScene)
    catalog = isceobj.Catalog.createCatalog(self._isce.procDoc.name)
    offsetField = run(imageAmp, imageSim, prf, infos, stdWriter, catalog=catalog, sceneid=sid)

    for pair in self._isce.pairsToCoreg:
        self._isce.offsetFields[pair] = offsetField
        self._isce.refinedOffsetFields[pair] = offsetField



def run(imageAmp, imageSim, prf, infos, stdWriter, catalog=None, sceneid='NO_ID'):
    logger.info("Running Rgoffset: %s" % sceneid)

    firstAc =  infos['firstSampleAcross']
    firstDown =  infos['firstSampleDown']
    numLocationAcross =  infos['numberLocationAcross']
    numLocationDown =  infos['numberLocationDown']

    objAmp = isceobj.createIntImage()
    IU.copyAttributes(imageAmp, objAmp)
    objAmp.setAccessMode('read')
    objAmp.createImage()
    widthAmp = objAmp.getWidth()
    intLength = objAmp.getLength()
    lastAc = widthAmp - firstAc
    lastDown = intLength - firstDown

    objSim = isceobj.createImage()
    IU.copyAttributes(imageSim, objSim)
    objSim.setAccessMode('read')
    objSim.createImage()

    objOffset = isceobj.createEstimateOffsets()

    objOffset.setSearchWindowSize(infos['offsetSearchWindowSize'], infos['sensorName'])
    objOffset.setFirstSampleAcross(firstAc)
    objOffset.setLastSampleAcross(lastAc)
    objOffset.setNumberLocationAcross(numLocationAcross)
    objOffset.setFirstSampleDown(firstDown)
    objOffset.setLastSampleDown(lastDown)
    objOffset.setNumberLocationDown(numLocationDown)
    #set the tag used in the outfile. each message is precided by this tag
    #if the writer is not of "file" type the call has no effect
    objOffset.stdWriter = stdWriter.set_file_tags("rgoffset",
                                                  "log",
                                                  "err",
                                                  "out")

    objOffset.setFirstPRF(prf)
    objOffset.setSecondPRF(prf)
    objOffset.setAcrossGrossOffset(0)
    objOffset.setDownGrossOffset(0)
    objOffset.estimateoffsets(image1=objSim, image2=objAmp, band1=0, band2=0)

    if catalog is not None:
        # Record the inputs and outputs
        isceobj.Catalog.recordInputsAndOutputs(catalog, objOffset,
                                               "runRgoffset.%s" % sceneid,
                                               logger,
                                               "runRgoffset.%s" % sceneid)

    objAmp.finalizeImage()
    objSim.finalizeImage()

    return objOffset.getOffsetField()
