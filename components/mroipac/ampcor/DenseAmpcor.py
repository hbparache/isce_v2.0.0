#! /usr/bin/env python 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2014 to the present, California Institute of Technology.
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
# Author: Brent Minchew
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





from __future__ import print_function
import sys
import os
import math
import isceobj
from isceobj.Location.Offset import OffsetField,Offset
from iscesys.Component.Component import Component,Port
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
from iscesys.StdOEL.StdOELPy import create_writer
from .Ampcor import Ampcor
from isceobj.Util.mathModule import is_power2
import logging
import numpy as np
import multiprocessing as mp
from iscesys.ImageUtil.ImageUtil import ImageUtil as IU

def intround(n):
    if (n <= 0):
        return int(n-0.5)
    else:
        return int(n+0.5)

logger = logging.getLogger('mroipac.ampcor.denseampcor')

WINDOW_SIZE_WIDTH = Component.Parameter('windowSizeWidth',
        public_name='WINDOW_SIZE_WIDTH',
        default = 64,
        type = int,
        mandatory = False,
        doc = 'Width of the reference data window to be used for correlation')

WINDOW_SIZE_HEIGHT = Component.Parameter('windowSizeHeight',
        public_name='WINDOW_SIZE_HEIGHT',
        default = 64,
        type = int,
        mandatory = False,
        doc = 'Height of the reference data window to be used for correlation')

SEARCH_WINDOW_SIZE_WIDTH = Component.Parameter('searchWindowSizeWidth',
        public_name='SEARCH_WINDOW_SIZE_WIDTH',
        default = 100,
        type = int,
        mandatory = False,
        doc = 'Width of the search data window to be used for correlation')

SEARCH_WINDOW_SIZE_HEIGHT = Component.Parameter('searchWindowSizeHeight',
        public_name='SEARCH_WINDOW_SIZE_HEIGHT',
        default = 100,
        type = int,
        mandatory = False,
        doc = 'Height of the search data window to be used for correlation')

ZOOM_WINDOW_SIZE = Component.Parameter('zoomWindowSize',
        public_name = 'ZOOM_WINDOW_SIZE',
        default = 16,
        type = int,
        mandatory = False,
        doc = 'Zoom window around the local maximum for first pass')

OVERSAMPLING_FACTOR = Component.Parameter('oversamplingFactor',
        public_name = 'OVERSAMPLING_FACTOR',
        default = 16,
        type = int,
        mandatory = False,
        doc = 'Oversampling factor for the FFTs to get sub-pixel shift.')

ACROSS_GROSS_OFFSET = Component.Parameter('acrossGrossOffset',
        public_name = 'ACROSS_GROSS_OFFSET',
        default = None,
        type = int,
        mandatory = False,
        doc = 'Gross offset in the range direction.')

DOWN_GROSS_OFFSET = Component.Parameter('downGrossOffset',
        public_name = 'DOWN_GROSS_OFFSET',
        default = None,
        type = int,
        mandatory = False,
        doc = 'Gross offset in the azimuth direction.')

ACROSS_LOOKS = Component.Parameter('acrossLooks',
        public_name = 'ACROSS_LOOKS',
        default = 1,
        type = int,
        mandatory = False,
        doc = 'Number of looks to take in range before correlation')

DOWN_LOOKS = Component.Parameter('downLooks',
        public_name = 'DOWN_LOOKS',
        default = 1,
        type = int,
        mandatory = False,
        doc = 'Number of looks to take in azimuth before correlation')

SKIP_SAMPLE_ACROSS = Component.Parameter('skipSampleAcross',
        public_name = 'SKIP_SAMPLE_ACROSS',
        default = None,
        type = int,
        mandatory = False,
        doc = 'Number of samples to skip in range direction')

SKIP_SAMPLE_DOWN = Component.Parameter('skipSampleDown',
        public_name = 'SKIP_SAMPLE_DOWN',
        default = None,
        type = int,
        mandatory = False,
        doc = 'Number of windows in azimuth direction')

DOWN_SPACING_PRF1 = Component.Parameter('prf1',
        public_name = 'DOWN_SPACING_PRF1',
        default = 1.0,
        type = float,
        mandatory = False,
        doc = 'PRF or a similar scale factor for azimuth spacing of reference image.')

DOWN_SPACING_PRF2 = Component.Parameter('prf2',
        public_name = 'DOWN_SPACING_PRF2',
        default = 1.0,
        type = float,
        mandatory = False,
        doc = 'PRF or a similar scale factor for azimuth spacing of search image.')

