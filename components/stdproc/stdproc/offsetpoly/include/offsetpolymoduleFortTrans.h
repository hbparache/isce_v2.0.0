//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Copyright: 2010 to the present, California Institute of Technology.
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





#ifndef offsetpolymoduleFortTrans_h
#define offsetpolymoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
			#define allocateFieldArrays_f allocatefieldarrays_
                        #define deallocateFieldArrays_f deallocatefieldarrays_
                        #define allocatePolyArray_f allocatepolyarray_
                        #define deallocatePolyArray_f deallocatepolyarray_
			#define getOffsetPoly_f getoffsetpoly_
			#define offsetpoly_f offsetpoly_
			#define setLocationAcross_f setlocationacross_
			#define setOffset_f setoffset_
			#define setLocationDown_f setlocationdown_
			#define setSNR_f setsnr_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif offsetpolymoduleFortTrans_h
