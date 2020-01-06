#!/usr/bin/env python3 

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



from __future__ import print_function
from iscesys.Component.Component import Component
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
from isceobj.Util import simamplitude
from isceobj.Util.decorators import dov, pickled, logged

@pickled
class Simamplitude(Component):

    logging_name = 'isce.stdproc.simamplitude'
    
    dictionaryOfVariables = { 
        'WIDTH' : ['width', int, False],
        'LENGTH' : ['length', int,  False], 
        'SHADE_SCALE' : ['shadeScale', float, False] 
        }

    @dov
    @logged
    def __init__(self):
        super(Simamplitude, self).__init__()
        self.topoImage = None
        self.simampImage = None
        self.width = None
        self.length = None
        self.shadeScale = None
        return None

    def simamplitude(self,
                    topoImage,
                    simampImage,
                    shade=None,
                    width=None,
                    length=None):
        if shade  is not None: self.shadeScale = shade
        if width  is not None: self.width = width
        if length is not None: self.length = length
        self.topoImage = topoImage 
        self.simampImage = simampImage
        topoAccessor = self.topoImage.getImagePointer()
        simampAccessor = self.simampImage.getImagePointer()
        self.setDefaults()
        self.setState()
        simamplitude.simamplitude_Py(topoAccessor, simampAccessor)
        return

    def setDefaults(self):
        if self.width is None: self.width = self.topoImage.getWidth() 
        if self.length is None:
            self.length = self.topoImage.getLength()
        if  self.shadeScale is None:
            self.shadeScale = 1
            self.logger.warning(
            'The shade scale factor has been set to the default value %s'%
            (self.shadeScale)
            )
            pass
        return

    def setState(self):
        simamplitude.setStdWriter_Py(int(self.stdWriter))
        simamplitude.setImageWidth_Py(int(self.width))
        simamplitude.setImageLength_Py(int(self.length))
        simamplitude.setShadeScale_Py(float(self.shadeScale))
        return

    def setImageWidth(self, var):
        self.width = int(var)
        return

    def setImageLength(self, var):
        self.length = int(var)
        return

    def setShadeScale(self, var):
        self.shadeScale = float(var)
        return
    pass
