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
import contextlib
from iscesys.Dumpers.XmlDumper import XmlDumper
from iscesys.Component.Configurable import Configurable
from iscesys.ImageApi.DataAccessorPy import DataAccessor
from iscesys.ImageApi import CasterFactory as CF
from iscesys.DictUtils.DictUtils import DictUtils as DU
from isceobj.Util import key_of_same_content
from isceobj.Util.decorators import pickled, logged

## \namespace ::isce.components.isceobj.Image Base class for Image API


## This is the default copy list-- it is not a class attribute because the
## I decided the class wwas too big-- but that's strictly subjective.
ATTRIBUTES = ('bands', 'scheme', 'caster', 'width', 'filename', 'byteOrder',
              'dataType', 'xmin', 'xmax', 'numberGoodBytes', 'firstLatitude',
              'firstLongitude', 'deltaLatitude', 'deltaLongitude')

## Map various byte order codes to Image's.
ENDIAN = {'l':'l', 'L':'l', '<':'l', 'little':'l', 'Little':'l',
          'b':'b', 'B':'b', '>':'b',    'big':'b', 'Big':'b'}
               

@pickled
class Image(DataAccessor,Configurable):
    
    logging_name = 'isce.isceobj.Image.Image'

    def __init__(self, name=None):
        DataAccessor.__init__(self)
        Configurable.__init__(self, 'image', name)
        self._instanceInit()
        return None

    ## New usage is: image.copy_attribute(image', *args), replacing:
    ## ImageUtil.ImageUtil.ImageUtil.copyAttributes(image, image', *args)
    def copy_attributes(self, other, *args):
        for item in args or ATTRIBUTES:
            try:
                setattr(other, item, getattr(self, item))
            except AttributeError:
                pass
        return other

    ## This method makes a new image sub-class object that are copies of
    ## existing ones.
    def copy(self, access_mode=None):
        obj_new = self.copy_attributes(self.__class__())
        if access_mode:
            obj_new.setAccessMode(access_mode)
        obj_new.createImage()
        return obj_new

    ## Call the copy method, as a context manager
    @contextlib.contextmanager
    def ccopy(self, access_mode=None):
        result = self.copy(access_mode=access_mode)
        yield result
        result.finalizeImage()
        pass

    ## creates a DataAccessor.DataAccessor instance. If the parameters tagged
    ## as mandatory are not set, an exception is thrown.
    def createImage(self):       
        self.createAccessor()
        da = self.getAccessor()
        try:
            fsize = os.path.getsize(self.filename)
        except OSError:
            print("File",self.filename,"not found")
            raise OSError
        size = self.getTypeSize()
        if(fsize != self.width*self.length*size*self.bands):
            print("Image.py::createImage():Size on disk and  size computed from metadata for file",\
                  self.filename,"do not match")
            sys.exit(1)
        return None
    
    
    ##
    # Initialize the image instance from an xml file
    def load(self,filename):
        from iscesys.Parsers.FileParserFactory import createFileParser
        parser = createFileParser('xml')
        #get the properties from the file
        prop, fac, misc = parser.parse(filename)
        self.init(prop,fac,misc)

    def renderHdr(self):
        from datetime import datetime
        from isceobj.XmlUtil import xmlUtils as xml
        from isce import release_version, release_svn_revision, release_date, svn_revision
