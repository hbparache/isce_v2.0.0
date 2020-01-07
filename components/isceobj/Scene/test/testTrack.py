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
# Author: Walter Szeliga
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




import os
import logging
import logging.config
logging.config.fileConfig(os.path.join(os.environ['ISCE_HOME'], 'defaults',
    'logging', 'logging.conf'))
from isceobj.Sensor.ERS import ERS
from isceobj.Scene.Track import Track
logger = logging.getLogger("testTrack")

def main():
    output = 'test.raw'
    frame1 = createERSFrame(leaderFile='/Users/szeliga/data/InSAR/raw/ers/track134/frame2961/930913/SARLEADER199309132961f134t',
                   imageryFile='/Users/szeliga/data/InSAR/raw/ers/track134/frame2961/930913/IMAGERY199309132961f134t',
                   output='frame2961.raw')
    frame2 = createERSFrame(leaderFile='/Users/szeliga/data/InSAR/raw/ers/track134/frame2979/930913/SARLEADER199309132979f134t',
                   imageryFile='/Users/szeliga/data/InSAR/raw/ers/track134/frame2979/930913/IMAGERY199309132979f134t',
                   output='frame2979.raw')

    track = Track()
    track.addFrame(frame1)
    track.addFrame(frame2)
    track.createTrack(output)

def createERSFrame(leaderFile=None,imageryFile=None,output=None):
    logger.info("Extracting ERS frame %s" % leaderFile)
    ers = ERS()
    ers._leaderFile = leaderFile
    ers._imageFile = imageryFile
    ers.output = output

    ers.extractImage()

    return ers.getFrame()

if __name__ == "__main__":
    main()
