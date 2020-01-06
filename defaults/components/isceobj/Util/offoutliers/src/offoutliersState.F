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





        module offoutliersState
            integer*8 ptStdWriter
            integer, allocatable, dimension(:) ::  indexArray
            integer dim1_indexArray
            integer indexArraySize
            real*4 cdn
            real*4 cac
            integer MP
            double precision, allocatable, dimension(:) ::  xd
            integer dim1_xd
            double precision, allocatable, dimension(:) ::  acshift
            integer dim1_acshift
            double precision, allocatable, dimension(:) ::  yd
            integer dim1_yd
            double precision, allocatable, dimension(:) ::  dnshift
            integer dim1_dnshift
            real*4 distance
            double precision, allocatable, dimension(:) ::  sig
            integer dim1_sig
            double precision, allocatable, dimension(:) ::  s
            integer dim1_s
        end module 
