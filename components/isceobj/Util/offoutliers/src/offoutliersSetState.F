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
            use offoutliersState
            implicit none
            integer*8 varInt
            ptStdWriter = varInt
        end

        subroutine setNumberOfPoints(varInt)
            use offoutliersState
            implicit none
            integer varInt
            MP = varInt
        end

        subroutine setLocationAcross(array1d,dim1)
            use offoutliersState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                xd(i) = array1d(i)
            enddo
        end

        subroutine setLocationAcrossOffset(array1d,dim1)
            use offoutliersState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                acshift(i) = array1d(i)
            enddo
        end

        subroutine setLocationDown(array1d,dim1)
            use offoutliersState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                yd(i) = array1d(i)
            enddo
        end

        subroutine setLocationDownOffset(array1d,dim1)
            use offoutliersState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                dnshift(i) = array1d(i)
            enddo
        end

        subroutine setDistance(varInt)
            use offoutliersState
            implicit none
            real*4 varInt
            distance = varInt
        end

        subroutine setSign(array1d,dim1)
            use offoutliersState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                sig(i) = array1d(i)
            enddo
        end

        subroutine setSNR(array1d,dim1)
            use offoutliersState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                s(i) = array1d(i)
            enddo
        end

