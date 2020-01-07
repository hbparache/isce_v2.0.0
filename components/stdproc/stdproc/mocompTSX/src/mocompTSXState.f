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





        module mocompTSXState
            integer stdWriter
            integer nr
            integer naz
            double precision, allocatable, dimension(:) ::  dopplerCentroidCoefficients
            integer dim1_dopplerCentroidCoefficients
            double precision, allocatable, dimension(:) ::  time
            integer dim1_time
            double precision, allocatable, dimension(:,:) ::  sch
            integer dim1_sch, dim2_sch
            double precision rcurv
            double precision vel
            double precision ht
            double precision prf
            double precision fs
            double precision wvl
            double precision r0
            integer dim1_i_mocomp
            integer mocompPositionSize
            integer ilrl
            double precision adjustr0
        end module 
