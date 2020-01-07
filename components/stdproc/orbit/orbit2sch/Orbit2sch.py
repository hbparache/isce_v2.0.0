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
import math
import datetime
import logging

from isceobj import Constants as CN
from isceobj.Orbit.Orbit import Orbit, StateVector
from iscesys.Component.Component import Component, Port
from iscesys.Compatibility import Compatibility
from stdproc.orbit import orbit2sch
from isceobj.Util.decorators import port, logged, pickled

ORBIT_POSITION = Component.Parameter(
    'orbitPosition',
    public_name='orbit xyz position vectors',
    default=[],
    type=list,
    units='m',
    mandatory=True,
    doc="Orbit xyz position vectors"
    )

ORBIT_VELOCITY = Component.Parameter(
    'orbitVelocity',
    public_name='orbit xyz velocity vectors',
    default=[],
    type=list,
    units='m/s',
    mandatory=True,
    doc="Orbit xyz velocity vectors"
    )

PLANET_GM = Component.Parameter(
    'planetGM',
    public_name='planet GM (m**3/s**2)',
    type=float,
    default= CN.EarthGM,
    units='m**3/s**2',
    mandatory=True,
    doc="Planet mass times Newton's constant in units m**3/s**2"
    )

ELLIPSOID_MAJOR_SEMIAXIS = Component.Parameter(
    'ellipsoidMajorSemiAxis',
    public_name='ellipsoid semi major axis (m)',
    type=float,
    default=CN.EarthMajorSemiAxis,
    units='m',
    mandatory=True,
    doc="Ellipsoid semi major axis"
    )

ELLIPSOID_ECCENTRICITY_SQUARED = Component.Parameter(
    'ellipsoidEccentricitySquared',
    public_name='ellipsoid eccentricity squared',
    type=float,
    default=CN.EarthEccentricitySquared,
    units=None,
    mandatory=True,
    doc="Ellipsoid eccentricity squared"
    )

COMPUTE_PEG_INFO_FLAG = Component.Parameter(
    'computePegInfoFlag',
    public_name='compute peg flag',
    type=int,
    default=-1,
    mandatory=False,
    doc=(
        "Compute peg point flag: "+
        "compute from orbit if value is not -1; "+
        "use given peg point if value = -1."
        )
    )

PEG_LATITUDE = Component.Parameter(
    'pegLatitude',
    public_name='peg latitude (rad)',
    default=0.,
    units='rad',
    type=float,
    mandatory=False,
    doc="Peg point latitude to use if compute peg flag = -1"
    )

PEG_LONGITUDE = Component.Parameter(
    'pegLongitude',
    public_name='peg longitude (rad)',
    default=0.,
    units='rad',
    type=float,
    mandatory=False,
    doc="Peg longitude to use if compute peg flag = -1"
    )

PEG_HEADING = Component.Parameter(
    'pegHeading',
    public_name='peg heading (rad)',
    default=0.,
    units='rad',
    type=float,
    mandatory=False,
    doc="Peg point heading to use if compute peg flag = -1"
    )

AVERAGE_HEIGHT = Component.Parameter(
    'averageHeight',
    public_name='average height (m)',
    default=0,
    units='m',
    type=float,
    mandatory=False,
    doc="Average orbital hieght; used only if compute peg flag = -1"
    )

