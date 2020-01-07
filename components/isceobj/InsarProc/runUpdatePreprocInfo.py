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




def runUpdatePreprocInfo(self, use_dop="average"):
    from .runFdMocomp import runFdMocomp
    
    peg = self.insar.peg
    pegRc = peg.radiusOfCurvature
    masterFrame = self.insar.masterFrame
    slaveFrame = self.insar.slaveFrame
    prf1 = masterFrame.getInstrument().getPulseRepetitionFrequency()
    prf2 = slaveFrame.getInstrument().getPulseRepetitionFrequency()
    masterDoppler = self.insar.masterDoppler
    slaveDoppler = self.insar.slaveDoppler

    ## red flag.
    fd = runFdMocomp(self, use_dop=use_dop)
    
    averageDoppler = masterDoppler.average(slaveDoppler)
    averageDoppler.fractionalCentroid = fd
    self.insar.dopplerCentroid =averageDoppler
    return None
