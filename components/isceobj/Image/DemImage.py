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
import logging
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()

from .Image import Image

from iscesys.Component.Component import Component
##
# This class allows the creation of a DemImage object. The parameters that need to be set are
#\verbatim
#WIDTH: width of the image in units of the DATA_TYPE. Mandatory. 
#FILE_NAME: name of the file containing the image. Mandatory.
#DATA_TYPE: data  type used to store the image. The naming convention is the one adopted by numpy (see LineAccessor class). Optional. Default value 'BYTE'. 
#ACCESS_MODE: access mode of the file such as 'read', 'write' etc. See LineAccessor class for all possible values. Mandatory.
#FIRST_LATITUDE: first latitude of the DEM image.
#FIRST_LONGITUDE: first longitude of the DEM image.
#DELTA_LATITUDE: separation in latitude between two pixels.
#DELTA_LONGITUDE: separation in longitude between two pixels.
#SCHEME: the interleaving scheme adopted for the image. Could be BIL (band interleaved by line), BIP (band intereleaved by pixel) and BSQ (band sequential). Optional. BIP set by default.
#CASTER: define the type of caster. For example DoubleToFloat reads the image data as double but puts it into a buffer that is of float type. Optional. If not provided casting is not performed.
#\endverbatim
#Since the DemImage class inherits the Image.Image, the methods of initialization described in the Component package can be used.
#Moreover each parameter can be set with the corresponding accessor method setParameter() (see the class member methods).
#@see DataAccessor.Image.
#@see Component.Component.
class DemImage(Image):


    def createImage(self):
        
        self.checkInitialization()
        Image.createImage(self)        

    family = "demimage"

    def __init__(self,family='',name=''):

        
        Image.__init__(self)

        self.dictionaryOfVariables.update({'REFERENCE':['reference','str','optional'],'FIRST_LATITUDE':['firstLatitude','float','optional'],'FIRST_LONGITUDE':['firstLongitude','float','optional'],'DELTA_LATITUDE':['deltaLatitude','float','optional'],'DELTA_LONGITUDE':['deltaLongitude','float','optional']})
        self.initOptionalAndMandatoryLists()
        self.imageType = 'dem'
            
        

        
        #optional variables
        self.bands = 1
        self.scheme = 'BIP'
        self.dataType = 'SHORT'
        self.firstLatitude = 0
        self.firstLongitude = 0
        self.deltaLatitude = 0
        self.deltaLongitude = 0
        self.reference = 'EGM96'
        
        #mandatory variables
        self.width = None
        self.filename = ''
        self.accessMode = ''

        self.logger = logging.getLogger('isce.Image.DemImageBase')
        
        
        
        return

    def getsnwe(self):
        '''Return the bounding box.'''

        lats = [self.firstLatitude, self.firstLatitude + (self.length-1)*self.deltaLatitude]
        lons = [self.firstLongitude, self.firstLongitude + (self.width-1)*self.deltaLongitude]

        snwe = [min(lats), max(lats), min(lons), max(lons)]
        return snwe
    
    def __getstate__(self):
        d = dict(self.__dict__)
        del d['logger']
        return d
    def __setstate__(self,d):
        self.__dict__.update(d)
        self.logger = logging.getLogger('isce.Image.DemImageBase')
        return
    
        # to make it backward compatible with the old way of working, basically we aliased this variables 
        # to the equivalent ones in the Image base class objects  coord1,coord2


#end class




if __name__ == "__main__":
    sys.exit(main())
