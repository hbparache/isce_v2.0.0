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
from stdproc.orbit.Setmocomppath import Setmocomppath

def main():
    obj = Setmocomppath()
    f1 = open(sys.argv[1])
    f2 = open(sys.argv[2])
    allLines1 = f1.readlines()
    allLines2 = f2.readlines()
    position1 = []
    position2 = []
    velocity1 = []
    velocity2 = []
    for i in range(len(allLines1)):
        split1 = allLines1[i].split()
        p1 = [float(split1[2]),float(split1[3]),float(split1[4])] 
        v1 = [float(split1[5]),float(split1[6]),float(split1[7])] 
        position1.append(p1)
        velocity1.append(v1)
    for i in range(len(allLines2)):
        split2 = allLines2[i].split()
        p2 = [float(split2[2]),float(split2[3]),float(split2[4])] 
        v2 = [float(split2[5]),float(split2[6]),float(split2[7])]
        position2.append(p2)
        velocity2.append(v2)
    obj.setFirstPosition(position1)
    obj.setFirstVelocity(velocity1)
    obj.setSecondPosition(position2)
    obj.setSecondVelocity(velocity2)
    obj.setmocomppath()
    h1 = obj.getFirstAverageHeight()
    h2 = obj.getSecondAverageHeight()
    v1 = obj.getFirstProcVelocity()
    v2 = obj.getSecondProcVelocity()

if __name__ == "__main__":
    sys.exit(main())
