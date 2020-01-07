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





#ifndef sch2orbitmoduleFortTrans_h
#define sch2orbitmoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
                        #define setStdWriter_f setstdwriter_
			#define allocateArrays_f allocatearrays_
                        #define deallocateArrays_f deallocatearrays_
			#define getXYZGravitationalAcceleration_f getxyzgravitationalacceleration_
			#define getXYZPosition_f getxyzposition_
			#define getXYZVelocity_f getxyzvelocity_
			#define sch2orbit_f sch2orbit_
			#define setRadiusOfCurvature_f setradiusofcurvature_
			#define setEllipsoidEccentricitySquared_f setellipsoideccentricitysquared_
			#define setEllipsoidMajorSemiAxis_f setellipsoidmajorsemiaxis_
			#define setOrbitPosition_f setorbitposition_
			#define setOrbitVelocity_f setorbitvelocity_
			#define setPegHeading_f setpegheading_
			#define setPegLatitude_f setpeglatitude_
			#define setPegLongitude_f setpeglongitude_
			#define setPlanetGM_f setplanetgm_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif sch2orbitmoduleFortTrans_h
