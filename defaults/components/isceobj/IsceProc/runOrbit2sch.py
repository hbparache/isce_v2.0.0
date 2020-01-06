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



# Comment: Adapted from InsarProc/runOrbit2sch.py
import logging
import stdproc
import isceobj

logger = logging.getLogger('isce.isceProc.runOrbit2sch')

def runOrbit2sch(self):
    planet = self._isce.planet
    peg = self._isce.peg
    pegHavg = self._isce.averageHeight
    stdWriter = self._stdWriter
    for sceneid in self._isce.selectedScenes:
        for pol in self._isce.selectedPols:
            frame = self._isce.frames[sceneid][pol]
            orbit = self._isce.orbits[sceneid][pol]
            catalog = isceobj.Catalog.createCatalog(self._isce.procDoc.name)
            sid = self._isce.formatname(sceneid, pol)
            orbit, velocity = run(orbit, peg, pegHavg, planet, stdWriter, catalog=catalog, sceneid=sid)
            self._isce.orbits[sceneid][pol] = orbit ##update orbit
            self._isce.pegProcVelocities[sceneid][pol] = velocity ##update velocity



def run(orbit, peg, pegHavg, planet, stdWriter, catalog=None, sceneid='NO_ID'):
    """
    Convert orbit to SCH.
    """
    logger.info("Converting the orbit to SCH coordinates: %s" % sceneid)

    objOrbit2sch = stdproc.createOrbit2sch(averageHeight=pegHavg)
    objOrbit2sch.stdWriter = stdWriter.set_file_tags("orbit2sch",
                                                     "log",
                                                     "err",
                                                     "log")

    objOrbit2sch(planet=planet, orbit=orbit, peg=peg)
    if catalog:
        isceobj.Catalog.recordInputsAndOutputs(catalog, objOrbit2sch,
                                               "runOrbit2sch." + sceneid,
                                               logger,
                                               "runOrbit2sch." + sceneid)


    #Piyush
    ####The heights and the velocities need to be updated now.
    (ttt, ppp, vvv, rrr) = objOrbit2sch.orbit._unpackOrbit()
    procVelocity = vvv[len(vvv)//2][0]

    return objOrbit2sch.orbit, procVelocity
