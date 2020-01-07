!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
! Copyright: 2013 to the present, California Institute of Technology.
! ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged.
! Any commercial use must be negotiated with the Office of Technology Transfer
! at the California Institute of Technology.
! 
! This software may be subject to U.S. export control laws. By accepting this
! software, the user agrees to comply with all applicable U.S. export laws and
! regulations. User has the responsibility to obtain export licenses,  or other
! export authority as may be required before exporting such information to
! foreign countries or providing access to foreign persons.
! 
! Installation and use of this software is restricted by a license agreement
! between the licensee and the California Institute of Technology. It is the
! User's responsibility to abide by the terms of the license agreement.
!
! Author: Giangi Sacco
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





        module fdmocompState
        ! Inputs
            double precision r001 !< Starting Range [m]
            double precision prf !< Pulse repetition frequency [Hz]
            double precision wavl !< Radar wavelength [m]
            integer nlinesaz !< Number of range bins
            integer nlines !< Number of values in the vsch array
            integer ht1 !< Satellite height [m]
            double precision fs !< Range sampling rate [Hz]
            double precision rcurv !< Radius of curvature [m]
            double precision, allocatable, dimension(:) ::  fdArray !< Cubic polynomial coefficients for the Doppler polynomial as a function of range [%PRF]
            integer dim1_fdArray
            double precision, allocatable, dimension(:,:) ::  vsch!< Velocity components in SCH coordinates
            integer dim1_vsch, dim2_vsch
        ! Output 
            double precision fdnew !< Motion compensated Doppler centroid [%PRF]
            integer ilrl
        end module 
