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





        subroutine getXYZPosition(array2dT,dim1)
            use sch2orbitState
            implicit none
            integer dim1,i,j
            double precision, dimension(3,dim1):: array2dT
            do i = 1, dim1
                do j = 1, 3
                    array2dT(j,i) = xyz(j,i)
                enddo
            enddo
        end

        subroutine getXYZVelocity(array2dT,dim1)
            use sch2orbitState
            implicit none
            integer dim1,i,j
            double precision, dimension(3,dim1):: array2dT
            do i = 1, dim1
                do j = 1, 3
                    array2dT(j,i) = vxyz(j,i)
                enddo
            enddo
        end

        subroutine getXYZGravitationalAcceleration(array2dT,dim1)
            use sch2orbitState
            implicit none
            integer dim1,i,j
            double precision, dimension(3,dim1):: array2dT
            do i = 1, dim1
                do j = 1, 3
                    array2dT(j,i) = axyz(j,i)
                enddo
            enddo
        end

