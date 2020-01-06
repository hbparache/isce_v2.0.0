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



# Comment: Adapted from InsarProc/runFormSLCTSX.py
import logging
import stdproc
import isceobj
from iscesys.ImageUtil.ImageUtil import ImageUtil as IU

logger = logging.getLogger('isce.isceProc.runFormSLCTSX')


def runFormSLC(self, patchSize=None, goodLines=None, numPatches=None):
    #NOTE tested the formslc() as a stand alone by passing the same inputs
    #computed in Howard terraSAR.py. The differences here arises from the
    #differences in the orbits when using the same orbits the results are very
    #close jng this will make the second term in coarseAz in offsetprf equal
    #zero. we do so since for tsx there is no such a term. Need to ask
    #confirmation
    self._isce.patchSize = self._isce.numberValidPulses
    # the below value is zero because of we just did above, but just want to be
    #  explicit in the definition of is_mocomp
    self._isce.get_is_mocomp()

    v, h = self._isce.vh()
    peg = self._isce.peg
    dopplerCentroid = self._isce.dopplerCentroid
    stdWriter = self._stdWriter
    sensorname = self.sensorName

    for sceneid in self._isce.selectedScenes:
        self._isce.slcImages[sceneid] = {}
        self._isce.formSLCs[sceneid] = {}
        for pol in self._isce.selectedPols:
            frame = self._isce.frames[sceneid][pol]
            orbit = self._isce.orbits[sceneid][pol]
            rawImage = self._isce.rawImages[sceneid][pol]
            catalog = isceobj.Catalog.createCatalog(self._isce.procDoc.name)
            sid = self._isce.formatname(sceneid, pol)
            slcImage, formSlc = run(rawImage, frame, dopplerCentroid, orbit, peg, v, h, sensorname, stdWriter, catalog=catalog, sceneid=sid)
            self._isce.slcImages[sceneid][pol] = slcImage
            self._isce.formSLCs[sceneid][pol] = formSlc

    self._isce.numberPatches = slcImage.getLength() / float(self._isce.numberValidPulses)


def run(rawImage, frame, dopplerCentroid, orbit, peg, velocity, height, sensorname, stdWriter, catalog=None, sceneid='NO_ID'):
    logger.info("Forming SLC: %s" % sceneid)

    imSlc = isceobj.createSlcImage()
    IU.copyAttributes(rawImage, imSlc)
    imSlc.setAccessMode('read')
    imSlc.createImage()
    formSlc = stdproc.createFormSLC(sensorname)
    formSlc.setBodyFixedVelocity(velocity)
    formSlc.setSpacecraftHeight(height)
    formSlc.wireInputPort(name='doppler', object=dopplerCentroid)
    formSlc.wireInputPort(name='peg', object=peg)
    formSlc.wireInputPort(name='frame', object=frame)
    formSlc.wireInputPort(name='orbit', object=orbit)
    formSlc.wireInputPort(name='slcInImage', object=imSlc)
    formSlc.stdWriter = stdWriter.set_file_tags("formslcTSX",
                                                "log",
                                                "err",
                                                "out")
    slcImage = formSlc()
    imSlc.finalizeImage()
    if catalog is not None:
        isceobj.Catalog.recordInputsAndOutputs(catalog, formSlc,
                                               "runFormSLCTSX.%s" % sceneid,
                                               logger,
                                               "runFormSLCTSX.%s" % sceneid)
    return slcImage, formSlc
