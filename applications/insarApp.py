#!/usr/bin/env python3

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
# Authors: Giangi Sacco, Eric Gurrola
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



from __future__ import print_function
import time
import os
import sys
import logging
import logging.config

import isce
import isceobj
import iscesys
from iscesys.Component.Application import Application
from iscesys.Compatibility import Compatibility
import isceobj.InsarProc as InsarProc
from isceobj.Scene.Frame import FrameMixin

logging.config.fileConfig(
    os.path.join(os.environ['ISCE_HOME'], 'defaults', 'logging',
        'logging.conf')
)

logger = logging.getLogger('isce.insar')


SENSOR_NAME = Application.Parameter('sensorName',
                                    public_name='sensor name',
                                    default=None,
                                    type=str,
                                    mandatory=True,
                                    doc="Sensor name"
                                    )
OFFSET_METHOD = Application.Parameter('offsetMethod',
                                    public_name='slc offset method',
                                    default="offsetprf",
                                    type=str,
                                    mandatory=False,
                                    doc=("SLC offset estimation method name. "+
                                         "Use value=ampcor to run ampcor")
                                    )
OFFSET_SEARCH_WINDOW_SIZE = Application.Parameter('offsetSearchWindowSize',
                                public_name='offset search window size',
                                default=None,
                                type=int,
                                mandatory=False,
                                doc=("Search window size used in offsetprf "+
                                     "and rgoffset.")
                                )
PEG_LAT = Application.Parameter('pegLat',
                                public_name='peg latitude (deg)',
                                default=None,
                                type='float',
                                mandatory=False,
                                doc='Peg Latitude in degrees'
                                )
PEG_LON = Application.Parameter('pegLon',
                                public_name='peg longitude (deg)',
                                default=None,
                                type='float',
                                mandatory=False,
                                doc='Peg Longitude in degrees'
                                )
PEG_HDG = Application.Parameter('pegHdg',
                                public_name='peg heading (deg)',
                                default=None,
                                type='float',
                                mandatory=False,
                                doc='Peg Heading in degrees'
                                )
PEG_RAD = Application.Parameter('pegRad',
                                public_name='peg radius (m)',
                                default=None,
                                type='float',
                                mandatory=False,
                                doc='Peg Radius of Curvature in meters'
                                )
FILTER_STRENGTH = Application.Parameter('filterStrength',
                                public_name='filter strength',
                                default = None,
                                type='float',
                                mandatory=False,
                                doc='Goldstein Werner Filter strength'
                                )
CORRELATION_METHOD = Application.Parameter('correlation_method',
                                           public_name='correlation_method',
                                           default='cchz_wave',
                                           type='str',
                                           mandatory=False,
                                           doc=(
        """Select coherence estimation method:
                  cchz=cchz_wave
                  phase_gradient=phase gradient"""
        )
                                           )
DOPPLER_METHOD = Application.Parameter('dopplerMethod',
                                       public_name='doppler method',
                                       default='useDOPIQ',
                                       type=str, mandatory=False,
                                       doc= (
        "Doppler calculation method.Choices: 'useDOPIQ', 'useCalcDop', \n" +
        "'useDoppler'.")
                                       )
USE_DOP = Application.Parameter('use_dop',
                                public_name='use_dop',
                                default="average",
                                type='float',
                                mandatory=False,
                                doc=(
        "Choose whether to use master, slave, or average Doppler for\n"+
        "processing."
        )
                                )

UNWRAPPER_NAME = Application.Parameter('unwrapper_name',
                                public_name='unwrapper name',
                                default='grass',
                                type=str,
                                mandatory=False,
                                doc="Unwrapping method to use. To be used in  combination with UNWRAP."
                                )

# to be replaced by DO_UNWRAP;
UNWRAP = Application.Parameter('unwrap',
                               public_name='unwrap',
                               default=False,
                               type=bool,
                               mandatory=False,
                               doc="True if unwrapping is desired. To be unsed in combination with UNWRAPPER_NAME."
                               )

# not fully supported yet; use UNWRAP instead
DO_UNWRAP = Application.Parameter('do_unwrap',
                               public_name='do unwrap',
                               default=False,
                               type=bool,
                               mandatory=False,
                               doc="True if unwrapping is desired. To be unsed in combination with UNWRAPPER_NAME."
                               )

