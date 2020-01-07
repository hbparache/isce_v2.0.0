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





        module correctState
            double precision, allocatable, dimension(:) ::  s_mocomp
            integer dim1_s_mocompArray
            double precision, allocatable, dimension(:,:) ::  mocbase
            integer dim1_mocbaseArray, dim2_mocbaseArray
            integer is_mocomp
            double precision major
            double precision eccentricitySquared
            integer length
            integer width
            double precision rspace
            double precision r0
            double precision height
            double precision rcurv
            real*4 vel
            integer Nrnglooks
            integer Nazlooks
            double precision peglat
            double precision peglon
            double precision peghdg
            double precision, dimension(:), allocatable :: dopcoeff
            integer :: ndop
            double precision prf
            double precision wvl
            double precision, allocatable, dimension(:,:) ::  midpoint
            integer dim1_midpoint, dim2_midpoint
            double precision, allocatable, dimension(:,:) ::  s1sch
            integer dim1_s1sch, dim2_s1sch
            double precision, allocatable, dimension(:,:) ::  s2sch
            integer dim1_s2sch, dim2_s2sch
            double precision, allocatable, dimension(:,:) ::  smsch
            integer dim1_smsch, dim2_smsch
            integer ilrl
        end module 
