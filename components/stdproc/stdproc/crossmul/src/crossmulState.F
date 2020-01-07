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





        module crossmulState
        use, intrinsic:: iso_c_binding

            type, bind(C) :: crossmulType
                integer(C_INT) :: na    !c Number across in range
                integer(C_INT) :: nd    !c Number down in azimuth
                real(C_DOUBLE)::  scale  !c Scaling the numbers numerically
                integer (C_INT):: looksac          !c Looks across
                integer (C_INT):: looksdn          !c Looks down
                integer (C_INT):: blocksize        !c Number of azimuth lines in a block
            end type crossmulType
        end module crossmulState
