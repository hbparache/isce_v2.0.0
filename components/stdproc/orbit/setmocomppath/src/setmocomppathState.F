c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c Copyright: 2010 to the present, California Institute of Technology.
c ALL RIGHTS RESERVED. United States Government Sponsorship acknowledged.
c Any commercial use must be negotiated with the Office of Technology Transfer
c at the California Institute of Technology.
c 
c This software may be subject to U.S. export control laws. By accepting this
c software, the user agrees to comply with all applicable U.S. export laws and
c regulations. User has the responsibility to obtain export licenses,  or other
c export authority as may be required before exporting such information to
c foreign countries or providing access to foreign persons.
c 
c Installation and use of this software is restricted by a license agreement
c between the licensee and the California Institute of Technology. It is the
c User's responsibility to abide by the terms of the license agreement.
c
c Author: Giangi Sacco
c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





        module setmocomppathState
            double precision, allocatable, dimension(:,:) ::  xyz1
            integer dim1_xyz1, dim2_xyz1
            double precision, allocatable, dimension(:,:) ::  vxyz1
            integer dim1_vxyz1, dim2_vxyz1
            double precision, allocatable, dimension(:,:) ::  xyz2
            integer dim1_xyz2, dim2_xyz2
            double precision, allocatable, dimension(:,:) ::  vxyz2
            integer dim1_vxyz2, dim2_vxyz2
            integer*8 ptStdWriter
            double precision GM
            double precision major
            double precision eccentricitySquared
            double precision pegLatitude
            double precision pegLongitude
            double precision pegHeading
            double precision pegRadiusOfCurvature
            double precision have1
            double precision have2
            double precision vel1
            double precision vel2
        end module 
