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
! Author: Piyush Agram
!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





        subroutine allocateFieldArrays(var)
            use offsetpolyState
            implicit none
            integer :: var
            numOffsets = var
            allocate(r_ranposV(var))
            allocate(r_offV(var))
            allocate(r_azposV(var))
            allocate(r_sigV(var))
        end subroutine allocateFieldArrays

        subroutine deallocateFieldArrays()
            use offsetpolyState
            implicit none
            numOffsets = 0
            deallocate(r_ranposV)
            deallocate(r_azposV)
            deallocate(r_offV)
            deallocate(r_sigV)
        end subroutine deallocateFieldArrays

        subroutine allocatePolyArray(var)
            use offsetpolyState
            implicit none

            integer :: var
            i_ma = var
            allocate(r_polyV(var))
        end subroutine allocatePolyArray

        subroutine deallocatePolyArray()
            use offsetpolyState
            implicit none
            i_ma = 0
            deallocate(r_polyV)
        end subroutine deallocatePolyArray

