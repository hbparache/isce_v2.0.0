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





#ifndef mocompTSXmoduleFortTrans_h
#define mocompTSXmoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
			#define allocate_dopplerCentroidCoefficients_f allocate_dopplercentroidcoefficients_
			#define allocate_sch_f allocate_sch_
			#define allocate_time_f allocate_time_
			#define deallocate_dopplerCentroidCoefficients_f deallocate_dopplercentroidcoefficients_
			#define deallocate_sch_f deallocate_sch_
			#define deallocate_time_f deallocate_time_
			#define getMocompIndex_f getmocompindex_
			#define getMocompPositionSize_f getmocomppositionsize_
			#define getMocompPosition_f getmocompposition_
			#define mocompTSX_f mocomptsx_
			#define setBodyFixedVelocity_f setbodyfixedvelocity_
			#define setDopplerCentroidCoefficients_f setdopplercentroidcoefficients_
			#define setNumberAzLines_f setnumberazlines_
			#define setNumberRangeBins_f setnumberrangebins_
			#define setPRF_f setprf_
			#define setPlanetLocalRadius_f setplanetlocalradius_
			#define setPosition_f setposition_
			#define setRadarWavelength_f setradarwavelength_
			#define setRangeFisrtSample_f setrangefisrtsample_
			#define setRangeSamplingRate_f setrangesamplingrate_
			#define setSpacecraftHeight_f setspacecraftheight_
			#define setStdWriter_f setstdwriter_
			#define setTime_f settime_
			#define setVelocity_f setvelocity_
                        #define setLookSide_f setlookside_
                        #define getStartingRange_f getstartingrange_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif mocompTSXmoduleFortTrans_h
