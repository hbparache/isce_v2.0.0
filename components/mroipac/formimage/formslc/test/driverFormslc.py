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
import sys
import os
import math
from iscesys.Component.FactoryInit import FactoryInit
from mroipac.formimage.FormSLC import FormSLC
from iscesys.Compatibility import Compatibility
import getopt
Compatibility.checkPythonVersion()

class DriverFormSLC(FactoryInit):
    
            
        
    
    def main(self):
        #get the initialized objects i.e. the raw and slc image and the FormSLC 
        objSlc = self.getComponent('SlcImage')
        objSlc.createImage()
        objRaw = self.getComponent('RawImage')
        objRaw.createImage()
        objFormSlc = self.getComponent('FormSlc')        
        ####
        objFormSlc.formSLCImage(objRaw,objSlc)
        objSlc.finalizeImage()
        objRaw.finalizeImage()

    def __init__(self,argv):
        FactoryInit.__init__(self)
        #call the init factory passing the init file DriverFormSLC.xml as a argument when calling the script
        self.initFactory(argv[1:])

if __name__ == "__main__":
    runObj = DriverFormSLC(sys.argv)
    runObj.main()
