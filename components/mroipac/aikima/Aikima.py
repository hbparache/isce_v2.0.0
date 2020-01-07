#!/usr/bin/env python3

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




from __future__ import print_function
import isce
import sys
import os
import numpy
from iscesys.Component.Component import Component
from mroipac.aikima import aikima

class Aikima(Component):

    def aikima(self, inImage=None, outImage=None, bands=None):
        if not (inImage == None):
            self.inImage = inImage
        if (self.inImage == None):
            print("Error. Input image not set.")
            raise Exception

        if not (outImage==None):
            self.outImage = outImage
        if (self.outImage == None):
            print("Error. Output image not set.")
            raise Exception

        inAcc = self.inImage.getImagePointer()
        outAcc = self.outImage.getImagePointer()

        self.width = self.inImage.getWidth()
        self.length = self.inImage.getLength()

        self.setState()

        if bands is None:
            bands = numpy.arange(1,self.inImage.bands+1)
        elif isinstance(bands,int):
            bands = [bands]

        
        for band in bands:
            self.inImage.rewind()
            self.outImage.rewind()
            aikima.aikima_Py(inAcc,outAcc, band, band)


    def setState(self):
        if self.lastPixelAcross is None:
            self.lastPixelAcross = self.width

        if self.lastLineDown is None:
            self.lastLineDown = self.length

        aikima.setWidth_Py(int(self.width))
        aikima.setLength_Py(int(self.length))
        aikima.setFirstPixelAcross_Py(int(self.firstPixelAcross))
        aikima.setLastPixelAcross_Py(int(self.lastPixelAcross))
        aikima.setFirstLineDown_Py(int(self.firstLineDown))
        aikima.setLastLineDown_Py(int(self.lastLineDown))
        aikima.setBlockSize_Py(int(self.blockSize))
        aikima.setPadSize_Py(int(self.padSize))
        aikima.setNumberPtsPartial_Py(int(self.numberPtsPartial))
        aikima.setThreshold_Py(float(self.threshold))
        aikima.setPrintFlag_Py(int(self.printFlag))
    
    def __init__(self):
        Component.__init__(self)
        self.width = None
        self.length = None
        self.blockSize = 64
        self.padSize = 9 
        self.numberPtsPartial = 3
        self.threshold = 0.9
        self.firstPixelAcross = 0
        self.lastPixelAcross = None
        self.firstLineDown = 0 
        self.lastLineDown = None
        self.printFlag = True
        self.inImage = None
        self.outImage = None

if __name__ == '__main__':
    import isceobj
    import numpy as np
    Nx = 500
    Ny = 300
    Nrand = np.int(0.4*Nx*Ny)

    x = np.arange(Nx, dtype=np.float32)/(1.0*Nx)
    y = np.arange(Ny, dtype=np.float32)/(1.0*Ny)

    d = (y[:,None])**2 + np.sin(x[None,:]*4*np.pi)

    ii = np.random.randint(0,high = Ny,size=Nrand)
    jj = np.random.randint(0,high=Nx, size=Nrand)

    dorig = d.copy()
    d[ii,jj] = np.nan

    d = d.astype(np.float32)
    d.tofile('test.flt')

    ####Setup inputs for the Aikima module
    inImage = isceobj.createImage()
    inImage.dataType='FLOAT'
    inImage.initImage('test.flt','read',Nx)
    inImage.createImage()

    outImage = isceobj.createImage()
    outImage.dataType='FLOAT'
    outImage.initImage('test.out','write',Nx)
    outImage.createImage()

    aObj = Aikima()
    aObj.printFlag = True
    aObj.aikima(inImage=inImage, outImage=outImage, bands=1)

    inImage.finalizeImage()
    outImage.finalizeImage()
