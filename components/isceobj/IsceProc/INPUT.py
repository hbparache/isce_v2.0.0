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



from iscesys.Component.Application import Application

SENSOR_NAME = Application.Parameter('sensorName',
                                    public_name='sensor name',
                                    default=None,
                                    type=str,
                                    mandatory=True,
                                    doc="Sensor name"
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
        "Choose whether to use scene_sid or average Doppler for\n"+
        "processing, where sid is the scene id to use."
        )
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
AZ_SHIFT = Application.Parameter('azShiftPixels',
                                 public_name='azimuth shift',
                                 default=None,
                                 type='float',
                                 mandatory=False,
                                 doc='Number of pixels to shift in azimuth'
                                 )
SLC_RGLOOKS = Application.Parameter('slcRgLooks',
                                   public_name='slc rangelooks',
                                   default=1,
                                   type=int,
                                   mandatory=False,
                                   doc="Multilooking factor in range direction for SLCs"
                                   )
SLC_AZLOOKS = Application.Parameter('slcAzLooks',
                                   public_name='slc azimuthlooks',
                                   default=1,
                                   type=int,
                                   mandatory=False,
                                   doc="Multilooking factor in azimuth direction for SLCs"
                                   )
SLC_FILTERMETHOD = Application.Parameter('slcFilterMethod',
                                   public_name='slc filtermethod',
                                   default='Gaussian',
                                   type=str,
                                   mandatory=False,
                                   doc="Filter method for SLCs: Gaussian, Goldstein, adaptative"
                                   )
SLC_FILTERHEIGHT = Application.Parameter('slcFilterHeight',
                                   public_name='slc filterheight',
                                   default=1,
                                   type=int,
                                   mandatory=False,
                                   doc="Window height for SLC filtering"
                                   )
SLC_FILTERWIDTH = Application.Parameter('slcFilterWidth',
                                   public_name='slc filterwidth',
                                   default=1,
                                   type=int,
                                   mandatory=False,
                                   doc="Window width for SLC filtering"
                                   )
OFFSET_METHOD = Application.Parameter('offsetMethod',
                                      public_name='slc offset method',
                                      default='offsetprf',
                                      type=str,
                                      mandatory=False,
                                      doc=("SLC offset estimation method name. "+
                                           "Use value=ampcor to run ampcor")
                                      )
COREG_STRATEGY = Application.Parameter('coregStrategy',
                                   public_name='coregistration strategy',
                                   default='single reference',
                                   type=str,
                                   mandatory=False,
                                   doc="How to coregister the stack: single reference or cascade"
                                   )
REF_SCENE = Application.Parameter('refScene',
                                   public_name='reference scene',
                                   default=None,
                                   type=str,
                                   mandatory=False,
                                   doc="Scene used as reference if coregistration strategy = single reference"
                                   )
REF_POL = Application.Parameter('refPol',
                                   public_name='reference polarization',
                                   default='hh',
                                   type=str,
                                   mandatory=False,
                                   doc="Polarization used as reference if coregistration strategy = single reference. Default: HH"
                                   )
