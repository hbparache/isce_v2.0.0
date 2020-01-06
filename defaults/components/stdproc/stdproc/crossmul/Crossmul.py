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
import isce
from iscesys.Component.Component import Component,Port
from iscesys.Compatibility import Compatibility
from stdproc.stdproc.crossmul import crossmul
import numpy as np

class Crossmul(Component):
    
    def crossmul(self, image1=None, image2=None, imageInt=None, imageAmp=None):
        
#        for port in self._inputPorts:
#            port()

        if image1 is not None:
            self.image1 = image1
        if self.image1 is None:
            raise Exception

        if image2 is not None:
            self.image2 = image2
        if self.image2 is None:
            raise Exception

        if imageInt is not None:
            self.imageInt= imageInt
        if self.imageInt is None:
            raise Exception

        if imageAmp is not None:
            self.imageAmp= imageAmp
        if self.imageAmp is None:
            raise Exception

        image1Accessor = self.image1.getImagePointer()
        image2Accessor = self.image2.getImagePointer()
        #create the int and amp file to allow random access
        lengthIntAmp = np.ceil(self.width / (self.LooksDown*1.0))
#        self.imageInt.createFile(lengthIntAmp)
#        self.imageAmp.createFile(lengthIntAmp)
        imageIntAccessor = self.imageInt.getImagePointer()
        imageAmpAccessor = self.imageAmp.getImagePointer()
       

        #remember we put the offset for the images in one array
        # so twice the length
        self.setState()
        crossmul.crossmul_Py(self._ptr, image1Accessor,
                         image2Accessor,
                         imageIntAccessor,
                         imageAmpAccessor)
        self.imageAmp.bandDescription = ['amplitude slc1','amplitude slc2']
        self.imageInt.renderHdr()
        self.imageAmp.renderHdr()
        
        #since the across and down offsets are returned in one array,
        # just split it for each location  #should be an even number
        return


    def setState(self):
        print('Self pointer: ', self._ptr)
        crossmul.setWidth_Py(self._ptr, self.width)
        crossmul.setLength_Py(self._ptr, self.length)
        crossmul.setLooksAcross_Py(self._ptr, self.LooksAcross)
        crossmul.setLooksDown_Py(self._ptr, self.LooksDown)
        crossmul.setBlocksize_Py(self._ptr, self.blocksize)
        crossmul.setScale_Py(self._ptr, self.scale)
        print('Completed set State')
        return


    def __init__(self):
        super(Crossmul, self).__init__()

        self.width = None
        self.length = None
        self.LooksAcross  = None
        self.LooksDown = None
        self.scale = 1.0
        self.blocksize = 1024
        self._ptr = crossmul.createCrossMul_Py()

        self.image1 = None
        self.image2 = None
        self.imageInt = None
        self.imageAmp = None

        self.dictionaryOfVariables = {} 
        self.dictionaryOfOutputVariables = {} 
        self.descriptionOfVariables = {}
        self.mandatoryVariables = []
        self.optionalVariables = []
        typePos = 2
        for key , val in self.dictionaryOfVariables.items():
            if val[typePos] == 'mandatory':
                self.mandatoryVariables.append(key)
            elif val[typePos] == 'optional':
                self.optionalVariables.append(key)
            else:
                print('Error. Variable can only be optional or mandatory')
                raise Exception
            pass
        return

    def __del__(self):
        crossmul.destroyCrossMul_Py(self._ptr)

    def createPorts(self):
        return None

    pass


if __name__ == '__main__':

    import isceobj
    from iscesys.ImageUtil.ImageUtil import ImageUtil as IU
    import numpy as np

    def load_pickle(step='correct'):
        import cPickle
        
        iObj = cPickle.load(open('PICKLE/{0}'.format(step),'rb'))
        return iObj


    rlooks =1 
    alooks = 1

    iObj = load_pickle()

    objSlc1 = iObj.topoIntImage
    objSlc1.setAccessMode('read')
    objSlc1.createImage()

    wid = objSlc1.getWidth()
    lgth = objSlc1.getLength()

    objSlc2 = isceobj.createSlcImage()
    objSlc2.initImage(iObj.topophaseMphFilename, 'read', wid)
    objSlc2.createImage()

    objInt = isceobj.createIntImage()
    objInt.setFilename('test.int')
    objInt.setWidth(wid/rlooks)
    objInt.setAccessMode('write')
    objInt.createImage()

    objAmp = isceobj.createAmpImage()
    objAmp.setFilename('test.amp')
    objAmp.setWidth(wid/rlooks)
    objAmp.setAccessMode('write')
    objAmp.createImage()

    mul = Crossmul()
    mul.width = wid
    mul.length = lgth
    mul.LooksAcross = rlooks
    mul.LooksDown = alooks
    mul.scale = 1.0
    mul.blocksize = 100

    mul.crossmul(objSlc1, objSlc2, objInt, objAmp)


    objSlc1.finalizeImage()
    objSlc2.finalizeImage()
    objInt.finalizeImage()
    objAmp.finalizeImage()
