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





        subroutine getGeoWidth(varInt)
            use geocodeState
            implicit none
            integer varInt
            varInt = geowidth
        end

        subroutine getGeoLength(varInt)
            use geocodeState
            implicit none
            integer varInt
            varInt = geolength
        end

        subroutine getLatitudeSpacing(varInt)
            use geocodeState
            implicit none
            double precision varInt
            varInt = latSpacing
        end

        subroutine getLongitudeSpacing(varInt)
            use geocodeState
            implicit none
            double precision varInt
            varInt = lonSpacing
        end

        subroutine getMinimumGeoLatitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            varInt = geomin_lat
        end

        subroutine getMinimumGeoLongitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            varInt = geomin_lon
        end

        subroutine getMaximumGeoLatitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            varInt = geomax_lat
        end

        subroutine getMaxmumGeoLongitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            varInt = geomax_lon
        end