#        odProp = {}
#        odMisc = {}
#        odFact = {}
        odProp = xml.OrderedDict()
        odFact = xml.OrderedDict()
        odMisc = xml.OrderedDict()
        # hack since the length is normally not set but obtained from the file
        # size, before rendering  make sure that coord1.size is set to length
        self.coord2.coordSize = self.length
        self.renderToDictionary(self, odProp,odFact,odMisc)
        # remove key,value parir with empty value (except if value is zero)
        DU.cleanDictionary(odProp)
        DU.cleanDictionary(odFact)
        DU.cleanDictionary(odMisc)
        odProp['ISCE_VERSION']  = "Release: %s, svn-%s, %s. Current: svn-%s." %  \
                             (release_version, release_svn_revision, release_date, svn_revision)
        outfile = self.getFilename() + '.xml'
        firstTag = 'imageFile'
        XD = XmlDumper()
        XD.dump(outfile, odProp, odFact, odMisc, firstTag)
        return None

    ##
    # This method renders and ENVI HDR file similar to the XML file.

    def renderEnviHDR(self):
        '''
        Renders a bare minimum ENVI HDR file, that can be used to directly ingest the outputs into a GIS package.
        '''

        typeMap = { 'BYTE'   : 1,
                    'SHORT'  : 2,
                    'INT'    : 3,
                    'LONG'   : 14,
                    'FLOAT'  : 4,
                    'DOUBLE' : 5,
                    'CFLOAT' : 6,
                    'CDOUBLE': 9 }

        orderMap = {'L' : 0,
                    'B' : 1}

        tempstring = """ENVI
description = {{Data product generated using ISCE}}
samples = {0}
lines   = {1}
bands   = {2}
header offset = 0
file type = ENVI Standard
data type = {3}
interleave = {4}
byte order = {5}
"""
        map_infostr = """coordinate system string = {{GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137, 298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]]}}
map_info = {{Geographic Lat/Lon, 1.0, 1.0, {0}, {1}, {2}, {3}, WGS-84, units=Degrees}}"""
        
        parList = list(range(4))
        parList[0] = self.coord1.coordStart
        parList[1] = self.coord2.coordStart
        parList[2] = self.coord1.coordDelta
        parList[3] = -self.coord2.coordDelta
    
        flag = any(v is None for v in parList)




        outfile = self.getFilename() + '.hdr'
        outstr = tempstring.format(self.width, self.length,
                self.bands, typeMap[self.dataType.upper()],
                self.scheme.lower(),
                orderMap[ENDIAN[self.byteOrder].upper()])
        if not flag:
            outstr += map_infostr.format(parList[0], parList[1], parList[2], parList[3])

        with open(outfile, 'w') as f:
            f.write(outstr)

        return



    ##
    # This method initialize the Image.
    #@param filename \c string the file name associated with the image.
    #@param accessmode \c string access mode of the  file.
    #@param bands \c int number of bands of the interleaving scheme.
    #@param type \c string data type used to store the data.
    #@param width \c int width of the image.
    #@param scheme \c string interleaving scheme.
    #@param caster \c string type of caster (ex. 'DoubleToFloat').
    def initImage(self, filename, accessmode, width,
                  type=None, bands=None, scheme = None,caster = None):
    
        self.initAccessor(filename,accessmode,width,type,bands,scheme,caster)
    ## This method gets the pointer associated to the DataAccessor.DataAccessor
    ## object created.
    #@return \c pointer pointer to the underlying DataAccessor.DataAccessor 
    ## object.
    def getImagePointer(self):
        return self.getAccessor()
    
    ## gets the string describing the image for the user
    ##@return \c text description string describing the image in English for 
    ## the user
    def getDescription(self):
        return self.description
    
    ## This method appends the string describing the image for the user create
    ## a list.
    ##@param doc \c text description string describing the image in English for
    ##  the user
    def addDescription(self, doc):
        if self.description == '':
            self.description = [doc]
        elif isinstance(self.description,list):
            self.description.append(doc)

    ## This method gets the length associated to the DataAccessor.DataAccessor 
    ## object created.
    ## @return \c int length of the underlying DataAccessor.DataAccessor object.
    def getLength(self):
        return self.coord2.coordSize or self.getFileLength()

    # Always call this function if  createImage() was previously invoked. 
    # It deletes the pointer to the object, closes the file associated with 
    # the object, frees memory. 
    def finalizeImage(self):
        self.finalizeAccessor()
    
    def setImageType(self, val):
        self.imageType = str(val)

    def setLength(self, val):
        #needed because the __init__ calls self.lenth = None which calls this 
        # function and the casting would fail with time possibly need to
        # refactor all the image API with better inheritance
        if not val is None:
            self.coord2.coordSize = int(val)
    
    def getWidth(self):
        return self.coord1.coordSize
    
    def setWidth(self, val):
        #see getLength
        if not val is None:
            width = int(val)
            self.coord1.coordSize = width
