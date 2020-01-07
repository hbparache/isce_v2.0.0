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





        subroutine setHeader(varInt)
            use calc_dopState
            implicit none
            integer varInt
            header = varInt
        end

        subroutine setWidth(varInt)
            use calc_dopState
            implicit none
            integer varInt
            width = varInt
        end

        subroutine setLastLine(varInt)
            use calc_dopState
            implicit none
            integer varInt
            last_line = varInt
        end

        subroutine setFirstLine(varInt)
            use calc_dopState
            implicit none
            integer varInt
            first_line = varInt
        end

        subroutine setIoffset(varInt)
            use calc_dopState
            implicit none
            double precision varInt
            Ioffset = varInt
        end

        subroutine setQoffset(varInt)
            use calc_dopState
            implicit none
            double precision varInt
            Qoffset = varInt
        end

