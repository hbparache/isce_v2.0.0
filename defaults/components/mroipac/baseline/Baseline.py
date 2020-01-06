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
import datetime
import logging
from iscesys.Component.Component import Component, Port
from isceobj.Util.mathModule import MathModule as MM
from isceobj.Orbit.Orbit import StateVector

# A class to hold three-dimensional basis vectors
class Basis(object):
    
    def __init__(self):
        self.x1 = []
        self.x2 = []
        self.x3 = []

# A class to hold three-dimensional basis vectors for spacecraft baselines
class BaselineBasis(Basis):
    
    def __init__(self):
        Basis.__init__(self)
    
    def setPositionVector(self,x):
        self.x1 = x
    
    def getPositionVector(self):
        return self.x1
        
    def setVelocityVector(self,v):
        self.x2 = v
        
    def getVelocityVector(self):
        return self.x2
    
    def setCrossTrackVector(self,c):
        self.x3 = c
    
    def getCrossTrackVector(self):
        return self.x3

class Baseline(Component):

    # Calculate the Look Angle of the master frame
    def calculateLookAngle(self):
        lookVector = self.calculateLookVector()
        return math.degrees(math.atan2(lookVector[1],lookVector[0]))

    # Calculate the look vector of the master frame
    def calculateLookVector(self):
        cosl = (2*self.height*self.radius + self.height*self.height +self.startingRange1*self.startingRange1)/(2*self.startingRange1*(self.radius + self.height))
        print('Height: ', self.height)
        print('Radius: ', self.radius)
        print('Range: ', self.startingRange1)
        print('COSL: ', cosl)
        sinl = math.sqrt(1 - cosl*cosl)
        return [cosl,sinl]
    
    # Calculate the scalar spacecraft velocity
    def calculateScalarVelocity(self,orbit,time):    
        sv = orbit.interpolateOrbit(time)
        v = sv.getVelocity()
        normV = MM.norm(v)
        
        return normV
    
    # Given an orbit and a time, calculate an orthogonal basis for cross-track and velocity directions
    # based on the spacecraft position        
    def calculateBasis(self,orbit,time):
        
        sv = orbit.interpolateOrbit(time)
        x1 = sv.getPosition()
        v = sv.getVelocity()
        r = MM.normalizeVector(x1) # Turn the position vector into a unit vector        
        v = MM.normalizeVector(v) # Turn the velocity vector into a unit vector
        c = MM.crossProduct(r,v) # Calculate the vector perpendicular to the platform position and velocity, this is the c, or cross-track vector
        c = MM.normalizeVector(c)
        v = MM.crossProduct(c,r) # Calculate a the "velocity" component that is perpendicular to the cross-track direction and position
        
        basis = BaselineBasis()
        basis.setPositionVector(r)
        basis.setVelocityVector(v)
        basis.setCrossTrackVector(c)
        
        return basis

    # Given two position vectors and a basis, calculate the offset between the two positions in this basis
    def calculateBasisOffset(self,x1,x2,basis):                
        dx = [(x2[j] - x1[j]) for j in range(len(x1))] # Calculate the difference between the master and slave position vectors
        z_offset = MM.dotProduct(dx,basis.getVelocityVector()) # Calculate the length of the projection of the difference in position and the "velocity" component
        v_offset = MM.dotProduct(dx,basis.getPositionVector())
        c_offset = MM.dotProduct(dx,basis.getCrossTrackVector())
        
        return z_offset,v_offset,c_offset

    # Calculate the baseline components between two frames
    def baseline(self):
        #TODO This could be further refactored into a method that calculates the baseline between
        #TODO frames when given a master time and a slave time and a method that calls this method 
        #TODO multiple times to calculate the rate of baseline change over time.
        for port in self.inputPorts:
            port()
            
        lookVector = self.calculateLookVector()
        
        az_offset = []
        vb = []
        hb = []
        csb = []
        asb = []
        s = [0]*3
        masterTime = [self.masterFrame.getSensingStart(),self.masterFrame.getSensingMid(),self.masterFrame.getSensingStop()]
        slaveTime = [self.slaveFrame.getSensingStart(),self.slaveFrame.getSensingMid(),self.slaveFrame.getSensingStop()]
        for i in range(3):
            # Calculate the Baseline at the start of the scene, mid-scene, and the end of the scene
            # First, get the position and velocity at the start of the scene
            self.logger.info("Sampling time %s" % i)
            masterBasis = self.calculateBasis(self.masterOrbit,masterTime[i])
            normV = self.calculateScalarVelocity(self.masterOrbit,masterTime[i])
            # Calculate the distance moved since the last baseline point
            if (i > 0):
                deltaT = self._timeDeltaToSeconds(masterTime[i] - masterTime[0])
                s[i] = s[i-1] + deltaT*normV
                       
                
            masterSV = self.masterOrbit.interpolateOrbit(masterTime[i])           

            slaveSV = self.slaveOrbit.interpolateOrbit(slaveTime[i])
            x1 = masterSV.getPosition()
            x2 = slaveSV.getPosition()
            (z_offset,v_offset,c_offset) = self.calculateBasisOffset(x1,x2,masterBasis)
            az_offset.append(z_offset) # Save the position offset
            # Calculate a new start time
            relativeSlaveTime = slaveTime[i] - datetime.timedelta(seconds=(z_offset/normV))
            slaveSV = self.slaveOrbit.interpolateOrbit(relativeSlaveTime)
            # Recalculate the offsets
            x2 = slaveSV.getPosition()
            (z_offset,v_offset,c_offset) = self.calculateBasisOffset(x1,x2,masterBasis)
            vb.append(v_offset)
            hb.append(c_offset)
            csb.append(-hb[i]*lookVector[0] + vb[i]*lookVector[1]) # Multiply the horizontal and vertical baseline components by the look angle vector
            asb.append(-hb[i]*lookVector[1] - vb[i]*lookVector[0])
        
        #Calculating baseline
        crossTrackBaselinePolynomialCoefficients = self.polynomialFit(s,hb)
        verticalBaselinePolynomialCoefficients = self.polynomialFit(s,vb)
        h_rate = crossTrackBaselinePolynomialCoefficients[1]
        # Calculate the gross azimuth and range offsets
        azb_avg = (az_offset[0] + az_offset[-1])/2.0
        asb_avg = (asb[0] + asb[-1])/2.0      
        az_offset = (-azb_avg - h_rate*self.startingRange1*lookVector[1])/(self.azimuthPixelSize)
        r_offset = (self.startingRange1 - self.startingRange2 - asb_avg)/(self.rangePixelSize)
        # Populate class attributes 
        self.hBaselineTop = crossTrackBaselinePolynomialCoefficients[0]
        self.hBaselineRate = crossTrackBaselinePolynomialCoefficients[1]
        self.hBaselineAcc = crossTrackBaselinePolynomialCoefficients[2]
        self.vBaselineTop = verticalBaselinePolynomialCoefficients[0]
        self.vBaselineRate = verticalBaselinePolynomialCoefficients[1]
        self.vBaselineAcc = verticalBaselinePolynomialCoefficients[2]
        self.pBaselineTop = csb[0]
        self.pBaselineBottom = csb[-1]
        self.orbSlcAzimuthOffset = az_offset
        self.orbSlcRangeOffset = r_offset
        self.rangeOffset = self.startingRange1 - self.startingRange2
        
            
    # Calculate a quadratic fit to the baseline polynomial
    def polynomialFit(self,xRef,yRef):
        size = len(xRef)
        if not (len(xRef) == len(yRef)):
            print("Error. Expecting input vectors of same length.")
            raise Exception
        if not (size == 3):
            print("Error. Expecting input vectors of length 3.")
            raise Exception
        Y = [0]*size
        A = [0]*size
        M = [[0 for i in range(size) ] for j in range(size)]
        for j in range(size):
            for i in range(size):
                M[j][i] = math.pow(xRef[j],i)
            Y[j] = yRef[j]
        MInv  = MM.invertMatrix(M)
        for i in range(size):
            for j in range(size):
                A[i] += MInv[i][j]*Y[j]

        return A

    def setRangePixelSize(self,pixelSize):
        self.rangePixelSize = pixelSize
        return

    def setAzimuthPixelSize(self,pixelSize):
        self.azimuthPixelSize = pixelSize
        return
    
    def setHeight(self,var):
        self.height = float(var)
        return

    def setRadius(self,radius):
        self.radius = radius
        return

    def setMasterStartingRange(self,range):
        self.startingRange1 = range
        return

    def setSlaveStartingRange(self,range):
        self.startingRange2 = range
        return
    
    def getHBaselineTop(self):
        return self.hBaselineTop

    def getHBaselineRate(self):
        return self.hBaselineRate

    def getHBaselineAcc(self):
        return self.hBaselineAcc

    def getVBaselineTop(self):
        return self.vBaselineTop

    def getVBaselineRate(self):
        return self.vBaselineRate

    def getVBaselineAcc(self):
        return self.vBaselineAcc

    def getPBaselineTop(self):
        return self.pBaselineTop

    def getPBaselineBottom(self):
        return self.pBaselineBottom

    def getOrbSlcAzimuthOffset(self):
        return self.orbSlcAzimuthOffset

    def getOrbSlcRangeOffset(self):
        return self.orbSlcRangeOffset

    def getRangeOffset(self):
        return self.rangeOffset

    def getPhaseConst(self):
        return self.phaseConst
    
    def getLookAngle(self):
        return self.lookAngle

    def _timeDeltaToSeconds(self,td):
        return (td.microseconds + (td.seconds + td.days * 24.0 * 3600) * 10**6) / 10**6 
            
        
    def addMasterFrame(self):
        frame = self._inputPorts.getPort(name='masterFrame').getObject()
        self.masterFrame = frame                      
        self.startingRange1 = frame.getStartingRange()

        prf = frame.getInstrument().getPulseRepetitionFrequency()
        self.rangePixelSize = frame.getInstrument().getRangePixelSize()
        self.masterOrbit = frame.getOrbit()
        midSV = self.masterOrbit.interpolateOrbit(frame.getSensingMid())

        self.azimuthPixelSize = prf * midSV.getScalarVelocity()
        ellipsoid = frame.getInstrument().getPlatform().getPlanet().get_elp()
        self.radius = ellipsoid.get_a()
        
        self.height = midSV.calculateHeight(ellipsoid)

    def addSlaveFrame(self):
        frame = self._inputPorts.getPort(name='slaveFrame').getObject()
        self.slaveFrame = frame              
        self.startingRange2 = frame.getStartingRange()
        self.slaveOrbit = frame.getOrbit()
        
    def __init__(self):
        Component.__init__(self)
        self.masterOrbit = None
        self.slaveOrbit = None
        self.masterFrame = None
        self.slaveFrame = None
        self.lookAngle = None        
        self.rangePixelSize = None
        self.azimuthPixelSize = None
        self.height = None
        self.radius = None
        self.startingRange1 = None
        self.startingRange2 = None
        self.hBaselineTop = None
        self.hBaselineRate = None
        self.hBaselineAcc = None
        self.vBaselineTop = None
        self.vBaselineRate = None
        self.vBaselineAcc = None
        self.pBaselineTop = None
        self.pBaselineBottom = None
        self.orbSlcAzimuthOffset = None
        self.orbSlcRangeOffset = None
        self.rangeOffset = None
        self.phaseConst = -99999
        self.logger = logging.getLogger('isce.mroipac.baseline')
        self.createPorts()
        
        # Satisfy the old Component
        self.dictionaryOfOutputVariables = {}        
        self.dictionaryOfVariables = {}        
        self.descriptionOfVariables = {}
        self.mandatoryVariables = []
        self.optionalVariables = []
        return None

    def createPorts(self):
        
        # Set input ports
        # It looks like we really need two orbits, a time, range and azimuth pixel sizes
        # the two starting ranges, a planet, and the two prfs
        # These provide the orbits
        # These provide the range and azimuth pixel sizes, starting ranges, 
        # satellite heights and times for the first lines
        masterFramePort = Port(name='masterFrame',method=self.addMasterFrame)  
        slaveFramePort = Port(name='slaveFrame',method=self.addSlaveFrame)       
        self._inputPorts.add(masterFramePort)
        self._inputPorts.add(slaveFramePort)
        return None

        
    def __str__(self):
        retstr = "Initial Baseline estimates \n"
        retstr += "Cross-track Baseline: %s\n"
        retlst = (self.hBaselineTop,)
        retstr += "Vertical Baseline: %s\n"
        retlst += (self.vBaselineTop,)
        retstr += "Perpendicular Baseline: %s\n"
        retlst += (self.pBaselineTop,)
        retstr += "Bulk Azimuth Offset: %s\n"
        retlst += (self.orbSlcAzimuthOffset,)
        retstr += "Bulk Range Offset: %s\n"
        retlst += (self.orbSlcRangeOffset,)
        return retstr % retlst      
