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



# Comment: Adapted from InsarProc/runFilter.py
import logging
import isceobj

from iscesys.ImageUtil.ImageUtil import ImageUtil as IU
from mroipac.filter.Filter import Filter
from mroipac.icu.Icu import Icu

logger = logging.getLogger('isce.isceProc.runFilter')

def runFilter(self, filterStrength):
    if filterStrength is not None:
        self._isce.filterStrength = filterStrength

    infos = {}
    for attribute in ['topophaseFlatFilename', 'filt_topophaseFlatFilename', 'phsigFilename', 'filterStrength']:
        infos[attribute] = getattr(self._isce, attribute)

    stdWriter = self._stdWriter

    for sceneid1, sceneid2 in self._isce.selectedPairs:
        pair = (sceneid1, sceneid2)
        resampAmpImages = self._isce.resampAmpImages[pair]
        widthInt = self._isce.resampIntImages[pair][self._isce.refPol].getWidth()
        for pol in self._isce.selectedPols:
            resampAmpImage = resampAmpImages[pol]
            sid = self._isce.formatname(pair, pol)
            infos['outputPath'] = os.path.join(self.getoutputdir(sceneid1, sceneid2), sid)
            catalog = isceobj.Catalog.createCatalog(self._isce.procDoc.name)
            run(resampAmpImage, infos, catalog=catalog, sceneid=sid)

    # Set the filtered image to be the one geocoded
    self._isce.topophaseFlatFilename = self._isce.filtIntFilename



def run(resampAmpImage, infos):
    logger.info("Applying power-spectral filter: %s" % sceneid)

    # Initialize the flattened interferogram
    topoflatIntFilename = infos['outputPath'] + '.' + infos['topophaseFlatFilename']
    intImage = isceobj.createIntImage()
    intImage.setFilename(topoflatIntFilename)
    intImage.setWidth(widthInt)
    intImage.setAccessMode('read')
    intImage.createImage()

    # Create the filtered interferogram
    filtIntFilename = infos['outputPath'] + '.' + infos['filt_topophaseFlatFilename']
    filtImage = isceobj.createIntImage()
    filtImage.setFilename(filtIntFilename)
    filtImage.setWidth(widthInt)
    filtImage.setAccessMode('write')
    filtImage.createImage()

    objFilter = Filter()
    objFilter.wireInputPort(name='interferogram',object=intImage)
    objFilter.wireOutputPort(name='filtered interferogram',object=filtImage)

    objFilter.goldsteinWerner(alpha=infos['filterStrength'])

    intImage.finalizeImage()
    filtImage.finalizeImage()

    
    #Create phase sigma correlation file here
    filtImage = isceobj.createIntImage()
    filtImage.setFilename(filtIntFilename)
    filtImage.setWidth(widthInt)
    filtImage.setAccessMode('read')
    filtImage.createImage()

    phsigFilename = infos['outputPath'] + '.' + infos['phsigFilename']
    phsigImage = isceobj.createImage()
    phsigImage.dataType='FLOAT'
    phsigImage.bands = 1
    phsigImage.setWidth(widthInt)
    phsigImage.setFilename(phsigFilename)
    phsigImage.setAccessMode('write')
    phsigImage.setImageType('cor')#the type in this case is not for mdx.py displaying but for geocoding method
    phsigImage.createImage()


    ampImage = isceobj.createAmpImage()
    IU.copyAttributes(resampAmpImage, ampImage)
    ampImage.setAccessMode('read')
    ampImage.createImage()


    icuObj = Icu()
    icuObj.filteringFlag = False
    icuObj.unwrappingFlag = False
    icuObj.initCorrThreshold = 0.1

    icuObj.icu(intImage=filtImage, ampImage=ampImage, phsigImage=phsigImage)
    phsigImage.renderHdr()

    filtImage.finalizeImage()
    phsigImage.finalizeImage()
    ampImage.finalizeImage()