class Orbit2sch(Component):
    
    ## An imperative flag? REFACTOR.
    computePegInfoFlag = -1 #false by default 

    planetGM = CN.EarthGM
    ellipsoidMajorSemiAxis = CN.EarthMajorSemiAxis
    ellipsoidEccentricitySquared = CN.EarthEccentricitySquared
    
    def __init__(self,
                 averageHeight=None,
                 planet=None,
                 orbit=None,
                 peg=None):

        super(Orbit2sch, self).__init__()

        self.averageHeight = averageHeight

        if planet is not None: self.wireInputPort(name='planet', object=planet)
        if orbit is not orbit: self.wireInputPort(name='orbit', object=orbit)
        if peg is not None: self.wireInputPort(name='peg', object=peg)

        self._time = None
        self._orbit = None
        self.orbitPosition = []
        self.dim1_orbitPosition = None
        self.dim2_orbitPosition = None
        self.orbitVelocity = []
        self.dim1_orbitVelocity = None
        self.dim2_orbitVelocity = None
        self.pegLatitude = None
        self.pegLongitude = None
        self.pegHeading = None
        
        self.position = []
        self.dim1_position = None
        self.dim2_position = None
        self.velocity = []
        self.dim1_velocity = None
        self.dim2_velocity = None
        self.acceleration = []
        self.dim1_acceleration = None
        self.dim2_acceleration = None
        self.logger = logging.getLogger('isce.orbit2sch')
        self.dictionaryOfOutputVariables = {'SCH_POSITION' : 'self.position', 
	
                                            'SCH_VELOCITY':'self.velocity',
	 
                                            'SCH_GRAVITATIONAL_ACCELERATION':'self.acceleration'}
        self.descriptionOfVariables = {}
        self.mandatoryVariables = []
        self.optionalVariables = []
        typePos = 2
        for key , val in self.dictionaryOfVariables.items():
            if val[typePos] == 'mandatory':
                self.mandatoryVariables.append(key)
            elif val[typePos] == 'optional':
                self.optionalVariables.append(key)
            else:
                print('Error. Variable can only be optional or mandatory')
                raise Exception
        return

    def createPorts(self):
        # Create input ports
        orbitPort = Port(name='orbit', method=self.addOrbit)
        planetPort = Port(name='planet', method=self.addPlanet)
        pegPort = Port(name='peg', method=self.addPeg)
        # Add the ports
        self.inputPorts.add(orbitPort)
        self.inputPorts.add(planetPort)
        self.inputPorts.add(pegPort)     
        return None


    def orbit2sch(self):
        for port in self.inputPorts:
            port()
        self.dim1_orbitPosition = len(self.orbitPosition)
        self.dim2_orbitPosition = len(self.orbitPosition[0])
        self.dim1_orbitVelocity = len(self.orbitVelocity)
        self.dim2_orbitVelocity = len(self.orbitVelocity[0])
        self.dim1_position = self.dim1_orbitPosition
        self.dim2_position = self.dim2_orbitPosition
        self.dim1_velocity = self.dim1_orbitVelocity
        self.dim2_velocity = self.dim2_orbitVelocity
        self.dim1_acceleration = self.dim1_orbitPosition
        self.dim2_acceleration = self.dim2_orbitPosition
        self.allocateArrays()
        self.setState()
        orbit2sch.orbit2sch_Py()
        self.getState()
        self.deallocateArrays()
        self._orbit = Orbit(source='SCH')
#        self._orbit.setOrbitSource('Orbit2SCH')
        self._orbit.setReferenceFrame('SCH')
