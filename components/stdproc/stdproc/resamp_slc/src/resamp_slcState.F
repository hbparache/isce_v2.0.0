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





        module resamp_slcState
            integer*8 ptStdWriter
            integer i_ma
            integer npl
            integer nl
            integer istoff
            real*4 WVL
            real*4 SLR
            double precision, allocatable, dimension(:) ::  dopplerCoefficients
            integer dim1_dopplerCoefficients
            double precision, allocatable, dimension(:) ::  r_ranposV
            integer dim1_r_ranpos
            double precision, allocatable, dimension(:) ::  r_ranoffV
            integer dim1_r_ranoff
            double precision, allocatable, dimension(:) ::  r_azposV
            integer dim1_r_azpos
            double precision, allocatable, dimension(:) ::  r_azoffV
            integer dim1_r_azoff
            double precision, allocatable, dimension(:) ::  r_sigV
            integer dim1_r_sig
            double precision, allocatable, dimension(:) ::  r_ranpos2V
            integer dim1_r_ranpos2
            double precision, allocatable, dimension(:) ::  r_ranoff2V
            integer dim1_r_ranoff2
            double precision, allocatable, dimension(:) ::  r_azpos2V
            integer dim1_r_azpos2
            double precision, allocatable, dimension(:) ::  r_azoff2V
            integer dim1_r_azoff2
            double precision, allocatable, dimension(:) ::  r_sig2V
            integer dim1_r_sig2
            double precision, allocatable, dimension(:) ::  azimuthCarrier
            integer dim1_azimuthCarrier
            double precision, allocatable, dimension(:) ::  rangeCarrier
            integer dim1_rangeCarrier
        end module 
