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





        subroutine allocate_locationAcross(dim1)
            use estimateoffsetsState
            implicit none
            integer dim1
            dim1_locationAcross = dim1
            allocate(locationAcross(dim1)) 
        end

        subroutine deallocate_locationAcross()
            use estimateoffsetsState
            deallocate(locationAcross) 
        end

        subroutine allocate_locationAcrossOffset(dim1)
            use estimateoffsetsState
            implicit none
            integer dim1
            dim1_locationAcrossOffset = dim1
            allocate(locationAcrossOffset(dim1)) 
        end

        subroutine deallocate_locationAcrossOffset()
            use estimateoffsetsState
            deallocate(locationAcrossOffset) 
        end

        subroutine allocate_locationDown(dim1)
            use estimateoffsetsState
            implicit none
            integer dim1
            dim1_locationDown = dim1
            allocate(locationDown(dim1)) 
        end

        subroutine deallocate_locationDown()
            use estimateoffsetsState
            deallocate(locationDown) 
        end

        subroutine allocate_locationDownOffset(dim1)
            use estimateoffsetsState
            implicit none
            integer dim1
            dim1_locationDownOffset = dim1
            allocate(locationDownOffset(dim1)) 
        end

        subroutine deallocate_locationDownOffset()
            use estimateoffsetsState
            deallocate(locationDownOffset) 
        end

        subroutine allocate_snrRet(dim1)
            use estimateoffsetsState
            implicit none
            integer dim1
            dim1_snrRet = dim1
            allocate(snrRet(dim1)) 
        end

        subroutine deallocate_snrRet()
            use estimateoffsetsState
            deallocate(snrRet) 
        end