OFFSET_SEARCH_WINDOW_SIZE = Application.Parameter('offsetSearchWindowSize',
                                                  public_name='offset search window size',
                                                  default=None,
                                                  type=int,
                                                  mandatory=False,
                                                  doc=("Search window size used in offsetprf "+
                                                       "and rgoffset.")
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
NUM_FIT_COEFF = Application.Parameter('numFitCoeff',
                                      public_name='Number of fit coefficients',
                                      default=6,
                                      type=int,
                                      doc="Number of fit coefficients for offoutliers."
                                      )
RESAMP_RGLOOKS = Application.Parameter('resampRgLooks',
                                    public_name='resamp range looks',
                                    default=None,
                                    type='float',
                                    mandatory=False,
                                    doc='Number of range looks to use in resamp'
                                    )
RESAMP_AZLOOKS = Application.Parameter('resampAzLooks',
                                 public_name='resamp azimuth looks',
                                 default=None,
                                 type='float',
                                 mandatory=False,
                                 doc='Number of azimuth looks to use in resamp'
                                 )
FR_FILTER = Application.Parameter('FR_filter',
                                 public_name='FR filter',
                                 default=None,
                                 type=str,
                                 mandatory=False,
                                 doc='Filter method for FR, if spatial filtering is desired'
                                 )
FR_FILTERSIZE_X = Application.Parameter('FR_filtersize_x',
                                 public_name='FR filtersize X',
                                 default=None,
                                 type=int,
                                 mandatory=False,
                                 doc='Filter width for FR'
                                 )
FR_FILTERSIZE_Y = Application.Parameter('FR_filtersize_y',
                                 public_name='FR filtersize Y',
                                 default=None,
                                 type=int,
                                 mandatory=False,
                                 doc='Filter height for FR'
                                 )
FILTER_STRENGTH = Application.Parameter('filterStrength', # KK 2013-12-12
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
UNWRAPPER_NAME = Application.Parameter('unwrapper_name',
				public_name='unwrapper name',
				default='',
				type=str,
				mandatory=False,
				doc="Unwrapping method to use. To be used in combination with UNWRAP."
				)
GEOCODE_LIST = Application.Parameter('geocode_list', #KK 2013-12-12
                                      public_name='geocode list',
                                      default = None,
                                      type=(tuple, list, iter),
                                      doc = "List of products to geocode.")
GEOCODE_BOX = Application.Parameter('geocode_bbox', #KK 2013-12-12
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
OUTPUT_DIR = Application.Parameter('outputDir',
                                   public_name='output directory',
                                   default='.',
                                   type=str,
                                   mandatory=False,
                                   doc="Output directory, where log files and output files will be dumped."
                                   )
SELECTED_SCENES = Application.Parameter('selectedScenes',
                                        public_name='selectScenes',
                                        default='',
                                        mandatory=False,
                                        doc="Comma-separated list of scene ids to process. If not given, process all scenes."
                                        )
SELECTED_PAIRS = Application.Parameter('selectedPairs',
                                       public_name='selectPairs',
                                       default='',
                                       mandatory=False,
                                       doc=(
            "Comma-separated list of pairs to process. Pairs are in the form sid1-sid2. "+
            "If not given, process all possible pairs."
            )
                                       )
SELECTED_POLS = Application.Parameter('selectedPols',
                                      public_name='selectPols',
                                      default='',
                                      mandatory=False,
                                      doc=(
            "Comma-separated list of polarizations to process. "+
            "If not given, process all polarizations."
            )
                                      )
DO_PREPROCESS = Application.Parameter('do_preprocess',
                                      public_name='do preprocess',
                                      default=False,
                                      type=bool,
                                      mandatory=False,
                                      doc="True if preprocessor is desired."
                                      )
DO_VERIFY_DEM = Application.Parameter('do_verifyDEM',
                                      public_name='do verifyDEM',
                                      default=False,
                                      type=bool,
                                      mandatory=False,
                                      doc="True if verify DEM is desired. If DEM not given, download DEM."
                                      )
DO_PULSETIMING = Application.Parameter('do_pulsetiming',
                                       public_name='do pulsetiming',
                                       default=False,
                                       type=bool,
                                       mandatory=False,
                                       doc="True if running pulsetiming is desired."
                                       )
DO_ESTIMATE_HEIGHTS = Application.Parameter('do_estimateheights',
                                            public_name='do estimateheights',
                                            default=False,
                                            type=bool,
                                            mandatory=False,
                                            doc="True if estimating heights is desired."
                                            )
DO_SET_MOCOMPPATH = Application.Parameter('do_mocomppath',
                                          public_name='do mocomppath',
                                          default=False,
                                          type=bool,
                                          mandatory=False,
                                          doc="True if setting mocomppath is desired."
                                          )
DO_ORBIT2SCH = Application.Parameter('do_orbit2sch',
                                     public_name='do orbit2sch',
                                     default=False,
                                     type=bool,
                                     mandatory=False,
                                     doc="True if converting orbit to SCH is desired."
                                     )
DO_UPDATE_PREPROCINFO = Application.Parameter('do_updatepreprocinfo',
                                              public_name='do updatepreprocinfo',
                                              default=False,
                                              type=bool,
                                              mandatory=False,
                                              doc="True if updating info is desired."
                                              )
DO_FORM_SLC = Application.Parameter('do_formslc',
                                    public_name='do formslc',
                                    default=False,
                                    type=bool,
                                    mandatory=False,
                                    doc="True if form_slc is desired."
                                    )
DO_MULTILOOK_SLC = Application.Parameter('do_multilookslc',
                                         public_name='do multilookslc',
                                         default=False,
                                         type=bool,
                                         mandatory=False,
                                         doc="True if slc multilooking is desired."
                                         )
DO_FILTER_SLC = Application.Parameter('do_filterslc',
                                      public_name='do filterslc',
                                      default=False,
                                      type=bool,
                                      mandatory=False,
                                      doc="True if slc filtering is desired."
                                      )
DO_GEOCODE_SLC = Application.Parameter('do_geocodeslc',
                                       public_name='do geocodeslc',
                                       default=False,
                                       type=bool,
                                       mandatory=False,
                                       doc="True if slc geocoding is desired."
                                       )
DO_OFFSETPRF = Application.Parameter('do_offsetprf',
                                     public_name='do offsetprf',
                                     default=False,
                                     type=bool,
                                     mandatory=False,
                                     doc="True if running offsetprf is desired."
                                     )
DO_OUTLIERS1 = Application.Parameter('do_outliers1',
                                     public_name='do outliers1',
                                     default=False,
                                     type=bool,
                                     mandatory=False,
                                     doc="True if running outliers is desired."
                                     )
DO_PREPARE_RESAMPS = Application.Parameter('do_prepareresamps',
                                            public_name='do prepareresamps',
                                            default=False,
                                            type=bool,
                                            mandatory=False,
                                            doc="True if preparing resamps is desired."
                                            )
DO_RESAMP = Application.Parameter('do_resamp',
                                  public_name='do resamp',
                                  default=False,
                                  type=bool,
                                  mandatory=False,
                                  doc="True if outputting of resampled slc is desired."
                                  )
DO_RESAMP_IMAGE = Application.Parameter('do_resamp_image',
                                        public_name='do resamp image',
                                        default=False,
                                        type=bool,
                                        mandatory=False,
                                        doc="True if outputting of offset images is desired."
                                        )
DO_POL_CORRECTION = Application.Parameter('do_pol_correction',
                                 public_name='do polarimetric correction',
                                 default=False,
                                 type=bool,
                                 mandatory=False,
                                 doc='True if polarimetric correction is desired.'
                                 )
DO_POL_FR = Application.Parameter('do_pol_fr',
                                 public_name='do calculate FR',
                                 default=False,
                                 type=bool,
                                 mandatory=False,
                                 doc='True if calculating Faraday Rotation is desired.'
                                 )
DO_POL_TEC = Application.Parameter('do_pol_tec',
                                 public_name='do FR to TEC',
                                 default=False,
                                 type=bool,
                                 mandatory=False,
                                 doc='True if converting FR to TEC is desired.'
                                 )
DO_POL_PHASE = Application.Parameter('do_pol_phase',
                                 public_name='do TEC to phase',
                                 default=False,
                                 type=bool,
                                 mandatory=False,
                                 doc='True if converting TEC to phase is desired.'
                                 )
DO_CROSSMUL = Application.Parameter('do_crossmul', #2013-11-26
                                  public_name='do crossmul',
                                  default=False,
                                  type=bool,
                                  mandatory=False,
                                  doc="True if crossmultiplication is desired."
                                  )
DO_MOCOMP_BASELINE = Application.Parameter('do_mocompbaseline',
                                           public_name='do mocomp baseline',
                                           default=False,
                                           type=bool,
                                           mandatory=False,
                                           doc="True if estimating mocomp baseline is desired."
                                           )
DO_SET_TOPOINT1 = Application.Parameter('do_settopoint1',
                                        public_name='do set topoint1',
                                        default=False,
                                        type=bool,
                                        mandatory=False,
                                        doc="True if setting toppoint1 is desired."
                                        )
DO_TOPO = Application.Parameter('do_topo',
                                public_name='do topo',
                                default=False,
                                type=bool,
                                mandatory=False,
                                doc="True if estimating topography is desired."
                                )
DO_SHADE_CPX2RG = Application.Parameter('do_shadecpx2rg',
                                        public_name='do shadecpx2rg',
                                        default=False,
                                        type=bool,
                                        mandatory=False,
                                        doc="True if shadecpx2rg is desired."
                                        )
DO_RG_OFFSET = Application.Parameter('do_rgoffset',
                                     public_name='do rgoffset',
                                     default=False,
                                     type=bool,
                                     mandatory=False,
                                     doc="True if rgoffset is desired."
                                     )
DO_RG_OUTLIERS2 = Application.Parameter('do_rg_outliers2',
                                        public_name='do rg outliers2',
                                        default=False,
                                        type=bool,
                                        mandatory=False,
                                        doc="True if rg outliers2 is desired."
                                        )
DO_RESAMP_ONLY = Application.Parameter('do_resamp_only',
                                       public_name='do resamp only',
                                       default=False,
                                       type=bool,
                                       mandatory=False,
                                       doc="True if resample only is desired."
                                       )
DO_SET_TOPOINT2 = Application.Parameter('do_settopoint2',
                                        public_name='do set topoint2',
                                        default=False,
                                        type=bool,
                                        mandatory=False,
                                        doc="True if setting topoint2 is desired."
                                        )
DO_CORRECT = Application.Parameter('do_correct',
                                   public_name='do correct',
                                   default=False,
                                   type=bool,
                                   mandatory=False,
                                   doc="True if correcting image is desired."
                                   )
DO_COHERENCE = Application.Parameter('do_coherence',
                                     public_name='do coherence',
                                     default=False,
                                     type=bool,
                                     mandatory=False,
                                     doc="True if coherence estimation is desired."
                                     )
DO_FILTER_INF = Application.Parameter('do_filterinf',
                                     public_name='do filter interferogram',
                                     default=False,
                                     type=bool,
                                     mandatory=False,
                                     doc="True if interferogram filtering is desired."
                                     )
DO_UNWRAP = Application.Parameter('do_unwrap',
                                  public_name='do unwrap',
                                  default=False,
                                  type=bool,
                                  mandatory=False,
                                  doc="True if unwrapping is desired. To be used in combination with UNWRAPPER_NAME."
                                  )
DO_GEOCODE_INF = Application.Parameter('do_geocodeinf',
                                       public_name='do geocode interferogram',
                                       default=False,
                                       type=bool,
                                       mandatory=False,
                                       doc="True if interferogram filtering is desired."
                                       )



STACK = Application.Facility('stack',
                             public_name='Stack',
                             module='isceobj.Stack',
                             factory='createStack',
                             mandatory=True,
                             doc="Stack component with a list of scenes."
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
                           )
RUN_FORM_SLC = Application.Facility('runFormSLC',
                                    public_name='Form SLC',
                                    module='isceobj.InsarProc',
                                    factory='createFormSLC',
                                    args=('do_formslc', 'sensorName',),
                                    mandatory=False,
                                    doc="SLC formation module"
                                    )
RUN_OFFSETPRF = Application.Facility('runOffsetprf',
                                     public_name='slc offsetter',
                                     module='isceobj.InsarProc',
                                     factory='createOffsetprf',
                                     args=('do_offsetprf', 'offsetMethod',),
                                     mandatory=False,
                                     doc="Offset a pair of SLC images."
                                    )
RUN_UNWRAPPER = Application.Facility('runUnwrapper',
				     public_name='Run unwrapper',
				     module='isceobj.Unwrap',
				     factory='createUnwrapper',
				     args=('do_unwrap', 'unwrapper_name',),
				     mandatory=False,
				     doc="Unwrapping module"
				     )
