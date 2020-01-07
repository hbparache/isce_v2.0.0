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





        subroutine setStdWriter(varInt)
            use geocodeState
            implicit none
            integer*8 varInt
            ptStdWriter = varInt
        end

        subroutine setEllipsoidMajorSemiAxis(varInt)
            use geocodeState
            implicit none
            double precision varInt
            majorSemiAxis = varInt
        end

        subroutine setEllipsoidEccentricitySquared(varInt)
            use geocodeState
            implicit none
            double precision varInt
            eccentricitySquared = varInt
        end

        subroutine setMinimumLatitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            min_lat = varInt
        end

        subroutine setMinimumLongitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            min_lon = varInt
        end

        subroutine setMaximumLatitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            max_lat = varInt
        end

        subroutine setMaximumLongitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            max_lon = varInt
        end

        subroutine setPegLatitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            peglat = varInt
        end

        subroutine setPegLongitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            peglon = varInt
        end

        subroutine setPegHeading(varInt)
            use geocodeState
            implicit none
            double precision varInt
            peghdg = varInt
        end

        subroutine setRangePixelSpacing(varInt)
            use geocodeState
            implicit none
            real*4 varInt
            drho = varInt
        end

        subroutine setLookSide(varInt)
            use geocodeState
            implicit none
            integer varInt
            ilrl = varInt
        end

        subroutine setRangeFirstSample(varInt)
            use geocodeState
            implicit none
            double precision varInt
            rho0 = varInt
        end

        subroutine setHeight(varInt)
            use geocodeState
            implicit none
            real*4 varInt
            h = varInt
        end

        subroutine setPlanetLocalRadius(varInt)
            use geocodeState
            implicit none
            double precision varInt
            ra = varInt
        end

        subroutine setVelocity(varInt)
            use geocodeState
            implicit none
            real*4 varInt
            vel = varInt
        end

        subroutine setDopplerCentroidConstantTerm(varInt)
            use geocodeState
            implicit none
            real*4 varInt
            fdprfs = varInt
        end

        subroutine setPRF(varInt)
            use geocodeState
            implicit none
            real*4 varInt
            prf = varInt
        end

        subroutine setRadarWavelength(varInt)
            use geocodeState
            implicit none
            real*4 varInt
            wvl = varInt
        end

        subroutine setSCoordinateFirstLine(varInt)
            use geocodeState
            implicit none
            double precision varInt
            s0 = varInt
        end

        subroutine setFirstLatitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            lat_first = varInt
        end

        subroutine setFirstLongitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            lon_first = varInt
        end

        subroutine setDeltaLatitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            dlat = varInt
        end

        subroutine setDeltaLongitude(varInt)
            use geocodeState
            implicit none
            double precision varInt
            dlon = varInt
        end

        subroutine setLength(varInt)
            use geocodeState
            implicit none
            integer varInt
            length = varInt
        end

        subroutine setWidth(varInt)
            use geocodeState
            implicit none
            integer varInt
            width = varInt
        end

        subroutine setNumberRangeLooks(varInt)
            use geocodeState
            implicit none
            integer varInt
            nrnglooks = varInt
        end

        subroutine setNumberAzimuthLooks(varInt)
            use geocodeState
            implicit none
            integer varInt
            nazlooks = varInt
        end

        subroutine setNumberPointsPerDemPost(varInt)
            use geocodeState
            implicit none
            integer varInt
            ipts = varInt
        end

        subroutine setISMocomp(varInt)
            use geocodeState
            implicit none
            integer varInt
            is_mocomp = varInt
        end

        subroutine setDemWidth(varInt)
            use geocodeState
            implicit none
            integer varInt
            demwidth = varInt
        end

        subroutine setDemLength(varInt)
            use geocodeState
            implicit none
            integer varInt
            demlength = varInt
        end

        subroutine setReferenceOrbit(array1d,dim1)
            use geocodeState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                s_mocomp(i) = array1d(i)
            enddo
        end

