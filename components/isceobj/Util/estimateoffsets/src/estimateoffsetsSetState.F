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




        subroutine setWindowSize(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            NPTS = varInt
        end

        subroutine setSearchWindowSize(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            NOFF = varInt
        end

        subroutine setZoomWindowSize(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            NDISP = varInt
        end

        subroutine setOversamplingFactor(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            NOVS = varInt
        end

        subroutine setLineLength1(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            len1 = varInt
        end

        subroutine setLineLength2(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            len2 = varInt
        end


        subroutine setFileLength1(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            lines1 = varInt
        end

        subroutine setFileLength2(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            lines2 = varInt
        end

        subroutine setFirstSampleAcross(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            isamp_s = varInt
        end

        subroutine setLastSampleAcross(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            isamp_f = varInt
        end

        subroutine setNumberLocationAcross(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            nloc = varInt
        end

        subroutine setFirstSampleDown(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            isamp_sdn = varInt
        end

        subroutine setLastSampleDown(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            isamp_fdn = varInt
        end

        subroutine setNumberLocationDown(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            nlocdn = varInt
        end

        subroutine setAcrossGrossOffset(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            ioffac = varInt
        end

        subroutine setDownGrossOffset(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            ioffdn = varInt
        end

        subroutine setFirstPRF(varInt)
            use estimateoffsetsState
            implicit none
            real*4 varInt
            prf1 = varInt
        end

        subroutine setSecondPRF(varInt)
            use estimateoffsetsState
            implicit none
            real*4 varInt
            prf2 = varInt
        end

        subroutine setIsComplex1(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            iscpx1 = varInt
        end

        subroutine setIsComplex2(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            iscpx2 = varInt
        end

        subroutine setBand1(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            band1 = varInt
        end
        
        subroutine setBand2(varInt)
            use estimateoffsetsState
            implicit none
            integer varInt
            band2 = varInt
        end

        subroutine setDebugFlag(varString, varInt)
            use estimateoffsetsState
            implicit none
            character*1 varString
            integer*4 varInt
            talk  = ''
            talk(1:varInt) = varString
        end

