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
# Author: Walter Szeliga
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




from iscesys.Component.Component import Component
from . import snaphu

class Snaphu(Component):
    """The Snaphu cost unwrapper"""
    
    def __init__(self):
        Component.__init__(self)
        self.width = None
        self.wavelength = None
        self.altitude = None
        self.costMode = 0
        self.earthRadius = 0
        self.input = None
        self.output = None
        self.corrfile = None
        self.corrLooks = None
        self.defoMaxCycles = 1.2
        self.initMethod = 1
        self.initOnly = False
        self.maxComponents = 32
        self.rangeLooks = 1
        self.azimuthLooks = 1
        self.dumpConnectedComponents = True
        self.minConnectedComponentFrac = 0.01
        self.connectedComponentCostThreshold = 300
        self.magnitude = None 
        
        self.descriptionOfVariables = {}
        self.dictionaryOfVariables = {'INPUT': ['self.input','str','mandatory'],
                                      'OUTPUT': ['self.output','str','mandatory'],
                                      'WAVELENGTH': ['self.wavelength','float','mandatory'],
                                      'ALTITUDE': ['self.altitude','float','mandatory'],
                                      'COSTMODE': ['self.costMode','str','mandatory'],
                                      'EARTHRADIUS': ['self.earthRadius','float','mandatory'],
                                      'WIDTH': ['self.width','float','mandatory'],
                                      'CORRELATION': ['self.correlation','str', 'optional']}

    def setCorrfile(self, corrfile):
        """Set the correlation filename for unwrapping"""
        self.corrfile = corrfile

    def setDefoMaxCycles(self, ncycles):
        """Set the maximum phase discontinuity expected."""
        self.defoMaxCycles = ncycles

    def setCorrLooks(self, looks):
        """Set the number of looks used for computing correlation"""
        self.corrLooks = looks

    def setInput(self,input):
        """Set the input filename for unwrapping"""
        self.input = input
        
    def setOutput(self,output):
        """Set the output filename for unwrapping"""
        self.output = output
        
    def setWidth(self,width):
        """Set the image width"""
        self.width = width
        
    def setWavelength(self,wavelength):
        """Set the radar wavelength"""
        self.wavelength = wavelength

    def setRangeLooks(self, looks):
        self.rangeLooks = looks

    def setAzimuthLooks(self, looks):
        self.azimuthLooks = looks
        
    def setCostMode(self,costMode):
        """Set the mode for cost calculation"""
        if (costMode == 'TOPO'):
            self.costMode = 1
        elif (costMode == 'DEFO'):
            self.costMode = 2
        elif (costMode == 'SMOOTH'):
            self.costMode = 3
        else:
            self.costMode = 0

    def setInitOnly(self, logic):
        self.initOnly = logic

    def dumpConnectedComponents(self, logic):
        self.dumpConnectedComponents = logic
        
    def setAltitude(self,altitude):
        """Set the satellite altitude"""
        self.altitude = altitude
        
    def setEarthRadius(self,earthRadius):
        """Set the local Earth radius"""
        self.earthRadius = earthRadius

    def setInitMethod(self, method):
        """Set the initialization method."""
        if (method == 'MST'):
            self.initMethod = 1
        elif (method == 'MCF'):
            self.initMethod = 2
        else:
            self.initMethod = 0

    def setMaxComponents(self, num):
        """Set the maximum number of connected components."""
        self.maxComponents = num
    
    def prepare(self):
        """Perform some initialization of defaults"""
        snaphu.setDefaults_Py()
        snaphu.setInitOnly_Py(int(self.initOnly))
        snaphu.setInput_Py(self.input)
        snaphu.setOutput_Py(self.output)
        if self.magnitude is not None:
            snaphu.setMagnitude_Py(self.magnitude)
        snaphu.setWavelength_Py(self.wavelength)
        snaphu.setCostMode_Py(self.costMode)
        snaphu.setAltitude_Py(self.altitude)
        snaphu.setEarthRadius_Py(self.earthRadius)       
        if self.corrfile is not None:
            snaphu.setCorrfile_Py(self.corrfile)

        if self.corrLooks is not None:
            snaphu.setCorrLooks_Py(self.corrLooks)

        if self.defoMaxCycles is not None:
            snaphu.setDefoMaxCycles_Py(self.defoMaxCycles)

        snaphu.setInitMethod_Py(self.initMethod)
        snaphu.setMaxComponents_Py(self.maxComponents)
        snaphu.setRangeLooks_Py(int(self.rangeLooks))
        snaphu.setAzimuthLooks_Py(int(self.azimuthLooks))
        snaphu.setMinConnectedComponentFraction_Py(int(self.minConnectedComponentFrac))
        snaphu.setConnectedComponentThreshold_Py(int(self.connectedComponentCostThreshold))


    def unwrap(self):
        """Unwrap the interferogram"""       

        ###Connected components can be dumped out in non-initonly mode
        if not self.initOnly and self.dumpConnectedComponents:
            snaphu.setConnectedComponents_Py(self.output+'.conncomp')
#            snaphu.setRegrowComponents_Py(int(True))

        snaphu.snaphu_Py(self.width)
        self._unwrappingCompleted = True

        ##Second pass if initOnly mode was used.
        if self.initOnly and self.dumpConnectedComponents:
            self.growConnectedComponentsOnly()

    def growConnectedComponentsOnly(self,infile=None,outfile=None):
        '''
        Grows the connected components using an unwrapped file.
        '''
        print('Growing connected components on second pass')
        if infile is None:
            inputFile = self.output
        else:
            inputFile = infile

        if outfile is None:
            outputFile = inputFile + '.conncomp'
        else:
            outputFile = outfile

        self.prepare()
        snaphu.setInitOnly_Py(int(False))
        snaphu.setInput_Py(inputFile)
        snaphu.setConnectedComponents_Py(outputFile)
        snaphu.setRegrowComponents_Py(int(True))
        snaphu.setUnwrappedInput_Py(int(True))
        snaphu.snaphu_Py(self.width)
          
