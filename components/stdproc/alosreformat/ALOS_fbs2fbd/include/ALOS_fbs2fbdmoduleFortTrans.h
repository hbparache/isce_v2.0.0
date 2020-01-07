//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2011 to the present, California Institute of Technology.
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





#ifndef ALOS_fbs2fbdmoduleFortTrans_h
#define ALOS_fbs2fbdmoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
			#define ALOS_fbs2fbd_f alos_fbs2fbd_
			#define setFirstSample_f setfirstsample_
			#define setInPhaseValue_f setinphasevalue_
			#define setNumberBytesPerLine_f setnumberbytesperline_
			#define setNumberGoodBytes_f setnumbergoodbytes_
			#define setNumberLines_f setnumberlines_
			#define setQuadratureValue_f setquadraturevalue_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif ALOS_fbs2fbdmoduleFortTrans_h
