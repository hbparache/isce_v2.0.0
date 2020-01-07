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
from stdproc.orbit.Orbit2sch import Orbit2sch

def main():
    obj = Orbit2sch()
    pegFlag = -1
    obj.setComputePegInfoFlag(pegFlag)
    f1 = open(sys.argv[1])  # position.out from mocomp
    allLines1 = f1.readlines()
    position1 = []
    velocity1 = []
    for i in range(len(allLines1)):
        split1 = allLines1[i].split()
        p1 = [float(split1[2]),float(split1[3]),float(split1[4])] 
        v1 = [float(split1[5]),float(split1[6]),float(split1[7])] 
        position1.append(p1)
        velocity1.append(v1)
    obj.setOrbitPosition(position1)
    obj.setOrbitVelocity(velocity1)
    
    if(pegFlag == -1): 
        pegLat = 0.589368483391443
        pegLon = -2.11721339735596
        pegHdg = -0.227032945109943
        pegHave = 698594.962390185
        obj.setPegLatitude(pegLat)
        obj.setPegLongitude(pegLon)
        obj.setPegHeading(pegHdg)
        obj.setAverageHeight(pegHave)
    obj.orbit2sch()

if __name__ == "__main__":
    sys.exit(main())
