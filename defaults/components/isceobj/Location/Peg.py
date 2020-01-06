'''
Copyright 2010, by the California Institute of Technology. 
ALL RIGHTS RESERVED. 
United States Government Sponsorship acknowledged. 
Any commercial use must be negotiated with the Office of 
Technology Transfer at the California Institute of Technology.

This software may be subject to U.S. export control laws. By 
accepting this software, the user agrees to comply with all applicable 
U.S. export laws and regulations. User has the responsibility to obtain 
export licenses, or other export authority as may be required before 
exporting such information to foreign countries or providing access 
to foreign persons.
'''
import math
from isceobj.Location.Coordinate import Coordinate
from iscesys.Component.Component import Component

class PegFactory(object):

    @staticmethod
    def fromEllipsoid(coordinate=None,heading=None,ellipsoid=None):
        """
        Create a Peg object from a coordinate, a heading, and an ellipsoid.

        @param coordinate: an isceobj.Location.Coordinate object
        @param heading: the heading in degrees
        @param ellipsoid: an object of type isceobj.Planet.Ellipsoid
        """
        radiusOfCurvature = 0.0
        # Calculate the radius of curvature at the peg point
        try:
            radiusOfCurvature = ellipsoid.radiusOfCurvature([coordinate.latitude,coordinate.longitude,0.0],hdg=heading)
        except AttributeError:
            print("Object %s requires radiusOfCurvature() methods" % (ellipsoid.__class__))

        return Peg(latitude=coordinate.latitude,longitude=coordinate.longitude, \
                   heading=heading,radiusOfCurvature=radiusOfCurvature)

class Peg(Coordinate,Component):
    """
    A class to hold peg point information
    """
    
    def __init__(self,latitude=None,longitude=None,heading=None,radiusOfCurvature=None):
        """
        @param latitude: the latitude in degrees
        @param longitude: the longitude in degrees
        @param heading: the heading in degrees
        @param radiusOfCurvature: the radius of curvature at the specified coordinates
        """
        
        Component.__init__(self)
        Coordinate.__init__(self,latitude=latitude,longitude=longitude,height=0.0)                        
        self._heading = heading
        self._radiusOfCurvature = radiusOfCurvature
        self.descriptionOfVariables = {}
        self.dictionaryOfVariables = {'LATITUDE': ['_latitude','float','mandatory'],
                                      'LONGITUDE': ['_longitude','float','mandatory'],
                                      'HEIGHT': ['_height','float','mandatory'],
                                      'RADIUS_OF_CURVATURE': ['_radiusOfCurvature','float','mandatory'],
                                      'HEADING': ['_heading','float','mandatory']}
        self.initOptionalAndMandatoryLists()
        
    def getHeading(self):
        return self._heading

    def setHeading(self, value):
        self._heading = value
        
    def setRadiusOfCurvature(self,rc):
        self._radiusOfCurvature = rc
    
    def getRadiusOfCurvature(self):
        return self._radiusOfCurvature

    def updateRadiusOfCurvature(self, ellipsoid):
        '''Updates the radius of curvature assuming the coordinate and heading information is correct.'''
        if self._radiusOfCurvature is not None:
            print('Radius field is not empty. \n Forcefully updating the value.')

        self._radiusOfCurvature = ellipsoid.radiusOfCurvature([self._latitude, self._longitude, 0.0], hdg=self._heading)
    
    def __str__(self):
        retstr = "Latitude: %s\n"
        retlst = (self._latitude,)
        retstr += "Longitude: %s\n"
        retlst += (self._longitude,)
        retstr += "Heading: %s\n"
        retlst += (self._heading,)
        retstr += "Radius of Curvature: %s\n"
        retlst += (self._radiusOfCurvature,)

        return retstr % retlst
    
    heading = property(getHeading, setHeading)
    radiusOfCurvature = property(getRadiusOfCurvature,setRadiusOfCurvature)
