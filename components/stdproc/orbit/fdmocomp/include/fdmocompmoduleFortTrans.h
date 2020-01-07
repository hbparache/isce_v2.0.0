//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2013 to the present, California Institute of Technology.
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





#ifndef fdmocompmoduleFortTrans_h
#define fdmocompmoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
			#define allocate_fdArray_f allocate_fdarray_
			#define allocate_vsch_f allocate_vsch_
			#define deallocate_fdArray_f deallocate_fdarray_
			#define deallocate_vsch_f deallocate_vsch_
			#define fdmocomp_f fdmocomp_
			#define getCorrectedDoppler_f getcorrecteddoppler_
			#define setDopplerCoefficients_f setdopplercoefficients_
			#define setHeigth_f setheigth_
			#define setPRF_f setprf_
			#define setPlatformHeigth_f setplatformheigth_
			#define setRadarWavelength_f setradarwavelength_
			#define setRadiusOfCurvature_f setradiusofcurvature_
			#define setRangeSamplingRate_f setrangesamplingrate_
			#define setSchVelocity_f setschvelocity_
			#define setStartingRange_f setstartingrange_
			#define setWidth_f setwidth_
                        #define setLookSide_f setlookside_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif fdmocompmoduleFortTrans_h
