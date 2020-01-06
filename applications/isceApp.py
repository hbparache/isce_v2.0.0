#!/usr/bin/env python3

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



# Comment: Adapted from applications/insarApp.py
from __future__ import print_function
import pdb
import time
import datetime
import os
import sys
import math
import logging
import logging.config

import isce
import isceobj
import iscesys
from iscesys.Compatibility import Compatibility
from iscesys.StdOEL.StdOELPy import create_writer
from isceobj import IsceProc

import isceobj.IsceProc as IsceProc
from isceobj.Location.Peg import Peg
from isceobj import Unwrap
from isceobj.Sensor import SENSORS
from contrib.demUtils.Correct_geoid_i2_srtm import Correct_geoid_i2_srtm

from isceobj.IsceProc.INPUT import *

from pprint import pprint

logger = None ##will be instantiated later

POLS = ['hh', 'hv', 'vh', 'vv'] ##accepted polarizations


class IsceApp(Application):
    """
    This class represents the application that reads the input xml file and runs the various processing steps accordingly.
    """

    family = "isce" #ML 2014-03-25

    ## Define Class parameters in this list
    parameter_list = (SENSOR_NAME,
                      PEG_LAT,
                      PEG_LON,
                      PEG_HDG,
                      PEG_RAD,
                      DOPPLER_METHOD,
                      USE_DOP,
                      USE_HIGH_RESOLUTION_DEM_ONLY,
                      DEM_FILENAME,
                      GEO_POSTING,
                      POSTING,
                      PATCH_SIZE,
                      GOOD_LINES,
                      NUM_PATCHES,
                      AZ_SHIFT,
                      SLC_RGLOOKS,
                      SLC_AZLOOKS,
                      SLC_FILTERMETHOD,
                      SLC_FILTERHEIGHT,
                      SLC_FILTERWIDTH,
                      OFFSET_METHOD,
                      COREG_STRATEGY,
                      REF_SCENE,
                      REF_POL,
                      OFFSET_SEARCH_WINDOW_SIZE,
                      GROSS_AZ,
                      GROSS_RG,
                      CULLING_SEQUENCE,
                      NUM_FIT_COEFF,
                      RESAMP_RGLOOKS,
                      RESAMP_AZLOOKS,
                      FR_FILTER,
                      FR_FILTERSIZE_X,
                      FR_FILTERSIZE_Y,
                      CORRELATION_METHOD,
                      FILTER_STRENGTH, #KK 2013-12-12
                      UNWRAPPER_NAME,
                      GEOCODE_LIST, #KK 2013-12-12
                      GEOCODE_BOX, #KK 2013-12-12
                      PICKLE_DUMPER_DIR,
                      PICKLE_LOAD_DIR,
                      OUTPUT_DIR,
                      SELECTED_SCENES,
                      SELECTED_PAIRS,
                      SELECTED_POLS,
                      DO_PREPROCESS,
                      DO_VERIFY_DEM,
                      DO_PULSETIMING,
                      DO_ESTIMATE_HEIGHTS,
                      DO_SET_MOCOMPPATH,
                      DO_ORBIT2SCH,
                      DO_UPDATE_PREPROCINFO,
                      DO_FORM_SLC,
                      DO_MULTILOOK_SLC,
                      DO_FILTER_SLC,
                      DO_GEOCODE_SLC,
                      DO_OFFSETPRF,
                      DO_OUTLIERS1,
                      DO_PREPARE_RESAMPS,
                      DO_RESAMP,
                      DO_RESAMP_IMAGE,
                      DO_POL_CORRECTION,
                      DO_POL_FR,
                      DO_POL_TEC,
                      DO_POL_PHASE,
                      DO_CROSSMUL, #2013-11-26
                      DO_MOCOMP_BASELINE,
                      DO_SET_TOPOINT1,
                      DO_TOPO,
                      DO_SHADE_CPX2RG,
                      DO_RG_OFFSET,
                      DO_RG_OUTLIERS2,
                      DO_RESAMP_ONLY,
                      DO_SET_TOPOINT2,
                      DO_CORRECT,
                      DO_COHERENCE,
                      DO_FILTER_INF,
                      DO_UNWRAP,
                      DO_GEOCODE_INF)

    facility_list = (STACK,
                     DEM,
                     RUN_FORM_SLC,
                     RUN_OFFSETPRF,
                     RUN_UNWRAPPER)

    _pickleObj = "_isce"


    # KK 2013-12-19
    def Usage(self):
        print("Usage: isceApp.py <input-file.xml> [options]")
        print("Options:")
        print("None\t\tRun isceApp.py from start to end without pickling")
        print("--help\t\tDisplay configurable parameters and facilities that can be specified in <input-file.xml>")
        print("--help --steps\tDisplay list of available steps according to <input-file.xml>")
        print("--steps\t\tRun isceApp.py from start to end and pickle at each step")
    # KK


    def __init__(self, family='',name='',cmdline=None):
        """
        Initialize the application: read the xml file and prepare the application.
        """
        super().__init__(family=family if family else  self.__class__.family, name=name,cmdline=cmdline)
        now = datetime.datetime.now()
        ##add timestamp to isceProc.xml file, so that they don't overwrite themselves
        self._isce = IsceProc.IsceProc(procDoc=isceobj.createCatalog('isceProc_%s' % now.strftime('%Y%m%d%H%M%S')))
        self._isce.procDoc._addItem("ISCE_VERSION",
                              "Release: %s, svn-%s, %s. Current svn-%s" %
                              (isce.release_version, isce.release_svn_revision,
                               isce.release_date, isce.svn_revision
                               ),
                              ["isceProc"]
                              )
        self._stdWriter = create_writer("log", "", True, filename="isce.log")
        self._add_methods()
        self.pairsToCoreg = [] ##pairs to coregister
        self.intromsg = '' ##intro message
        self.peg = None


    def _init(self):
        message =  (
            ("ISCE VERSION = %s, RELEASE_SVN_REVISION = %s,"+
             "RELEASE_DATE = %s, CURRENT_SVN_REVISION = %s") %
            (isce.__version__,
             isce.release_svn_revision,
             isce.release_date,
             isce.svn_revision)
            )
        self.intromsg = message

        print(message)
        if ( self.pegLat is not None
             and self.pegLon is not None
             and self.pegHdg is not None
             and self.pegRad is not None ):
             self.peg = Peg(latitude=self.pegLat,
                            longitude=self.pegLon,
                            heading=self.pegHdg,
                            radiusOfCurvature=self.pegRad)
        #for attribute in ["sensorName", "correlation_method", "use_dop", "geoPosting", "posting", "resampRgLooks", "resampAzLooks", "offsetMethod", "peg"]:
        #    print("%s = %s" % (attribute, getattr(self, attribute)))


    def _configure(self):
        #This is a temporary fix to get the user interface back to the dem
        #facility interface while changes are being made in the DemImage class
        #to include within it the capabilities urrently in extractInfo and
        #createDem.
        if self.demFilename:
            errmsg = "The demFilename property is no longer supported as an input parameter.\n"
            errmsg += "The original method using a configurable facility for the Dem is now restored.\n"
            errmsg += "The automatic download feature is still supported in the same way as before:\n"
            errmsg += "If you want automatic download of a Dem, then simply omit any configuration\ninformation in your input file regarding the Dem.\n\n"
            errmsg += "Please replace the following information in your input file:\n"
            errmsg += "<property name='demFilename'><value>%s</value></property>\n" % self.demFilename
            errmsg += "with the following information and try again:\n"
            errmsg += "<component name=\'Dem\'><catalog>%s</catalog></component>\n" % self.demFilename
            sys.exit(errmsg)
        else:
            try:
                self.dem.checkInitialization()
                # Give self.demFilename a value so that the SRTM Dem will not
                # be downloaded
                # Temporary fix that will be removed when the download option
                # is handled within demImage
                self.demFilename = "demFilename"
            except Exception as err:
                print("The Dem specified was not properly initialized. An SRTM Dem will be downloaded.")
                #self.dem was not properly initialized
                #and self.demFilename is undefined.
                #There is a check on self.demFilename
                #below to download if necessary
            # KK 2013-12-12
            else:
                dem_snwe = self.dem.getsnwe()

                if self.geocode_bbox:
                    ####Adjust bbox according to dem
                    if self.geocode_bbox[0] < dem_snwe[0]:
                        logger.warn('Geocoding southern extent changed to match DEM')
                        self.geocode_bbox[0] = dem_snwe[0]

                    if self.geocode_bbox[1] > dem_snwe[1]:
                        logger.warn('Geocoding northern extent changed to match DEM')
                        self.geocode_bbox[1] = dem_snwe[1]

                    if self.geocode_bbox[2] < dem_snwe[2]:
                        logger.warn('Geocoding western extent changed to match DEM')
                        self.geocode_bbox[2] = dem_snwe[2]

                    if self.geocode_bbox[3] > dem_snwe[3]:
                        logger.warn('Geocoding eastern extent changed to match DEM')
                        self.geocode_bbox[3] = dem_snwe[3]

        #if not provided by the user use the default from IsceProc
        if self.geocode_list is None:
            self.geocode_list = self._isce.geocode_list
        # KK


    def _facilities(self):
        """
        Define the user configurable facilities for this application.
        """
        self.stack = self.facility(
            'stack',
            public_name='Stack',
            module='isceobj.Stack',
            factory='createStack',
            mandatory=True,
            doc="Stack component with a list of scenes (src format)."
            )
        self.dem = self.facility(
            'dem',
            public_name='Dem',
            module='isceobj.Image',
            factory='createDemImage',
            mandatory=False,
            doc=(
                "Dem Image configurable component.  Do not include this "+
                "in the input file and an SRTM Dem will be downloaded for you."
                )
            )
        self.demStitcher = self.facility(
            'demStitcher',
            public_name='demStitcher',
            module='contrib.demUtils',
            factory='createDemStitcher',
            args=('iscestitcher',),
            mandatory=False,
            doc=(
                "Object that based on the frame bounding boxes creates a DEM"
                )
            )
        self.runFormSLC  = self.facility(
            'runFormSLC',
            public_name='Form SLC',
            module='isceobj.IsceProc',
            factory='createFormSLC',
            args=(self, self.do_formslc, self.sensorName,),
            mandatory=False,
            doc="SLC formation module"
        )
        self.runOffsetprf  = self.facility(
            'runOffsetprf',
            public_name='slc offsetter',
            module='isceobj.IsceProc',
            factory='createOffsetprf',
            args=(self, self.do_offsetprf, self.offsetMethod,),
            mandatory=False,
            doc="SLC offset estimator."
        )
        self.runRgoffset = self.facility(
                'runRgoffset',
                public_name='dem offseter',
                module = 'isceobj.IsceProc',
                factory= 'createRgoffset',
                args=(self, self.offsetMethod),
                mandatory=False,
                doc="Dem offset estimator."
        )
        self.runUnwrapper = self.facility(
            'runUnwrapper',
            public_name='Run Unwrapper',
            module='isceobj.Unwrap',
            factory='createUnwrapper',
            args=(self.do_unwrap, self.unwrapper_name,),
            mandatory=False,
            doc="Unwrapping module"
        )
        return None

    @property
    def isce(self):
        return self._isce
    @isce.setter
    def isce(self, value):
        self._isce = value


    def _finalize(self):
        pass


    def help(self):
        print(self.__doc__)
        lsensors = list(SENSORS.keys())
        lsensors.sort()
        print("The currently supported sensors are: ", lsensors)


    # KK 2013-12-12
    def help_steps(self):
        print(self.__doc__)
        print("A description of the individual steps can be found in the README file")
        print("and also in the ISCE.pdf document")
    # KK


    def formatAttributes(self):
        self.sensorName = self.sensorName.upper()
        if not self.dopplerMethod.startswith('use'):
            self.dopplerMethod = 'use' + self.dopplerMethod
        ##selected Scenes
        sels = map(str.strip, self.selectedScenes.split(','))
        self.selectedScenes = [ s for s in sels if s ] ##might be empty
        ##selected pols
        sels = map(str.strip, self.selectedPols.split(','))
        self.selectedPols = [ s.lower() for s in sels if s ] ##might be empty
        ##selected pairs
        sels = map(str.strip, self.selectedPairs.split(','))
        self.selectedPairs = [ s for s in sels if s ]


    def prepareStack(self):
        """
        Populate stack with user data and prepare to run.
        """
        ##Get all scenes as given in xml file
        sceneids = []
        allscenes = []
        scenekeys = []
        for i in range(100):
            try:
                scene = getattr(self.stack, 'scene'+str(i))
            except AttributeError:
                pass
            else:
                if scene:
                    sceneids.append(scene['id'])
                    allscenes.append(scene)
                    scenekeys.extend(scene.keys())
        unique_scenekeys = set(scenekeys)

        sels = []
        for scene in self.selectedScenes:
            pairs = scene.split('-')
            if len(pairs) == 1:
                sid = pairs[0]
                try:
                    idx = sceneids.index(sid)
                except ValueError:
                    sys.exit("Scene id '%s' is not in list of scenes." % sid)
                else:
                    sels.append(sid)
            elif len(pairs) == 2:
                sid1 = pairs[0].strip()
                sid2 = pairs[1].strip()
                try:
                    idx1 = sceneids.index(sid1)
                    idx2 = sceneids.index(sid2)
                except ValueError as e:
                    print(e)
                    print(sceneids)
                    sys.exit(1)
                else:
                    first = min(idx1, idx2)
                    last = max(idx1, idx2)
                    for i in range(first, last+1):
                        sels.append(sceneids[i])
            else:
                sys.exit("Unknow value '%s' in selected scenes." % scene)

        # make sure that we have unique selected scenes ordered by their scene number
        self.selectedScenes = [ s for s in sceneids if s in sels ]
        if not self.selectedScenes: ##no scenes selected: process all scenes
            self.selectedScenes = sceneids
        for sceneid in self.selectedScenes:
            idx = sceneids.index(sceneid)
            scene = allscenes[idx]
            self.stack.addscene(scene)
            outdir = self.getoutputdir(sceneid)
            if not os.path.exists(outdir):
                os.mkdir(outdir)

        sels = []
        if not self.selectedPols: ##empty pols
            self.selectedPols = list(POLS) ##select all pols
        for pol in self.selectedPols:
            if pol in POLS:
                if pol in unique_scenekeys: ##the selected pols might not be in the givenkeys
                    sels.append(pol)
            else:
                sys.exit("Polarization '%s' is not in accepted list." % pol)
        if not sels:
            sys.exit("Make sure that all scenes have at least one accepted polarization: %s" % ', '.join(POLS))

        # make sure that we have unique selected pols in the same order as in POLS
        self.selectedPols = [ p for p in POLS if p in sels ]

        selPairs = []
        for pair in self.selectedPairs:
            try:
                scene1, scene2 = map(str.strip, pair.split('/')) # assume that it's a pair scene1/scene2
                if scene1 in self.selectedScenes and scene2 in self.selectedScenes:
                    selPairs.append( (scene1, scene2) )
            except ValueError: # not p1/p2
                try:
                    sid1, sid2 = map(str.strip, pair.split('-')) # assume that it's a range first-last
                    idx1 = sceneids.index(sid1)
                    idx2 = sceneids.index(sid2)
                    first = min(idx1, idx2)
                    last = max(idx1, idx2)
                    for i in range(first, last):
                        for j in range(i + 1, last + 1): #KK 2013-12-17
                            selPairs.append( (sceneids[i], sceneids[j]) )
                except ValueError: # unknown format
                    sys.exit("Unknow format in <selectPairs>: %s" % pair)
        self.selectedPairs = list(set(selPairs)) # keep unique values but pairs like (scene1, scene2) and (scene2, scene1) are considered different
        # they will be processed as different pairs for now ; we might need to check that and remove one of the pairs (to be done)

        if not self.selectedPairs: ##empty value
            self.selectedPairs = []
            nbscenes = len(self.selectedScenes)
            for i in range(nbscenes):
                for j in range(i+1, nbscenes):
                    self.selectedPairs.append((self.selectedScenes[i], self.selectedScenes[j]))

        if self.refPol not in self.selectedPols:
            self.refPol = self.selectedPols[0] # get first selected polarization
        if self.refScene not in self.selectedScenes:
            self.refScene = self.selectedScenes[0] # get first selected scene

        if self.do_offsetprf:
            scenesInPairs = [] ##list of scenes that compose selected pairs
            for pair in self.selectedPairs:
                scenesInPairs.extend(pair) ##add scene1 and scene2 to list
            scenesInPairs = list(set(scenesInPairs)) ##keep unique values
            orderedScenesInPairs = [ s for s in self.selectedScenes if s in scenesInPairs ] ##order scenes by their scene number

            if self.coregStrategy == 'single reference':
                for scene in orderedScenesInPairs:
                    self.pairsToCoreg.append( (self.refScene, scene) )
                if (self.refScene, self.refScene) in self.pairsToCoreg:
                    self.pairsToCoreg.remove( (self.refScene, self.refScene) )
            elif self.coregStrategy == 'cascade':
                for i in range(len(orderedScenesInPairs)-1):
                    self.pairsToCoreg.append( (orderedScenesInPairs[i], orderedScenesInPairs[i+1]) )
            else:
                sys.exit("Unknown coregistration strategy '%s' in runOffsetprf" % self.coregStrategy)

            # creating output directories according to selectedPairs and pairsToCoreg
            outputPairs = list(self.pairsToCoreg) #copy pairsToCoreg
            for (p1, p2) in self.selectedPairs:
                if (p1, p2) not in self.pairsToCoreg: #(p2, p1) might be already in pairsToCoreg but we consider them as different pairs
                    outputPairs.append((p1, p2))
            for (p1, p2) in outputPairs:
                outdir = self.getoutputdir(p1, p2)
                if not os.path.exists(outdir):
                    os.mkdir(outdir)

        self._isce.selectedPols = self.selectedPols
        self._isce.selectedScenes = self.selectedScenes
        self._isce.selectedPairs = self.selectedPairs
        self._isce.coregStrategy = self.coregStrategy
        self._isce.refScene = self.refScene
        self._isce.refPol = self.refPol
        self._isce.pairsToCoreg = self.pairsToCoreg
        self._isce.srcFiles = self.stack.getscenes()

    def getoutputdir(self, sid1, sid2=''):
        """
        Return output directory for scene sid1.
        If sid2 is given, return output directory for pair sid1__sid2.
        """
        if sid2:
            outdir = '%s__%s' % (sid1, sid2)
        else:
            outdir = sid1
        return os.path.join(self.outputDir, outdir)


    def verifyOutput(self):
        """
        Check that output directory exists and instantiate logger.
        """
        global logger
        if not os.path.isdir(self.outputDir):
            sys.exit("Could not find the output directory: %s" % self.outputDir)
        os.chdir(self.outputDir) ##change working directory to given output directory
        ##read configfile only here so that log path is in output directory
        logging.config.fileConfig(
            os.path.join(os.environ['ISCE_HOME'], 'defaults', 'logging',
                'logging.conf')
        )
        logger = logging.getLogger('isce.isceProc')
        logger.info(self.intromsg)
        self._isce.dataDirectory = self.outputDir
        self._isce.processingDirectory = self.outputDir


    def verifyDEM(self):
        #if an image has been specified, then no need to create one
        if not self.dem.filename:
            #the following lines should be included in the check on demFilename
            frames = self._isce.getAllFromPol(self._isce.refPol, self._isce.frames)
            bbox = self.extractInfo(frames)
            self.createDem(bbox)
        else:
            self._isce.demImage = self.dem

        #at this point a dem image has been set into self.insar, wheater it
        #was sitched together or read in input
        demImage =  self._isce.demImage
        #check what is the dem reference if EGM96 then convert to WGS84
        if demImage.reference.upper() == 'EGM96':
            self._isce.demImage = self.demStitcher.correct(demImage)
            pass
            #cg = Correct_geoid_i2_srtm(self._writer_set_file_tags(
            #    "correct_geoid_i2_srtm", "log", "err", "out"
            #    ))
            #self._isce.demImage = cg(demImage) #KK 2014-01-12
        return None

    '''KK 2013-12-12
    def verifyUnwrap(self):
        if self.runUnwrapper:
            obj = self.runUnwrapper(self)
            obj.unwrap()
    '''

    def renderProcDoc(self):
        self._isce.procDoc.renderXml()


    ## Run Offoutliers() repeatedly with arguments from "iterator" keyword
    def iterate_runOffoutliers(self, iterator=None):
        """
        runs runOffoutliers multiple times with values (integers) from iterator.
        iterator defaults to Stack._default_culling_sequence
        """
        if iterator is None:
            iterator = self.culling_sequence
        map(self.runOffoutliers, iterator)


    def set_topoint1(self):
        self._isce.topoIntImages = dict(self._isce.resampIntImages)


    def set_topoint2(self):
        self._isce.topoIntImages = dict(self._isce.resampOnlyImages)


    def startup(self):
        self.verifyOutput()
        self.help()
        self.formatAttributes()
        self.prepareStack()
        self.timeStart = time.time()


    def endup(self):
        self.renderProcDoc()
        self.timeEnd = time.time()
        logger.info("Total Time: %i seconds" % (self.timeEnd - self.timeStart))



    ## Add instance attribute RunWrapper functions, which emulate methods.
    def _add_methods(self):
        self.runPreprocessor = IsceProc.createPreprocessor(self)
        self.extractInfo = IsceProc.createExtractInfo(self)
        self.createDem = IsceProc.createCreateDem(self)
        self.runPulseTiming = IsceProc.createPulseTiming(self)
        self.runEstimateHeights = IsceProc.createEstimateHeights(self)
        self.runSetmocomppath = IsceProc.createSetmocomppath(self)
        self.runOrbit2sch = IsceProc.createOrbit2sch(self)
        self.updatePreprocInfo = IsceProc.createUpdatePreprocInfo(self)
        self.runOffoutliers = IsceProc.createOffoutliers(self)
        self.prepareResamps = IsceProc.createPrepareResamps(self)
        self.runResamp = IsceProc.createResamp(self)
        self.runResamp_image = IsceProc.createResamp_image(self)
        self.runISSI = IsceProc.createISSI(self)
        self.runCrossmul = IsceProc.createCrossmul(self) #2013-11-26
        self.runMocompbaseline = IsceProc.createMocompbaseline(self)
        self.runTopo = IsceProc.createTopo(self)
        self.runCorrect = IsceProc.createCorrect(self)
        self.runShadecpx2rg = IsceProc.createShadecpx2rg(self)
