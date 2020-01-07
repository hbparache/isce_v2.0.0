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
            use mocompbaselineState
            implicit none
            integer*8 varInt
            ptStdWriter = varInt
        end

        subroutine setSchPosition1(array2dT,dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    sch1(i,j) = array2dT(i,j)
                enddo
            enddo
        end

        subroutine setSchPosition2(array2dT,dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    sch2(i,j) = array2dT(i,j)
                enddo
            enddo
        end

        subroutine setMocompPosition1(array1d,dim1)
            use mocompbaselineState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                s1(i) = array1d(i)
            enddo
        end

        subroutine setMocompPositionIndex1(array1d,dim1)
            use mocompbaselineState
            implicit none
            integer dim1,i
            integer, dimension(dim1):: array1d
            do i = 1, dim1
                is1(i) = array1d(i)
            enddo
        end

        subroutine setMocompPosition2(array1d,dim1)
            use mocompbaselineState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                s2(i) = array1d(i)
            enddo
        end

        subroutine setMocompPositionIndex2(array1d,dim1)
            use mocompbaselineState
            implicit none
            integer dim1,i
            integer, dimension(dim1):: array1d
            do i = 1, dim1
                is2(i) = array1d(i)
            enddo
        end

        subroutine setEllipsoidMajorSemiAxis(varInt)
            use mocompbaselineState
            implicit none
            double precision varInt
            major = varInt
        end

        subroutine setEllipsoidEccentricitySquared(varInt)
            use mocompbaselineState
            implicit none
            double precision varInt
            eccentricitySquared = varInt
        end

        subroutine setPegLatitude(varInt)
            use mocompbaselineState
            implicit none
            double precision varInt
            peglat = varInt
        end

        subroutine setHeight(varInt)
            use mocompbaselineState
            implicit none
            double precision varInt
            height = varInt
        end
        subroutine setPegLongitude(varInt)
            use mocompbaselineState
            implicit none
            double precision varInt
            peglon = varInt
        end

        subroutine setPegHeading(varInt)
            use mocompbaselineState
            implicit none
            double precision varInt
            peghdg = varInt
        end

