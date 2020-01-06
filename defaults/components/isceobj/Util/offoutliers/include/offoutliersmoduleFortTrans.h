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





#ifndef offoutliersmoduleFortTrans_h
#define offoutliersmoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
            #define setStdWriter_f setstdwriter_
			#define allocate_acshift_f allocate_acshift_
			#define allocate_dnshift_f allocate_dnshift_
			#define allocate_indexArray_f allocate_indexarray_
			#define allocate_s_f allocate_s_
			#define allocate_sig_f allocate_sig_
			#define allocate_xd_f allocate_xd_
			#define allocate_yd_f allocate_yd_
			#define deallocate_acshift_f deallocate_acshift_
			#define deallocate_dnshift_f deallocate_dnshift_
			#define deallocate_indexArray_f deallocate_indexarray_
			#define deallocate_s_f deallocate_s_
			#define deallocate_sig_f deallocate_sig_
			#define deallocate_xd_f deallocate_xd_
			#define deallocate_yd_f deallocate_yd_
			#define getAverageOffsetAcross_f getaverageoffsetacross_
			#define getAverageOffsetDown_f getaverageoffsetdown_
			#define getIndexArraySize_f getindexarraysize_
			#define getIndexArray_f getindexarray_
			#define offoutliers_f offoutliers_
			#define setDistance_f setdistance_
			#define setLocationAcrossOffset_f setlocationacrossoffset_
			#define setLocationAcross_f setlocationacross_
			#define setLocationDownOffset_f setlocationdownoffset_
			#define setLocationDown_f setlocationdown_
			#define setNumberOfPoints_f setnumberofpoints_
			#define setSNR_f setsnr_
			#define setSign_f setsign_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif offoutliersmoduleFortTrans_h
