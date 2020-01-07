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





#ifndef calc_dopmoduleFortTrans_h
#define calc_dopmoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
			#define allocate_rngDoppler_f allocate_rngdoppler_
			#define calc_dop_f calc_dop_
			#define deallocate_rngDoppler_f deallocate_rngdoppler_
			#define getDoppler_f getdoppler_
			#define getRngDoppler_f getrngdoppler_
			#define setFirstLine_f setfirstline_
			#define setHeader_f setheader_
			#define setIoffset_f setioffset_
			#define setLastLine_f setlastline_
			#define setQoffset_f setqoffset_
			#define setWidth_f setwidth_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif calc_dopmoduleFortTrans_h
