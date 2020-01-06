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





        subroutine setWidth(varInt)
            use readOrbitPulseERSState
            implicit none
            integer varInt
            width = varInt
        end

        subroutine setICUoffset(varInt)
            use readOrbitPulseERSState
            implicit none
            integer varInt
            ICUoffset = varInt
        end

        subroutine setNumberLines(varInt)
            use readOrbitPulseERSState
            implicit none
            integer varInt
            lines = varInt
        end

        subroutine setSatelliteUTC(varInt)
            use readOrbitPulseERSState
            implicit none
            double precision varInt
            sat_utc = varInt
        end

        subroutine setPRF(varInt)
            use readOrbitPulseERSState
            implicit none
            double precision varInt
            prf = varInt
        end

        subroutine setDeltaClock(varInt)
            use readOrbitPulseERSState
            implicit none
            double precision varInt
            dICU = varInt
        end

        subroutine setEncodedBinaryTimeCode(varInt)
            use readOrbitPulseERSState
            implicit none
            integer*8 varInt
            ICUb = varInt
        end
