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
import isceobj
import copy

logger = logging.getLogger('isce.insar.runOrbit2sch')


def runOrbit2sch_piyush(self):
    from isceobj.Catalog import recordInputsAndOutputs
    import numpy
    logger.info("Converting the orbit to SCH coordinates")

    # Piyush
    ####We don't know the correct SCH heights yet.
    ####Not computing average peg height yet.
    peg = self.insar.peg
    pegHavg = self.insar.averageHeight
    planet = self.insar.planet

    masterOrbit = self.insar.masterOrbit
    slaveOrbit = self.insar.slaveOrbit

    objOrbit2sch1 = stdproc.createOrbit2sch(averageHeight=pegHavg)
    objOrbit2sch1.stdWriter = self.stdWriter.set_file_tags("orbit2sch",
                                                           "log",
                                                           "err",
                                                           "log")
    objOrbit2sch2 = stdproc.createOrbit2sch(averageHeight=pegHavg)
    objOrbit2sch2.stdWriter = self.stdWriter

    ## loop over master/slave orbits
    for obj, orb, tag, order in zip((objOrbit2sch1, objOrbit2sch2),
                                    (self.insar.masterOrbit, self.insar.slaveOrbit),
                                    ('master', 'slave'),
                                    ('First', 'Second')):
        obj(planet=planet, orbit=orb, peg=peg)
        recordInputsAndOutputs(self.insar.procDoc, obj,
                               "runOrbit2sch." + tag,
                               logger,
                               "runOrbit2sch." + tag)

        #equivalent to self.insar.masterOrbit =
        setattr(self.insar,'%sOrbit'%(tag), obj.orbit)

        #Piyush
        ####The heights and the velocities need to be updated now.
        (ttt, ppp, vvv, rrr) = obj.orbit._unpackOrbit()

        #equivalent to self.insar.setFirstAverageHeight()
        # SCH heights replacing the earlier llh heights
        # getattr(self.insar,'set%sAverageHeight'%(order))(numpy.sum(numpy.array(ppp),axis=0)[2] /(1.0*len(ppp)))

        #equivalent to self.insar.setFirstProcVelocity()
        getattr(self.insar,'set%sProcVelocity'%(order))(vvv[len(vvv)//2][0])

    return None


def runOrbit2sch_new(self):
    from isceobj.Catalog import recordInputsAndOutputs
    logger.info("Converting the orbit to SCH coordinates")
    pegHAvg = self.insar.averageHeight
    peg = self.insar.peg
    planet = self.insar.planet

    masterOrbit = self.insar.masterOrbit
    slaveOrbit = self.insar.slaveOrbit

    objOrbit2sch1 = stdproc.createOrbit2sch(averageHeight=pegHAvg)
    objOrbit2sch1.stdWriter = self.stdWriter.set_file_tags("orbit2sch",
                                                           "log",
                                                           "err",
                                                           "log")
    objOrbit2sch2 = stdproc.createOrbit2sch(averageHeight=pegHAvg)
    objOrbit2sch2.stdWriter = self.stdWriter

    ## loop over master/slave orbits
    for obj, orb, tag in zip((objOrbit2sch1, objOrbit2sch2),
                             (self.insar.masterOrbit, self.insar.slaveOrbit),
                             ('master', 'slave')):
        obj(planet=planet, orbit=orb, peg=peg)
        recordInputsAndOutputs(self.insar.procDoc, obj,
                               "runOrbit2sch." + tag,
                               logger,
                               "runOrbit2sch." + tag)


    self.insar.masterOrbit = objOrbit2sch1.orbit
    self.insar.slaveOrbit = objOrbit2sch2.orbit
    return None



def runOrbit2sch_old(self):
    from isceobj.Catalog import recordInputsAndOutputs
    logger.info("Converting the orbit to SCH coordinates")
    pegHAvg = self.insar.averageHeight
    peg = self.insar.peg
    planet = self.insar.planet

    masterOrbit = self.insar.masterOrbit
    slaveOrbit = self.insar.slaveOrbit

    objOrbit2sch1 = stdproc.createOrbit2sch(averageHeight=pegHAvg)
    objOrbit2sch1.stdWriter = self.stdWriter.set_file_tags("orbit2sch",
                                                           "log",
                                                           "err",
                                                           "log")

    objOrbit2sch1(planet=planet, orbit=masterOrbit, peg=peg)

    # Record the inputs and outputs
    recordInputsAndOutputs(self.insar.procDoc,
                           objOrbit2sch1,
                           "runOrbit2sch.master",
                           logger,
                           "runOrbit2sch.master")

    objOrbit2sch2 = stdproc.createOrbit2sch(averageHeight=pegHAvg)
    objOrbit2sch2.stdWriter = self.stdWriter

#    objOrbit2sch2.wireInputPort(name='planet', object=planet)
#    objOrbit2sch2.wireInputPort(name='orbit', object=slaveOrbit)
#    objOrbit2sch2.wireInputPort(name='peg', object=peg)

    objOrbit2sch2(planet=planet, orbit=slaveOrbit, peg=peg)


    # Record the inputs and outputs
    recordInputsAndOutputs(self.insar.procDoc,
                           objOrbit2sch2,
                           "runOrbit2sch.slave",
                           logger,
                           "runOrbit2sch.slave")

    self.insar.masterOrbit = objOrbit2sch1.orbit
    self.insar.slaveOrbit = objOrbit2sch2.orbit
    return None


runOrbit2sch = runOrbit2sch_piyush
