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





        subroutine setStdWriter(var)
            use mocompTSXState
            implicit none
            integer var
            stdWriter = var
        end

        subroutine setNumberRangeBins(var)
            use mocompTSXState
            implicit none
            integer var
            nr = var
        end

        subroutine setNumberAzLines(var)
            use mocompTSXState
            implicit none
            integer var
            naz = var
        end

        subroutine setDopplerCentroidCoefficients(array1d,dim1)
            use mocompTSXState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                dopplerCentroidCoefficients(i) = array1d(i)
            enddo
        end

        subroutine setTime(array1d,dim1)
            use mocompTSXState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                time(i) = array1d(i)
            enddo
        end

        subroutine setPosition(array2dT,dim1,dim2)
            use mocompTSXState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    sch(i,j) = array2dT(i,j)
                enddo
            enddo
        end


        subroutine setPlanetLocalRadius(var)
            use mocompTSXState
            implicit none
            double precision var
            rcurv = var
        end

        subroutine setBodyFixedVelocity(var)
            use mocompTSXState
            implicit none
            double precision var
            vel = var
        end

        subroutine setSpacecraftHeight(var)
            use mocompTSXState
            implicit none
            double precision var
            ht = var
        end

        subroutine setPRF(var)
            use mocompTSXState
            implicit none
            double precision var
            prf = var
        end

        subroutine setRangeSamplingRate(var)
            use mocompTSXState
            implicit none
            double precision var
            fs = var
        end

        subroutine setRadarWavelength(var)
            use mocompTSXState
            implicit none
            double precision var
            wvl = var
        end

        subroutine setRangeFisrtSample(var)
            use mocompTSXState
            implicit none
            double precision var
            r0 = var
        end

        subroutine setLookSide(var)
            use mocompTSXState
            implicit none
            integer var
            ilrl = var
        end

