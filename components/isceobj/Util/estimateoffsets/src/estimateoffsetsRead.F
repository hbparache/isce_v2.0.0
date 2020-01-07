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





        module estimateoffsetsRead
            implicit none

            contains
                subroutine readCpxAmp(acc,arr,irow,band,n,carr)
                    complex, dimension(:) :: carr
                    real, dimension(:)  :: arr
                    integer*8 :: acc
                    integer :: irow,band,n,i

                    call getLineBand(acc,carr,band,irow)
                    !call getLine(acc, carr, irow)
                    do i=1,n
                        arr(i) = cabs(carr(i))
                    end do
                end subroutine readCpxAmp

                subroutine readAmp(acc,arr,irow,band,n,carr)
                    complex, dimension(:) :: carr
                    real, dimension(:) :: arr
                    integer*8 :: acc
                    integer :: irow,band,n

                    call getLineBand(acc,arr,band,irow)
                end subroutine

        end module estimateoffsetsRead 
