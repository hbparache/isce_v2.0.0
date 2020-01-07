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





#ifndef geocodemoduleFortTrans_h
#define geocodemoduleFortTrans_h

	#if defined(NEEDS_F77_TRANSLATION)

		#if defined(F77EXTERNS_LOWERCASE_TRAILINGBAR)
            #define setStdWriter_f setstdwriter_
			#define allocate_s_mocomp_f allocate_s_mocomp_
			#define deallocate_s_mocomp_f deallocate_s_mocomp_
			#define geocode_f geocode_
			#define getGeoLength_f getgeolength_
			#define getGeoWidth_f getgeowidth_
			#define getLatitudeSpacing_f getlatitudespacing_
			#define getLongitudeSpacing_f getlongitudespacing_
			#define getMaximumGeoLatitude_f getmaximumgeolatitude_
			#define getMaxmumGeoLongitude_f getmaxmumgeolongitude_
			#define getMinimumGeoLatitude_f getminimumgeolatitude_
			#define getMinimumGeoLongitude_f getminimumgeolongitude_
			#define setDeltaLatitude_f setdeltalatitude_
			#define setDeltaLongitude_f setdeltalongitude_
			#define setDemLength_f setdemlength_
			#define setDemWidth_f setdemwidth_
                        #define setLookSide_f setlookside_
			#define setDopplerCentroidConstantTerm_f setdopplercentroidconstantterm_
			#define setEllipsoidEccentricitySquared_f setellipsoideccentricitysquared_
			#define setEllipsoidMajorSemiAxis_f setellipsoidmajorsemiaxis_
			#define setFirstLatitude_f setfirstlatitude_
			#define setFirstLongitude_f setfirstlongitude_
			#define setHeight_f setheight_
			#define setISMocomp_f setismocomp_
			#define setLength_f setlength_
			#define setMaximumLatitude_f setmaximumlatitude_
			#define setMaximumLongitude_f setmaximumlongitude_
			#define setMinimumLatitude_f setminimumlatitude_
			#define setMinimumLongitude_f setminimumlongitude_
			#define setNumberAzimuthLooks_f setnumberazimuthlooks_
			#define setNumberPointsPerDemPost_f setnumberpointsperdempost_
			#define setNumberRangeLooks_f setnumberrangelooks_
			#define setPRF_f setprf_
			#define setPegHeading_f setpegheading_
			#define setPegLatitude_f setpeglatitude_
			#define setPegLongitude_f setpeglongitude_
			#define setPlanetLocalRadius_f setplanetlocalradius_
			#define setRadarWavelength_f setradarwavelength_
			#define setRangeFirstSample_f setrangefirstsample_
			#define setRangePixelSpacing_f setrangepixelspacing_
			#define setReferenceOrbit_f setreferenceorbit_
			#define setSCoordinateFirstLine_f setscoordinatefirstline_
			#define setVelocity_f setvelocity_
			#define setWidth_f setwidth_
		#else
			#error Unknown translation for FORTRAN external symbols
		#endif

	#endif

#endif geocodemoduleFortTrans_h