#
        for i in range(len(self.position)):
            sv = StateVector()
            sv.setTime(self._time[i])
            sv.setPosition(self.position[i])
            sv.setVelocity(self.velocity[i])
            self._orbit.addStateVector(sv)
        return

    def setState(self):
        orbit2sch.setStdWriter_Py(int(self.stdWriter))
        if self.computePegInfoFlag == -1:
            orbit2sch.setPegLatitude_Py(float(self.pegLatitude))
            orbit2sch.setPegLongitude_Py(float(self.pegLongitude))
            orbit2sch.setPegHeading_Py(float(self.pegHeading))
            orbit2sch.setAverageHeight_Py(float(self.averageHeight))
            
        orbit2sch.setOrbitPosition_Py(self.orbitPosition, 
                                      self.dim1_orbitPosition, 
                                      self.dim2_orbitPosition)
        orbit2sch.setOrbitVelocity_Py(self.orbitVelocity, 
                                      self.dim1_orbitVelocity, 
                                      self.dim2_orbitVelocity)
        orbit2sch.setPlanetGM_Py(float(self.planetGM))
        orbit2sch.setEllipsoidMajorSemiAxis_Py(
            float(self.ellipsoidMajorSemiAxis)
            )
        orbit2sch.setEllipsoidEccentricitySquared_Py(
            float(self.ellipsoidEccentricitySquared)
            )
        orbit2sch.setComputePegInfoFlag_Py(
            int(self.computePegInfoFlag)
            )
        return None

    def setOrbitPosition(self, var):
        self.orbitPosition = var
        return

    def setOrbitVelocity(self, var):
        self.orbitVelocity = var
        return

    def setPlanetGM(self, var):
        self.planetGM = float(var)
        return

    def setEllipsoidMajorSemiAxis(self, var):
        self.ellipsoidMajorSemiAxis = float(var)
        return

    def setEllipsoidEccentricitySquared(self, var):
        self.ellipsoidEccentricitySquared = float(var)
        return

    def setComputePegInfoFlag(self, var):
        self.computePegInfoFlag = int(var)
        return

    def setPegLatitude(self, var):
        self.pegLatitude = float(var)
        return

    def setPegLongitude(self, var):
        self.pegLongitude = float(var)
        return

    def setPegHeading(self, var):
        self.pegHeading = float(var)
        return

    def setAverageHeight(self, var):
        self.averageHeight = float(var)
        return

    def getState(self):
        self.position = orbit2sch.getSchPosition_Py(self.dim1_position,
                                                    self.dim2_position)
        self.velocity = orbit2sch.getSchVelocity_Py(self.dim1_velocity,
                                                    self.dim2_velocity)
        self.acceleration = orbit2sch.getSchGravitationalAcceleration_Py(
            self.dim1_acceleration, self.dim2_acceleration
            )
        return

#    def getStdWriter(self):
#        return self.position

    def getSchVelocity(self):
        return self.velocity

    def getSchGravitationalAcceleration(self):
        return self.acceleration

    def getOrbit(self):
        return self._orbit

    def allocateArrays(self):
        if self.dim1_orbitPosition is None:
            self.dim1_orbitPosition = len(self.orbitPosition)
            self.dim2_orbitPosition = len(self.orbitPosition[0])

        if (not self.dim1_orbitPosition) or (not self.dim2_orbitPosition):
            raise ValueError("Error. Trying to allocate zero size array")

        orbit2sch.allocate_xyz_Py(self.dim1_orbitPosition, 
                                  self.dim2_orbitPosition)

        if self.dim1_orbitVelocity is None:
            self.dim1_orbitVelocity = len(self.orbitVelocity)
            self.dim2_orbitVelocity = len(self.orbitVelocity[0])

        if (not self.dim1_orbitVelocity) or (not self.dim2_orbitVelocity):
            raise Value("Error. Trying to allocate zero size array")

        orbit2sch.allocate_vxyz_Py(self.dim1_orbitVelocity, 
                                   self.dim2_orbitVelocity)

        if self.dim1_position is None:
            self.dim1_position = len(self.position)
            self.dim2_position = len(self.position[0])

        if (not self.dim1_position) or (not self.dim2_position):
            ("Error. Trying to allocate zero size array")

            raise Exception

        orbit2sch.allocate_sch_Py(self.dim1_position, self.dim2_position)

        if self.dim1_velocity is None:
            self.dim1_velocity = len(self.velocity)
            self.dim2_velocity = len(self.velocity[0])

        if (not self.dim1_velocity) or (not self.dim2_velocity):
            print("Error. Trying to allocate zero size array")

            raise Exception

        orbit2sch.allocate_vsch_Py(self.dim1_velocity, self.dim2_velocity)

        if self.dim1_acceleration is None:
            self.dim1_acceleration = len(self.acceleration)
            self.dim2_acceleration = len(self.acceleration[0])

        if (not self.dim1_acceleration) or (not self.dim2_acceleration):
            print("Error. Trying to allocate zero size array")

            raise Exception

        orbit2sch.allocate_asch_Py(self.dim1_acceleration, self.dim2_acceleration)


        return





    def deallocateArrays(self):
        orbit2sch.deallocate_xyz_Py()
        orbit2sch.deallocate_vxyz_Py()
        orbit2sch.deallocate_sch_Py()
        orbit2sch.deallocate_vsch_Py()
        orbit2sch.deallocate_asch_Py()

        return
    

    @property
    def orbit(self):
        return self._orbit
    @orbit.setter
    def orbit(self, orbit):
        self.orbit = orbit
        return None

    @property
    def time(self):
        return self._time
    @time.setter
    def time(self):
        self.time = time
        return None

    def addOrbit(self):                
        orbit = self.inputPorts['orbit']
        if orbit:
            try:
                time, self.orbitPosition, self.orbitVelocity, offset = orbit.to_tuple()
                self._time = []
                for t in time:
                    self._time.append(offset +  datetime.timedelta(seconds=t))
            except AttributeError:
                self.logger.error(
                    "orbit port should look like an orbit, not: %s" %
                    (orbit.__class__)
                    )  
                raise AttributeError 
            pass
        return None
        
    def addPlanet(self):        
        planet = self._inputPorts.getPort('planet').getObject()
        if(planet):
            try:
                self.planetGM = planet.get_GM()
                self.ellipsoidMajorSemiAxis = planet.get_elp().get_a()
                self.ellipsoidEccentricitySquared = planet.get_elp().get_e2()
            except AttributeError:
                self.logger.error(
                    "Object %s requires get_GM(), get_elp().get_a() and get_elp().get_e2() methods" % (planet.__class__)
                    )
                raise AttributeError 
        
    def addPeg(self):        
        peg = self._inputPorts.getPort('peg').getObject()
        if(peg):
            try:
                self.pegLatitude = math.radians(peg.getLatitude())
                self.pegLongitude = math.radians(peg.getLongitude())
                self.pegHeading = math.radians(peg.getHeading())
                self.logger.debug("Peg Object: %s" % (str(peg)))
            except AttributeError:
                self.logger.error(
                    "Object %s requires getLatitude(), getLongitude() and getHeading() methods" %
                    (peg.__class__)
                    )
                raise AttributeError 
                   
            pass
        pass
    pass


