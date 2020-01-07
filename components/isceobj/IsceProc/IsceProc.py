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
# Author: Kosal Khun
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# Comment: Adapted from InsarProc/InsarProc.py
from __future__ import print_function
import os
import sys
import logging
import logging.config
from iscesys.Component.Component import Component
from iscesys.DateTimeUtil.DateTimeUtil import DateTimeUtil as DTU
from iscesys.Compatibility import Compatibility
from isceobj.Scene.Frame import FrameMixin


class IsceProc(Component, FrameMixin):

    def __init__(self, procDoc=None):
        """
        Initiate all the attributes that will be used
        """
        self.procDoc = procDoc
        self.workingDirectory = os.getcwd()
        self.dataDirectory = None
        self.processingDirectory = None

        self.selectedScenes = [] # ids of selected scenes, ordered by scene number
        self.selectedPols = [] # hh, hv, vh, vv
        self.selectedPairs = [] # list of tuples (p1, p2) selected for inSAR
        self.srcFiles = {} # path and info about provider's data (for each scene and each pol)
        self.frames = {}
        self.dopplers = {}
        self.orbits = {}
        self.shifts = {} # azimuth shifts
        self.peg = None
        self.pegAverageHeights = {}
        self.pegProcVelocities = {}
        self.fdHeights = {}
        self.is_mocomp = None
        self.rawImages = {}
        self.slcImages = {}
        self.formSLCs = {}
        self.squints = {}
        self.offsetAzimuthImages = {}
        self.offsetRangeImages = {}
        self.resampAmpImages = {}
        self.resampIntImages = {}
        self.resampOnlyImages = {}
        self.resampOnlyAmps = {}
        self.topoIntImages = {}
        self.heightTopoImage = None #KK 2014-01-20
        self.rgImageName = 'rgImage'
        self.rgImage = None
        self.simAmpImageName = 'simamp.rdr'
        self.simAmpImages = None #KK 2014-01-20
        self.resampImageName = 'resampImage'
        self.resampOnlyImageName = 'resampOnlyImage.int'
        self.offsetImageName = 'Offset.mht'
        self.demImage = None
        self.demInitFile = 'DemImage.xml'
        self.firstSampleAcrossPrf = 50
        self.firstSampleDownPrf = 50
        self.numberLocationAcrossPrf = 40
        self.numberLocationDownPrf = 50
        self.numberRangeBins = None
        self.firstSampleAcross = 50
        self.firstSampleDown = 50
        self.numberLocationAcross = 40
        self.numberLocationDown = 40
        self.topocorrectFlatImage = None
        self.offsetFields = {}
        self.refinedOffsetFields = {}
        self.offsetField1 = None
        self.refinedOffsetField1 = None
        self.topophaseIterations = 25
        self.coherenceFilename = 'topophase.cor'
        self.unwrappedIntFilename = 'filt_topophase.unw'
        self.phsigFilename = 'phsig.cor'
        self.topophaseMphFilename = 'topophase.mph'
        self.topophaseFlatFilename = 'topophase.flat'
        self.filt_topophaseFlatFilename = 'filt_' + self.topophaseFlatFilename
        self.heightFilename = 'z.rdr' #real height file
        self.heightSchFilename = 'zsch.rdr' #sch height file
        self.latFilename = 'lat.rdr' #KK 2013-12-12: latitude file
        self.lonFilename = 'lon.rdr' #KK 2013-12-12: longitude file
        self.losFilename = 'los.rdr' #KK 2013-12-12: los file
        self.geocodeFilename = 'topophase.geo'
        self.demCropFilename = 'dem.crop'
        # The strength of the Goldstein-Werner filter
        self.filterStrength = 0.7
        # This is hard-coded from the original script
        self.numberValidPulses = 2048
        self.numberPatches = None
        self.patchSize = 8192
        self.machineEndianness = 'l'
        self.secondaryRangeMigrationFlag = None
        self.chirpExtension = 0
        self.slantRangePixelSpacing = None
        self.dopplerCentroid = None
        self.posting = 15
        self.numberFitCoefficients = 6
        self.numberLooks = 4
        self.numberAzimuthLooks = 1
        self.numberRangeLooks = None
        self.numberResampLines = None
        self.shadeFactor = 3
        self.checkPointer =  None
        self.mocompBaselines = {}
        self.topocorrect = None
        self.topo = None #KK 2014-01-20
        self.lookSide = -1 #right looking by default
        self.geocode_list = [
                        self.coherenceFilename,
                        self.unwrappedIntFilename,
                        self.phsigFilename,
                        self.losFilename,
                        self.topophaseFlatFilename, 
                        self.filt_topophaseFlatFilename, 
                        self.resampOnlyImageName.replace('.int', '.amp')
                       ] 

        # Polarimetric calibration
        self.focusers = {}
        self.frOutputName = 'fr'
        self.tecOutputName = 'tec'
        self.phaseOutputName = 'phase'


    def __setstate__(self, state):
        """
        Restore state from the unpickled state values.
        see: http://www.developertutorials.com/tutorials/python/python-persistence-management-050405-1306/
        """
        # When unpickling, we need to update the values from state
        # because all the attributes in __init__ don't exist at this step.
        self.__dict__.update(state)


    def formatname(self, sceneid, pol=None, ext=None):
        """
        Return a string that identifies uniquely a scene from its id and pol.
        ext can be given if we want a filename.
        If sceneid is a tuple: format a string to identy uniquely a pair.
        """
        if isinstance(sceneid, tuple):
            name = '__'.join(sceneid)
        else:
            name = sceneid
        if pol:
            name += '_' + pol
        if ext:
            name += '.' + ext
        return name


    ## This overides the _FrameMixin.frame
    @property
    def frame(self):
        """
        Get the reference frame in self.frames and
        return reference pol in frame.
        This is needed to get information about a frame,
        supposing that all frames have the same information.
        """
        return self.frames[self.refScene][self.refPol]


    def getAllFromPol(self, pol, obj):
        """
        Get all values from obj, where polarization is pol.
        obj should be a dictionary with the following structure:
        { sceneid: { pol1: v1, pol2: v2 }, sceneid2: {...} }
        """
        objlist = []
        if pol not in self.selectedPols:
            return objlist

        if isinstance(obj, str):
            try:
                obj = getattr(self, obj)
            except AttributeError:
                sys.exit("%s is not an attribute of IsceProc." % obj)
        for sceneid in self.selectedScenes:
            try:
                objlist.append(obj[sceneid][pol])
            except:
                sys.exit("%s is not a readable dictionary" % obj)
        return objlist


    def average(self, objdict):
        """
        Average values in a dict of dict: { k1: { k2: ... } }
        """
        N = 0 ##number of values
        s = 0 ##sum
        vals = objdict.values()
        for val in vals:
            ###val is a dictionary
            N += len(val)
            s += sum(val.values())
        return s / float(N)

    def get_is_mocomp(self):
        self.is_mocomp = int( (self.patchSize - self.numberValidPulses) / 2 )

    @property
    def averageHeight(self):
        return self.average(self.pegAverageHeights)

    @property
    def procVelocity(self):
        return self.average(self.pegProcVelocities)

    # <v>, <h>
    def vh(self):
        return self.procVelocity, self.averageHeight

    @property
    def chirpExtensionPercentage(self):
        return NotImplemented
    @chirpExtensionPercentage.setter
    def chirpExtensionPercentage(self, value):
        raise AttributeError("Can only set chirpExtension")

    ## folowing are tbd to split formSLC.
    def _hasher(self, attr, sid, pol=None):
        obj = getattr(self, attr)[sid]
        if pol:
            obj = obj[pol]
        return obj

    def select_frame(self, sid, pol=None): return self._hasher('frames', sid, pol)
    def select_orbit(self, sid, pol=None): return self._hasher('orbits', sid, pol)
    def select_doppler(self, sid, pol=None): return self._hasher('dopplers', sid, pol)
    def select_rawimage(self, sid, pol=None): return self._hasher('rawImages', sid, pol)
    def select_slcimage(self, sid, pol=None): return self._hasher('slcImages', sid, pol)
    def select_squint(self, sid, pol=None): return self._hasher('squints', sid, pol)

    def select_swath(self, sid, pol=None):
        return RadarSwath(frame=self.select_frame(sid, pol),
                          orbit=self.select_orbit(sid, pol),
                          doppler=self.select_doppler(sid, pol),
                          rawimage=self.select_rawimage(sid, pol),
                          slcimage=self.select_slcimage(sid, pol),
                          squint=self.select_squint(sid, pol))



## Why this: the code bloat with master this and slave that indicates the
## design princple does not use composition, this is an attempt to
## fix that
class RadarSwath(object):
    def __init__(self,
                 frame=None,
                 orbit=None,
                 doppler=None,
                 rawimage=None,
                 slcimage=None,
                 squint=None):
        self.frame = frame
        self.orbit = orbit
        self.doppler = doppler
        self.rawimage = rawimage
        self.slcimage = slcimage
        self.squint = squint


