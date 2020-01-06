#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2012 to the present, California Institute of Technology.
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
# Author: Brett George
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import logging
import stdproc
logger = logging.getLogger('isce.insar.runSetmocomppath')



def runSetmocomppath_old(self, peg=None):
    logger.info("Selecting Peg Points")
    objSetmocomppath = stdproc.createSetmocomppath()
    if peg:
        objSetmocomppath.setPeg(peg)
    planet = self._insar.getMasterFrame().getInstrument().getPlatform().getPlanet()
    masterOrbit = self._insar.getMasterOrbit()
    slaveOrbit = self._insar.getSlaveOrbit()

    objSetmocomppath.wireInputPort(name='planet', object=planet)
    objSetmocomppath.wireInputPort(name='masterOrbit', object=masterOrbit)
    objSetmocomppath.wireInputPort(name='slaveOrbit', object=slaveOrbit)

    #set the tag used in the outfile. each message is precided by this tag
    #is the writer is not of "file" type the call has no effect
    self._stdWriter.setFileTag("setmocomppath", "log")
    self._stdWriter.setFileTag("setmocomppath", "err")
    self._stdWriter.setFileTag("setmocomppath", "out")
    objSetmocomppath.setStdWriter(self._stdWriter)

    objSetmocomppath.setmocomppath()

    # Record the inputs and outputs
    from isceobj.Catalog import recordInputsAndOutputs
    recordInputsAndOutputs(self._insar.procDoc, objSetmocomppath, "setmocomppath", \
                  logger, "runSetmocomppath")

    # Set peg information in the self._insar object
    peg = objSetmocomppath.getPeg()
    h1 = objSetmocomppath.getFirstAverageHeight()
    h2 = objSetmocomppath.getSecondAverageHeight()
    v1 = objSetmocomppath.getFirstProcVelocity()
    v2 = objSetmocomppath.getSecondProcVelocity()
    self._insar.setPeg(peg)
    self._insar.setFirstAverageHeight(h1)
    self._insar.setSecondAverageHeight(h2)
    self._insar.setFirstProcVelocity(v1)
    self._insar.setSecondProcVelocity(v2)

def runSetmocomppath_new(self, peg=None):
    from isceobj.Location.Peg import Peg
    from stdproc.orbit.pegManipulator import averagePeg
    from isceobj.Catalog import recordInputsAndOutputs

    logger.info("Selecting individual peg points")

    planet = self._insar.getMasterFrame().getInstrument().getPlatform().getPlanet()
    masterOrbit = self._insar.getMasterOrbit()
    slaveOrbit = self._insar.getSlaveOrbit()


    pegpts = []

    for orbitObj, order in zip((masterOrbit, slaveOrbit)
                                ,('First', 'Second')):
        objGetpeg = stdproc.createGetpeg()
        if peg:
            objGetpeg.setPeg(peg)

        objGetpeg.wireInputPort(name='planet', object=planet)
        objGetpeg.wireInputPort(name='Orbit', object=orbitObj)
        self._stdWriter.setFileTag("getpeg", "log")
        self._stdWriter.setFileTag("getpeg", "err")
        self._stdWriter.setFileTag("getpeg", "out")
        objGetpeg.setStdWriter(self._stdWriter)
        logger.info('Peg points are computed for individual SAR scenes.')
        objGetpeg.estimatePeg()
        pegpts.append(objGetpeg.getPeg())

        recordInputsAndOutputs(self._insar.procDoc, objGetpeg, "getpeg", \
                    logger, "runSetmocomppath")
        #Piyush
        # I set these values here for the sake of continuity, but they need to be updated
        # in orbit2sch as the correct peg point is not yet known
        getattr(self._insar,'set%sAverageHeight'%(order))(objGetpeg.getAverageHeight())
        getattr(self._insar,'set%sProcVelocity'%(order))(objGetpeg.getProcVelocity())


    logger.info('Combining individual peg points.')
    peg = averagePeg(pegpts, planet)
    self._insar.setPeg(peg)


runSetmocomppath = runSetmocomppath_new