#        self.runRgoffset = IsceProc.createRgoffset(self)
        self.runResamp_only = IsceProc.createResamp_only(self)
        self.runCoherence = IsceProc.createCoherence(self)
        self.runFilter = IsceProc.createFilter(self)
        self.runGrass = IsceProc.createGrass(self)
        self.runGeocode = IsceProc.createGeocode(self)


    def _steps(self):
        self.step('startup', func=self.startup,
                     doc=("Print a helpful message and "+
                          "set the startTime of processing")
                  )

        if self.do_preprocess:
            # Run a preprocessor for the sets of frames
            self.step('preprocess',
                      func=self.runPreprocessor,
                      doc=(
                    """Preprocess scenes to raw images"""
                    )
                      )

        if self.do_verifyDEM:
            # Verify whether the DEM was initialized properly.
            # If not, download a DEM
            self.step('verifyDEM', func=self.verifyDEM)

        if self.do_pulsetiming:
            # Run pulsetiming for each set of frames
            self.step('pulsetiming', func=self.runPulseTiming)

        if self.do_estimateheights:
            self.step('estimateHeights', func=self.runEstimateHeights)

        if self.do_mocomppath:
            # Run setmocomppath
            self.step('mocompath', func=self.runSetmocomppath, args=(self.peg,))

        if self.do_orbit2sch:
        #init and run orbit2sch
            self.step('orbit2sch', func=self.runOrbit2sch)

        if self.do_updatepreprocinfo:
            # update quantities in objPreProc obtained from previous steps
            self.step('updatepreprocinfo',
                      func=self.updatePreprocInfo,
                      args=(self.use_dop,))

        if self.do_formslc:
            self.step('formslc', func=self.runFormSLC)

        polopList = [] #list of polarimetric operations
        if self.do_pol_correction:
            polopList.append('polcal')
        if self.do_pol_fr:
            polopList.append('fr')
        if self.do_pol_tec:
            polopList.append('tec')
        if self.do_pol_phase:
            polopList.append('phase')
        if polopList: #not empty
            # run polarimetric correction
            self.step('pol_correction', func=self.runISSI, args=(polopList,))


        if self.do_offsetprf:
            self.step('offsetprf', func=self.runOffsetprf)

        if self.do_outliers1:
            # cull offoutliers
            self.step('outliers1', func=self.iterate_runOffoutliers)

        if self.do_prepareresamps:
            # determine rg and az looks
            self.step('prepareresamps',
                      func=self.prepareResamps,
                      args=(self.resampRgLooks,self.resampAzLooks))

        if self.do_resamp:
            # output resampled slc (skip int and amp files)
            self.step('resamp', func=self.runResamp)

        if self.do_resamp_image:
            # output images of offsets
            self.step('resamp_image', func=self.runResamp_image)

        if self.do_crossmul: #2013-11-26
            # run crossmultiplication (output int and amp)
            self.step('crossmul', func=self.runCrossmul)

        if self.do_mocompbaseline:
            # mocompbaseline
            self.step('mocompbaseline', func=self.runMocompbaseline)

        if self.do_settopoint1:
            # assign resampIntImage to topoIntImage
            self.step('settopoint1', func=self.set_topoint1)

        if self.do_topo:
            self.step('topo', func=self.runTopo)

        if self.do_shadecpx2rg:
            self.step('shadecpx2rg', func=self.runShadecpx2rg)

        if self.do_rgoffset:
            # compute offsets and cull offoutliers
            self.step('rgoffset', func=self.runRgoffset)

        if self.do_rg_outliers2:
            self.step('rg_outliers2', func=self.iterate_runOffoutliers)

        if self.do_resamp_only:
            self.step('resamp_only', func=self.runResamp_only)

        if self.do_settopoint2:
            # assign resampOnlyImage to topoIntImage
            self.step('settopoint2', func=self.set_topoint2)

        if self.do_correct:
            self.step('correct', func=self.runCorrect)

        if self.do_coherence:
            # coherence ?
            self.step('coherence',
                      func=self.runCoherence,
                      args=(self.correlation_method,))

        if self.do_filterinf:
            # filter ?
            self.step('filterinf', func=self.runFilter,
                      args=(self.filterStrength,)) #KK 2013-12-12

        if self.do_unwrap:
            # unwrap ?
            self.step('unwrap', func=self.runUnwrapper) #KK 2013-12-12 runUnwrapper instead of verifyUnwrap

        if self.do_geocodeinf:
            # geocode
            self.step('geocodeinf', func=self.runGeocode,
                      args=(self.geocode_list, self.do_unwrap, self.geocode_bbox))

        self.step('endup', func=self.endup)


    def main(self):
        """
        Run the given processing steps.
        """
        self.startup()

        if self.do_preprocess:
            # Run a preprocessor for the sets of frames
            self.runPreprocessor()

        if self.do_verifyDEM:
            # Verify whether user defined  a dem component.  If not, then download
            # SRTM DEM.
            self.verifyDEM()

        if self.do_pulsetiming:
            # Run pulsetiming for each set of frames
            self.runPulseTiming()

        if self.do_estimateheights:
            self.runEstimateHeights()

        if self.do_mocomppath:
            # Run setmocomppath
            self.runSetmocomppath(peg=self.peg)

        if self.do_orbit2sch:
            # init and run orbit2sch
            self.runOrbit2sch()

        if self.do_updatepreprocinfo:
            # update quantities in objPreProc obtained from previous steps
            self.updatePreprocInfo(use_dop=self.use_dop)

        if self.do_formslc:
            self.runFormSLC()

        polopList = []
        if self.do_pol_correction:
            polopList.append('polcal')
        if self.do_pol_fr:
            polopList.append('fr')
        if self.do_pol_tec:
            polopList.append('tec')
        if self.do_pol_phase:
            polopList.append('phase')
        if polopList:
            self.runISSI(polopList)

        if self.do_offsetprf:
            self.runOffsetprf()

        if self.do_outliers1:
            # Cull offoutliers
            self.iterate_runOffoutliers()

        if self.do_prepareresamps:
            self.prepareResamps(self.resampRgLooks, self.resampAzLooks)

        if self.do_resamp:
            self.runResamp()

        if self.do_resamp_image:
            self.runResamp_image()

        if self.do_crossmul: #2013-11-26
            self.runCrossmul()

        if self.do_mocompbaseline:
            # mocompbaseline
            self.runMocompbaseline()

        if self.do_settopoint1:
            # assign resampIntImage to topoIntImage
            self.set_topoint1()

        if self.do_topo:
            # topocorrect
            self.runTopo()

#        self.runCorrect()

        self.runShadecpx2rg()

        self.runRgoffset()

        # Cull offoutliers
        self.iterate_runOffoutliers()

        self.runResamp_only()

        self.set_topint2()
#        self.runTopo()

        self.runCorrect()

        # Coherence ?
        self.runCoherence(method=self.correlation_method)

        # Filter ?
        self.runFilter(self.filterStrength) #KK 2013-12-12 filterStrength as argument

        # Unwrap ?
        self.runUnwrapper() #KK 2013-12-12 instead of self.verifyUnwrap()

        # Geocode
        self.runGeocode(self.geocode_list, self.do_unwrap, self.geocode_bbox) #KK 2013-12-12 added arguments

        self.endup()



if __name__ == "__main__":
    ##create the isce object
    isceapp = IsceApp(name='isceApp')
    isceapp.configure()
    ##run the app
    isceapp.run()
