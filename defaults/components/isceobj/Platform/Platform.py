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



import math
from iscesys.Component.Component import Component
from isceobj.Planet.Planet import Planet
from isceobj.Util.decorators import type_check


PLANET = Component.Parameter('_planet',
    public_name='PLANET',
    default=None,
    type = Planet,
    mandatory = True,
    doc = 'Planet description')

SPACECRAFT_NAME = Component.Parameter('spacecraftName',
    public_name='SPACECRAFT_NAME',
    default=None,
    type = str,
    mandatory = True,
    doc = 'Name of the space craft')

MISSION = Component.Parameter('_mission',
    public_name='MISSION',
    default=None,
    type = str,
    mandatory = True,
    doc = 'Mission name')

ANTENNA_LENGTH = Component.Parameter('antennaLength',
    public_name='ANTENNA_LENGTH',
    default=None,
    type = float,
    mandatory = True,
    doc = 'Length of the antenna')

POINTING_DIRECTION = Component.Parameter('pointingDirection',
    public_name='POINTING_DIRECTION',
    default=None,
    type = int,
    mandatory = True,
    doc = '-1 for RIGHT, 1 for LEFT')

##
# This class allows the creation of a Platform object. The parameters that need to be set are
#\verbatim
#PLANET: Name of the planet about which the platform orbits. Mandatory.
#SPACECRAFT_NAME: Name of the spacecraft. Mandatory.
#BODY_FIXED_VELOCITY:
#SPACECRAFT_HEIGHT: Height of the sapcecraft. Mandatory.
#POINTING_DIRECTION: 
#ANTENNA_LENGTH: Length of the antenna. Mandatory.
#ANTENNA_SCH_VELOCITY
#ANTENNA_SCH_ACCELERATION
#HEIGHT_DT
#\endverbatim
#Since the Platform class inherits the Component.Component, the methods of initialization described in the Component package can be used.
#Moreover each parameter can be set with the corresponding accessor method setParameter() (see the class member methods).
class Platform(Component):

    family = 'platform'
    logging_name = 'isce.isceobj.platform'

    parameter_list = (PLANET,
                      SPACECRAFT_NAME,
                      MISSION,
                      ANTENNA_LENGTH,
                      POINTING_DIRECTION)
    
    
    def __init__(self, name=''):
        super(Platform, self).__init__(family=self.__class__.family, name=name)
        return None

    def setSpacecraftName(self,var):
        self.spacecraftName = str(var)
        return
        
    def setAntennaLength(self,var):
        self.antennaLength = float(var)
        return
    
    def setPointingDirection(self,var):
        self.pointingDirection = int(var)
        return
    
    def setMission(self,mission):
        self._mission = mission
        
    def getMission(self):
        return self._mission
    
    def getSpacecraftName(self):
        return self.spacecraftName or self._mission

    def getAntennaLength(self):
        return self.antennaLength
    
    def getPlanet(self):
        return self._planet
    
    @type_check(Planet)
    def setPlanet(self,planet):
        self._planet = planet
        return None
        
    planet = property(getPlanet, setPlanet)

    def __str__(self):
        retstr = "Mission: (%s)\n"
        retlst = (self._mission,)
        retstr += "Look Direction: (%s)\n"
        retlst += (self.pointingDirection,)
        retstr += "Antenna Length: (%s)\n"
        retlst += (self.antennaLength,)
        return retstr % retlst
    

class Orientation(Component):
    """A class for holding platform orientation information, such as squint
    angle and platform height"""

    dictionaryOfVariables = {'BODY_FIXED_VELOCITY' :
                                 ['self.bodyFixedVelocity', 'float',True],
                             'ANTENNA_SCH_VELOCITY' :
                                 ['self.antennaSCHVelocity','float',True],
                             'ANTENNA_SCH_ACCELERATION' :
                                 ['self.antennaSCHAcceleration','float',True]}    
    
    def __init__(self):
        super(Orientation, self).__init__()
        self.antennaSCHVelocity = []
        self.antennaSCHAcceleration = []        
        self.bodyFixedVelocity = None        
        self.pointingDirection = None
        self.descriptionOfVariables = {}
        return None
        
    def setSpacecraftHeight(self, var):
        self.spacecraftHeight = float(var)
    
    def getSpacecraftHeight(self):
        return self.spacecraftHeight
    
    def setBodyFixedVelocity(self, var):
        self.bodyFixedVelocity = float(var)
        return
    
    def setAntennaSCHVelocity(self, var):
        self.antennaSCHVelocity = var
        return

    def setAntennaSCHAcceleration(self, var):
        self.antennaSCHAcceleration = var
        return


def createPlatform():
    return Platform()
