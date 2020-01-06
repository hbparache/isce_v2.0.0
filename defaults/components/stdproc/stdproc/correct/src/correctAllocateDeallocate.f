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





        subroutine allocate_s_mocompArray(dim1)
            use correctState
            implicit none
            integer dim1
            dim1_s_mocompArray = dim1
            allocate(s_mocomp(dim1)) 
        end

        subroutine deallocate_s_mocompArray()
            use correctState
            deallocate(s_mocomp) 
        end

        subroutine allocate_mocbaseArray(dim1,dim2)
            use correctState
            implicit none
            integer dim1,dim2
            dim1_mocbaseArray = dim2
            dim2_mocbaseArray = dim1
            allocate(mocbase(dim2,dim1)) 
        end

        subroutine deallocate_mocbaseArray()
            use correctState
            deallocate(mocbase) 
        end

        subroutine allocate_midpoint(dim1,dim2)
            use correctState
            implicit none
            integer dim1,dim2
            dim1_midpoint = dim2
            dim2_midpoint = dim1
            allocate(midpoint(dim2,dim1)) 
        end

        subroutine deallocate_midpoint()
            use correctState
            deallocate(midpoint) 
        end

        subroutine allocate_s1sch(dim1,dim2)
            use correctState
            implicit none
            integer dim1,dim2
            dim1_s1sch = dim2
            dim2_s1sch = dim1
            allocate(s1sch(dim2,dim1)) 
        end

        subroutine deallocate_s1sch()
            use correctState
            deallocate(s1sch) 
        end

        subroutine allocate_s2sch(dim1,dim2)
            use correctState
            implicit none
            integer dim1,dim2
            dim1_s2sch = dim2
            dim2_s2sch = dim1
            allocate(s2sch(dim2,dim1)) 
        end

        subroutine deallocate_s2sch()
            use correctState
            deallocate(s2sch) 
        end

        subroutine allocate_smsch(dim1,dim2)
            use correctState
            implicit none
            integer dim1,dim2
            dim1_smsch = dim2
            dim2_smsch = dim1
            allocate(smsch(dim2,dim1)) 
        end

        subroutine deallocate_smsch()
            use correctState
            deallocate(smsch) 
        end

        subroutine allocate_dopcoeff(dim1)
            use correctState
            implicit none
            integer dim1
            ndop = dim1
            allocate(dopcoeff(dim1))
        end

        subroutine deallocate_dopcoeff()
            use correctState
            deallocate(dopcoeff)
        end