ACROSS_SPACING1 = Component.Parameter('rangeSpacing1',
        public_name = 'ACROSS_SPACING1',
        default = 1.0,
        type = float,
        mandatory = False,
        doc = 'Range pixel spacing or similar scale factor for reference image.')

ACROSS_SPACING2 = Component.Parameter('rangeSpacing2',
        public_name = 'ACROSS_SPACING2',
        default = 1.0,
        type = float,
        mandatory = False,
        doc = 'Range pixel spacing or similar scale for search image.')

IMAGE_DATATYPE1 = Component.Parameter('imageDataType1',
        public_name = 'IMAGE_DATATYPE1',
        default='',
        type = str,
        mandatory = False,
        doc = 'Image data type for reference image (complex / real)')

IMAGE_DATATYPE2 = Component.Parameter('imageDataType2',
        default='',
        type = str,
        mandatory=False,
        doc = 'Image data type for search image (complex / real)')


SNR_THRESHOLD = Component.Parameter('thresholdSNR',
        public_name = 'SNR_THRESHOLD',
        default = 0.0,
        type = float,
        mandatory=False,
        doc = 'SNR threshold for valid matches.')

COV_THRESHOLD = Component.Parameter('thresholdCov',
        public_name = 'COV_THRESHOLD',
        default = 1000.0,
        type = float,
        mandatory=False,
        doc = 'Covariance threshold for valid matches.')

BAND1 = Component.Parameter('band1',
        public_name='BAND1',
        default=0,
        type = int,
        mandatory = False,
        doc = 'Band number of image1')

BAND2 = Component.Parameter('band2',
        public_name='BAND2',
        default=0,
        type=int,
        mandatory=False,
        doc = 'Band number of image2')

OFFSET_IMAGE_NAME = Component.Parameter('offsetImageName',
        public_name='OFFSET_IMAGE_NAME',
        default='dense_ampcor.bil',
        type=str,
        mandatory=False,
        doc = 'File name for two channel output')

SNR_IMAGE_NAME = Component.Parameter('snrImageName',
        public_name = 'SNR_IMAGE_NAME',
        default = 'dense_ampcor_snr.bil',
        type=str,
        mandatory=False,
        doc = 'File name for output SNR')

MARGIN = Component.Parameter('margin',
        public_name = 'MARGIN',
        default = 50,
        type = int,
        mandatory=False,
        doc = 'Margin around the edge of the image to avoid')

NUMBER_THREADS = Component.Parameter('numberThreads',
        public_name = 'NUMBER_THREADS',
        default=8,
        type=int,
        mandatory=False,
        doc = 'Number of parallel ampcor threads to launch')


