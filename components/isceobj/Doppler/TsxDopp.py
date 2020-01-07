#!usr/bin/env python

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
import sys
import numpy as np
from iscesys.Component.Component import Component, Port

class TsxDopp(Component):
   
    ##### NOTE. there is no leapsecond here since all the formulas in Howard's
    # tsxpreproc where the doppler time is computed (look for dopplerEstimate)
    # and in tsxdopp where initial and ending times are computed, the
    # leapsecond cancels out when taking the differences.The dopplerTime
    # returned here is without leapsecond, so be aware of that
    def calculateDoppler(self):
        self.activateInputPorts()
        
        self._dopplerCoefficients = self.extractDopplerCoefficients(self._dopplerArray)
        self._dopplerTime = self.extractDopplerTime(self._dopplerArray)
        self._numDopplers = len(self._dopplerCoefficients)
        ts = self._startTimeGPS + self._startTimeGPSFraction
        te = self._stopTimeGPS + self._stopTimeGPSFraction
        dt = (te - ts)/float(self._numAzLines - 1)
        time = ts + dt*np.arange(self._numAzLines)
        self._fdc_mid = np.zeros(self._numAzLines)
        indxMax = len(self._dopplerTime)-2
        i = 0
        for t in time:
            indx = self.getTimeIndex(t)
            if(indx < 0 or indx > indxMax):
                self.logger.error("Time provided is not withing the starting and ending doppler time")
                break
#                raise Exception
            frac = (t - self._dopplerTime[indx])/(self._dopplerTime[indx + 1] - self._dopplerTime[indx])
            fdc0 = self._dopplerCoefficients[indx][0]
            fdc1 = self._dopplerCoefficients[indx+1][0]
            self._fdc_mid[i] = fdc0*(1-frac) + fdc1*frac
            i += 1

    
    def fitDoppler(self):
        #compute also the avd doppler which is the one used later on
        nd = len(self._dopplerAtMidRangeList)
        fdAve = 0
        for fd in self._dopplerAtMidRangeList:
            fdAve += fd.dopplerAtMidRange
        
        if nd:
            self.quadratic['a'] = fdAve/nd/self._prf 
        else:
            self.quadratic['a'] = 0 
        self.quadratic['b'] = 0
        self.quadratic['c'] = 0

    def getMidDoppler(self):
        return self._fdc_mid
    
    def getDopplerTime(self):
        return self._dopppleTime

    #this is the time save in Dopp.out in Howard's tsxpreproc.py
    def extractDopplerTime(self,dopArray):
        
        ret = []
        for el in dopArray:
            ret.append(self._startTimeGPS +  self.total_seconds(el['time'] - self._startTimeUTC))
        return np.array(ret)
    
    #compute total number of sec in time delta. it's a timedelta method for python 2.7
    def total_seconds(self,td):
        return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / float(10**6)

    def extractDopplerCoefficients(self,dopArray):
        
        ret = []
        for el in dopArray:
            ret.append(el['dopplerCoefficients'])

        return ret
    def getTimeIndex(self,t):
        ret = -1
        res = np.nonzero(t >= self._dopplerTime)[0]
        if(len(res) > 0):#take the last one for which the above relationship is true
            ret = res[-1]

        return ret

    def setStartTimeUTC(self,val):
        self._startTimeUTC = val
    def setStartTimeGPS(self,val):
        self._startTimeGPS = val
    def setStartTimeGPSFraction(self,val):
        self._startTimeGPSFraction = val
    def setStopTimeGPS(self,val):
        self._stopTimeGPS = val
    def setStopTimeGPSFraction(self,val):
        self._stopTimeGPSFraction = val
    def setNumberRangeSamples(self,val):
        self._numRangeSamples = val
    def setNumberLines(self,val):
        self._numAzLines = val
    def setDopplerArray(self,val):
        self._dopplerArray = val

    def addSensor(self):
        sensor = self._inputPorts.getPort('sensor').getObject()
        self._sensor =  sensor
        if (sensor):
            # the %10e4 comes from tsxpreproc in Howard TSX
            self._startTimeUTC = sensor.getFrame().getSensingStart()
            self._startTimeGPS = sensor.productInfo.sceneInfo.start.timeGPS%10e4
            self._startTimeGPSFraction =  sensor.productInfo.sceneInfo.start.timeGPSFraction
            self._stopTimeGPS = sensor.productInfo.sceneInfo.stop.timeGPS%10e4
            self._stopTimeGPSFraction = sensor.productInfo.sceneInfo.stop.timeGPSFraction
            self._numRangeSamples = sensor.productInfo.imageDataInfo.imageRaster.numberOfColumns
            self._numAzLines = sensor.productInfo.imageDataInfo.imageRaster.numberOfRows
            self._dopplerArray = sensor.dopplerArray 
            self._dopplerAtMidRangeList = sensor.processing.doppler.dopplerCentroid.dopplerEstimate
            self._prf = sensor.productSpecific.complexImageInfo.commonPRF

    logging_name = 'TsxDopp'

    def __init__(self):
        super(TsxDopp, self).__init__()
        self.quadratic = {}
        self._dopplerTime = []
        self._dopplerCoefficients = []
        self._startTimeGPS = None
        self._startTimeUTC = None
        self._startTimeGPSFractions = None
        self._stopTimeGPS = None
        self._stopTimeGPSFractions = None
        self._numRangeSamples = None
        self._numAzLines = None
        self._fdc_mid = None
        self._dopplerArray = []
        self._averageDoppler = []
        self._prf = None
#        self.logger = logging.getLogger('TsxDopp')
#        self.createPorts()
        return None

    def createPorts(self):
        sensorPort = Port(name='sensor',method=self.addSensor)
        self._inputPorts.add(sensorPort)
        return None
    pass


def main():
    import cPickle as cp
    fp = open(sys.argv[1])
    sensor = cp.load(fp)
    fp.close()
    TD = TsxDopp()
    TD.wireInputPort(name='sensor', object=sensor)
    TD.calculateDoppler()
    TD.fitDoppler()
    return None

if __name__ == '__main__':
    sys.exit(main())