DO_OFFSETPRF = Application.Parameter('do_offsetprf',
                               public_name='do offsetprf',
                               default=True,
                               type=bool,
                               mandatory=False,
                               doc="Set to False if offsetprf is not required."
                               )

DO_RGOFFSET = Application.Parameter('do_rgoffset',
                               public_name='do rgoffset',
                               default=True,
                               type=bool,
                               mandatory=False,
                               doc="Set to False if offsetprf is not required."
                               )

USE_HIGH_RESOLUTION_DEM_ONLY = Application.Parameter('useHighResolutionDemOnly',
                                                public_name=(
        'useHighResolutionDemOnly'
        ),
                                                default=False,
                                                type=int,
                                                mandatory=False,
                                                doc=(
        """If True and a dem is not specified in input, it will only
           download the SRTM highest resolution dem if it is available
           and fill the missing portion with null values (typically -32767)."""
        )
                                                )
DEM_FILENAME = Application.Parameter('demFilename',
                                     public_name='demFilename',
                                     default='',
                                     type=str,
                                     mandatory=False,
                                     doc="Filename of the DEM init file"
                                     )
GEO_POSTING = Application.Parameter('geoPosting',
                                    public_name='geoPosting',
                                    default=None,
                                    type='float',
                                    mandatory=False,
                                    doc=(
        "Output posting for geocoded images in degrees (latitude = longitude)"
        )
    )
POSTING = Application.Parameter('posting',
                                public_name='posting',
                                default=15,
                                type=int,
                                mandatory=False,
                                doc="posting for interferogram"
                                )
RANGE_LOOKS = Application.Parameter('rangeLooks',
                                    public_name='range looks',
                                    default=None,
                                    type='float',
                                    mandatory=False,
                                    doc='Number of range looks to use in resamp'
                                    )
AZ_LOOKS = Application.Parameter('azLooks',
                                 public_name='azimuth looks',
                                 default=None,
                                 type='float',
                                 mandatory=False,
                                 doc='Number of azimuth looks to use in resamp'
                                 )
PATCH_SIZE = Application.Parameter('patchSize',
                                  public_name='azimuth patch size',
                                  default=None,
                                  type=int,
                                  mandatory=False,
                                   doc=(
        "Size of overlap/save patch size for formslc"
        )
                                   )
GOOD_LINES = Application.Parameter('goodLines',
                                   public_name='patch valid pulses',
                                   default=None,
                                   type=int,
                                   mandatory=False,
                                   doc=(
        "Size of overlap/save save region for formslc"
        )
                                   )
NUM_PATCHES = Application.Parameter('numPatches',
                                    public_name='number of patches',
                                    default=None,
                                    type=int,
                                    mandatory=False,
                                    doc=(
        "How many patches to process of all available patches"
        )
                                    )
GROSS_AZ = Application.Parameter('grossAz',
                                 public_name='gross azimuth offset',
                                 default=None,
                                 type=int,
                                 mandatory=False,
                                 doc=(
        "Override the value of the gross azimuth offset for offset " +
        "estimation prior to interferogram formation"
        )
                                 )
GROSS_RG = Application.Parameter('grossRg',
                                 public_name='gross range offset',
                                 default=None,
                                 type=int,
                                 mandatory=False,
                                 doc=(
        "Override the value of the gross range offset for offset" +
        "estimation prior to interferogram formation"
        )
                                 )
CULLING_SEQUENCE = Application.Parameter('culling_sequence',
                                         public_name='Culling Sequence',
                                         default= (10,5,3),
                                         type=(tuple, list, iter),
                                         doc="TBD"
                                         )
CULLING_ERROR_LIMIT = Application.Parameter('culling_error_limit',
                                        public_name='Culling error limit',
                                        default=100,
                                        type = int,
                                        mandatory = False,
                                        doc = 'Minimum number of culled offsets to be used for offset field polynomial estimation')
GEOCODE_LIST = Application.Parameter('geocode_list',
                                      public_name='geocode list',
                                      default = None,
                                      type=(tuple, list, iter),
                                      doc = "List of products to geocode.")
