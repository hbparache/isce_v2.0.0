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



# Comment: Adapted from InsarProc/runEstimateHeights.py
import logging
import stdproc
import isceobj

logger = logging.getLogger('isce.isceProc.runEstimateHeights')

def runEstimateHeights(self):
    for sceneid in self._isce.selectedScenes:
        self._isce.fdHeights[sceneid] = {}
        for pol in self._isce.selectedPols:
            frame = self._isce.frames[sceneid][pol]
            orbit = self._isce.orbits[sceneid][pol]
            catalog = isceobj.Catalog.createCatalog(self._isce.procDoc.name)
            sid = self._isce.formatname(sceneid, pol)
            chv = run(frame, orbit, catalog=catalog, sceneid=sid)
            self._isce.procDoc.addAllFromCatalog(catalog)
            self._isce.fdHeights[sceneid][pol] = chv.height


def run(frame, orbit, catalog=None, sceneid='NO_ID'):
    """
    Estimate heights from orbit.
    """
    chv = stdproc.createCalculateFdHeights()
    planet = frame.getInstrument().getPlatform().getPlanet()
    chv(frame=frame, orbit=orbit, planet=planet)
    if catalog is not None:
        isceobj.Catalog.recordInputsAndOutputs(catalog, chv,
                                               "runEstimateHeights.CHV.%s" % sceneid,
                                               logger,
                                               "runEstimateHeights.CHV.%s" % sceneid)
    return chv

