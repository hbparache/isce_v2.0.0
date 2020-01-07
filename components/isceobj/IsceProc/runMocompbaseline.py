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



# Comment: Adapted from InsarProc/runMocompbaseline.py
import logging
import stdproc
import isceobj

logger = logging.getLogger('isce.isceProc.runMocompbaseline')


def runMocompbaseline(self):
    refPol = self._isce.refPol
    averageHeight = self._isce.averageHeight
    peg = self._isce.peg
    stdWriter = self._stdWriter
    for sceneid1, sceneid2 in self._isce.selectedPairs:
        pair = (sceneid1, sceneid2)
        objFormSlc1 = self._isce.formSLCs[sceneid1][refPol]
        objFormSlc2 = self._isce.formSLCs[sceneid2][refPol]
        orbit1 = self._isce.orbits[sceneid1][refPol]
        orbit2 = self._isce.orbits[sceneid2][refPol]
        frame1 = self._isce.frames[sceneid1][refPol]
        ellipsoid = frame1.getInstrument().getPlatform().getPlanet().get_elp()
        catalog = isceobj.Catalog.createCatalog(self._isce.procDoc.name)
        sid = self._isce.formatname(pair)
        objMocompbaseline = run(objFormSlc1, objFormSlc2, orbit1, orbit2, ellipsoid, averageHeight, peg, stdWriter, catalog=catalog, sceneid=sid)
        self._isce.mocompBaselines[pair] = objMocompbaseline


# index of the position in the  mocompPosition array
# (the 0 element is the time)
posIndx = 1


def run(objFormSlc1, objFormSlc2, orbit1, orbit2, ellipsoid, averageHeight, peg, stdWriter, catalog=None, sceneid='NO_ID'):
    logger.info("Calculating Baseline: %s" % sceneid)

    # schPositions computed in orbit2sch
    # objFormSlc's  created during formSlc

    mocompPosition1 = objFormSlc1.getMocompPosition()
    mocompIndex1 = objFormSlc1.getMocompIndex()
    mocompPosition2 = objFormSlc2.getMocompPosition()
    mocompIndex2 = objFormSlc2.getMocompIndex()

    objMocompbaseline = stdproc.createMocompbaseline()

    objMocompbaseline.setMocompPosition1(mocompPosition1[posIndx])
    objMocompbaseline.setMocompPositionIndex1(mocompIndex1)
    objMocompbaseline.setMocompPosition2(mocompPosition2[posIndx])
    objMocompbaseline.setMocompPositionIndex2(mocompIndex2)

    objMocompbaseline.wireInputPort(name='masterOrbit',
                                    object=orbit1)
    objMocompbaseline.wireInputPort(name='slaveOrbit',
                                    object=orbit2)
    objMocompbaseline.wireInputPort(name='ellipsoid', object=ellipsoid)
    objMocompbaseline.wireInputPort(name='peg', object=peg)
    objMocompbaseline.setHeight(averageHeight)

    #set the tag used in the outfile. each message is precided by this tag
    #is the writer is not of "file" type the call has no effect
    objMocompbaseline.stdWriter = stdWriter.set_file_tags("mocompbaseline",
                                                          "log",
                                                          "err",
                                                          "out")

    objMocompbaseline.mocompbaseline()

    if catalog is not None:
        # Record the inputs and outputs
        isceobj.Catalog.recordInputsAndOutputs(catalog, objMocompbaseline,
                                               "runMocompbaseline.%s" % sceneid,
                                               logger,
                                               "runMocompbaseline.%s" % sceneid)

    return objMocompbaseline
