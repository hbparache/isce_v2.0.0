//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2012 to the present, California Institute of Technology.
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
// Author: Giangi Sacco
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





#ifndef estimateoffsetsmoduleFortTrans_h
#define estimateoffsetsmoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
			#define allocate_locationAcrossOffset_f allocate_locationacrossoffset_
			#define allocate_locationAcross_f allocate_locationacross_
			#define allocate_locationDownOffset_f allocate_locationdownoffset_
			#define allocate_locationDown_f allocate_locationdown_
			#define allocate_snrRet_f allocate_snrret_
			#define deallocate_locationAcrossOffset_f deallocate_locationacrossoffset_
			#define deallocate_locationAcross_f deallocate_locationacross_
			#define deallocate_locationDownOffset_f deallocate_locationdownoffset_
			#define deallocate_locationDown_f deallocate_locationdown_
			#define deallocate_snrRet_f deallocate_snrret_
			#define getLocationAcrossOffset_f getlocationacrossoffset_
			#define getLocationAcross_f getlocationacross_
			#define getLocationDownOffset_f getlocationdownoffset_
			#define getLocationDown_f getlocationdown_
			#define getSNR_f getsnr_
			#define estimateoffsets_f estimateoffsets_
			#define setAcrossGrossOffset_f setacrossgrossoffset_
			#define setDebugFlag_f setdebugflag_
			#define setDownGrossOffset_f setdowngrossoffset_
			#define setFileLength1_f setfilelength1_
			#define setFileLength2_f setfilelength2_
			#define setFirstPRF_f setfirstprf_
			#define setFirstSampleAcross_f setfirstsampleacross_
			#define setFirstSampleDown_f setfirstsampledown_
			#define setLastSampleAcross_f setlastsampleacross_
			#define setLastSampleDown_f setlastsampledown_
			#define setLineLength1_f setlinelength1_
			#define setLineLength2_f setlinelength2_
			#define setNumberLocationAcross_f setnumberlocationacross_
			#define setNumberLocationDown_f setnumberlocationdown_
			#define setSecondPRF_f setsecondprf_
			#define setWindowSize_f setwindowsize_
			#define setSearchWindowSize_f setsearchwindowsize_
			#define setZoomWindowSize_f setzoomwindowsize_
			#define setOversamplingFactor_f setoversamplingfactor_
                        #define setIsComplex1_f setiscomplex1_
                        #define setIsComplex2_f setiscomplex2_
                        #define setBand1_f setband1_
                        #define setBand2_f setband2_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif estimateoffsetsmoduleFortTrans_h
