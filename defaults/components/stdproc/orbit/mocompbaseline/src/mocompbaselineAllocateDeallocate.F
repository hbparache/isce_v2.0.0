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





        subroutine allocate_sch1(dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2
            dim1_sch1 = dim2
            dim2_sch1 = dim1
            allocate(sch1(dim2,dim1))
        end

        subroutine deallocate_sch1()
            use mocompbaselineState
            deallocate(sch1)
        end

        subroutine allocate_sch2(dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2
            dim1_sch2 = dim2
            dim2_sch2 = dim1
            allocate(sch2(dim2,dim1))
        end

        subroutine deallocate_sch2()
            use mocompbaselineState
            deallocate(sch2)
        end

        subroutine allocate_s1(dim1)
            use mocompbaselineState
            implicit none
            integer dim1
            dim1_s1 = dim1
            allocate(s1(dim1))
        end

        subroutine deallocate_s1()
            use mocompbaselineState
            deallocate(s1)
        end

        subroutine allocate_is1(dim1)
            use mocompbaselineState
            implicit none
            integer dim1
            dim1_is1 = dim1
            allocate(is1(dim1))
        end

        subroutine deallocate_is1()
            use mocompbaselineState
            deallocate(is1)
        end

        subroutine allocate_s2(dim1)
            use mocompbaselineState
            implicit none
            integer dim1
            dim1_s2 = dim1
            allocate(s2(dim1))
        end

        subroutine deallocate_s2()
            use mocompbaselineState
            deallocate(s2)
        end

        subroutine allocate_is2(dim1)
            use mocompbaselineState
            implicit none
            integer dim1
            dim1_is2 = dim1
            allocate(is2(dim1))
        end

        subroutine deallocate_is2()
            use mocompbaselineState
            deallocate(is2)
        end

        subroutine allocate_baselineArray(dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2
            dim1_baselineArray = dim2
            dim2_baselineArray = dim1
            allocate(baselineArray(dim2,dim1))
        end

        subroutine deallocate_baselineArray()
            use mocompbaselineState
            deallocate(baselineArray)
        end
        subroutine allocate_midPointArray(dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2
            dim1_midPointArray = dim2
            dim2_midPointArray = dim1
            allocate(midPointArray(dim2,dim1))
        end

        subroutine deallocate_midPointArray()
            use mocompbaselineState
            deallocate(midPointArray)
        end

        subroutine allocate_midPointArray1(dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2
            dim1_midPointArray1 = dim2
            dim2_midPointArray1 = dim1
            allocate(midPointArray1(dim2,dim1))
        end

        subroutine deallocate_midPointArray1()
            use mocompbaselineState
            deallocate(midPointArray1)
        end

        subroutine allocate_midPointArray2(dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2
            dim1_midPointArray2 = dim2
            dim2_midPointArray2 = dim1
            allocate(midPointArray2(dim2,dim1))
        end

        subroutine deallocate_midPointArray2()
            use mocompbaselineState
            deallocate(midPointArray2)
        end

        subroutine allocate_baselineArray1(dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2
            dim1_baselineArray1 = dim2
            dim2_baselineArray1 = dim1
            allocate(baselineArray1(dim2,dim1))
        end

        subroutine deallocate_baselineArray1()
            use mocompbaselineState
            deallocate(baselineArray1)
        end

        subroutine allocate_baselineArray2(dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2
            dim1_baselineArray2 = dim2
            dim2_baselineArray2 = dim1
            allocate(baselineArray2(dim2,dim1))
        end

        subroutine deallocate_baselineArray2()
            use mocompbaselineState
            deallocate(baselineArray2)
        end

        subroutine allocate_schArray(dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2
            dim1_schArray = dim2
            dim2_schArray = dim1
            allocate(schArray(dim2,dim1))
        end

        subroutine deallocate_schArray()
            use mocompbaselineState
            deallocate(schArray)
        end

        subroutine allocate_scArray(dim1,dim2)
            use mocompbaselineState
            implicit none
            integer dim1,dim2
            dim1_scArray = dim2
            dim2_scArray = dim1
            allocate(scArray(dim2,dim1))
        end

        subroutine deallocate_scArray()
            use mocompbaselineState
            deallocate(scArray)
        end