class DenseAmpcor(Component):

    family = 'denseampcor'
    logging_name = 'isce.mroipac.denseampcor'

    parameter_list = (WINDOW_SIZE_WIDTH,
                      WINDOW_SIZE_HEIGHT,
                      SEARCH_WINDOW_SIZE_WIDTH,
                      SEARCH_WINDOW_SIZE_HEIGHT,
                      ZOOM_WINDOW_SIZE,
                      OVERSAMPLING_FACTOR,
                      ACROSS_GROSS_OFFSET,
                      DOWN_GROSS_OFFSET,
                      ACROSS_LOOKS,
                      DOWN_LOOKS,
                      SKIP_SAMPLE_ACROSS,
                      SKIP_SAMPLE_DOWN,
                      DOWN_SPACING_PRF1,
                      DOWN_SPACING_PRF2,
                      ACROSS_SPACING1,
                      ACROSS_SPACING2,
                      IMAGE_DATATYPE1,
                      IMAGE_DATATYPE2,
                      SNR_THRESHOLD,
                      COV_THRESHOLD,
                      BAND1,
                      BAND2,
                      OFFSET_IMAGE_NAME,
                      SNR_IMAGE_NAME,
                      MARGIN,
                      NUMBER_THREADS)

    def denseampcor(self,slcImage1 = None,slcImage2 = None):
        if not (slcImage1 == None):
            self.slcImage1 = slcImage1
        if (self.slcImage1 == None):
            logger.error("Error. master slc image not set.")
            raise Exception
        if not (slcImage2 == None):
            self.slcImage2 = slcImage2
        if (self.slcImage2 == None):
            logger.error("Error. slave slc image not set.")
            raise Exception
      
        self.fileLength1 = self.slcImage1.getLength()
        self.lineLength1 = self.slcImage1.getWidth()
        self.fileLength2 = self.slcImage2.getLength()
        self.lineLength2 = self.slcImage2.getWidth()

        ####Run checks
        self.checkTypes()
        self.checkWindows()

        ####Actual processing
        coarseAcross = self.acrossGrossOffset
        coarseDown = self.downGrossOffset

        xMargin = 2*self.searchWindowSizeWidth + self.windowSizeWidth
        yMargin = 2*self.searchWindowSizeHeight + self.windowSizeHeight

        #####Set image limits for search
        offAc = max(self.margin,-coarseAcross)+xMargin
        if offAc % self.skipSampleAcross != 0:
            leftlim = offAc
            offAc = self.skipSampleAcross*(1 + int(offAc/self.skipSampleAcross)) - self.pixLocOffAc
            while offAc < leftlim:
                offAc += self.skipSampleAcross

        offDn = max(self.margin,-coarseDown)+yMargin
        if offDn % self.skipSampleDown != 0:
            toplim = offDn
            offDn = self.skipSampleDown*(1 + int(offDn/self.skipSampleDown)) - self.pixLocOffDn
            while offDn < toplim:
                offDn += self.skipSampleDown

        offAcmax = int(coarseAcross + ((self.rangeSpacing1/self.rangeSpacing2)-1)*self.lineLength1)
        lastAc = int(min(self.lineLength1, self.lineLength2-offAcmax) - xMargin -1 - self.margin) 

        offDnmax = int(coarseDown + ((self.prf2/self.prf1)-1)*self.fileLength1)
        lastDn = int(min(self.fileLength1, self.fileLength2-offDnmax)  - yMargin -1 - self.margin) 


        self.gridLocAcross = range(offAc + self.pixLocOffAc, lastAc - self.pixLocOffAc, self.skipSampleAcross)
        self.gridLocDown = range(offDn + self.pixLocOffDn, lastDn - self.pixLocOffDn, self.skipSampleDown)
        
        startAc, endAc = offAc, self.gridLocAcross[-1] - self.pixLocOffAc
        self.numLocationAcross = int((endAc-startAc)/self.skipSampleAcross + 1)
        self.numLocationDown = len(self.gridLocDown)

        self.offsetCols, self.offsetLines = self.numLocationAcross, self.numLocationDown

        print('Pixels: ', self.lineLength1, self.lineLength2)
        print('Lines: ', self.fileLength1, self.fileLength2)
        print('Wins : ', self.windowSizeWidth, self.windowSizeHeight)
        print('Srch: ', self.searchWindowSizeWidth, self.searchWindowSizeHeight)


        #####Create shared memory objects
        numlen = self.numLocationAcross * self.numLocationDown
        self.locationDown = mp.Array('i', numlen)
        self.locationDownOffset = mp.Array('f', numlen)
        self.locationAcross = mp.Array('i', numlen)
        self.locationAcrossOffset = mp.Array('f', numlen)
        self.snr = mp.Array('f', numlen)

        ###run ampcor on parallel processes
        threads = []
        block = np.max([1, intround(self.numLocationDown/float(self.numberThreads))])
        if (self.numLocationDown-block*(self.numberThreads-1) > 2 + block) and \
                (self.numLocationDown - (block+1)*(self.numberThreads-1)) > 0 :
                block += 1

        for thrd in range(self.numberThreads):

            firstind = thrd * block * self.numLocationAcross
            startDown = self.gridLocDown[thrd*block] - self.pixLocOffDn

            if thrd == self.numberThreads - 1:
                endDown = self.gridLocDown[-1] - self.pixLocOffDn
                lastind = numlen
            else:
                endDown = self.gridLocDown[(thrd+1)*block] - self.pixLocOffDn
                lastind = (thrd+1)*block*self.numLocationAcross

            numDown = int((endDown - startDown)//self.skipSampleDown + 1)

            print('Thread : ', thrd, firstind, lastind, startAc, endAc, startDown, endDown)

            threads.append(mp.Process(target=self._run_ampcor,
                    args=(startAc,endAc,startDown,endDown,self.numLocationAcross,numDown,firstind,lastind)))

            threads[thrd].start()

        for thread in threads:
            thread.join()

#        sys.exit(0)


        #####Switch shared memory objects to numpy arrays
        self.locationDown = np.asarray(self.locationDown[:], dtype=np.int32)
        self.locationDownOffset = np.asarray(self.locationDownOffset[:], dtype=np.float32)
        self.locationAcross = np.asarray(self.locationAcross[:], dtype=np.int32)
        self.locationAcrossOffset = np.asarray(self.locationAcrossOffset[:], dtype=np.float32)
        self.snr = np.asarray(self.snr[:], dtype=np.float32)
        self.firstSampAc, self.firstSampDown = self.locationAcross[0], self.locationDown[0]
        self.lastSampAc, self.lastSampDown = self.locationAcross[-1], self.locationDown[-1]

        self.write_slantrange_images()


    def _run_ampcor(self, firstAc, lastAc, firstDn, lastDn,
                        numAc, numDn, firstind, lastind):
        '''
        Individual calls to ampcor.
        '''

        objAmpcor = Ampcor()

        objAmpcor.setWindowSizeWidth(self.windowSizeWidth)
        objAmpcor.setWindowSizeHeight(self.windowSizeHeight)
        objAmpcor.setSearchWindowSizeWidth(self.searchWindowSizeWidth)
        objAmpcor.setSearchWindowSizeHeight(self.searchWindowSizeHeight)
        objAmpcor.setImageDataType1(self.imageDataType1)
        objAmpcor.setImageDataType2(self.imageDataType2)

        objAmpcor.setFirstSampleAcross(firstAc)
        objAmpcor.setLastSampleAcross(lastAc)
        objAmpcor.setNumberLocationAcross(numAc)

        objAmpcor.setFirstSampleDown(firstDn)
        objAmpcor.setLastSampleDown(lastDn)
        objAmpcor.setNumberLocationDown(numDn)

        objAmpcor.setAcrossGrossOffset(self.acrossGrossOffset)
        objAmpcor.setDownGrossOffset(self.downGrossOffset)
        objAmpcor.setFirstPRF(self.prf1)
        objAmpcor.setSecondPRF(self.prf2)
        objAmpcor.setFirstRangeSpacing(self.rangeSpacing1)
        objAmpcor.setSecondRangeSpacing(self.rangeSpacing2)
        objAmpcor.thresholdSNR = 1.0e-6
        objAmpcor.thresholdCov = self.thresholdCov

        mSlc = isceobj.createImage()
        IU.copyAttributes(self.slcImage1, mSlc)
        mSlc.setAccessMode('read')
        mSlc.createImage()

        sSlc = isceobj.createImage()
        IU.copyAttributes(self.slcImage2, sSlc)
        sSlc.setAccessMode('read')
        sSlc.createImage()

        objAmpcor.ampcor(mSlc, sSlc)
        mSlc.finalizeImage()
        sSlc.finalizeImage()


        j = 0 
        length = len(objAmpcor.locationDown)
        for i in range(lastind-firstind):
            acInd = firstAc + self.pixLocOffAc + (i % numAc)*self.skipSampleAcross
            downInd = firstDn + self.pixLocOffDn + (i//numAc)*self.skipSampleDown
        
            if j < length and objAmpcor.locationDown[j] == downInd and objAmpcor.locationAcross[j] == acInd: 
                self.locationDown[firstind+i] = objAmpcor.locationDown[j]
                self.locationDownOffset[firstind+i] = objAmpcor.locationDownOffset[j]
                self.locationAcross[firstind+i] = objAmpcor.locationAcross[j]
                self.locationAcrossOffset[firstind+i] = objAmpcor.locationAcrossOffset[j]
                self.snr[firstind+i] = objAmpcor.snrRet[j]
                j += 1
            else:
                self.locationDown[firstind+i] = downInd
                self.locationDownOffset[firstind+i] = -10000.
                self.locationAcross[firstind+i] = acInd
                self.locationAcrossOffset[firstind+i] = -10000.
                self.snr[firstind+i] = 0.

        return


    def write_slantrange_images(self):
        '''Write output images'''

        ####Snsure everything is 2D image first

        if self.locationDownOffset.ndim == 1:
            self.locationDownOffset = self.locationDownOffset.reshape(-1,self.offsetCols)

        if self.locationAcrossOffset.ndim == 1:
            self.locationAcrossOffset = self.locationAcrossOffset.reshape(-1,self.offsetCols)

        if self.snr.ndim == 1:
            self.snr = self.snr.reshape(-1,self.offsetCols)

        if self.locationDown.ndim == 1:
            self.locationDown = self.locationDown.reshape(-1,self.offsetCols)

        if self.locationAcross.ndim == 1:
            self.locationAcross = self.locationAcross.reshape(-1,self.offsetCols)


        outdata = np.empty((2*self.offsetLines, self.offsetCols), dtype=np.float32)
        outdata[::2,:] = self.locationDownOffset
        outdata[1::2,:] = self.locationAcrossOffset
        outdata.tofile(self.offsetImageName)
        del outdata
        outImg = isceobj.createImage()
        outImg.setDataType('FLOAT')
        outImg.setFilename(self.offsetImageName)
        outImg.setBands(2)
        outImg.scheme = 'BIL'
        outImg.setWidth(self.offsetCols)
        outImg.setLength(self.offsetLines)
        outImg.setAccessMode('read')
        outImg.renderHdr()

        ####Create SNR image
        self.snr.astype(np.float32).tofile(self.snrImageName)
        snrImg = isceobj.createImage()
        snrImg.setFilename(self.snrImageName)
        snrImg.setDataType('FLOAT')
        snrImg.setBands(1)
        snrImg.setWidth(self.offsetCols)
        snrImg.setLength(self.offsetLines)
        snrImg.setAccessMode('read')
        snrImg.renderHdr()
        

    def checkTypes(self):
        '''Check if the image datatypes are set.'''

        if self.imageDataType1 == '':
            if self.slcImage1.getDataType().upper().startswith('C'):
                self.imageDataType1 = 'complex'
            else:
                raise ValueError('Undefined value for imageDataType1. Should be complex/real/rmg1/rmg2')
        else:
            if self.imageDataType1 not in ('complex','real'):
                raise ValueError('ImageDataType1 should be either complex/real/rmg1/rmg2.')

        if self.imageDataType2 == '':
            if self.slcImage2.getDataType().upper().startswith('C'):
                self.imageDataType2 = 'complex'
            else:
                raise ValueError('Undefined value for imageDataType2. Should be complex/real/rmg1/rmg2')
        else:
            if self.imageDataType2 not in ('complex','real'):
                raise ValueError('ImageDataType1 should be either complex/real.')
        

    def checkWindows(self):
        '''Ensure that the window sizes are valid for the code to work.'''

        if (self.windowSizeWidth%2 == 1):
            raise ValueError('Window size width needs to be an even number.')

        if (self.windowSizeHeight%2 == 1):
            raise ValueError('Window size height needs to be an even number.')

        if not is_power2(self.zoomWindowSize):
            raise ValueError('Zoom window size needs to be a power of 2.')

        if not is_power2(self.oversamplingFactor):
            raise ValueError('Oversampling factor needs to be a power of 2.')

        if self.searchWindowSizeWidth >=  2*self.windowSizeWidth :
            raise ValueError('Search Window Size Width should be < 2 * Window Size Width')

        if self.searchWindowSizeHeight >= 2*self.windowSizeHeight :
            raise ValueError('Search Window Size Height should be < 2 * Window Size Height')

        if self.zoomWindowSize >= min(self.searchWindowSizeWidth, self.searchWindowSizeHeight):
            raise ValueError('Zoom window size should be <= Search window size')

        if self._stdWriter is None:
            self._stdWriter = create_writer("log", "", True, filename="denseampcor.log")

        self.pixLocOffAc = self.windowSizeWidth//2 + self.searchWindowSizeWidth - 1
        self.pixLocOffDn = self.windowSizeHeight//2 + self.searchWindowSizeHeight - 1

    def setImageDataType1(self, var):
        self.imageDataType1 = str(var)
        return

    def setImageDataType2(self, var):
        self.imageDataType2 = str(var)
        return

    def setLineLength1(self,var):
        self.lineLength1 = int(var)
        return

    def setLineLength2(self, var):
        self.LineLength2 = int(var)
        return

    def setFileLength1(self,var):
        self.fileLength1 = int(var)
        return

    def setFileLength2(self, var):
        self.fileLength2 = int(var)

    def setSkipSampleAcross(self,var):
        self.skipSampleAcross = int(var)
        return

    def setSkipSampleDown(self,var):
        self.skipSampleDown = int(var)
        return

    def setAcrossGrossOffset(self,var):
        self.acrossGrossOffset = int(var)
        return

    def setDownGrossOffset(self,var):
        self.downGrossOffset = int(var)
        return

    def setFirstPRF(self,var):
        self.prf1 = float(var)
        return

    def setSecondPRF(self,var):
        self.prf2 = float(var)
        return

    def setFirstRangeSpacing(self,var):
        self.rangeSpacing1 = float(var)
        return
    
    def setSecondRangeSpacing(self,var):
        self.rangeSpacing2 = float(var)

    
    def setMasterSlcImage(self,im):
        self.slcImage1 = im
        return
    
    def setSlaveSlcImage(self,im):
        self.slcImage2 = im
        return

    def setWindowSizeWidth(self, var):
        temp = int(var)
        if (temp%2 == 1):
            raise ValueError('Window width needs to be an even number.')
        self.windowSizeWidth = temp
        return

    def setWindowSizeHeight(self, var):
        temp = int(var)
        if (temp%2 == 1):
            raise ValueError('Window height needs to be an even number.')
        self.windowSizeHeight = temp
        return

    def setZoomWindowSize(self, var):
        temp = int(var)
        if not is_power2(temp):
            raise ValueError('Zoom window size needs to be a power of 2.')
        self.zoomWindowSize = temp

    def setOversamplingFactor(self, var):
        temp = int(var)
        if not is_power2(temp):
            raise ValueError('Oversampling factor needs to be a power of 2.')
        self.oversamplingFactor = temp

    def setSearchWindowSizeWidth(self, var):
        self.searchWindowSizeWidth = int(var)
        return

    def setSearchWindowSizeHeight(self, var):
        self.searchWindowSizeHeight = int(var)
        return

    def setAcrossLooks(self, var):
        self.acrossLooks = int(var)
        return

    def setDownLooks(self, var):
        self.downLooks = int(var)
        return

    def stdWriter(self, var):
        self._stdWriter = var
        return

    def __init__(self, name=''):
        super(DenseAmpcor, self).__init__(family=self.__class__.family, name=name)
        self.locationAcross = []
        self.locationAcrossOffset = []
        self.locationDown = []
        self.locationDownOffset = []
        self.snrRet = []
        self.cov1Ret = []
        self.cov2Ret = []
        self.cov3Ret = []
        self.lineLength1 = None
        self.lineLength2 = None
        self.fileLength1 = None
        self.fileLength2 = None
        self.scaleFactorX = None
        self.scaleFactorY = None
        self.firstSampAc = None
        self.lastSampAc = None
        self.firstSampDown = None
        self.lastSampDown = None
        self.numLocationAcross = None
        self.numLocationDown = None
        self.offsetCols = None
        self.offsetLines = None
        self.gridLocAcross = None
        self.gridLocDown = None
        self.pixLocOffAc = None
        self.pixLocOffDn = None
        self._stdWriter = None
        self.offsetLines = None
        self.offsetCols = None
        self.dictionaryOfVariables = { \
                                      'IMAGETYPE1' : ['imageDataType1', 'str', 'optional'], \
                                      'IMAGETYPE2' : ['imageDataType2', 'str', 'optional'], \
                                      'SKIP_SAMPLE_ACROSS' : ['skipSampleAcross', 'int','mandatory'], \
                                      'SKIP_SAMPLE_DOWN' : ['skipSampleDown', 'int','mandatory'], \
                                      'COARSE_NUMBER_LOCATION_ACROSS' : ['coarseNumWinAcross','int','mandatory'], \
                                      'COARSE_NUMBER_LOCATION_DOWN' : ['coarseNumWinDown', 'int', 'mandatory'], \
                                      'ACROSS_GROSS_OFFSET' : ['acrossGrossOffset', 'int','optional'], \
                                      'DOWN_GROSS_OFFSET' : ['downGrossOffset', 'int','optional'], \
                                      'PRF1' : ['prf1', 'float','optional'], \
                                      'PRF2' : ['prf2', 'float','optional'], \
                                      'RANGE_SPACING1' : ['rangeSpacing1', 'float', 'optional'], \
                                      'RANGE_SPACING2' : ['rangeSpacing2', 'float', 'optional'], \
                                      }
        self.dictionaryOfOutputVariables = {
                                            'FIRST_SAMPLE_ACROSS' : 'firstSampAc',
                                            'FIRST_SAMPLE_DOWN' : 'firstSampDn',
                                            'NUMBER_LINES': 'offsetLines',
                                            'NUMBER_PIXELS' : 'offsetCols'}
        return None


#end class
if __name__ == "__main__":
    sys.exit(main())
