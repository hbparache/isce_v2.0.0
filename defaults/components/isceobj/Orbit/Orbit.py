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



import datetime
import logging
import operator
from functools import reduce
#from iscesys.DateTimeUtil.DateTimeUtil import DateTimeUtil as DTU
from iscesys import DateTimeUtil as DTU
from iscesys.Component.Component import Component
from isceobj.Util.decorators import type_check, pickled, logged

# This class stores platform position and velocity information.
class StateVector(Component):    
    
    dictionaryOfVariables = {'TIME': ['_time','float','mandatory'],
                             'POSITION': ['_position','float','mandatory'],
                             'VELOCITY': ['_velocity','float','mandatory']}


    def __init__(self, time=None, position=None, velocity=None):
        super(StateVector, self).__init__()
        self._time = time
        self._position = position or []
        self._velocity = velocity or []
        self.descriptionOfVariables = {}
        return None

    def __str__(self):
        return "%s\t%s\t%s" % (self._time, self._position, self._velocity)
    
    def __iter__(self):
        return self
    
    @type_check(datetime.datetime)
    def setTime(self, time):
        self._time = time            
        pass
                    
    def getTime(self):
        return self._time
    
    def setPosition(self, position):
        self._position = position
        
    def getPosition(self):
        return self._position
    
    def setVelocity(self, velocity):
        self._velocity = velocity
        
    def getVelocity(self):
        return self._velocity
    
    def getScalarVelocity(self):
        """Calculate the scalar velocity M{sqrt(vx^2 + vy^2 + vz^2)}.
        @rtype: float
        @return: the scalar velocity
        """
        return reduce(operator.add, [item**2 for item in self.velocity])**0.5
    
    def calculateHeight(self, ellipsoid):
        """Calculate the height above the provided ellipsoid.
        @type ellipsoid: Ellipsoid
        @param ellipsoid: an ellipsoid
        @rtype: float
        @return: the height above the ellipsoid
        """
        lat, lon, height = ellipsoid.xyz_to_llh(self.position)
        return height

    __todo__ = " 2.7 python functools.cmp decorator."
    def __cmp__(self, other):
        return cmp(self.time, other.time)

    def __str__(self):
        retstr = "Time: %s\n"
        retlst = (self._time,)
        retstr += "Position: %s\n"
        retlst += (self._position,)
        retstr += "Velocity: %s\n"
        retlst += (self._velocity,)
        return retstr % retlst
    
    time = property(getTime,setTime)
    position = property(getPosition,setPosition)
    velocity = property(getVelocity,setVelocity)
    pass

