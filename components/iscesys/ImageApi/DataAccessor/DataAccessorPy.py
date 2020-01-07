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
from iscesys.ImageApi import DataAccessor as DA
import os
## If you finalize more than once, do you get an error?
ERROR_CHECK_FINALIZE = False

class DataAccessor(object):

    def __init__(self):
        self._accessor = None
        self._factory = None
        self.scheme = ''
        self.caster = ''
        self.width = None
        self.bands = None
        self.length = None
        self.accessMode = ''
        self.filename = ''
        self.dataType = ''
        self._size = None
        return None

    ## Experimental
    def __int__(self):
        return self.getAccessor()

    def initAccessor(self, filename, filemode, width, 
                     type=None, bands=None, scheme=None, caster=None):
        self.filename = filename
        self.accessMode = filemode
        self.width = int(width)
        if type:
            self.dataType = type
        if bands:
            self.bands = int(bands)
        if scheme:
            self.scheme = scheme
        if caster:
            self.caster = caster
        return None

    def createAccessor(self):
        if self._accessor is None:#to avoid to creating duplicates
            size = DA.getTypeSize(self.dataType)
            caster = '' or self.caster
            self._accessor, self._factory = DA.createAccessor(
                self.filename, self.accessMode, size, self.bands, 
                self.width, self.scheme,caster
                )
        return None

    def finalizeAccessor(self):
        try:
            DA.finalizeAccessor(self._accessor, self._factory)
        except TypeError:
            message = "Image %s is already finalized" % str(self) 
            if ERROR_CHECK_FINALIZE:
                raise RuntimeError(message)
            else:
                print(message)

        self._accessor = None
        self._factory = None
        return None

    def getTypeSize(self):
        return DA.getTypeSize(self.dataType)
    def rewind(self):
        DA.rewind(self._accessor)

    def createFile(self, lines):
        DA.createFile(self._accessor, lines)
    
    def getFileLength(self):
        openedHere = False

        if self._accessor is None:
            openedHere = True
            self.initAccessor(self.filename, 'read', int(self.width),
                              self.dataType, int(self.bands), self.scheme)
            self.createAccessor()
        length = DA.getFileLength(self._accessor)

        if openedHere:
            self.finalizeAccessor()

        return length

    def getAccessor(self):
        return self._accessor
    
    def getFilename(self):
        return self.filename
    
    def getAccessMode(self):
        return self.accessMode
    
    def getSize(self):
        return self.size
    
    def getBands(self):
        return self.bands

    ## Get the width associated to the DataAccessor.DataAccessor object created.
    #@return \c int width of the DataAccessor.DataAccessor object.
    def getWidth(self):
        return self.width
    
    def getInterleavedScheme(self):
        return self.scheme
    
    def getCaster(self):
        return self.caster
    
    def getDataType(self):
        return self.dataType
    
    def setFilename(self, val):
        self.filename = str(val)
    
    def setAccessMode(self, val):
        self.accessMode = str(val)
    
    def setBands(self, val):
        self.bands = int(val)
    
    def setWidth(self, val):
        self.width = int(val)
    
    def setInterleavedScheme(self, val):
        self.scheme = str(val)
    
    def setCaster(self, val):
        self.caster = val
    
    def setDataType(self, val):
        self.dataType = val
    
    pass

