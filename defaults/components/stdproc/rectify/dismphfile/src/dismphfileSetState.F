!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
! Copyright: 2011 to the present, California Institute of Technology.
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





        subroutine setLength(varInt)
            use dismphfileState
            implicit none
            integer varInt
            len = varInt
        end

        subroutine setFirstLine(varInt)
            use dismphfileState
            implicit none
            integer varInt
            ifirst = varInt
        end

        subroutine setNumberLines(varInt)
            use dismphfileState
            implicit none
            integer varInt
            lines = varInt
        end

        subroutine setFlipFlag(varInt)
            use dismphfileState
            implicit none
            integer varInt
            iflip = varInt
        end

        subroutine setScale(varInt)
            use dismphfileState
            implicit none
            real*4 varInt
            scale = varInt
        end

        subroutine setExponent(varInt)
            use dismphfileState
            implicit none
            real*4 varInt
            expo = varInt
        end