##
# This class encapsulates orbital information\n
# The Orbit class consists of a list of \c StateVector objects
# and provides an iterator over this list.
@pickled
class Orbit(Component):    
    
    dictionaryOfVariables = {'STATE_VECTORS':
                                 ['_stateVectors',float, 'mandatory'],
                             'ORBIT_QUALITY': ['_orbitQuality',str,'optional'],
                             'ORBIT_SOURCE': ['_orbitSource',str, 'optional'],
                             'ORBIT_REFERENCE_FRAME':
                                 ['_referenceFrame',str,'optional']
                             }
    
    logging_name = "isce.Orbit"
    
    _minTime = datetime.datetime(year=datetime.MAXYEAR,month=12,day=31)
    _maxTime = datetime.datetime(year=datetime.MINYEAR,month=1,day=1)

    @logged
    def __init__(self, source=None, quality=None, stateVectors=None):
        super(Orbit, self).__init__()
        self._last = 0
        self._orbitQuality = quality or None
        self._orbitSource = source or None
        self._referenceFrame = None
        self._stateVectors = stateVectors or []
        self.descriptionOfVariables = {}
        return None
        
    def __iter__(self):
        return self
    
    def __len__(self):
        return len(self.stateVectors)

    def __getitem__(self, index):
        return self.stateVectors[index]

    def __contains__(self, time):
        return self._inRange(time)

    @property
    def stateVectors(self):
        return self._stateVectors

    @property
    def maxTime(self):
        return self._maxTime

    @maxTime.setter
    def maxTime(self, time):
        self._maxTime = time

    @property
    def minTime(self):
        return self._minTime

    @minTime.setter
    def minTime(self, time):
        self._minTime = time
    
    
    def setOrbitQuality(self,qual):
        self._orbitQuality = qual
        
    def getOrbitQuality(self):
        return self._orbitQuality
    
    def setOrbitSource(self,source):
        self._orbitSource = source
        
    def getOrbitSource(self):
        return self._orbitSource
   
    def setReferenceFrame(self,ref):
        self._referenceFrame = ref

    def getReferenceFrame(self):
        return self._referenceFrame

    @type_check(StateVector)
    def addStateVector(self, vec):
        """
        Add a state vector to the orbit.
        @type vec: Orbit.StateVector
        @param vec: a state vector
        @raise TypeError: if vec is not of type StateVector
        """
        self._stateVectors.append(vec)
        # Reset the minimum and maximum time bounds if necessary
        if vec.time < self.minTime: self.minTime = vec._time
        if vec.time > self.maxTime: self.maxTime = vec._time
        
    def __next__(self):
        if self._last < len(self):
            next = self._stateVectors[self._last]
            self._last += 1
            return next
        else:
            self._last = 0 # This is so that we can restart iteration
            raise StopIteration()
    

    def interpolateOrbit(self, time, method='linear'):
        """Interpolate the state vector of the orbit at a given time.
        @type time: datetime.datetime
        @param time: the time at which interpolation is desired
        @type method: string
        @param method: the interpolation method, valid values are 'linear',
        'legendre' and 'hermite'
        @rtype: Orbit.StateVector
        @return: a state vector at the desired time otherwise None
        @raises ValueError: if the time lies outside of the time spanned by
        the orbit
        @raises NotImplementedError: if the desired interpolation method
        cannot be decoded
        """
        if time not in self:
            raise ValueError(
                "Time stamp (%s) falls outside of the interpolation interval [%s:%s]" %
                (time,self.minTime,self.maxTime)
                )
        
        if method == 'linear':
            newSV = self._linearOrbitInterpolation(time)
        elif method == 'legendre':
            newSV = self._legendreOrbitInterpolation(time)
        elif method == 'hermite':
            newSV = self._hermiteOrbitInterpolation(time)
        else:
            raise NotImplementedError(
                "Orbit interpolation type %s, is not implemented" % method
                )
        return newSV
    
    ## Isn't orbit redundant? -copmute the method base on name
    def interpolate(self, time, method='linear'):
        if time not in self:
            raise ValueError("Time stamp (%s) falls outside of the interpolation interval [%s:%s]" % (time,self.minTime,self.maxTime))
        try:
            return getattr(self, '_'+method+'OrbitInterpolation')(time)
        except AttributeError:
            pass
        raise NotImplementedError(
            "Orbit interpolation type %s, is not implemented" % method
            )
    
    interpolateOrbit = interpolate

    def _linearOrbitInterpolation(self,time):
        """
        Linearly interpolate a state vector.  This method returns None if
        there are fewer than 2 state vectors in the orbit.
        @type time: datetime.datetime
        @param time: the time at which to interpolate a state vector
        @rtype: Orbit.StateVector
        @return: the state vector at the desired time
        """
        if len(self) < 2:
            self.logger.error("Fewer than 2 state vectors present in orbit, cannot interpolate")
            return None

        position = [0.0 for i in range(3)]
        velocity = [0.0 for i in range(3)]        
        
        for sv1 in self.stateVectors:
            tmp=1.0
            for sv2 in self.stateVectors:
                if sv1.time == sv2.time:  
                    continue
                numerator = float(DTU.timeDeltaToSeconds(sv2.time-time))
                denominator = float(
                    DTU.timeDeltaToSeconds(sv2.time - sv1.time)
                    )
                tmp = tmp*(numerator)/(denominator)
            for i in range(3):                
                position[i] = position[i] + sv1.getPosition()[i]*tmp
                velocity[i] = velocity[i] + sv1.getVelocity()[i]*tmp
                
        return StateVector(time, position, velocity)
    
    def _legendreOrbitInterpolation(self,time):
        """Interpolate a state vector using an 8th order Legendre polynomial.
        This method returns None if there are fewer than 9 state vectors in
        the orbit.
        @type time: datetime.datetime
        @param time: the time at which to interpolate a state vector
        @rtype: Orbit.StateVector
        @return: the state vector at the desired time
        """
        if len(self) < 9:
            self.logger.error(
                "Fewer than 9 state vectors present in orbit, cannot interpolate"
                )
            return None
        try:
            newOrbit = self.selectStateVectors(time, 4, 5)
        except LookupError as e:
            return None
        obsTime, obsPos, obsVel, offset = newOrbit.to_tuple(
        relativeTo=self.minTime
        )
        t = DTU.timeDeltaToSeconds(time-self.minTime)        
        t0 = DTU.timeDeltaToSeconds(newOrbit.minTime-self.minTime)
        tn = DTU.timeDeltaToSeconds(newOrbit.maxTime-self.minTime)        
        ansPos = self._legendre8(t0, tn, t, obsPos)
        ansVel = self._legendre8(t0, tn, t, obsVel)
        
        return StateVector(time, ansPos, ansVel)



    def _legendre8(self,t0,tn,t,v):
        """Interpolate an orbit using an 8th order Legendre polynomial
        @type t0: float
        @param t0: starting time
        @type tn: float
        @param tn: ending time
        @type t: float
        @param t: time at which vt must be interpolated
        @type v: list
        @param v: 9 consecutive points
        @rtype: float
        @return: interpolated point at time t
        """        
        trel = (t-t0)/(tn-t0)*(len(v)-1)+1
        itrel=max(1,min(int(trel)-4,len(v)-9))+1
        t = trel-itrel       
        vt = [0 for i in range(3)]
        kx = 0
        x=t+1
        noemer = [40320,-5040,1440,-720,576,-720,1440,-5040,40320]
    
        teller=(x)*(x-1)*(x-2)*(x-3)*(x-4)*(x-5)*(x-6)*(x-7)*(x-8)
        if (teller == 0):
            kx = int(x)
            for i in range(3):
                vt[i] = v[kx][i]
        else:
            for kx in range(9):
                coeff=teller/noemer[kx]/(x-kx)
                for i in range(3):                                
                    vt[i] = vt[i] + coeff*v[kx][i]
    
        return vt


    def _hermiteOrbitInterpolation(self,time):
        """
        Interpolate a state vector using Hermite interpolation.
        This method returns None if there are fewer than 4 state
        vectors in the orbit.
        @type time: datetime.datetime
        @param time: the time at which to interpolate a state vector
        @rtype: Orbit.StateVector
        @return: the state vector at the desired time
        """

        import os
        from ctypes import c_double, cdll,byref
        orbitHermite = (
            cdll.LoadLibrary(os.path.dirname(__file__)+'/orbitHermite.so')
            )
        
        if len(self) < 4:
            self.logger.error(
                "Fewer than 4 state vectors present in orbit, cannot interpolate"
                )
            return None

        # The Fortran routine assumes that it is getting an array of four
        # state vectors
        try:
            newOrbit = self.selectStateVectors(time, 2, 2)
        except LookupError:
            self.logger.error("Unable to select 2 state vectors before and after chosen time %s" % (time))
            return None
        
        # For now, assume that time is an array containing the times at which
        # we want to interpolate
        obsTime, obsPos, obsVel,offset = newOrbit.to_tuple(
            relativeTo=self.minTime
            )
        
        td = time - self.minTime
        ansTime = DTU.timeDeltaToSeconds(td)        
        flatObsPos = [item for sublist in obsPos for item in sublist]
        flatObsVel = [item for sublist in obsVel for item in sublist]
        flatAnsPos= [0.,0.,0.]# list([0.0 for i in range(3)])
        flatAnsVel= [0.,0.,0.]#list([0.0 for i in range(3)])
        obsTime_C = (c_double*len(obsTime))(*obsTime)
        obsPos_C = (c_double*len(flatObsPos))(*flatObsPos)
        obsVel_C = (c_double*len(flatObsVel))(*flatObsVel)
        ansTime_C = c_double(ansTime)
        ansPos_C = (c_double*3)(*flatAnsPos)
        ansVel_C = (c_double*3)(*flatAnsVel)
                
        # Use the C wrapper to the fortran Hermite interpolator        
        orbitHermite.orbitHermite_C(obsPos_C,
                                    obsVel_C,
                                    obsTime_C,
                                    byref(ansTime_C),
                                    ansPos_C,
                                    ansVel_C)

        return StateVector(time, ansPos_C[:], ansVel_C[:])
        
    ## This need to be public -very confusing since there is an __iter__
    def to_tuple(self, relativeTo=None):
        return self._unpackOrbit(relativeTo=relativeTo)

    def _unpackOrbit(self, relativeTo=None):
        """Convert and orbit object into tuple of lists containing time,
        position and velocity.
        @type relativeTo: datetime.datetime
        @param relativeTo: the time with which to reference the unpacked orbit
        @return: a tuple containing a list of time, position, velocity and
        relative time offset
        """
        time = []
        position = []
        velocity = []
        if relativeTo is None:
            relativeTo = self.minTime
        
        for sv in self.stateVectors:
            td = sv.time - relativeTo
            currentTime = ((
                    td.microseconds +
                    (td.seconds + td.days * 24 * 3600.0) * 10**6) / 10**6
                           )
            currentPosition = sv.getPosition()
            currentVelocity = sv.getVelocity()        
            time.append(currentTime)
            position.append(currentPosition)
            velocity.append(currentVelocity)
    
        return time, position, velocity, relativeTo
    
    ## Why does this version fail ERS and not ALOS?
    def selectStateVectorsBroken(self, time, before, after):
        """Given a time and a number of before and after state vectors, 
        return an Orbit with (before+after) state vectors with reference to
        time.
        @type time: datetime.datetime
        @param time: the reference time for subselection
        @type before: integer
        @param before: the number of state vectors before the chosen time to
        select
        @type after: integer
        @param after: the number of state vectors after the chosen time to
        select
        @rtype: Orbit.Orbit
        @return: an orbit containing (before+after) state vectors relative to
        time
        @raises LookupError: if there are insufficient state vectors in the
        orbit
        """        
        # First, find the index closest to the requested time
        i=0
        while self.stateVectors[i].time <= time:
            i += 1
        beforeIndex = i
        
        # Check that we can grab enough data
        if (beforeIndex-before) < 0:
            raise LookupError("Requested index %s is out of bounds" %
                              (beforeIndex-before))
        elif (beforeIndex+after) > len(self):
            raise LookupError("Requested index %s is out of bounds" %
                              (beforeIndex+after))
        
        # Create a new orbit object - filled with goodies.
        return Orbit(source=self.orbitSource,
                     quality=self.orbitQuality,
                     stateVectors=[
                self[i] for i in range(
                    (beforeIndex-before),(beforeIndex+after)
                    )])
        


    def selectStateVectors(self,time,before,after):
        """
        Given a time and a number of before and after state vectors, 
        return an Orbit with (before+after) state vectors with reference to
        time.
        """        
        # First, find the index closest to the requested time
        i=0
        while(self._stateVectors[i].getTime() <= time):
            i += 1
        beforeIndex = i
        
        # Check that we can grab enough data
        if ((beforeIndex-before) < 0):
            raise LookupError(
                "Requested index %s is out of bounds" % (beforeIndex-before)
                )
        elif ((beforeIndex+after) > len(self._stateVectors)):
            raise LookupError(
                "Requested index %s is out of bounds" % (beforeIndex+after)
                )
        
        # Create a new orbit object 
        newOrbit = Orbit()
        # inject dependencies
        newOrbit.setOrbitSource(self.orbitSource)
        newOrbit.setOrbitQuality(self.orbitQuality)
        for i in range((beforeIndex-before),(beforeIndex+after)):
            newOrbit.addStateVector(self[i])
        
        return newOrbit

        

    def trimOrbit(self, startTime, stopTime):
        """Trim the list of state vectors to encompass the time span
        [startTime:stopTime]
        @type startTime: datetime.datetime
        @param startTime: the desired starting time for the output orbit
        @type stopTime: datetime.datetime
        @param stopTime: the desired stopping time for the output orbit
        @rtype: Orbit.Orbit
        @return: an orbit containing all of the state vectors within the time
        span [startTime:stopTime]
        """
        
        newOrbit = Orbit()        
        newOrbit.setOrbitSource(self._orbitSource)
        newOrbit.setReferenceFrame(self._referenceFrame)
        for sv in self._stateVectors:
            if startTime < sv.time < stopTime:
                newOrbit.addStateVector(sv)
                
        return newOrbit

    def _inRange(self,time):
        """Check whether a given time is within the range of values for an
        orbit.
        @type time: datetime.datetime
        @param time: a time 
        @rtype: boolean
        @return: True if the time falls within the time span of the orbit,
        otherwise False
        """
        return self.minTime <= time <= self.maxTime

    def __str__(self):
        retstr = "Orbit Source: %s\n"
        retlst = (self._orbitSource,)
        retstr += "Orbit Quality: %s\n"
        retlst += (self._orbitQuality,)
        retstr += "Orbit Reference Frame: %s\n"
        retlst += (self._referenceFrame,)
        return retstr % retlst
    
    stateVector = property()
    orbitQuality = property(getOrbitQuality, setOrbitQuality)
    orbitSource = property(getOrbitSource, setOrbitSource)                   

    pass


    def exportToC(self):
        from isceobj.Util import combinedlib
        orb = []

        for sv in self._stateVectors:
            tim = DTU.seconds_since_midnight(sv.getTime())
            pos = sv.getPosition()
            vel = sv.getVelocity()
            
            row = [tim] + pos + vel
            orb.append(row)

        cOrbit = combinedlib.exportOrbitToC(orb)
        return cOrbit


def createOrbit():
    return Orbit()