class JUNK:
    def addOrbit(self):                
        orbit = self.inputPorts['orbit']
        if orbit:
            try:
                time, self.orbitPosition, self.orbitVelocity, offset = orbit.to_tuple()
                self._time = []
                for t in time:
                    self._time.append(offset +  datetime.timedelta(seconds=t))
            except AttributeError:
                self.logger.error(
                    "orbit port should look like an orbit, not: %s" %
                    (orbit.__class__)
                    )  
                raise AttributeError 
            pass
        return None
        
    def addPlanet(self):        
        planet = self._inputPorts.getPort('planet').getObject()
        if(planet):
            try:
                self.planetGM = planet.get_GM()
                self.ellipsoidMajorSemiAxis = planet.get_elp().get_a()
                self.ellipsoidEccentricitySquared = planet.get_elp().get_e2()
            except AttributeError:
                self.logger.error(
                    "Object %s requires get_GM(), get_elp().get_a() and get_elp().get_e2() methods" % (planet.__class__)
                    )
                raise AttributeError 
        
    def addPeg(self):        
        peg = self._inputPorts.getPort('peg').getObject()
        if(peg):
            try:
                self.pegLatitude = math.radians(peg.getLatitude())
                self.pegLongitude = math.radians(peg.getLongitude())
                self.pegHeading = math.radians(peg.getHeading())
                self.logger.debug("Peg Object: %s" % (str(peg)))
            except AttributeError:
                self.logger.error(
                    "Object %s requires getLatitude(), getLongitude() and getHeading() methods" %
                    (peg.__class__)
                    )
                raise AttributeError 
                   
            pass
        pass

    

    def __getstate__(self):
        d = dict(self.__dict__)
        del d['logger']
        return d

    def __setstate__(self, d):
        self.__dict__.update(d)
        self.logger = logging.getLogger('isce.orbit2sch')
        return

