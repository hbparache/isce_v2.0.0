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





        subroutine getBaseline(array2dT,dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    array2dT(i,j) = baselineArray(i,j)
                enddo
            enddo
        end

        subroutine getMidpoint(array2dT,dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    array2dT(i,j) = midPointArray(i,j)
                enddo
            enddo
        end

        subroutine getMidpoint1(array2dT,dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    array2dT(i,j) = midPointArray1(i,j)
                enddo
            enddo
        end

        subroutine getMidpoint2(array2dT,dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    array2dT(i,j) = midPointArray2(i,j)
                enddo
            enddo
        end

        subroutine getBaseline1(array2dT,dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    array2dT(i,j) = baselineArray1(i,j)
                enddo
            enddo
        end

        subroutine getBaseline2(array2dT,dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    array2dT(i,j) = baselineArray2(i,j)
                enddo
            enddo
        end

        subroutine getSch(array2dT,dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    array2dT(i,j) = schArray(i,j)
                enddo
            enddo
        end

        subroutine getSc(array2dT,dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    array2dT(i,j) = scArray(i,j)
                enddo
            enddo
        end

        subroutine get_dim1_s1(dim1)
            use mocompbaselineState
            implicit none
            integer dim1
            dim1 = dim1_s1
        end
