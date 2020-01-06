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





        subroutine getAzimuthSpacing(var)
            use topoState
            implicit none
            double precision var
            var = azspace
        end

        subroutine getPlanetLocalRadius(var)
            use topoState
            implicit none
            double precision var
            var = re
        end

        subroutine getSCoordinateFirstLine(var)
            use topoState
            implicit none
            double precision var
            var = s0
        end

        subroutine getSCoordinateLastLine(var)
            use topoState
            implicit none
            double precision var
            var = send
        end

        subroutine getMinimumLatitude(var)
            use topoState
            implicit none
            double precision var
            var = min_lat
        end

        subroutine getMinimumLongitude(var)
            use topoState
            implicit none
            double precision var
            var = min_lon
        end

        subroutine getMaximumLatitude(var)
            use topoState
            implicit none
            double precision var
            var = max_lat
        end

        subroutine getMaximumLongitude(var)
            use topoState
            implicit none
            double precision var
            var = max_lon
        end

        subroutine getSquintShift(array1d,dim1)
            use topoState
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                array1d(i) = squintshift(i)
            enddo
        end

        subroutine getLength(dim1)
            use topoState
            implicit none
            integer dim1
            dim1 = length
        end

