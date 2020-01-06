!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
! Copyright: 2012 to the present, California Institute of Technology.
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





        subroutine setNumberIterations(var)
            use topoState
            implicit none
            integer var
            numiter = var
        end

        subroutine setDemWidth(var)
            use topoState
            implicit none
            integer var
            idemwidth = var
        end

        subroutine setDemLength(var)
            use topoState
            implicit none
            integer var
            idemlength = var
        end

        subroutine setReferenceOrbit(array1d,dim1)
            use topoState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                s_mocomp(i) = array1d(i)
            enddo
        end

        subroutine setFirstLatitude(var)
            use topoState
            implicit none
            double precision var
            firstlat = var
        end

        subroutine setFirstLongitude(var)
            use topoState
            implicit none
            double precision var
            firstlon = var
        end

        subroutine setDeltaLatitude(var)
            use topoState
            implicit none
            double precision var
            deltalat = var
        end

        subroutine setDeltaLongitude(var)
            use topoState
            implicit none
            double precision var
            deltalon = var
        end

        subroutine setISMocomp(var)
            use topoState
            implicit none
            integer var
            is_mocomp = var
        end

        subroutine setEllipsoidMajorSemiAxis(var)
            use topoState
            implicit none
            double precision var
            major = var
        end

        subroutine setEllipsoidEccentricitySquared(var)
            use topoState
            implicit none
            double precision var
            eccentricitySquared = var
        end

        subroutine setLength(var)
            use topoState
            implicit none
            integer var
            length = var
        end

        subroutine setWidth(var)
            use topoState
            implicit none
            integer var
            width = var
        end

        subroutine setRangePixelSpacing(var)
            use topoState
            implicit none
            double precision var
            rspace = var
        end

        subroutine setRangeFirstSample(var)
            use topoState
            implicit none
            double precision var
            r0 = var
        end

        subroutine setSpacecraftHeight(var)
            use topoState
            implicit none
            double precision var
            height = var
        end

        subroutine setPlanetLocalRadius(var)
            use topoState
            implicit none
            double precision var
            rcurv = var
        end

        subroutine setBodyFixedVelocity(var)
            use topoState
            implicit none
            real*4 var
            vel = var
        end

        subroutine setNumberRangeLooks(var)
            use topoState
            implicit none
            integer var
            Nrnglooks = var
        end

        subroutine setNumberAzimuthLooks(var)
            use topoState
            implicit none
            integer var
            Nazlooks = var
        end

        subroutine setPegLatitude(var)
            use topoState
            implicit none
            double precision var
            peglat = var
        end

        subroutine setPegLongitude(var)
            use topoState
            implicit none
            double precision var
            peglon = var
        end

        subroutine setPegHeading(var)
            use topoState
            implicit none
            double precision var
            peghdg = var
        end

        subroutine setDopplerCentroidConstantTerm(var)
            use topoState
            implicit none
            double precision var
            fdprfs = var
        end

        subroutine setPRF(var)
            use topoState
            implicit none
            double precision var
            prf = var
        end

        subroutine setRadarWavelength(var)
            use topoState
            implicit none
            double precision var
            wvl = var
        end

        subroutine setLatitudePointer(var)
            use topoState
            implicit none
            integer*8 var
            latAccessor = var
        end

        subroutine setLongitudePointer(var)
            use topoState
            implicit none
            integer*8 var
            lonAccessor = var
        end

        subroutine setHeightRPointer(var)
            use topoState
            implicit none
            integer*8 var
            heightRAccessor = var
        end

        subroutine setHeightSchPointer(var)
            use topoState
            implicit none
            integer*8 var
            heightSchAccessor = var
        end

        subroutine setLosPointer(var)
            use topoState
            implicit none
            integer*8 var
            losAccessor=var
        end

        subroutine setLookSide(var)
            use topoState
            implicit none
            integer var
            ilrl = var
        end
