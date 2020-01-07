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
logger = logging.getLogger('isce.insar.runEstimateHeights')

def runEstimateHeights(self):
    from isceobj.Catalog import recordInputsAndOutputs
    chv = []
    for frame, orbit, tag in zip((self._insar.getMasterFrame(),
                                  self._insar.getSlaveFrame()),
                                 (self.insar.masterOrbit,
                                  self.insar.slaveOrbit),
                                 ('master', 'slave')):
        chv.append(stdproc.createCalculateFdHeights())
        chv[-1](frame=frame, orbit=orbit, planet=self.planet)
        
        recordInputsAndOutputs(self.procDoc, chv[-1],
                               "runEstimateHeights.CHV_"+tag, logger,
                               "runEstimateHeights.CHV_"+tag)
        
    self.insar.fdH1, self.insar.fdH2 = [item.height for item in chv]
    return None

