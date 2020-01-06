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





        module mocompbaselineState
            integer*8 ptStdWriter
            double precision, allocatable, dimension(:,:) ::  sch1
            integer dim1_sch1, dim2_sch1
            double precision, allocatable, dimension(:,:) ::  sch2
            integer dim1_sch2, dim2_sch2
            double precision, allocatable, dimension(:) ::  s1
            integer dim1_s1
            integer, allocatable, dimension(:) ::  is1
            integer dim1_is1
            double precision, allocatable, dimension(:) ::  s2
            integer dim1_s2
            integer, allocatable, dimension(:) ::  is2
            integer dim1_is2
            double precision height
            double precision major
            double precision eccentricitySquared
            double precision peglat
            double precision peglon
            double precision peghdg
            double precision, allocatable, dimension(:,:) ::  baselineArray
            integer dim1_baselineArray, dim2_baselineArray
            double precision, allocatable, dimension(:,:) ::  midPointArray
            integer dim1_midPointArray, dim2_midPointArray
            double precision, allocatable, dimension(:,:) ::  midPointArray1
            integer dim1_midPointArray1, dim2_midPointArray1
            double precision, allocatable, dimension(:,:) ::  midPointArray2
            integer dim1_midPointArray2, dim2_midPointArray2
            double precision, allocatable, dimension(:,:) ::  baselineArray1
            integer dim1_baselineArray1, dim2_baselineArray1
            double precision, allocatable, dimension(:,:) ::  baselineArray2
            integer dim1_baselineArray2, dim2_baselineArray2
            double precision, allocatable, dimension(:,:) ::  schArray
            integer dim1_schArray, dim2_schArray
            double precision, allocatable, dimension(:,:) ::  scArray
            integer dim1_scArray, dim2_scArray
        end module
