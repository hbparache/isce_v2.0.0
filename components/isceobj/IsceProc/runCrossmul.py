#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2013 to the present, California Institute of Technology.
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



# Comment: Adapted from IsceProc/runResamp.py
import os
import logging
from stdproc.stdproc import crossmul
import isceobj

from iscesys.ImageUtil.ImageUtil import ImageUtil as IU

logger = logging.getLogger('isce.isceProc.runCrossmul')

def runCrossmul(self):
    #stdWriter = self._stdWriter
    resampName = self._isce.resampImageName
    azLooks = self._isce.numberAzimuthLooks
    rgLooks = self._isce.numberRangeLooks
    lines = self._isce.numberResampLines

    for sceneid1, sceneid2 in self._isce.selectedPairs:
        pair = (sceneid1, sceneid2)
        self._isce.resampIntImages[pair] = {}
        self._isce.resampAmpImages[pair] = {}
        for pol in self._isce.selectedPols:
            imageSlc1 = self._isce.slcImages[sceneid1][pol]
            imageSlc2 = self._isce.slcImages[sceneid2][pol]
            catalog = isceobj.Catalog.createCatalog(self._isce.procDoc.name)
            sid = self._isce.formatname(pair, pol)
            resampFilename = os.path.join(self.getoutputdir(sceneid1, sceneid2), self._isce.formatname(pair, pol, resampName))
            imageInt, imageAmp = run(imageSlc1, imageSlc2, resampFilename, azLooks, rgLooks, lines, catalog=catalog, sceneid=sid)
            self._isce.resampIntImages[pair][pol] = imageInt
            self._isce.resampAmpImages[pair][pol] = imageAmp


def run(imageSlc1, imageSlc2, resampName, azLooks, rgLooks, lines, catalog=None, sceneid='NO_ID'):
    logger.info("Generating interferogram: %s" % sceneid)

    objSlc1 = isceobj.createSlcImage()
    IU.copyAttributes(imageSlc1, objSlc1)
    objSlc1.setAccessMode('read')
    objSlc1.createImage()

    objSlc2 = isceobj.createSlcImage()
    IU.copyAttributes(imageSlc2, objSlc2)
    objSlc2.setAccessMode('read')
    objSlc2.createImage()

    slcWidth = imageSlc1.getWidth()
    intWidth = int(slcWidth / rgLooks)

    logger.info("Will ouput interferogram and amplitude: %s" % sceneid)
    resampAmp = resampName + '.amp'
    resampInt = resampName + '.int'

    objInt = isceobj.createIntImage()
    objInt.setFilename(resampInt)
    objInt.setWidth(intWidth)
    imageInt = isceobj.createIntImage()
    IU.copyAttributes(objInt, imageInt)
    objInt.setAccessMode('write')
    objInt.createImage()

    objAmp = isceobj.createAmpImage()
    objAmp.setFilename(resampAmp)
    objAmp.setWidth(intWidth)
    imageAmp = isceobj.createAmpImage()
    IU.copyAttributes(objAmp, imageAmp)
    objAmp.setAccessMode('write')
    objAmp.createImage()
    
    objCrossmul = crossmul.createcrossmul()
    objCrossmul.width = intWidth
    objCrossmul.length = lines
    objCrossmul.LooksDown = azLooks
    objCrossmul.LooksAcross = rgLooks

    #set the tag used in the outfile. each message is precided by this tag
    #is the writer is not of "file" type the call has no effect
#    objCrossmul.stdWriter = stdWriter.set_file_tags("resamp",
#                                                  "log",
#                                                  "err",
#                                                  "out")
    objCrossmul.crossmul(objSlc1, objSlc2, objInt, objAmp)

    if catalog is not None:
        # Record the inputs and outputs
        isceobj.Catalog.recordInputsAndOutputs(catalog, objCrossmul,
                                               "runCrossmul.%s" % sceneid,
                                               logger,
                                               "runCrossmul.%s" % sceneid)

    for obj in [objInt, objAmp, objSlc1, objSlc2]:
        obj.finalizeImage()

    return imageInt, imageAmp
