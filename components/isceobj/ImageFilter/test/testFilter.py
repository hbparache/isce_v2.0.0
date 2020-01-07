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
import isce
from iscesys.Compatibility import Compatibility
Compatibility.checkPythonVersion()
from isceobj.ImageFilter.FilterFactory import createFilter
from isceobj.Image.Image import Image
import pdb

#Run as ./testFilte.py x (with x = 1,...,9 see if blocks below).
#To create test files compile g++ -o test.ex test.cpp and run ./test.ex 1
def main():
    
    opt = sys.argv[1]
    if opt == '1':
        #extract phase from complex image in polar coordinates
        filename = 'complexPolarBIP'
        scheme = 'BIP'
        bands = 2
        typeF = 'CDOUBLE'
        accessmode = 'read'
        width = 3
        img = Image()
        img.initImage(filename,accessmode,width,typeF,bands,scheme)
        filter = createFilter('PhaseExtractor','polar')
        outfile = 'phasePolarBIP'
        filter.init(img,outfile)
        filter.extract()
        filter.finalize()
        img.finalizeImage()
    elif opt == '2':
        #extract magnitude from complex image in polar coordinates
        filename = 'complexPolarBIP'
        scheme = 'BIP'
        bands = 2
        typeF = 'CDOUBLE'
        accessmode = 'read'
        width = 3
        img = Image()
        img.initImage(filename,accessmode,width,typeF,bands,scheme)
        filter = createFilter('MagnitudeExtractor','polar')
        outfile = 'magnitudePolarBIP'
        filter.init(img,outfile)
        filter.extract()
        filter.finalize()
        img.finalizeImage()
    elif opt == '3':
        #extract phase from complex image in cartesian coordinates
        filename = 'complexXYBIP'
        scheme = 'BIP'
        bands = 2
        typeF = 'CDOUBLE'
        accessmode = 'read'
        width = 3
        img = Image()
        img.initImage(filename,accessmode,width,typeF,bands,scheme)
        filter = createFilter('PhaseExtractor','cartesian')
        outfile = 'phaseBIP'
        filter.init(img,outfile)
        filter.extract()
        filter.finalize()
        img.finalizeImage()
    elif opt == '4':
        #extract magnitude from complex image in cartesian coordinates
        filename = 'complexXYBIP'
        scheme = 'BIP'
        bands = 2
        typeF = 'CDOUBLE'
        accessmode = 'read'
        width = 3
        img = Image()
        img.initImage(filename,accessmode,width,typeF,bands,scheme)
        filter = createFilter('MagnitudeExtractor','cartesian')
        outfile = 'magnitudeBIP'
        filter.init(img,outfile)
        filter.extract()
        filter.finalize()
        img.finalizeImage()
    elif opt == '5':
        #extract real part from complex image in cartesian coordinates
        filename = 'complexXYBIP'
        scheme = 'BIP'
        bands = 2
        typeF = 'CDOUBLE'
        accessmode = 'read'
        width = 3
        img = Image()
        img.initImage(filename,accessmode,width,typeF,bands,scheme)
        filter = createFilter('RealExtractor','cartesian')
        outfile = 'realBIP'
        filter.init(img,outfile)
        filter.extract()
        filter.finalize()
        img.finalizeImage()
    elif opt == '6':
        #extract imaginary part from complex image in cartesian coordinates
        filename = 'complexXYBIP'
        scheme = 'BIP'
        bands = 2
        typeF = 'CDOUBLE'
        accessmode = 'read'
        width = 3
        img = Image()
        img.initImage(filename,accessmode,width,typeF,bands,scheme)
        filter = createFilter('ImagExtractor','cartesian')
        outfile = 'imagBIP'
        filter.init(img,outfile)
        filter.extract()
        filter.finalize()
        img.finalizeImage()
    elif opt == '7':
        #extract real part from complex image in polar coordinates
        filename = 'complexPolarBIP'
        scheme = 'BIP'
        bands = 2
        typeF = 'CDOUBLE'
        accessmode = 'read'
        width = 3
        img = Image()
        img.initImage(filename,accessmode,width,typeF,bands,scheme)
        filter = createFilter('RealExtractor','polar')
        outfile = 'realPolarBIP'
        filter.init(img,outfile)
        filter.extract()
        filter.finalize()
        img.finalizeImage()
    elif opt == '8':
        #extract imaginary part from complex image in polar coordinates
        filename = 'complexPolarBIP'
        scheme = 'BIP'
        bands = 2
        typeF = 'CDOUBLE'
        accessmode = 'read'
        width = 3
        img = Image()
        img.initImage(filename,accessmode,width,typeF,bands,scheme)
        filter = createFilter('ImagExtractor','polar')
        outfile = 'imagPolarBIP'
        filter.init(img,outfile)
        filter.extract()
        filter.finalize()
        img.finalizeImage()
    elif opt == '9':    
        #extract band from image
        filename = 'complexXYBIP'
        scheme = 'BIP'
        bands = 2
        typeF = 'CDOUBLE'
        accessmode = 'read'
        width = 3
        img = Image()
        img.initImage(filename,accessmode,width,typeF,bands,scheme)
        #bands are zero based
        bandToExtract = 0
        filter = createFilter('BandExtractor',bandToExtract)
        outfile = 'band0BIP'
        filter.init(img,outfile)
        filter.extract()
        filter.finalize()
        
        #need to rewind the image to the beginning 
        img.rewind()
        #bands are zero based
        bandToExtract = 1
        filter = createFilter('BandExtractor',bandToExtract)
        outfile = 'band1BIP'
        filter.init(img,outfile)
        filter.extract()
        filter.finalize()
        img.finalizeImage()

                





if __name__ == "__main__":
    sys.exit(main())
