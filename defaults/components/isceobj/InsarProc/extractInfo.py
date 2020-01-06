#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copyright: 2012 to the present, California Institute of Technology.
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
# Author: Brett George
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



import isceobj.Catalog
import logging
logger = logging.getLogger('isce.insar.extractInfo')

def extractInfo(self, master, slave):
    from contrib.frameUtils.FrameInfoExtractor import FrameInfoExtractor
    FIE = FrameInfoExtractor()
    masterInfo = FIE.extractInfoFromFrame(master)
    slaveInfo = FIE.extractInfoFromFrame(slave)
    masterInfo.sensingStart = [masterInfo.sensingStart, slaveInfo.sensingStart]
    masterInfo.sensingStop = [masterInfo.sensingStop, slaveInfo.sensingStop]
    # for stitched frames do not make sense anymore
    mbb = masterInfo.getBBox()
    sbb = slaveInfo.getBBox()
    latEarlyNear = mbb[0][0]
    latLateNear = mbb[2][0]
 
    #figure out which one is the bottom
    if latEarlyNear > latLateNear: 
        #early is the top
        ret = []
        # the calculation computes the minimum bbox. it is not exact, bu given
        # the approximation in the estimate of the corners, it's ok 
        ret.append([min(mbb[0][0], sbb[0][0]), max(mbb[0][1], sbb[0][1])])
        ret.append([min(mbb[1][0], sbb[1][0]), min(mbb[1][1], sbb[1][1])])
        ret.append([max(mbb[2][0], sbb[2][0]), max(mbb[2][1], sbb[2][1])])
        ret.append([max(mbb[3][0], sbb[3][0]), min(mbb[3][1], sbb[3][1])])
    else:
        # late is the top
        ret = []
        ret.append([max(mbb[0][0], sbb[0][0]), max(mbb[0][1], sbb[0][1])])
        ret.append([max(mbb[1][0], sbb[1][0]), min(mbb[1][1], sbb[1][1])])
        ret.append([min(mbb[2][0], sbb[2][0]), max(mbb[2][1], sbb[2][1])])
        ret.append([min(mbb[3][0], sbb[3][0]), min(mbb[3][1], sbb[3][1])])
    
    masterInfo.bbox = ret
    return masterInfo
    # the track should be the same for both

