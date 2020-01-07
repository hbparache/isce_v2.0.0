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



import stdproc
import isceobj
from isceobj import Constants


def runResamp_slc(self):
    frame = self._isce.frames[self._isce.refScene][self._isce.refPol]
    instrument = frame.instrument
    fs = instrument.getRangeSamplingRate()
    pixelSpacing = Constants.SPEED_OF_LIGHT / (2.0 * fs)
    dopplerCentroid = self._isce.dopplerCentroid.fractionalCentroid
    for sceneid1, sceneid2 in self._isce.pairsToCoreg:
        pair = (sceneid1, sceneid2)
        offsetField = self._isce.refinedOffsetFields[pair]
        for pol in self._isce.selectedPols:
            slcImage2 = self._isce.slcImages[sceneid2][pol]
            resampledFilename = slcImage2.filename[:-3] + 'resampled.slc'
            sid = self._isce.formatname(pair, pol)
            catalog = isceobj.Catalog.createCatalog(self._isce.procDoc.name)
            resampSlcImage = run(slcImage2, resampledFilename, offsetField, instrument, pixelSpacing, dopplerCentroid, catalog=catalog, sceneid=sid)
            self._isce.procDoc.addAllFromCatalog(catalog)
            self._isce.slcImages[sceneid2][pol] = resampSlcImage


def run(slcImage, resampledFilename, offsetField, instrument, pixelSpacing, doppler, catalog=None, sceneid='NO_ID'):
    # Create the resampled SLC image
    resampledSlcImage = isceobj.createSlcImage()
    resampledSlcImage.setFilename(resampledFilename)
    resampledSlcImage.setAccessMode('write')
    resampledSlcImage.setDataType('CFLOAT')
    resampledSlcImage.setWidth(slcImage.width)
    resampledSlcImage.createImage()

    resamp = stdproc.createResamp_slc()
    resamp.setNumberLines(slcImage.length)
    resamp.setNumberRangeBin(slcImage.width)
    resamp.setNumberFitCoefficients(1)
    resamp.setSlantRangePixelSpacing(pixelSpacing)
    resamp.setDopplerCentroidCoefficients([doppler, 0.0, 0.0, 0.0])
    resamp.wireInputPort(name='offsets', object=offsetField)
    resamp.wireInputPort(name='instrument', object=instrument)
    resamp.stdWriter = stdWriter.set_file_tags("resamp_slc",
                                               "log",
                                               "err",
                                               "out")
    resamp.resamp_slc(slcImage, resampledSlcImage)
    slcImage.finalizeImage()
    resampledSlcImage.finalizeImage()
    return resampledSlcImage
