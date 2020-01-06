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





#ifndef correct_geoid_i2_srtmmoduleFortTrans_h
#define correct_geoid_i2_srtmmoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
			#define correct_geoid_i2_srtm_f correct_geoid_i2_srtm_
			#define setConversionType_f setconversiontype_
			#define setDeltaLatitude_f setdeltalatitude_
			#define setDeltaLongitude_f setdeltalongitude_
			#define setGeoidFilename_f setgeoidfilename_
			#define setNumberLines_f setnumberlines_
			#define setStartLatitude_f setstartlatitude_
			#define setStartLongitude_f setstartlongitude_
			#define setWidth_f setwidth_
			#define setStdWriter_f setstdwriter_

		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif correct_geoid_i2_srtmmoduleFortTrans_h
