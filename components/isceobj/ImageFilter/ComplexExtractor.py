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
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
#this is the c bindings
from isceobj.ImageFilter import Filter as FL
from isceobj.ImageFilter.ImageFilter import Filter
from isceobj.Image.Image import Image
import logging
class ComplexExtractor(Filter):
    """Extracts components (real, imaginary, magnitude, phase) from a complex datatype"""
#Use kwargs so each subclass can add parameters to the init function.  
#If nameOut is a string then create the image using the input image info,
#otherwise check if it is an image object and raise an exception if not.

    def init(self,imgIn,nameOut,**kwargs):
        """Method to pass the input and output image to the  filter"""
        # check if the output image nameOut is provided. If it is a string create the image here using
        # the input image as template
        if isinstance(nameOut,str):
            #create generic image
            self._imgOut = Image()
            width = imgIn.getWidth()
            accessmode = 'write'
            bands = imgIn.getBands()
            scheme = imgIn.getInterleavedScheme()
            typec = imgIn.getDataType()
            #The assumption is that the imgIn is complex. The single component is the imgIn data type without the C
            # for instace CREAL becomes REAL
            typeF = typec[1:]
            #create output image of the same type as input
            self._imgOut.initImage(nameOut,accessmode,width,typeF,bands,scheme)
            self._imgOut.createImage()
            #if created here then need to finalize at the end
            self._outCreatedHere = True
        elif(nameOut,Image):
            self._imgOut = nameOut

        else:
            print("Error. The second argument of ComplexExtractor.init() must be a string or an Image object")
            raise TypeError


        imgIn.createImage() # just in case has not been run before. if it was run then it does not have any effect 
        accessorIn = imgIn.getImagePointer()
        accessorOut = self._imgOut.getImagePointer()
        FL.init(self._filter,accessorIn,accessorOut)
    
    def finalize(self):#extend base one
        """Finalize filter baseclass and output accessor if created here and not passed"""
        if self._outCreatedHere: 
            self._imgOut.finalizeImage()
        Filter.finalize(self)
    def __getstate__(self):
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self,d):
        self.__dict__.update(d)
        self.logger = logging.getLogger('isce.isceobj.ImageFilter.ComplexExtractor')
        return
    
    def __init__(self,typeExtractor,fromWhat):
        """Initialize the filter passing what is extracted and from what type of complex image"""
        Filter.__init__(self)
        self.logger = logging.getLogger('isce.isceobj.ImageFilter.ComplexExtractor')
        #possible inputs
        #(MagnitudeExctractor,'cartesian') 
        #(MagnitudeExctractor,'polar') 
        #(PhaseExctractor,'cartesian')
        #(PhaseExctractor,'polar')
        #(RealExctractor,'cartesian') 
        #(ImagExctractor,'cartesian')
        #(RealExctractor,'polar')
        #(ImagExctractor,'polar') 
        #get the filter C++ object pointer calling the Filtermodule.cpp which calls the FilterFactory.cpp
        self._filter = FL.createFilter(typeExtractor,fromWhat)
        self._outCreatedHere = False
        self._imgOut = None 




if __name__ == "__main__":
    sys.exit(main())
