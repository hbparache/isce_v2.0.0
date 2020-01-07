c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c Copyright: 2013 to the present, California Institute of Technology.
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
c Authors: Piyush Agram, Giangi Sacco
c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





        module getpegState
            double precision, allocatable, dimension(:,:) ::  xyz
            integer dim1_xyz, dim2_xyz
            double precision, allocatable, dimension(:,:) ::  vxyz
            integer dim1_vxyz, dim2_vxyz
            integer*8 ptStdWriter
            double precision GM
            double precision major
            double precision eccentricitySquared
            double precision pegLatitude
            double precision pegLongitude
            double precision pegHeading
            double precision pegRadiusOfCurvature
            double precision have
            double precision vel
        end module 
