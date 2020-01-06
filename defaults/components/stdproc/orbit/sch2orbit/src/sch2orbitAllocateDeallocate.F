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





        subroutine allocateArrays(dim1)
            use sch2orbitState
            implicit none
            integer dim1
            len_vec = dim1
            allocate(xyz(3,len_vec))
            allocate(vxyz(3,len_vec))
            allocate(axyz(3,len_vec))
            allocate(sch(3,len_vec))
            allocate(vsch(3,len_vec))
        end

        subroutine deallocateArrays()
            use sch2orbitState
            deallocate(xyz)
            deallocate(vxyz)
            deallocate(axyz)
            deallocate(sch)
            deallocate(vsch)
        end

