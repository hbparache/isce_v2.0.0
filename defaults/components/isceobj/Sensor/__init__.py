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
# Authors: Walter Szeliga, Eric Gurrola
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



from __future__ import print_function
from functools import partial
import os
from collections import namedtuple

SENSOR_DB = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'db')
xmlPrefix = SENSOR_DB

def getFactoriesInfo():
    """
    Returns a dictionary with information on how to create an object Sensor from its factory
    """
    return  {'Sensor':
                     {'args':
                           {
                            'sensor':{'value':SENSORS.keys(),'type':'str'},
                            'name':{'value':'','type':'str'}
                            },
                     'factory':'createSensor'
                     }
              }

def factory_template(sat,name=None):
    """factory_template(sat [,name=None])

    sat  is  sensor and module name, e.g., 'ALOS'
    name is  not implemented yet

    returns <sat>.<sat>(), i.e.,  generates factory for the sensor
    indicated by sat

    """
    modname = 'isceobj.Sensor.' + sat
    cls = getattr(__import__(modname, globals(), locals(), [sat], 0), sat)

    #The following 'if' statement is temporary until all of the sensors
    #are modified to accept name as an argument to their constructor.
    #Configuration from a name.xml file will not work for those
    #senors until they do implement this feature.
    try:
        return cls(name=name)
    except:
        return cls()

createALOS = partial(factory_template,'ALOS')
createCOSMO_SkyMed = partial(factory_template,'COSMO_SkyMed')
createERS = partial(factory_template,'ERS')
createEnviSAT = partial(factory_template,'EnviSAT')
createJERS = partial(factory_template,'JERS')
createRadarsat1 = partial(factory_template,'Radarsat1')
createRadarsat2 = partial(factory_template,'Radarsat2')
createTerraSARX = partial(factory_template,'TerraSARX')
createTanDEMX = partial(factory_template,'TanDEMX')
createSentinel1A = partial(factory_template,'Sentinel1A')
createGeneric = partial(factory_template,'Generic')
createCOSMO_SkyMed_SLC = partial(factory_template, 'COSMO_SkyMed_SLC')
createROI_PAC = partial(factory_template, 'ROI_PAC')
createKOMPSAT5 = partial(factory_template, 'KOMPSAT5')


SENSORS = {'ALOS' : createALOS,
           'COSMO_SKYMED' : createCOSMO_SkyMed,
           'COSMO_SKYMED_SLC' : createCOSMO_SkyMed_SLC,
           'ENVISAT' : createEnviSAT,
           'ERS' : createERS,
           'KOMPSAT5' : createKOMPSAT5,
           'RADARSAT1' : createRadarsat1,
           'RADARSAT2' : createRadarsat2,
           'ROI_PAC' : createROI_PAC,
           'TERRASARX' : createTerraSARX}

#These are experimental and can be added in as they become ready
#           'JERS': createJERS,
#           'SENTINEL1A' : createSentinel1A,
#           'TANDEMX' : createTanDEMX,



def createSensor(sensor='', name=None):
    try:
        cls = SENSORS[str(sensor).upper()]
        try:
            instance = cls(name)
        except AttributeError:
            raise TypeError("'sensor name'=%s  cannot be interpreted" %
                            str(sensor))
        pass
    except KeyError:
        print("Sensor type not recognized. Valid Sensor types:\n",
              SENSORS.keys())
        instance = None
        pass
    return instance

