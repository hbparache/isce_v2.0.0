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





#ifndef readOrbitPulseERSmoduleFortTrans_h
#define readOrbitPulseERSmoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
			#define getStartingTime_f getstartingtime_
			#define readOrbitPulseERS_f readorbitpulseers_
			#define setDeltaClock_f setdeltaclock_
			#define setICUoffset_f seticuoffset_
			#define setNumberLines_f setnumberlines_
			#define setPRF_f setprf_
			#define setSatelliteUTC_f setsatelliteutc_
			#define setWidth_f setwidth_
			#define setEncodedBinaryTimeCode_f setencodedbinarytimecode_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif readOrbitPulseERSmoduleFortTrans_h
