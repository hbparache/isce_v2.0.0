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





        subroutine setWidth(var)
            use correct_geoid_i2_srtmState
            implicit none
            integer var
            i_samples = var
        end
        subroutine setStdWriter(var)
            use correct_geoid_i2_srtmState
            implicit none
            integer*8 var
            stdWriter = var
        end
        subroutine setStartLatitude(var)
            use correct_geoid_i2_srtmState
            implicit none
            double precision var
            d_clat = var
        end

        subroutine setStartLongitude(var)
            use correct_geoid_i2_srtmState
            implicit none
            double precision var
            d_clon = var
        end

        subroutine setDeltaLatitude(var)
            use correct_geoid_i2_srtmState
            implicit none
            double precision var
            d_dlat = var
        end

        subroutine setDeltaLongitude(var)
            use correct_geoid_i2_srtmState
            implicit none
            double precision var
            d_dlon = var
        end

        subroutine setNumberLines(var)
            use correct_geoid_i2_srtmState
            implicit none
            integer var
            i_numlines = var
        end

        subroutine setConversionType(var)
            use correct_geoid_i2_srtmState
            implicit none
            integer var
            i_sign = var
        end

        subroutine setGeoidFilename(varString, var)
            use iso_c_binding, only: c_char
            use correct_geoid_i2_srtmState
            use fortranUtils
            implicit none
            integer*4 var
            character(kind=c_char, len=1),dimension(var),intent(in)::  varString
            character*50, parameter :: pName = "correct_geoid_i2_srtmSetState::setGeoidFilename"
            call c_to_f_string(pName, varString, var, a_geoidfile, len_geoidfile)
        end