#            self.width = width
#            DataAccessor.setWidth(self, width)
    
    def setXmin(self, xmin):
        self.xmin = int(xmin)
        
    def getXmin(self):
        return self.xmin
    
    def setXmax(self, xmax):
        self.xmax = int(xmax)
        
    def getXmax(self):
        return self.xmax

    def setByteOrder(self, byteOrder):
        try:
            b0 = ENDIAN[byteOrder]
        except KeyError:
            self.logger.error(
                self.__class__.__name__ +
                ".setByteOorder got a bad argument:" +
                str(byteOrder)
                )
            raise ValueError(str(byteOrder) +
                             " is not a valid byte ordering, e.g.\n"+
                             str(ENDIAN.keys()))
        self.byteOrder = b0
        return None
       
    ## Set the caster type if needed
    #@param accessMode \c string access mode of the file. Can be 'read' or 'write'
    #@param dataType \c string is the dataType from or to the caster writes or reads.
    def setCaster(self,accessMode,dataType):
        self.accessMode = accessMode
        if(accessMode == 'read'):
            self.caster = CF.getCaster(self.dataType,dataType)
        elif(accessMode == 'write'):
            self.caster = CF.getCaster(dataType,self.dataType)
        else:
            print('Unrecorgnized access mode',accessMode)
            raise ValueError

    
    def setFirstLatitude(self, val):
        self.coord2.coordStart = val
    
    def setFirstLongitude(self, val):
        self.coord1.coordStart = val

    def setDeltaLatitude(self, val):
        self.coord2.coordDelta = val
    
    def setDeltaLongitude(self, val):
        self.coord1.coordDelta = val
    
    def getFirstLatitude(self):
        return self.coord2.coordStart
    
    def getFirstLongitude(self):
        return self.coord1.coordStart

    def getDeltaLatitude(self):
        return self.coord2.coordDelta
    
    def getDeltaLongitude(self):
        return self.coord1.coordDelta
    def getImageType(self):
        return self.imageType

    def getByteOrder(self):
        return self.byteOrder

    def getProduct(self):
        return self.product
    
    def setProduct(self, val):
        self.product = val

    def _facilities(self):
        self.coord1 = self.facility('coord1',public_name='Coordinate1',module='isceobj.Image',factory='createCoordinate',mandatory='True',doc='First coordinate of a 2D image (witdh).')
        self.coord2 = self.facility('coord2',public_name='Coordinate2',module='isceobj.Image',factory='createCoordinate',mandatory='True',doc='Second coordinate of a 2D image (length).')
    
    def _parameters(self):
        self.byteOrder = self.parameter('byteOrder',public_name='BYTE_ORDER',default=sys.byteorder[0].lower(),
                                       type=str,mandatory=False,doc='Endianness of the image.')
        self.scheme = self.parameter('scheme',public_name='SCHEME',default='BIP',
                                       type=str,mandatory=False,doc='Interleaving scheme of the image.')
        self.caster = self.parameter('caster',public_name='CASTER',default='',
                                       type=str,mandatory=None,doc='Type of conversion to be performed from input '
                                     + 'source to output source. Being input or output source will depend on the type of operations performed (read or write)')
        self.bands = self.parameter('bands',public_name='NUMBER_BANDS',default=1,
                                       type=int,mandatory=False,doc='Number of image bands.')
        self.width = self.parameter('width',public_name='WIDTH',default=None,
                                       type=int,mandatory=True,doc='Image width.')

        self.length = self.parameter('length',public_name='LENGTH',default=None,
                                       type=int,mandatory=None,doc='Image length.')
        self.dataType = self.parameter('dataType',public_name='DATA_TYPE',default='',
                                       type=str,mandatory=True,doc='Image data type.')
        self.imageType = self.parameter('imageType',public_name='IMAGE_TYPE',default='',
                                       type=str,mandatory=None,doc='Image type used for displaying.')
        self.filename = self.parameter('filename',public_name='FILE_NAME',default='',
                                       type=str,mandatory=True,doc='Name of the image file.')
        self.accessMode = self.parameter('accessMode',public_name='ACCESS_MODE',default='',
                                       type=str,mandatory=True,doc='Image access mode.')
        self.description  = self.parameter('description',public_name='DESCRIPTION',default='',
                                       type=str,mandatory=None,doc='Image description')
        self.xmin  = self.parameter('xmin',public_name='XMIN',default=None,
                                       type=float,mandatory=None,doc='Minimum range value')
        self.xmax  = self.parameter('xmax',public_name='XMAX',default=None,
                                       type=float,mandatory=None,doc='Maximum range value')
        self.isce_version  = self.parameter('isce_version',public_name='ISCE_VERSION',default=None,
                                       type=float,mandatory=None,doc='Information about the isce release version.')

    firstLatitude = property(getFirstLatitude,setFirstLatitude)
    firstLongitude = property(getFirstLongitude,setFirstLongitude)
    deltaLatitude = property(getDeltaLatitude,setDeltaLatitude)
    deltaLongitude = property(getDeltaLongitude,setDeltaLongitude)
    width = property(getWidth,setWidth)
    length = property(getLength,setLength)

    pass

## because of backward compatibility where the size of the corrdinate had two 
## different names  (i.e. width and lenth), let's distinguish between to two 
## coordinate. Can subclass but it seems an overkill
class ImageCoordinate(Configurable):

    def __init__(self):
        ## Call super with class name
        super(ImageCoordinate, self).__init__(self.__class__.__name__)
        self.coordDescription = ''
        self.coordStart = None
        self.coordDelta = None
        self.coordSize = None
        self.mandatoryVariables = []
        self.optionalVariables = []
        self._parameters()
        self.initOptionalAndMandatoryLists()

        return None

    def _parameters(self):
        self.coordStart = self.parameter('coordStart', public_name='startingValue', default=None,units='degree',
                                         type=float, mandatory=False,
                                         doc="Starting value of the coordinate.")
        self.coordDelta = self.parameter('coordDelta', public_name='delta', default=None,units='',
                                         type=float, mandatory=False,
                                         doc="Coordinate quantization.")
        
        self.coordSize = self.parameter('coordSize', public_name='size', default=None,
                                         type=float, mandatory=None,
                                         doc="Coordinate size.")
 
    pass
    
