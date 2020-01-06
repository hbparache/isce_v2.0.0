#!/usr/bin/env python3 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2011 to the present, California Institute of Technology.
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





from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()

from iscesys.Component.FactoryInit import FactoryInit
class FormSLCApp(FactoryInit):
    
  def main(self):
    self.objFormSlc.formSLCImage(self.objRaw,self.objSlc)
    print('second time')
    self.objFormSlc.formSLCImage(self.objRaw,self.objSlc)
    self.objSlc.finalizeImage()
    self.objRaw.finalizeImage()
    return
  
  def __init__(self, arglist):
    FactoryInit.__init__(self)
    self.initFactory(arglist)
    self.objSlc = self.getComponent('SlcImage')
    self.objSlc.createImage()
    self.objRaw = self.getComponent('RawImage')
    self.objRaw.createImage()
    self.objFormSlc = self.getComponent('FormSlc')        
    return
    
if __name__ == "__main__":
  import sys    
  runObj = FormSLCApp(sys.argv[1:])
  runObj.main()
    
