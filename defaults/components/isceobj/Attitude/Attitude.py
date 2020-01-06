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



import math
import datetime
import logging
from iscesys.Component.Component import Component
from isceobj.Util.decorators import type_check, pickled, logged


## This class stores platform pitch, roll and yaw information.
class StateVector(Component):

    
    dictionaryOfVariables = {'TIME': ['_time', datetime ,'mandatory'],
                             'PITCH': ['_pitch', list,'mandatory'],
                             'ROLL': ['_roll', list,'mandatory'],
                             'YAW': ['_yaw', list,'mandatory']}

    def __init__(self, time=None, pitch=None, roll=None, yaw=None):
        super(StateVector, self).__init__()
        self._time = time
        self._pitch = pitch
        self._roll = roll
        self._yaw = yaw
        self.descriptionOfVariables = {}
        return None

    @type_check(datetime.datetime)
    def setTime(self, time):
        self._time = time            
        pass
                    
    def getTime(self):
        return self._time
    
    def setPitch(self, pitch):
        self._pitch = pitch
        
    def getPitch(self):
        return self._pitch
    
    def setRoll(self, roll):
        self._roll = roll
        
    def getRoll(self):
        return self._roll
    
    def setYaw(self, yaw):
        self._yaw = yaw
        
    def getYaw(self):
        return self._yaw
            
    def __str__(self):
        retstr = "Time: %s\n"
        retlst = (self.time,)
        retstr += "Pitch: %s\n"
        retlst += (self.pitch,)
        retstr += "Roll: %s\n"
        retlst += (self.roll,)
        retstr += "Yaw: %s\n"
        retlst += (self.yaw,)
        return retstr % retlst
    
    time = property(getTime, setTime)
    pitch = property(getPitch, setPitch)
    roll = property(getRoll, setRoll)
    yaw = property(getYaw, setYaw)
    pass

## This class encapsulates spacecraft attitude information
## The Attitude class consists of a list of  StateVector objects
## and provides an iterator over this list.
@pickled
class Attitude(Component):    
    
    logging_name = 'isce.Attitude'
    
    dictionaryOfVariables = {'STATE_VECTORS': ['_stateVectors',
                                               list,
                                               'mandatory'],
                             'ATTITUDE_QUALITY': ['_attitudeQuality',
                                                  str,
                                                  'optional'],
                             'ATTITUDE_SOURCE': ['_attitudeSource',
                                                 str,
                                                 'optional']}

    min_length_for_interpolation = 3

    def __init__(self):
        super(Attitude, self).__init__()
        self._last = 0
        self._minTime = datetime.datetime(year=datetime.MAXYEAR,
                                          month=12,
                                          day=31)
        self._maxTime = datetime.datetime(year=datetime.MINYEAR,
                                          month=1,
                                          day=1)
        self._attitudeQuality = None
        self._attitudeSource = None        
        self._stateVectors = []
        self.descriptionOfVariables = {}
        return None
    
    @property
    def stateVectors(self):
        return self._stateVectors
               
    ## A container needs a length.
    def __len__(self):
        return len(self.stateVectors)
     
    ## A container needs a getitem
    def __getitem__(self, index):
        return self.stateVectors[index]

    def __setitem__(self, *args):
        raise TypeError("'%s' object does not support item assignment" %
                        self.__class__.__name__
                        )
    
    def __delitem__(self, *args):
        raise TypeError("'%s' object does not support item deletion"
                        %self.__class__.__name__)
    
    def __iter__(self):
        return self

    def next(self):
        if self._last < len(self):
            result = self.stateVectors[self._last]
            self._last += 1
            return result
        raise StopIteration()

    def setAttitudeQuality(self, qual):
        self._attitudeQuality = qual
        
    def getAttitudeQuality(self):
        return self._attitudeQuality
    
    def setAttitudeSource(self, source):
        self._attitudeSource = source
        
    def getAttitudeSource(self):
        return self._attitudeSource   

    @type_check(StateVector)
    def addStateVector(self, vec):
        self._stateVectors.append(vec)
        # Reset the minimum and maximum time bounds if necessary
        if (vec.time < self._minTime): self._minTime = vec.time
        if (vec.time > self._maxTime): self._maxTime = vec.time
        pass
    
    #TODO This needs to be fixed to work with scalar pitch, roll and yaw data
    #TODO- use Utils/geo/charts and let numpy do the work (JEB).
    def interpolate(self, time):
        if len(self) < self.min_length_for_interpolation:
            message = ("Fewer than %d state vectors present in attitude, "+
                       "cannot interpolate" % self.min_length_for_interpolation
                       )
            self.logger.error(
                message
                )
            return None
        if not self._inRange(time):
            message = (
                "Time stamp (%s) falls outside of the interpolation interval"+
                "[%s:%s]"
                ) % (time, self._minTime, self._maxTime)
            raise ValueError(message)
        pitch = 0.0
        roll = 0.0
        yaw = 0.0
        for sv1 in self.stateVectors:
            tmp=1.0
            for sv2 in self.stateVectors:
                if sv1.time == sv2.time: 
                    continue
                numerator = float(self._timeDeltaToSeconds(sv2.time-time))
                denominator = float(
                    self._timeDeltaToSeconds(sv2.time - sv1.time)
                    )
                tmp *= numerator/denominator
                pass
            pitch += sv1.pitch*tmp
            roll  += sv1.roll*tmp
            yaw   += sv1.yaw*tmp
            pass
        return StateVector(time, pitch, roll, yaw)

    def _inRange(self, time):
        """Check whether a given time stamp is within the range of values for
        an orbit"""
        return self._minTime <= time <= self._maxTime
        
    @type_check(datetime.timedelta)
    def _timeDeltaToSeconds(self, td):
        return (
            td.microseconds +
            (td.seconds + td.days * 24.0 * 3600) * 10**6
            ) / 10**6   

    def __str__(self):
        retstr = "Attitude Source: %s\n"
        retlst = (self.attitudeSource,)
        retstr += "Attitude Quality: %s\n"
        retlst += (self.attitudeQuality,)
        return retstr % retlst

    attitudeQuality = property(getAttitudeQuality, setAttitudeQuality)
    attitudeSource = property(getAttitudeSource, setAttitudeSource)
    pass


def createAttitude():
    return Attitude()
