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





        subroutine allocate_xyz1(dim1,dim2)
            use setmocomppathState
            implicit none
            integer dim1,dim2
            dim1_xyz1 = dim2
            dim2_xyz1 = dim1
            allocate(xyz1(dim2,dim1)) 
        end

        subroutine deallocate_xyz1()
            use setmocomppathState
            deallocate(xyz1) 
        end

        subroutine allocate_vxyz1(dim1,dim2)
            use setmocomppathState
            implicit none
            integer dim1,dim2
            dim1_vxyz1 = dim2
            dim2_vxyz1 = dim1
            allocate(vxyz1(dim2,dim1)) 
        end

        subroutine deallocate_vxyz1()
            use setmocomppathState
            deallocate(vxyz1) 
        end

        subroutine allocate_xyz2(dim1,dim2)
            use setmocomppathState
            implicit none
            integer dim1,dim2
            dim1_xyz2 = dim2
            dim2_xyz2 = dim1
            allocate(xyz2(dim2,dim1)) 
        end

        subroutine deallocate_xyz2()
            use setmocomppathState
            deallocate(xyz2) 
        end

        subroutine allocate_vxyz2(dim1,dim2)
            use setmocomppathState
            implicit none
            integer dim1,dim2
            dim1_vxyz2 = dim2
            dim2_vxyz2 = dim1
            allocate(vxyz2(dim2,dim1)) 
        end

        subroutine deallocate_vxyz2()
            use setmocomppathState
            deallocate(vxyz2) 
        end

