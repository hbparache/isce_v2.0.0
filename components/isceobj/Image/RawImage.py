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
import logging
from .Image import Image

##
# This class allows the creation of a RawImage object. The parameters that need to be set are
#\verbatim
#WIDTH: width of the image in units of the DATA_TYPE. Mandatory.
#FILE_NAME: name of the file containing the image. Mandatory.
#DATA_TYPE: data  type used to store the image. The naming convention is the one adopted by numpy (see LineAccessor class). Optional. Default value 'BYTE'.
#ACCESS_MODE: access mode of the file such as 'read', 'write' etc. See LineAccessor class for all possible values. Mandatory.
#NUMBER_GOOD_BYTES: number of bytes cosidered good for computation. Must be less or equal WIDTH. Optional. Default value WIDTH.
#SCHEME: the interleaving scheme adopted for the image. Could be BIL (band interleaved by line), BIP (band intereleaved by pixel) and BSQ (band sequential). Optional. BIP set by default.
#CASTER: define the type of caster. For example DoubleToFloat reads the image data as double but puts it into a buffer that is of float type. Optional. If not provided casting is not performed.
#\endverbatim
#Since the RawImage class inherits the Image.Image, the methods of initialization described in the Component package can be used.
#Moreover each parameter can be set with the corresponding accessor method setParameter() (see the class member methods).
#@see DataAccessor.Image.
#@see Component.Component.
class RawImage(Image):

    def __init__(self):

      Image.__init__(self)
      self.imageType = 'raw'
      self.dictionaryOfVariables.update({'NUMBER_GOOD_BYTES':['self.numberGoodBytes','int','optional']})

      self.mandatoryVariables = []
      self.optionalVariables = []
      self.initOptionalAndMandatoryLists()
        #optional variables
      self.numberGoodBytes = None
      self.dataType = 'BYTE'
      self.bands = 1
      self.scheme = 'BIP'

        #mandatory variables
      self.width = None
      self.filename = ''
      self.accessMode = ''

      self.logger = logging.getLogger('isce.Image.RawImageBase')
      return None


    def __getstate__(self):
        d = dict(self.__dict__)
        del d['logger']
        return d
    def __setstate__(self,d):
        self.__dict__.update(d)
        self.logger = logging.getLogger('isce.Image.RawImageBase')
        return

##
# This method creates a LineAccessor.LineAccessor instance. The method also runs Component.InitComponent.checkIntialization().
# If the parameters tagged as mandatory are not set, an exception is thrown.
    def createImage(self):


        if self.xmin == None:
            self.xmin = 0
        if self.xmax == None:
            self.xmax = self.width
        if self.numberGoodBytes == None:
            self.logger.info('Variable NUMBER_GOOD_BYTES of the raw image %s set equal to (xmax - xmin)   = %i in RawImageBase.py' % (self.filename,self.xmax - self.xmin))
            self.numberGoodBytes = self.xmax - self.xmin

        self.checkInitialization()
        Image.createImage(self)
        return None

    def setNumberGoodBytes(self,num):
        self.numberGoodBytes = int(num)
    def getNumberGoodBytes(self):
        return self.numberGoodBytes
    pass

