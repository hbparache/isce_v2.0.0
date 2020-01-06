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
from isceobj.RawImage.RawImage import RawImage
from isceobj.SlcImage.SlcImage import SlcImage
from isceobj.Platform.Platform import Platform
from isceobj.Radar.Radar import Radar
from iscesys.Component.InitFromXmlFile import InitFromXmlFile
from iscesys.Component.InitFromObject import InitFromObject
from iscesys.Component.InitFromDictionary import InitFromDictionary
from mroipac.formimage.FormSLC import FormSLC
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()

def main():
    
    # create FormSLC object and initilaize it using FormSLC930110.xml. it actually contains all the parameters already except the raw and slc images.
    # one could use the Platform and Radar objects to change some of the parameters.
    obj = FormSLC()
    initfileForm = 'FormSCL930110.xml'
    #instantiate a InitFromXmlFile object passinf the file name in the contructor
    fileInit = InitFromXmlFile(initfileForm)
    # init FormSLC by passing the init object
    obj.initComponent(fileInit)
    
    
    initfilePl = 'Platform930110.xml'
    fileInit = InitFromXmlFile(initfilePl)
    objPl = Platform()
    objPl.initComponent(fileInit)
    
    #instantiate a InitFromObject object passing the object from which to initialize in the contructor
    objInit = InitFromObject(objPl)
    obj.initComponent(objInit)
    
    initfileRadar = 'Radar930110.xml'
    fileInit = InitFromXmlFile(initfileRadar)
    objRadar = Radar()
    objRadar.initComponent(fileInit)
    
    objInit = InitFromObject(objRadar)
    obj.initComponent(objInit)
    obj.printComponent()    
    filename = "930110.raw"
    accessmode = 'read'
    endian = 'l'
    width = 11812 
    
    objRaw = RawImage()
    # only sets the parameter
    objRaw.initImage(filename,accessmode,endian,width)
    # it actually creates the C++ object
    objRaw.createImage()
    
    filenameSLC ="930110.slc"
    accessmode = 'write'
    endian = 'l'
    width = 5700
    
    dict = {'FILE_NAME':filenameSLC,'ACCESS_MODE':accessmode,'BYTE_ORDER':endian,'WIDTH':width}
    dictInit = InitFromDictionary(dict)
    objSlc = SlcImage()
    
    objSlc.initComponent(dictInit)
    objSlc.createImage()
   
    
    obj.formSLCImage(objRaw,objSlc)
    #call this to do some cleaning. always call it if initImage (or the initComponent) was called
    objSlc.finalizeImage()
    objRaw.finalizeImage()
    
if __name__ == "__main__":
    sys.exit(main())