GEOCODE_BOX = Application.Parameter('geocode_bbox',
                                    public_name='geocode bounding box',
                                    default = None,
                                    type=(tuple,list,iter),
                                    doc='Bounding box for geocoding - South, North, West, East in degrees')
PICKLE_DUMPER_DIR = Application.Parameter('pickleDumpDir',
                                          public_name='pickle dump directory',
                                          default='PICKLE',
                                          type=str,
                                          mandatory=False,
                                          doc=(
        "If steps is used, the directory in which to store pickle objects."
        )
                                          )
PICKLE_LOAD_DIR = Application.Parameter('pickleLoadDir',
                                        public_name='pickle load directory',
                                        default='PICKLE',
                                        type=str,
                                        mandatory=False,
                                        doc=(
        "If steps is used, the directory from which to retrieve pickle objects"
        )
                                        )

MASTER = Application.Facility('master',
                              public_name='Master',
                              module='isceobj.Sensor',
                              factory='createSensor',
                              args=('sensorName',),
                              mandatory=True,
                              doc="Master raw data component"
                              )
SLAVE = Application.Facility('slave',
                             public_name='Slave',
                             module='isceobj.Sensor',
                             factory='createSensor',
                             args=('sensorName',),
                             mandatory=True,
                             doc="Slave raw data component"
                             )
MASTERDOP = Application.Facility('masterdop',
                                 public_name='Master Doppler',
                                 module='isceobj.Doppler',
                                 factory='createDoppler',
                                 args=('dopplerMethod',),
                                 mandatory=False,
                                 doc="Master Doppler calculation method"
                                 )
SLAVEDOP = Application.Facility('slavedop',
                                public_name='Slave Doppler',
                                module='isceobj.Doppler',
                                factory='createDoppler',
                                args=('dopplerMethod',),
                                mandatory=False,
                                doc="Master Doppler calculation method"
                                )
DEM = Application.Facility('dem',
                           public_name='Dem',
                           module='isceobj.Image',
                           factory='createDemImage',
                           mandatory=False,
                           doc=(
        "Dem Image configurable component.  Do not include this in the "+
        "input file and an SRTM Dem will be downloaded for you."
        )
                           ),
RUN_FORM_SLC = Application.Facility('runFormSLC',
                                    public_name='Form SLC',
                                    module='isceobj.InsarProc',
                                    factory='createFormSLC',
                                    args=('self.sensorName,'),# self? how./ why?
                                    mandatory=False,
                                    doc="SLC formation module"
                                    )
RUN_OFFSETPRF = Application.Facility('runOffsetprf',
                                     public_name='slc offsetter',
                                     module='isceobj.InsarProc',
                                     factory='createOffsetprf',
                                     args=('self.offsetMethod'),
                                     mandatory=False,
                                     doc="Offset a pair of SLC images."
                                    )
RUN_UNWRAPPER = Application.Facility('runUnwrapper',
                                      public_name='Run unwrapper',
                                      module='isceobj.Unwrap',
                                      factory='createUnwrapper',
                                      args=('self.unwrap', 'self.unwrapper_name',),
                                      mandatory=False,
                                      doc="Unwrapping module"
                                      )


