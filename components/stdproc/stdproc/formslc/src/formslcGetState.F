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





        subroutine getMocompPosition(array2d,dim1,dim2)
            use arraymodule
            use formslcStateSoi
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2d
                do j = 1, dim2
                    array2d(j,1) = t_ mocomp(j)
                    array2d(j,2) = s_ mocomp(j)
                enddo
                deallocate(t_mocomp)
                deallocate(s_mocomp)
        end

        subroutine getMocompIndex(array1d,dim1)
            use arraymodule
            use formslcStateSoi
            implicit none
            integer dim1,i
            integer, dimension(dim1):: array1d
            do i = 1, dim1
                array1d(i) = i_mocomp(i)
            enddo
            deallocate(i_mocomp)
        end

        subroutine getMocompPositionSize(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            varInt = mocompPositionSize
        end
	
        subroutine getStartingRange(varDbl)
	    use formslcStateSoi
	    implicit none
	    double precision varDbl
	    varDbl = slcr01
	end
