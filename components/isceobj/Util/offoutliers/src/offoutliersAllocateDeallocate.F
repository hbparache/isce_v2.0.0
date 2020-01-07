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





        subroutine allocate_indexArray(dim1)
            use offoutliersState
            implicit none
            integer dim1
            dim1_indexArray = dim1
            allocate(indexArray(dim1)) 
            indexArray=0
        end

        subroutine deallocate_indexArray()
            use offoutliersState
            deallocate(indexArray) 
        end

        subroutine allocate_xd(dim1)
            use offoutliersState
            implicit none
            integer dim1
            dim1_xd = dim1
            allocate(xd(dim1))
            xd=0
        end

        subroutine deallocate_xd()
            use offoutliersState
            deallocate(xd) 
        end

        subroutine allocate_acshift(dim1)
            use offoutliersState
            implicit none
            integer dim1
            dim1_acshift = dim1
            allocate(acshift(dim1))
            acshift=0 
        end

        subroutine deallocate_acshift()
            use offoutliersState
            deallocate(acshift) 
        end

        subroutine allocate_yd(dim1)
            use offoutliersState
            implicit none
            integer dim1
            dim1_yd = dim1
            allocate(yd(dim1)) 
            yd=0
        end

        subroutine deallocate_yd()
            use offoutliersState
            deallocate(yd) 
        end

        subroutine allocate_dnshift(dim1)
            use offoutliersState
            implicit none
            integer dim1
            dim1_dnshift = dim1
            allocate(dnshift(dim1))
            dnshift=0
        end

        subroutine deallocate_dnshift()
            use offoutliersState
            deallocate(dnshift) 
        end

        subroutine allocate_sig(dim1)
            use offoutliersState
            implicit none
            integer dim1
            dim1_sig = dim1
            allocate(sig(dim1)) 
            sig=0
        end

        subroutine deallocate_sig()
            use offoutliersState
            deallocate(sig) 
        end

        subroutine allocate_s(dim1)
            use offoutliersState
            implicit none
            integer dim1
            dim1_s = dim1
            allocate(s(dim1)) 
            s = 0
        end

        subroutine deallocate_s()
            use offoutliersState
            deallocate(s) 
        end

