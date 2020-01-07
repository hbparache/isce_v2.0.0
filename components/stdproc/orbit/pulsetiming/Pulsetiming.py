#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2010 to the present, California Institute of Technology.
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
# Author: Giangi Sacco
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import datetime
from isceobj.Orbit.Orbit import Orbit
from isceobj.Scene.Frame import Frame
from iscesys.Component.Component import Component, Port

class Pulsetiming(Component):

    logging_name = "isce.stdproc.pulsetiming"    

    def __init__(self):
        super(Pulsetiming, self).__init__()
        self.frame = None
        self.orbit = Orbit(source='Pulsetiming')
        return None

    def createPorts(self):
        framePort = Port(name='frame',method=self.addFrame)
        self._inputPorts.add(framePort)
        return None

    def getOrbit(self):
        return self.orbit
    
    def addFrame(self):        
        frame = self.inputPorts['frame']
        if frame:
            if isinstance(frame, Frame):
                self.frame = frame                
            else:
                self.logger.error(
                    "Object must be of type Frame, not %s" % (frame.__class__)
                    )
                raise TypeError
            pass
        return None
                 
#    @port(Frame)
#    def addFrame(self):
#        return None

    def pulsetiming(self):
        self.activateInputPorts()
                                   
        numberOfLines = self.frame.getNumberOfLines()
        prf = self.frame.getInstrument().getPulseRepetitionFrequency()
        pri = 1.0/prf
        startTime = self.frame.getSensingStart()
        thisOrbit = self.frame.getOrbit()
        self.orbit.setReferenceFrame(thisOrbit.getReferenceFrame())
        
        for i in range(numberOfLines):
            dt = i*pri
            time = startTime + datetime.timedelta(seconds=dt)
            sv = thisOrbit.interpolateOrbit(time,method='hermite')
            self.orbit.addStateVector(sv)                
        