## Common interface for all insar applications.
class _InsarBase(Application, FrameMixin):

    family = 'insar'
    ## Define Class parameters in this list
    parameter_list = (SENSOR_NAME,
                      OFFSET_METHOD,
                      OFFSET_SEARCH_WINDOW_SIZE,
                      PEG_LAT,
                      PEG_LON,
                      PEG_HDG,
                      PEG_RAD,
                      FILTER_STRENGTH,
                      CORRELATION_METHOD,
                      DOPPLER_METHOD,
                      USE_DOP,
                      UNWRAP,
                      UNWRAPPER_NAME,
                      DO_UNWRAP,
                      DO_OFFSETPRF,
                      DO_RGOFFSET,
                      USE_HIGH_RESOLUTION_DEM_ONLY,
                      DEM_FILENAME,
                      GEO_POSTING,
                      POSTING,
                      RANGE_LOOKS,
                      AZ_LOOKS,
                      PATCH_SIZE,
                      GOOD_LINES,
                      NUM_PATCHES,
                      GROSS_AZ,
                      GROSS_RG,
                      CULLING_SEQUENCE,
                      CULLING_ERROR_LIMIT,
                      GEOCODE_LIST,
                      GEOCODE_BOX,
                      PICKLE_DUMPER_DIR,
                      PICKLE_LOAD_DIR)

    facility_list = (MASTER,
                     SLAVE,
                     MASTERDOP,
                     SLAVEDOP,
                     DEM,
                     RUN_FORM_SLC,
                     RUN_UNWRAPPER,
                     RUN_OFFSETPRF)

    _pickleObj = "_insar"

    def __init__(self, family='', name='',cmdline=None):
        import isceobj
        super(_InsarBase, self).__init__(family=family, name=name,
            cmdline=cmdline)

        from iscesys.StdOEL.StdOELPy import create_writer
        self._stdWriter = create_writer("log", "", True, filename="insar.log")
        self._add_methods()

        procDoc = isceobj.createCatalog('insarProc')
        self._insar = InsarProc.InsarProc(name='insarApp_conf',
            procDoc=procDoc
            )
        self.insar.procDoc._addItem("ISCE_VERSION",
            "Release: %s, svn-%s, %s. Current svn-%s" %
            (isce.release_version, isce.release_svn_revision,
             isce.release_date, isce.svn_revision
            ),
            ["insarProc"]
            )

        return None

    def _init(self):
        message =  (
            ("ISCE VERSION = %s, RELEASE_SVN_REVISION = %s,"+
             "RELEASE_DATE = %s, CURRENT_SVN_REVISION = %s") %
            (isce.__version__,
             isce.release_svn_revision,
             isce.release_date,
             isce.svn_revision)
            )
        logger.info(message)

        print(message)
#        print("self.sensorName = ", self.sensorName)
#        print("self.correlation_method = ", self.correlation_method)
#        print("self.use_dop = ", self.use_dop)
#        print("self.geoPosting = ", self.geoPosting)
#        print("self.posting = ", self.posting)
#        print("self.rangeLooks = ", self.rangeLooks)
#        print("self.azLooks = ", self.azLooks)
#        print("self.offsetMethod = ", self.offsetMethod)
#        print("self.grossRg, self.grossAz =  ", self.grossRg, self.grossAz )
        if ( self.pegLat is not None and
             self.pegLon is not None and
             self.pegHdg is not None and
             self.pegRad is not None ):
            from isceobj.Location.Peg import Peg
            self.peg = Peg(latitude=self.pegLat,
                           longitude=self.pegLon,
                           heading=self.pegHdg,
                           radiusOfCurvature=self.pegRad)
