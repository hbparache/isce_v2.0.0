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
from iscesys.Component.InitFromDictionary import InitFromDictionary
from mroipac.looks.Rilooks import Rilooks

def main():
    obj = Rilooks()
    infile = "/Users/giangi/TEST_DIR/int_930110_950523/flat_PRC_930110-950523.int"
    outfile = 'testRi'
    rlook = 4;
    alook = 4;
    width = 5700
    height = 2593
    #with all arguments
    #dict = {'INPUT_ENDIANNESS':enIn,'OUTPUT_ENDIANNESS':enOut,'LENGTH':length,'WIDTH':width,'INPUT_IMAGE':infile,'OUTPUT_IMAGE':outfile,'RANGE_LOOK':rlook,'AZIMUTH_LOOK':alook}
    #with only mandatory arguments
    dict = {'WIDTH':width,'INPUT_IMAGE':infile,'OUTPUT_IMAGE':outfile,'RANGE_LOOK':rlook,'AZIMUTH_LOOK':alook}
    initDict = InitFromDictionary(dict)
    obj.initComponent(initDict)
    obj.rilooks()

if __name__ == "__main__":
    sys.exit(main())
