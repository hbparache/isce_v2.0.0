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
# Author: Walter Szeliga
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




from iscesys.Component.Component import Component

##
# This class provides a basis for image and metadata renderers
#
class BaseRenderer(Component):
    
    def __init__(self):
        Component.__init__(self)        
        
        
        self.dictionaryOfVariables = {'COMPONENT': ['self.component','Component','mandatory']}
        
    def setComponent(self,component):
        if (isinstance(component,Component)):
            self.component = component
        else:
            raise TypeError("component should be of type Component but was of type %s" % component.__class__)
        
    def getComponent(self):
        return self.component
