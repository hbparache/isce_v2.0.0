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
            use resamp_onlyState
            implicit none
            integer*8 varInt
            ptStdWriter = varInt
        end

        subroutine setNumberFitCoefficients(varInt)
            use resamp_onlyState
            implicit none
            integer varInt
            i_ma = varInt
        end

        subroutine setNumberRangeBin(varInt)
            use resamp_onlyState
            implicit none
            integer varInt
            npl = varInt
        end

        subroutine setNumberLines(varInt)
            use resamp_onlyState
            implicit none
            integer varInt
            nl = varInt
        end

        subroutine setFirstLineOffset(varInt)
            use resamp_onlyState
            implicit none
            integer varInt
            istoff = varInt
        end

        subroutine setRadarWavelength(varInt)
            use resamp_onlyState
            implicit none
            real*4 varInt
            WVL = varInt
        end

        subroutine setSlantRangePixelSpacing(varInt)
            use resamp_onlyState
            implicit none
            real*4 varInt
            SLR = varInt
        end

        subroutine setDopplerCentroidCoefficients(array1d,dim1)
            use resamp_onlyState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                dopplerCoefficients(i) = array1d(i)
            enddo
        end

        subroutine setLocationAcross1(array1d,dim1)
            use resamp_onlyState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                r_ranposV(i) = array1d(i)
            enddo
        end

        subroutine setLocationAcrossOffset1(array1d,dim1)
            use resamp_onlyState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                r_ranoffV(i) = array1d(i)
            enddo
        end

        subroutine setLocationDown1(array1d,dim1)
            use resamp_onlyState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                r_azposV(i) = array1d(i)
            enddo
        end

        subroutine setLocationDownOffset1(array1d,dim1)
            use resamp_onlyState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                r_azoffV(i) = array1d(i)
            enddo
        end

        subroutine setSNR1(array1d,dim1)
            use resamp_onlyState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                r_sigV(i) = array1d(i)
            enddo
        end

        subroutine setLocationAcross2(array1d,dim1)
            use resamp_onlyState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                r_ranpos2V(i) = array1d(i)
            enddo
        end

        subroutine setLocationAcrossOffset2(array1d,dim1)
            use resamp_onlyState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                r_ranoff2V(i) = array1d(i)
            enddo
        end

        subroutine setLocationDown2(array1d,dim1)
            use resamp_onlyState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                r_azpos2V(i) = array1d(i)
            enddo
        end

        subroutine setLocationDownOffset2(array1d,dim1)
            use resamp_onlyState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                r_azoff2V(i) = array1d(i)
            enddo
        end

        subroutine setSNR2(array1d,dim1)
            use resamp_onlyState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                r_sig2V(i) = array1d(i)
            enddo
        end