# Some sensors have a static constants dictionary, that needs
# to be a class. THis class is it. It should be a named tuple,
# but that's not backwards compatible
class Constants(object):
    """SensorConstants(*self._keys)

    since the original dictionary had a key 'Antenna Length' - it could
    neiter be made into a named tuple, nor a **kwargs constructor.

    The class is:
     Sensor.Constants
    There is no longer a
     Constants.Constants
    to collide with, but there my be confusion until the Constants module
    conforms to PEP008.
    """

    ## The keys to the dictionary
    _keys = ('iBias', 'qBias', 'pointingDirection', 'antennaLength')

    ## Fortran pointing direction flag: Left/Right -/+1
    POINTING_DIRECTION = {-1:'L',1: 'R'}

    ## Blind init - build now, parse later
    def __init__(self, iBias=0., qBias=0., pointingDirection=1,
        antennaLength=None):
        self._args = (iBias, qBias, pointingDirection, antennaLength)
        return None

    ## Emulate a dictionary 1st, and then a tuple.
    def __getitem__(self, key):
        try:
            result = self._args[self._keys.index(key)]
        except ValueError:
            try:
                result = self._args[key]
            except TypeError:
                message = str(key) + ' is neither a key nor an index'
                raise TypeError(message)
            pass
        return result

    def __complex__(self):
        return complex(self.i_bias +(1j)*self.q_bias)

    def __int__(self):
        return int(self.pointing_direction)

    def __float__(self):
        return float(self.antenna_length)

    @property
    def i_bias(self): return self['iBias']
    @property
    def q_bias(self): return self['qBias']
    @property
    def pointing_direction(self): return self['pointingDirection']
    @property
    def antenna_length(self): return self['antennaLength']

    pass


def createAuxFile(frame,filename):
    import math
    import array
    import datetime
    from iscesys.DateTimeUtil.DateTimeUtil import DateTimeUtil as DTU
    prf = frame.getInstrument().getPulseRepetitionFrequency()
    senStart = frame.getSensingStart()
    numPulses = int(math.ceil(DTU.timeDeltaToSeconds(frame.getSensingStop()-
                    senStart)*prf))
    # the aux files has two entries per line. day of the year and microseconds
    #in the day
    musec0 = (senStart.hour*3600 + senStart.minute*60 + senStart.second)*10**6
    musec0 += senStart.microsecond
    maxMusec = (24*3600)*10**6
    day0 = (datetime.datetime(senStart.year,senStart.month,senStart.day)
           -datetime.datetime(senStart.year,1,1)).days + 1
    outputArray  = array.array('d',[0]*2*numPulses)
    frame.auxFile = filename
    fp = open(frame.auxFile,'wb')
    j = -1
    for i1 in range(numPulses):
        j += 1
        musec = round((j/prf)*10**6) + musec0
        if musec >= maxMusec:
            day0 += 1
            musec0 = musec%maxMusec
            musec = musec0
            j = 0
        outputArray[2*i1] = day0
        outputArray[2*i1+1] = musec

    outputArray.tofile(fp)
    fp.close()


## refactor in: ALOS, ERS, EnviSat - should be a method for all of them
def tkfunc(self):
    from isceobj.Scene.Track import Track
    tk = Track()
    if(len(self._imageFileList) > 1):
        self.frame = tk.combineFrames(self.output, self.frameList)
        for i in range(len(self._imageFileList)):
            try:
                print (self.output + "_" + str(i))
                os.remove(self.output + "_" + str(i))
            except OSError:
                print(
                    "Error. Cannot remove temporary file",
                    self.output + "_" + str(i)
                    )
                raise OSError
            pass
        pass
    pass


class VolumeDirectoryBase(object):
    """Base class for VolumeDirectoryFile -- sub class needs a static:
    volume_fdr_arg
    that is the path argument to CEOS.CEOSDB
    """

    def __init__(self, file=None):
        self.file = file
        self.metadata = {}
        return None

    def parse(self):
        import CEOS
        try:
            with open(self.file,'r') as fp:
                volumeFDR = CEOS.CEOSDB(
                    xml=os.path.join(
                        xmlPrefix,
                        self.__class__.volume_fdr_arg
                        ),
                    dataFile=fp
                    )
                volumeFDR.parse()
                fp.seek(volumeFDR.getEndOfRecordPosition())
                pass
        except IOError as errs:
            errno, stderr = errs
            print("IOError: %s" % strerr)
            pass
        return None
    pass
