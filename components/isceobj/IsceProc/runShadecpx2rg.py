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



# Comment: Adapted from InsarProc/runShadecpx2rg.py
import logging
import isceobj
import os

from iscesys.ImageUtil.ImageUtil import ImageUtil as IU

logger = logging.getLogger('isce.isce.runShadecpx2rg')

def runShadecpx2rg(self):
    infos = {}
    for attribute in ['machineEndianness', 'simAmpImageName', 'heightFilename', 'shadeFactor']:
        infos[attribute] = getattr(self._isce, attribute)

    stdWriter = self._stdWriter

    refScene = self._isce.refScene
    refPol = self._isce.refPol
    imgSlc1  =  self._isce.slcImages[refScene][refPol]
    widthAmp = int(imgSlc1.getWidth() / self._isce.numberRangeLooks)
    infos['outputPath'] = os.path.join(self.getoutputdir(refScene), refScene)
    catalog = isceobj.Catalog.createCatalog(self._isce.procDoc.name)
    sid = self._isce.formatname(refScene)
    imageSimAmp, imageHgt = run(widthAmp, infos, stdWriter, catalog=catalog, sceneid=sid)
    self._isce.simAmpImage = imageSimAmp
    self._isce.heightTopoImage = imageHgt


def run(widthAmp, infos, stdWriter, catalog=None, sceneid='NO_ID'):
    logger.info("Running shadecpx2rg: %s" % sceneid)

    endian = infos['machineEndianness']
    filenameSimAmp = infos['outputPath'] + '.' + infos['simAmpImageName']
    filenameHt = infos['outputPath'] + '.' + infos['heightFilename']
    shade = infos['shadeFactor']

    objSimAmp = isceobj.createImage()
    widthSimAmp = widthAmp
    objSimAmp.initImage(filenameSimAmp, 'read', widthSimAmp, 'FLOAT')
    
    imageSimAmp = isceobj.createImage()
    IU.copyAttributes(objSimAmp, imageSimAmp)

    objSimAmp.setAccessMode('write')
    objSimAmp.createImage()

    widthHgtImage = widthAmp # they have same width by construction
    objHgtImage = isceobj.createImage()
    objHgtImage.initImage(filenameHt, 'read', widthHgtImage, 'FLOAT')
    imageHgt = isceobj.createImage()
    IU.copyAttributes(objHgtImage, imageHgt)
    
    objHgtImage.createImage()
   
    objShade = isceobj.createSimamplitude()
    #set the tag used in the outfile. each message is precided by this tag
    #if the writer is not of "file" type the call has no effect
    objShade.stdWriter = stdWriter.set_file_tags("simamplitude",
                                                 "log",
                                                 "err",
                                                 "out")

    objShade.simamplitude(objHgtImage, objSimAmp, shade=shade)

    if catalog is not None:
        # Record the inputs and outputs
        isceobj.Catalog.recordInputsAndOutputs(catalog, objShade,
                                               "runSimamplitude.%s" % sceneid,
                                               logger,
                                               "runSimamplitude.%s" % sceneid)
    
    objSimAmp.renderHdr()
    objHgtImage.finalizeImage()
    objSimAmp.finalizeImage()

    return imageSimAmp, imageHgt
