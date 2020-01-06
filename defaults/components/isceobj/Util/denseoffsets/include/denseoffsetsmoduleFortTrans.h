//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2014 to the present, California Institute of Technology.
// ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged.
// Any commercial use must be negotiated with the Office of Technology Transfer
// at the California Institute of Technology.
// 
// This software may be subject to U.S. export control laws. By accepting this
// software, the user agrees to comply with all applicable U.S. export laws and
// regulations. User has the responsibility to obtain export licenses,  or other
// export authority as may be required before exporting such information to
// foreign countries or providing access to foreign persons.
// 
// Installation and use of this software is restricted by a license agreement
// between the licensee and the California Institute of Technology. It is the
// User's responsibility to abide by the terms of the license agreement.
//
// Author: Piyush Agram
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





#ifndef denseoffsetsmoduleFortTrans_h
#define denseoffsetsmoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
			#define denseoffsets_f denseoffsets_
			#define setAcrossGrossOffset_f setacrossgrossoffset_
			#define setDebugFlag_f setdebugflag_
			#define setDownGrossOffset_f setdowngrossoffset_
			#define setFileLength1_f setfilelength1_
			#define setFileLength2_f setfilelength2_
			#define setScaleFactorX_f setscalefactorx_
			#define setFirstSampleAcross_f setfirstsampleacross_
			#define setFirstSampleDown_f setfirstsampledown_
			#define setLastSampleAcross_f setlastsampleacross_
			#define setLastSampleDown_f setlastsampledown_
			#define setLineLength1_f setlinelength1_
			#define setLineLength2_f setlinelength2_
			#define setSkipSampleAcross_f setskipsampleacross_
			#define setSkipSampleDown_f setskipsampledown_
			#define setScaleFactorY_f setscalefactory_
			#define setWindowSizeWidth_f setwindowsizewidth_
                        #define setWindowSizeHeight_f setwindowsizeheight_
			#define setSearchWindowSizeWidth_f setsearchwindowsizewidth_
                        #define setSearchWindowSizeHeight_f setsearchwindowsizeheight_
			#define setZoomWindowSize_f setzoomwindowsize_
			#define setOversamplingFactor_f setoversamplingfactor_
                        #define setIsComplex1_f setiscomplex1_
                        #define setIsComplex2_f setiscomplex2_
                        #define setBand1_f setband1_
                        #define setBand2_f setband2_
                        #define setNormalizeFlag_f setnormalizeflag_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif denseoffsetsmoduleFortTrans_h
