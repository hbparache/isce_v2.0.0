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



# Comment: Adapted from InsarProc/runGeocode.py
import logging
import stdproc
from stdproc.rectify.geocode.Geocodable import Geocodable
import isceobj
import iscesys
#from contextlib import nested
from iscesys.ImageUtil.ImageUtil import ImageUtil as IU
from iscesys.StdOEL.StdOELPy import create_writer

logger = logging.getLogger('isce.isceProc.runGeocode')
posIndx = 1


def runGeocode(self, prodlist, unwrapflag, bbox):
    '''Generalized geocoding of all the files listed above (in prodlist).'''
    if isinstance(prodlist, str):
        tobeGeocoded = [prodlist]
    else:
        tobeGeocoded = prodlist

    #####Remove the unwrapped interferogram if no unwrapping is done
    if not unwrapflag:
        try:
            tobeGeocoded.remove(self._isce.unwrappedIntFilename)
        except ValueError:
            pass

    print('Number of products to geocode: ', len(tobeGeocoded))

    if bbox is not None:
        snwe = list(bbox)
        if len(snwe) != 4:
            raise valueError('Bounding box should be a list/tuple of length 4')
    else:
        snwe = None

    v, h = self._isce.vh()

    infos = {}
    for attribute in ['demCropFilename', 'numberRangeLooks', 'numberAzimuthLooks', 'is_mocomp', 'demImage', 'peg', 'dopplerCentroid']:
        infos[attribute] = getattr(self._isce, attribute)

    for sceneid1, sceneid2 in self._isce.selectedPairs:
        pair = (sceneid1, sceneid2)
        frame1 = self._isce.frames[sceneid1]
        formSLC1 = self._isce.formSLCs[sceneid1]
        if snwe is None:
            snwe = self._isce.topos[pair].snwe
        for pol in self._isce.selectedPols:
            sid = self._isce.formatname(pair, pol)
            infos['outputPath'] = os.path.join(self.getoutputdir(sceneid1, sceneid2), sid)
            catalog = isceobj.Catalog.createCatalog(self._isce.procDoc.name)
            run(tobeGeocoded, frame1, formSLC1, velocity, height, snwe, infos, catalog=catalog, sceneid=sid)


def run(tobeGeocoded, frame1, formSLC1, velocity, height, snwe, infos, catalog=None, sceneid='NO_ID'):
    logger.info("Geocoding Image: %s" % sceneid)

    stdWriter = create_writer("log", "", True, filename=infos['ouputPath'] + ".geo.log")

    planet = frame1.getInstrument().getPlatform().getPlanet()
    referenceOrbit = formSLC1.getMocompPosition(posIndx)
    doppler = dopplerCentroid.getDopplerCoefficients(inHz=False)[0]
    #####Geocode one by one
    ge = Geocodable()
    for prod in tobeGeocoded:
        objGeo = stdproc.createGeocode(
                    snwe = snwe,
                    demCropFilename = infos['outputPath'] + '.' + infos['demCropFilename'],
                    referenceOrbit = referenceOrbit,
                    dopplerCentroidConstantTerm = doppler,
                    bodyFixedVelocity = velocity,
                    spacecraftHeight = height,
                    numberRangeLooks = infos['numberRangeLooks'],
                    numberAzimuthLooks = infos['numberAzimuthLooks'],
                    isMocomp = infos['is_mocomp'])

        objGeo.stdWriter = stdWriter

        #create the instance of the image and return the method is supposed to use
        inImage, objGeo.method = ge.create(infos['outputPath'] + '.' + prod)
        if inImage:
            demImage = isceobj.createDemImage()
            IU.copyAttributes(infos['demImage'], demImage)
            objGeo(peg=infos['peg'], frame=frame1,
                           planet=planet, dem=demImage, tobegeocoded=inImage,
                           geoPosting=None, masterslc=formSLC1)

            if catalog is not None:
                isceobj.Catalog.recordInputsAndOutputs(catalog, objGeo,
                                                       "runGeocode.%s" % sceneid,
                                                       logger,
                                                       "runGeocode.%s" % sceneid)

    stdWriter.finalize()
