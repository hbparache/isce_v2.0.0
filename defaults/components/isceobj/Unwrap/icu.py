#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2013 to the present, California Institute of Technology.
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
# Author: Piyush Agram
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




import sys
import isce
from mroipac.icu.Icu import Icu
from iscesys.Component.Component import Component
from isceobj.Constants import SPEED_OF_LIGHT
import isceobj


class icu(Component):
    '''Specific connector from an insarApp object to a Snaphu object.'''
    def __init__(self, obj):

        basename = obj.insar.topophaseFlatFilename
        wrapName = basename
        unwrapName = basename.replace('.flat', '.unw')

        #Setup images
        self.ampImage = obj.insar.resampAmpImage.copy(access_mode='read')
        self.width = self.ampImage.getWidth()

        #intImage
        intImage = isceobj.createIntImage()
        intImage.initImage(wrapName, 'read', self.width)
        intImage.createImage()
        self.intImage = intImage

        #unwImage
        unwImage = isceobj.Image.createImage()
        unwImage.setFilename(unwrapName)
        unwImage.setWidth(self.width)
        unwImage.imageType = 'unw'
        unwImage.bands = 2
        unwImage.scheme = 'BIL'
        unwImage.dataType = 'FLOAT'
        unwImage.setAccessMode('write')
        unwImage.createImage()
        self.unwImage = unwImage


    def unwrap(self):
        icuObj = Icu()
        icuObj.filteringFlag = False      ##insarApp.py already filters it
        icuObj.initCorrThreshold = 0.1
        icuObj.icu(intImage=self.intImage, ampImage=self.ampImage, unwImage = self.unwImage)

        self.ampImage.finalizeImage()
        self.intImage.finalizeImage()
        self.unwImage.renderHdr()
        self.unwImage.finalizeImage()

