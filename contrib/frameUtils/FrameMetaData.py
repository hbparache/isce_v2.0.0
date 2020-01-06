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
import os
from mroipac.geolocate.Geolocate import Geolocate
import logging

class FrameMetaData(object):
    
    def getSpacecraftName(self):
        return self._spacecraftName
    def getOrbitNumber(self):
        return self._orbitNumber
    def getTrackNumber(self):
        return self._trackNumber
    def getFrameNumber(self):
        return self._frameNumber
    def getBBox(self):
        return self._bbox
    def getSensingStart(self):
        return self._sensingStart
    def getSensingStop(self):
        return self._sensingStop
    def getDirection(self):
        return self._direction
    
    def setOrbitNumber(self,val):
        self._orbitNumber = val
    def setTrackNumber(self,val):
        self._trackNumber = val
    def setFrameNumber(self,val):
        self._frameNumber = val
    def setSpacecraftName(self,val):
        self._spacecraftName = val
    def setBBox(self,val):
        self._bbox = val
    def setSensingStart(self,val):
        self._sensingStart = val
    def setSensingStop(self,val):
        self._sensingStop = val
    def setDirection(self,val):
        self._direction = val

    def __init__(self):
        self._spacecraftName = ''
        self._orbitNumber = None
        self._trackNumber = None
        self._frameNumber = None
        self._bbox = [] # [near start, far start, near end, far end]  
        self._sensingStart = None
        self._sensingStop = None
        self._direction = ''
        
    spacecraftName = property(getSpacecraftName,setSpacecraftName)
    orbitNumber = property(getOrbitNumber,setOrbitNumber)
    trackNumber = property(getTrackNumber,setTrackNumber)
    frameNumber = property(getFrameNumber,setFrameNumber)
    bbox =  property(getBBox,setBBox)
    sensingStart = property(getSensingStart,setSensingStart)
    sensingStop = property(getSensingStop,setSensingStop)
    direction = property(getDirection,setDirection)
