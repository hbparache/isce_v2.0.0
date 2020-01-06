!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
! Copyright: 2013 to the present, California Institute of Technology.
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





        subroutine setWidth(var)
            use upsampledemState
            implicit none
            integer var
            i_samples = var
        end
        subroutine setStdWriter(var)
            use upsampledemState
            implicit none
            integer*8 var
            stdWriter = var
        end
        subroutine setXFactor(var)
            use upsampledemState
            implicit none
            integer var
            i_xfactor = var
        end

        subroutine setYFactor(var)
            use upsampledemState
            implicit none
            integer var
            i_yfactor = var
        end

        subroutine setNumberLines(var)
            use upsampledemState
            implicit none
            integer var
            i_numlines = var
        end

        subroutine setPatchSize(var)
            use upsampledemState
            implicit none
            integer var
            i_patch = var
        end

