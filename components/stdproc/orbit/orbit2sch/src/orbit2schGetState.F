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





        subroutine getSchPosition(array2dT,dim1,dim2)
            use orbit2schState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    array2dT(i,j) = sch(i,j)
                enddo
            enddo
        end

        subroutine getSchVelocity(array2dT,dim1,dim2)
            use orbit2schState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    array2dT(i,j) = vsch(i,j)
                enddo
            enddo
        end

        subroutine getSchGravitationalAcceleration(array2dT,dim1,dim2)
            use orbit2schState
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    array2dT(i,j) = asch(i,j)
                enddo
            enddo
        end

