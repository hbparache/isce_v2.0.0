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




import datetime
import logging
import isceobj
from isceobj.Scene.Frame import Frame
from iscesys.Component.Component import Component

class Sensor(Component):
    """
    Base class for storing Sensor data
    """

    logging_name =  None
    lookMap = {'RIGHT' : -1,
               'LEFT'  : 1}

    def __init__(self):
        super(Sensor, self).__init__()
        self.output = None
        self.frame = Frame()
        self.frame.configure()

        self.logger = logging.getLogger(self.logging_name)

        self.frameList = []
        self.descriptionOfVariables = {}
        self.dictionaryOfVariables = {
            'OUTPUT': ['self.output','str','optional']}
        return None


    def getFrame(self):
        '''
        Return the frame object.
        '''
        return self.frame

    def parse(self):
        '''
        Dummy routine.
        '''
        raise NotImplementedError("In Sensor Base Class")


    def populateMetadata(self, **kwargs):
        """
        Create the appropriate metadata objects from our HDF5 file
        """
        self._populatePlatform(**kwargs)
        self._populateInstrument(**kwargs)
        self._populateFrame(**kwargs)
        self._populateOrbit(**kwargs)

    def _populatePlatform(self,**kwargs):
        '''
        Dummy routine to populate platform information.
        '''
        raise NotImplementedError("In Sensor Base Class")

    def _populateInstrument(self,**kwargs):
        """
        Dummy routine to populate instrument information.
        """
        raise NotImplementedError("In Sensor Base Class")

    def _populateFrame(self,**kwargs):
        """
        Dummy routine to populate frame object.
        """
        raise NotImplementedError("In Sensor Base Class")

    def _populateOrbit(self,**kwargs):
        """
        Dummy routine to populate orbit information.
        """
        raise NotImplementedError("In Sensor Base Class")

    def extractImage(self):
        """
        Dummy routine to extract image.
        """
        raise NotImplementedError("In Sensor Base Class")

    def extractDoppler(self):
        """
        Dummy routine to extract doppler centroid information.
        """
        raise NotImplementedError("In Sensor Base Class")
