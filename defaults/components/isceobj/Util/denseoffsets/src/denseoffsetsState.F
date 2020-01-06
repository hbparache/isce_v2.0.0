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





        module denseoffsetsState
            !File widths in range pixels
            integer len1, len2

            !If input data is complex
            integer iscpx1, iscpx2

            !Band numbers for input data
            integer band1, band2

            !File lengths in azimuth lines
            integer lines1, lines2
            integer isamp_s
            integer isamp_f
            integer iskipac
            integer iskipdn
            integer isamp_sdn
            integer isamp_fdn
            integer nlocdn
            integer ioffac
            integer ioffdn
            real*4 scalex
            real*4 scaley
            character*1 talk

            integer NPTSW   !Window width
            integer NPTSH   !Window Height
            integer NOFFW   !Search width
            integer NOFFH   !Search height
            integer NDISP  !Search window around maximum
            integer NOVS   !Oversampling factor 
            logical normalize !False = Acchen vs True = Ampcor-like
        end module denseoffsetsState 