#            print("self.peg = ", self.peg)
        else:
            self.peg = None
        return None

    ## You need this to use the FrameMixin
    @property
    def frame(self):
        return self.insar.frame


    def _configure(self):
        #This is a temporary fix to get the user interface back to the dem
        #facility interface while changes are being made in the DemImage class
        #to include within it the capabilities urrently in extractInfo and
        #createDem.
        #jng ask Eric No longer needed
        if self.demFilename:
            import sys
            print(
            "The demFilename property is no longer supported as an " +
            "input parameter."
                )
            print(
                "The original method using a configurable facility for the " +
                "Dem is now restored."
                )
            print(
                "The automatic download feature is still supported in the " +
                " same way as before:"
                )
            print(
                "If you want automatic download of a Dem, then simply omit "+
                "any configuration\ninformation in your input file regarding "+
                "the Dem."
                )
            print()
            print(
                "Please replace the following information in your input file:"
                )
            print()
            print(
                "<property name='demFilename'><value>%s</value></property>" %
                self.demFilename
                )
            print()
            print("with the following information and try again:")
            print()
            print(
                "<component name=\'Dem\'><catalog>%s</catalog></component>" %
                self.demFilename
                )
            print()
        else:
            try:
                self.dem.checkInitialization()
                #jng ask Eric. self.demFilename no longer needed
                # Give self.demFilename a value so that the SRTM Dem will not
                # be downloaded
                # Temporary fix that will be removed when the download option
                # is handled within demImage
                self.demFilename = "demFilename"
                self.insar.demImage = self.dem
            except Exception as err:
                print(
                    "The Dem specified was not properly initialized. An SRTM" +
                    " Dem will be downloaded."
                    )
                #self.dem was not properly initialized
                #and self.demFilename is undefined.
                #There is a check on self.demFilename
                #below to download if necessary
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

        #if not provided by the user use the default from InsarProc
        if(self.geocode_list is None):
            self.geocode_list = self.insar.geocode_list

        return None


    def _facilities(self):
        """
        Define the user configurable facilities for this application.
        """
        self.master = self.facility(
            'master',
            public_name='Master',
            module='isceobj.Sensor',
            factory='createSensor',
            args=(self.sensorName, 'master'),
            mandatory=True,
            doc="Master raw data component"
        )
        self.slave  = self.facility(
            'slave',
            public_name='Slave',
            module='isceobj.Sensor',
            factory='createSensor',
            args=(self.sensorName, 'slave'),
            mandatory=True,
            doc="Slave raw data component"
        )
        self.masterdop = self.facility(
            'masterdop',
            public_name='Master Doppler',
            module='isceobj.Doppler',
            factory='createDoppler',
            args=(self.dopplerMethod,),
            mandatory=False,
            doc="Master Doppler calculation method"
        )
        self.slavedop  = self.facility(
            'slavedop',
            public_name='Slave Doppler',
            module='isceobj.Doppler',
            factory='createDoppler',
            args=(self.dopplerMethod,),
            mandatory=False,
            doc="Master Doppler calculation method"
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
            module='isceobj.InsarProc',
            factory='createFormSLC',
            args=(self, self.sensorName,),
            mandatory=False,
            doc="SLC formation module"
        )
        self.runOffsetprf  = self.facility(
            'runOffsetprf',
            public_name='slc offsetter',
            module='isceobj.InsarProc',
            factory='createOffsetprf',
            args=(self, self.offsetMethod, self.do_offsetprf,),
            mandatory=False,
            doc="SLC offset estimator."
        )
        self.runRgoffset = self.facility(
                'runRgoffset',
                public_name='dem offseter',
                module = 'isceobj.InsarProc',
                factory= 'createRgoffset',
                args=(self, self.offsetMethod, self.do_rgoffset,),
                mandatory=False,
                doc="Dem offset estimator."
        )
        self.runUnwrapper = self.facility(
            'runUnwrapper',
            public_name='Run Unwrapper',
            module='isceobj.InsarProc',
            factory='createUnwrapper',
            args=(self,self.do_unwrap,self.unwrapper_name,self.unwrap),
            mandatory=False,
            doc="Unwrapping module"
        )
        return None

    @property
    def insar(self):
        return self._insar
    @insar.setter
    def insar(self, value):
        self._insar = value
        return None

    @property
    def procDoc(self):
        return self.insar.procDoc
    @procDoc.setter
    def procDoc(self):
        raise AttributeError(
            "Can not assign to .insar.procDoc-- but you hit all its other stuff"
            )

    def _finalize(self):
        pass

    def help(self):
        from isceobj.Sensor import SENSORS
        print(self.__doc__)
        lsensors = list(SENSORS.keys())
        lsensors.sort()
        print("The currently supported sensors are: ", lsensors)
        return None

    def help_steps(self):
        print(self.__doc__)
        print("A description of the individual steps can be found in the README file")
        print("and also in the ISCE.pdf document")
        return

    ## Method return True iff it changes the demFilename.
    def verifyDEM(self):
        #if an image has been specified, then no need to create one
        if not self.dem.filename:
            #the following lines should be included in the check on demFilename
            import math
            masterF = self._insar.masterFrame
            slaveF = self._insar.slaveFrame
            info = self.extractInfo(masterF, slaveF)
            self.createDem(info)
        else:
            self.insar.demImage = self.dem

        #at this point a dem image has been set into self.insar, wheater it
        #was sitched together or read in input
        demImage =  self.insar.demImage
        #check what is the dem reference if EGM96 then convert to WGS84
        if demImage.reference.upper() == 'EGM96':
            self.insar.demImage = self.demStitcher.correct(demImage)
            pass
        return None



    def renderProcDoc(self):
        self.procDoc.renderXml()

    ## Run runOffoutliers() repeatedly with arguments from "iterator" keyword
    def iterate_runOffoutliers(self, iterator=None):
        """iterate_runOffoutliers(iterator)

        runs runOffoutliers multiple times with values (integers) from iterator.

        iterator defaults to Insar._default_culling_sequence
        """
        if iterator is None: iterator = self.culling_sequence
        erriterator = [self.culling_error_limit]*len(iterator)
        list(map(self.runOffoutliers, iterator, erriterator))
        return None

    def set_topoint1(self):
        self._insar.topoIntImage = self._insar.resampIntImage
        return None

    def set_topoint2(self):
        self._insar.topoIntImage = self._insar.resampOnlyImage
        return None

    def startup(self):
        self.help()
        self._insar.timeStart = time.time()

    def endup(self):
        self.renderProcDoc()
        self._insar.timeEnd = time.time()
        logger.info("Total Time: %i seconds" %
                    (self._insar.timeEnd-self._insar.timeStart))
        return None

    ## Add instance attribute RunWrapper functions, which emulate methods.
    def _add_methods(self):
        self.runPreprocessor = InsarProc.createPreprocessor(self)
        self.extractInfo = InsarProc.createExtractInfo(self)
        self.createDem = InsarProc.createCreateDem(self)
        self.runPulseTiming = InsarProc.createPulseTiming(self)
        self.runEstimateHeights = InsarProc.createEstimateHeights(self)
        self.runSetmocomppath = InsarProc.createSetmocomppath(self)
        self.runOrbit2sch = InsarProc.createOrbit2sch(self)
        self.updatePreprocInfo = InsarProc.createUpdatePreprocInfo(self)
        self.runOffoutliers = InsarProc.createOffoutliers(self)
        self.prepareResamps = InsarProc.createPrepareResamps(self)
        self.runResamp = InsarProc.createResamp(self)
        self.runResamp_image = InsarProc.createResamp_image(self)
        self.runMocompbaseline = InsarProc.createMocompbaseline(self)
        self.runTopo = InsarProc.createTopo(self)
        self.runCorrect = InsarProc.createCorrect(self)
        self.runShadecpx2rg = InsarProc.createShadecpx2rg(self)
