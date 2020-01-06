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
// Authors: Piyush Agram, Giangi Sacco
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





#ifndef getpegmoduleFortTrans_h
#define getpegmoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
			#define allocate_vxyz_f allocate_vxyz_
			#define allocate_xyz_f allocate_xyz_
			#define deallocate_vxyz_f deallocate_vxyz_
			#define deallocate_xyz_f deallocate_xyz_
			#define getAverageHeight_f getaverageheight_
			#define getProcVelocity_f getprocvelocity_
			#define getPegHeading_f getpegheading_
			#define getPegLatitude_f getpeglatitude_
			#define getPegLongitude_f getpeglongitude_
			#define getPegRadiusOfCurvature_f getpegradiusofcurvature_
			#define setEllipsoidEccentricitySquared_f setellipsoideccentricitysquared_
			#define setEllipsoidMajorSemiAxis_f setellipsoidmajorsemiaxis_
			#define setPosition_f setposition_
			#define setVelocity_f setvelocity_
			#define setStdWriter_f setstdwriter_
			#define setPlanetGM_f setplanetgm_
			#define getpeg_f getpeg_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif getpegmoduleFortTrans_h
