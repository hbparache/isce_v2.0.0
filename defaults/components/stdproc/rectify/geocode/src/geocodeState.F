!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
! Copyright: 2010 to the present, California Institute of Technology.
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





        module geocodeState
            integer*8 ptStdWriter
            double precision majorSemiAxis
            double precision eccentricitySquared
            double precision min_lat
            double precision min_lon
            double precision max_lat
            double precision max_lon
            double precision peglat
            double precision peglon
            double precision peghdg
            real*4 drho
            double precision rho0
            real*4 h
            double precision ra
            real*4 vel
            real*4 fdprfs
            real*4 prf
            real*4 wvl
            double precision s0
            double precision daz
            double precision lat_first
            double precision lon_first
            double precision dlat
            double precision dlon
            integer length
            integer width
            integer nrnglooks
            integer nazlooks
            integer ipts
            integer is_mocomp
            integer demwidth
            integer demlength
            double precision, allocatable, dimension(:) ::  s_mocomp
            integer dim1_s_mocomp
            integer geowidth
            integer geolength
            double precision latSpacing
            double precision lonSpacing
            double precision geomin_lat
            double precision geomin_lon
            double precision geomax_lat
            double precision geomax_lon
            integer ilrl
        end module geocodeState 
