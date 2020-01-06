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




        subroutine setStdWriter(varInt)
            use formslcStateSoi
            implicit none
            integer*8 varInt
            ptStdWriter = varInt
        end

        subroutine setNumberGoodBytes(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            ngood = varInt
        end

        subroutine setNumberBytesPerLine(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            nbytes = varInt
        end

        subroutine setFirstLine(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            ifirstline = varInt
        end

        subroutine setNumberValidPulses(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            na_valid = varInt
        end

        subroutine setFirstSample(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            ifirstpix = varInt
        end

        subroutine setNumberPatches(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            npatches = varInt
        end

        subroutine setStartRangeBin(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            ifirstrgsave = varInt
        end

        subroutine setNumberRangeBin(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            nrange = varInt
        end

        subroutine setNumberAzimuthLooks(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            nlooks = varInt
        end

        subroutine setRangeChirpExtensionPoints(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            nextend = varInt
        end

        subroutine setAzimuthPatchSize(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            nazpatch = varInt
        end

        subroutine setLookSide(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            ilrl = varInt
        end

        subroutine setOverlap(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            overlap = varInt
        end

        subroutine setRanfftov(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            ranfftov = varInt
        end

        subroutine setRanfftiq(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            ranfftiq = varInt
        end

        subroutine setDebugFlag(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            iflag = varInt
        end

        subroutine setCaltoneLocation(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            caltone1 = varInt
        end

        subroutine setPlanetLocalRadius(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            rcurv = varInt
        end

        subroutine setBodyFixedVelocity(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            vel1 = varInt
        end

        subroutine setSpacecraftHeight(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            ht1 = varInt
        end

        subroutine setPRF(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            prf1 = varInt
        end

        subroutine setInPhaseValue(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            xmi1 = varInt
        end

        subroutine setQuadratureValue(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            xmq1 = varInt
        end

        subroutine setAzimuthResolution(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            azres = varInt
        end

        subroutine setRangeSamplingRate(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            fs = varInt
        end

        subroutine setChirpSlope(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            slope = varInt
        end

        subroutine setRangePulseDuration(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            pulsedur = varInt
        end

        subroutine setRadarWavelength(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            wavl = varInt
        end

        subroutine setRangeFirstSample(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            rawr001 = varInt
        end

        subroutine setRangeSpectralWeighting(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            rhww = varInt
        end

        subroutine setSpectralShiftFraction(varInt)
            use formslcStateSoi
            implicit none
            double precision varInt
            pctbw = varInt
        end

        subroutine setIMRC1(varInt)
            use formslcStateSoi
            implicit none
            integer*8 varInt
            imrc1Accessor = varInt
        end

        subroutine setIMMocomp(varInt)
            use formslcStateSoi
            implicit none
            integer*8 varInt
            immocompAccessor = varInt
        end

        subroutine setIMRCAS1(varInt)
            use formslcStateSoi
            implicit none
            integer*8 varInt
            imrcas1Accessor = varInt
        end

        subroutine setIMRCRM1(varInt)
            use formslcStateSoi
            implicit none
            integer*8 varInt
            imrcrm1Accessor = varInt
        end

        subroutine setTransDat(varInt)
            use formslcStateSoi
            implicit none
            integer*8 varInt
            transAccessor = varInt
        end

        subroutine setIQFlip(varString, varInt)
            use formslcStateSoi
            use fortranUtils
            implicit none
            integer*4 varInt
            character*(varInt) varString
            !IQFlip is declared as character*1 in formslcStateSoi
            if( varInt .gt. 1 ) then
                !Write a message to Fortran logfile.
                !Should call this subroutine once at the beginning of processing.
                !Need to write that routine.  It doesn't hurt to call it multiple
                !times, though, so until the routine is written call when needed.
                call set_stdoel_units()
                write(UNIT_LOG,*) 
     +          "formslcSetState.setIQFlip: ",
     +          "length of input variable varString exceeds length ",
     +          "of receiving variable IQFlip(1)."
                write(UNIT_LOG,*) "Truncating varString to fit = ", varString(1:1)
            endif
            iqflip = varString(1:1)
        end

        subroutine setDeskewFlag(varString, varInt)
            use formslcStateSoi
            use fortranUtils
            implicit none
            integer*4 varInt
            character*(varInt) varString
            !deskew is declared as character*1 in formslcStateSoi
            if( varInt .gt. 1 ) then
                !Write a message to Fortran logfile.
                !Should call this subroutine once at the beginning of processing.
                !Need to write that routine.  It doesn't hurt to call it multiple
                !times, though, so until the routine is written call when needed.
                call set_stdoel_units()
                write(UNIT_LOG,*) 
     +          "formslcSetState.setDeskewFlag: ",
     +          "length of input variable varString exceeds length ",
     +          "of receiving variable, deskew(1)."
                write(UNIT_LOG,*) "Truncating varString to fit = ",  varString(1:1)
            endif
            deskew = varString(1:1)
        end

        subroutine setSecondaryRangeMigrationFlag(varString, varInt)
            use formslcStateSoi
            use fortranUtils
            implicit none
            integer*4 varInt
            character*(varInt) varString
            !srm is declared as character*1 in formslcStateSoi
            if( varInt .gt. 1 ) then
                !Write a message to Fortran logfile.
                !Should call this subroutine once at the beginning of processing.
                !Need to write that routine.  It doesn't hurt to call it multiple
                !times, though, so until the routine is written call when needed.
                call set_stdoel_units()
                write(UNIT_LOG,*) 
     +          "formslcSetState.setSecondaryRangeMigrationFlag: ",
     +          "length of input variable varString exceeds length ",
     +          "of receiving variable srm(1)."
                write(UNIT_LOG,*) "Truncating varString to fit = ", varString(1:1)
            endif
            srm = varString(1:1)
        end

        subroutine setPosition(array2dT,dim1,dim2)
            use formslcStateSoi
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    sch(i,j) = array2dT(i,j)
                enddo
            enddo
        end

        subroutine setVelocity(array2dT,dim1,dim2)
            use formslcStateSoi
            implicit none
            integer dim1,dim2,i,j
            double precision, dimension(dim2,dim1):: array2dT
            do i = 1, dim2
                do j = 1, dim1
                    vsch(i,j) = array2dT(i,j)
                enddo
            enddo
        end

        subroutine setTime(array1d,dim1)
            use formslcStateSoi
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                time(i) = array1d(i)
            enddo
        end

        subroutine setDopplerCentroidCoefficients(array1d,dim1)
            use formslcStateSoi
            implicit none
            integer dim1,i
            double precision, dimension(dim1):: array1d
            do i = 1, dim1
                dopplerCoefficients(i) = array1d(i)
            enddo
        end

        subroutine setPegPoint(lat,lon,hdg)
            use formslcStateSoi
            implicit none
            double precision :: lat,lon,hdg
            peg%r_lat = lat
            peg%r_lon = lon
            peg%r_hdg = hdg
        end subroutine setPegPoint

        subroutine setEllipsoid(a,e2)
            use formslcStateSoi
            implicit none
            double precision :: a, e2
            elp%r_a = a
            elp%r_e2 = e2
        end subroutine setEllipsoid

        subroutine setPlanet(spin,gm)
            use formslcStateSoi
            implicit none
            double precision :: spin,gm
            pln%r_spindot = spin
            pln%r_gm = gm
        end subroutine setPlanet

	subroutine setSlcWidth(varInt)
            use formslcStateSoi
            implicit none
            integer varInt
            nrangeout = varInt
	end

        subroutine setStartingRange(varDbl)
            use formslcStateSoi
            implicit none
            double precision varDbl
            rawr01 = varDbl
        end

        !KK,ML 2013-07-15
        subroutine setShift(varDbl)
            use formslcStateSoi
            implicit none
            double precision varDbl
            shift = varDbl
        end
        !KK,ML