#        self.runRgoffset = InsarProc.createRgoffset(self)
        self.runResamp_only = InsarProc.createResamp_only(self)
        self.runCoherence = InsarProc.createCoherence(self)
        self.runFilter = InsarProc.createFilter(self)
        self.runGrass = InsarProc.createGrass(self)
        self.runGeocode = InsarProc.createGeocode(self)
        return None

    def _steps(self):

        self.step('startup', func=self.startup,
                     doc=("Print a helpful message and "+
                          "set the startTime of processing")
                  )

        # Run a preprocessor for the two sets of frames
        self.step('preprocess',
                  func=self.runPreprocessor,
                  doc=(
                """Preprocess the master and slave sensor data to raw images"""
                )
                  )

        # Verify whether the DEM was initialized properly.  If not, download
        # a DEM
        self.step('verifyDEM', func=self.verifyDEM)

        # Run pulsetiming for each set of frames
        self.step('pulsetiming', func=self.runPulseTiming)

        self.step('estimateHeights', func=self.runEstimateHeights)

        # Run setmocomppath
        self.step('mocompath', func=self.runSetmocomppath, args=(self.peg,))

        #init and run orbit2sch
        self.step('orbit2sch', func=self.runOrbit2sch)

        #update quantities in objPreProc obtained from previous steps
        self.step('updatepreprocinfo',
                  func=self.updatePreprocInfo,
                  args=(self.use_dop,))

        self.step('formslc', func=self.runFormSLC)

        self.step('offsetprf', func=self.runOffsetprf)

        # Cull offoutliers
        self.step('outliers1', func=self.iterate_runOffoutliers)

        self.step('prepareresamps',
                  func=self.prepareResamps,
                  args=(self.rangeLooks,self.azLooks))

        self.step('resamp', func=self.runResamp)

        self.step('resamp_image', func=self.runResamp_image)

        # Mocompbaseline
        self.step('mocompbaseline', func=self.runMocompbaseline)

        # Topocorrect
        #self.step('settopoint1',
        #          func=self.insar.delayed_attrcopy_from_to('resampIntImage',
        #                                                    'topoIntImage')
        #          )
        self.step('settopoint1', func=self.set_topoint1)

        self.step('topo', func=self.runTopo)

        self.step('shadecpx2rg', func=self.runShadecpx2rg)

        # Compute offsets and cull offoutliers
        self.step('rgoffset', func=self.runRgoffset)
        self.step('rg_outliers2', func=self.iterate_runOffoutliers)

        self.step('resamp_only', func=self.runResamp_only)

        #Topocorrect
        #self.step('settopoint2',
        #          func=self.insar.delayed_attrcopy_from_to('resampOnlyImage',
        #                                                    'topoIntImage')
        #          )
        self.step('settopoint2', func=self.set_topoint2)

        self.step('correct', func=self.runCorrect)

        # Coherence ?
        self.step('coherence',
                  func=self.runCoherence,
                  args=(self.correlation_method,))

        # Filter ?
        self.step('filter', func=self.runFilter,
                  args=(self.filterStrength,))

        # Unwrap ?
        self.step('unwrap', func=self.runUnwrapper)
        return None

    ## Main has the common start to both insarApp and dpmApp.
    def main(self):
        self.help()

        # Run a preprocessor for the two sets of frames
        self.runPreprocessor()

        #Verify whether user defined  a dem component.  If not, then download
        # SRTM DEM.
        self.verifyDEM()

        # Run pulsetiming for each set of frames
        self.runPulseTiming()

        self.runEstimateHeights()

        # Run setmocomppath
        self.runSetmocomppath(peg=self.peg)

        #init and run orbit2sch
        self.runOrbit2sch()

        #update quantities in objPreProc obtained from previous steps
        self.updatePreprocInfo(use_dop=self.use_dop)

        self.runFormSLC()

        self.runOffsetprf()

        # Cull offoutliers
        self.iterate_runOffoutliers()

        self.prepareResamps(self.rangeLooks, self.azLooks)
        self.runResamp()
        self.runResamp_image()

        # Mocompbaseline
        self.runMocompbaseline()

        # Topocorrect
        self.insar.topoIntImage = self.insar.resampIntImage
        self.runTopo()
        return None

    @property
    def resampAmpImage(self):
        return self.insar.resampAmpImage


    pass




class Insar(_InsarBase):
    """
    Insar Application:
    Implements InSAR processing flow for a pair of scenes from
    sensor raw data to geocoded, flattened interferograms.
    """

    family = "insar"

    def __init__(self, family='',name='',cmdline=None):
        #to allow inheritance with different family name use the locally
        #defined only if the subclass (if any) does not specify one

        super(Insar, self).__init__(
            family=family if family else  self.__class__.family, name=name,
            cmdline=cmdline)

    def Usage(self):
        print("Usages: ")
        print("insarApp.py <input-file.xml>")
        print("insarApp.py --steps")
        print("insarApp.py --help")
        print("insarApp.py --help --steps")


    ## extends _InsarBase_steps, but not in the same was as main
    def _steps(self):
        super(Insar, self)._steps()

        # Geocode
        self.step('geocode', func=self.runGeocode,
                args=(self.geocode_list, self.unwrap, self.geocode_bbox))

        self.step('endup', func=self.endup)

        return None

    ## main() extends _InsarBase.main()
    def main(self):
        import time
        timeStart = time.time()

        super(Insar, self).main()

        # self.runCorrect()

        self.runShadecpx2rg()

        self.runRgoffset()

        # Cull offoutliers
        self.iterate_runOffoutliers()

        self.runResamp_only()

        self.insar.topoIntImage=self.insar.resampOnlyImage
        #self.runTopo()
        self.runCorrect()
  
        # Coherence ?
        self.runCoherence(method=self.correlation_method)


        # Filter ?
        self.runFilter(self.filterStrength)

        # Unwrap ?
        self.runUnwrapper()

        # Geocode
        self.runGeocode(self.geocode_list, self.unwrap, self.geocode_bbox)

        timeEnd = time.time()
        logger.info("Total Time: %i seconds" %(timeEnd - timeStart))

        self.renderProcDoc()


        return None




if __name__ == "__main__":
    import sys
    insar = Insar(name="insarApp")
    insar.configure()
    insar.run()
