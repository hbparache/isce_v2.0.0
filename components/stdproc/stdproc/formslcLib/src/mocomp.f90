!c mocomp - apply mocomp to move data to a desired reference
!c temporary subroutine for proof of concept
!c  modified for sch definition 1-dec-08 by hz
!c  save phase gradient added 12sep09

      subroutine mocomp(nnn,nlinesaz,irec,r001,delr,ht1,re,wvl,vel, &
          fd,fdd,fddd,focuscorr,numLines,ilrl, rawr001)

!c inputs
!c
!c nnn - array size in range bins
!c nlinesaz - array size in azimuth lines
!c irec - starting line number in patch
!c r001 - near range, m
!c delr - range spacing in m
!c ht1 - height of reference track, m
!c re  - local earth radius, m
!c wvl - wavelength
!c vel - velocity
!c fd   - Doppler constant term
!c fdd  - Doppler vs Range
!c fddd - Doppler vs Range^2
!c outputs
!c focuscorr - focus correction (2nd order) term B/rho
!c numLines  - number of lines processed
!c ilrl      - Left [1], Right [-1] Look side of the satellite
!c rawr001   - If the range compressed line starts at a diff range

      use arraymodule
      use fortranUtils
      use uniform_interp

      implicit none
      include 'omp_lib.h'

      integer MAXDECFACTOR      ! maximum lags in interpolation kernels
      parameter(MAXDECFACTOR=8192)                        
    
      integer MAXINTKERLGH      ! maximum interpolation kernel length
      parameter (MAXINTKERLGH=8)
      
      integer MAXINTLGH         ! maximum interpolation kernel array size
      parameter (MAXINTLGH=MAXINTKERLGH*MAXDECFACTOR)

      complex*8 c
      complex*8, allocatable :: rangeline(:)        !One line of data
      integer*4 MAX_SIZE_ARRAYS,RANGELINE_SIZE       
      parameter(RANGELINE_SIZE = 32768)

      !Beta is angle between ideal satellite and zero doppler position at 
      ! the center of the local sphere [Fig 1]
      real*8 sinbeta,cosbeta, tanbeta
      real*8 betadot        !Angular velocity

      !"b" is the mocomp baseline. The distance between the ideal satellite
      ! and the actual satellite at midrange. Arg is the angle subtended by
      ! b at a midrange target.
      real*8 b,cosarg

      !Delta is the squint angle to the target when satellite position 
      ! is projected on to the reference path  [Fig 3]
      real*8 cosdelta,sindelta,tandelta
      real*8 rho,rhoprime
      real*8 r001,delr             !Starting range, range pixel spacing
      real*8 ht1,re                !Reference height, Radius of local sphere
      real*8 phase,wvl         !Wavelength
      real*8 focuscorr             !correction factor for azimuth compression
      real*8 vel           !ideal satellite velocity
      real*8 freq,shiftphase
      real*8 frac,bin
      real*8, allocatable :: phasemoc(:) !Array for storing phase corrections

      !Actual satellite position
      real*8 s0,c0,h0

      !Raw ranges
      real*8, intent(in), optional :: rawr001
      real*8 ::  rc01
      !Ideal satellite position
      ! c=0 and h is fixed
      real*8 s_sc

      !Alpha is angle between ideal satellite and target at the center of the 
      ! local sphere.  [Fig 1] 
      real*8 cosalpha,sinalpha
      real*8 cosdeltaalpha    !cos(delta+alpha)
   
      real*8 f0 
      !Gamma is the angle between target and ideal satellite at corresponding 
      ! zero doppler position at the center of local sphere [Fig 1] 
      real*8 cosgamma,singamma

      !Alphaprime is the angle between the actual satellite and target at the 
      ! center of the local sphere [Fig 4]
      real*8 sinalphaprime, cosalphaprime

      !Epsilon is the angle between the actual satellite and the ideal satellite
      ! along the line of constant doppler [Fig 3., labelled segment d]
      real*8 sinepsilon, cosepsilon

      !Doppler coefficients
      real*8 fd,fdd,fddd

      !Temporary products stored for azimuth compression
      real*8, allocatable :: s_scsave(:),b_save(:),rho_save(:),time_save(:)

      !For the interpolator
      real*4 fintp
!c      integer, allocatable :: rec(:)    

      ! Local variables  
      integer i,j,lines,line,irec,nnn,nlinesaz,ibin,irange,iline,numLines
      integer :: i_intplength,i_filtercoef, i_decfactor, i_weight
      real*8  r_pedestal, r_relfiltlen, r_beta,r_delay
      double precision :: r_filter(0:MAXINTLGH)
      real*8  pi,sol
      integer ilrl
      integer firsttime
      data firsttime/1/
      save firsttime, r_delay, i_decfactor, i_intplength

      common /fintp/ fintp(0:MAXINTLGH)

      ! jng it turned out that when stitching frames together the
      ! MAX_SIZE_ARRAYS = 100000 is not sufficient. use mocompSize
      ! defined in arraymodule which is un upper bound
      ! Allocation of memory for various arrays
      MAX_SIZE_ARRAYS = mocompSize
      allocate(phasemoc(RANGELINE_SIZE ))   !Phase adjustment for every range pixel
!c      allocate(rec(MAX_SIZE_ARRAYS))
      allocate(s_scsave(MAX_SIZE_ARRAYS))
      allocate(b_save(MAX_SIZE_ARRAYS))
      allocate(rho_save(MAX_SIZE_ARRAYS))
      allocate(time_save(MAX_SIZE_ARRAYS))

      pi = getPi()      !Pi
      sol = getSpeedOfLight()   !Speed of light

      if (present(rawr001)) then
          rc01 = rawr001
      else
          rc01 = r001
      endif

      !Initialize the sinc interpolator array for range sampling
      if(firsttime .eq. 1) then
         r_beta = 1.d0
         r_relfiltlen = 8.d0
         i_decfactor = 8192
         r_pedestal = 0.d0
         i_weight = 1

         write(6,*) ' '
         write(6,'(a)') 'Computing mocomp sinc coefficients...'
         write(6,*) ' '

         call sinc_coef(r_beta,r_relfiltlen,i_decfactor,r_pedestal, &
                   i_weight,i_intplength,i_filtercoef,r_filter)

         r_delay = i_intplength/2.d0

         do i = 0 , i_intplength - 1
            do j = 0 , i_decfactor - 1
               fintp(i+j*i_intplength) = r_filter(j+i*i_decfactor)
            enddo
         enddo
        firsttime=0
      end if

      lines = numLines 

!c  set up coordinates, find s values to solve locations for

!$omp parallel private(i,line,irange,rangeline,rho,cosalpha,sinalpha,f0,betadot,cosbeta,sinbeta,tanbeta,cosgamma,singamma,tandelta,sindelta,cosdelta,s_sc,cosepsilon,sinepsilon,cosalphaprime,rhoprime,bin,phase,ibin,frac,c,s0,c0,h0,iline) &
!$omp shared(irec,nnn,schMoc,re,trans1,fintp,r001,delr,ht1,wvl,nlinesaz,fd,fdd,fddd,timeMoc,vel,s_mocomp,t_mocomp,i_mocomp,phasemoc,pi,sol,r_delay,i_decfactor,i_intplength,ilrl,rc01) 
      allocate(rangeline(RANGELINE_SIZE))
!$omp do
      do iline=irec,irec+nnn-1       !For each range line
         i=iline                 !Line number
         line=i-irec+1           !Line index
         if(i.gt.lines) i=lines   
         if(i.lt.1) i=1
         s0=schMoc(1,i)          !Actual satellite position
         c0=schMoc(2,i)
         h0=schMoc(3,i)
         !c copy line into temporary array
         do irange=1,nlinesaz
             rangeline(irange)=trans1(line,irange)
         end do

         !c loop over range pixels
         do irange=1,nlinesaz
            !Range to given pixel
            rho=r001+(irange-1)*delr

            ! Equation 26. Angles at ideal satellite for given range.
            ! Postive angle alpha. Independent of look side.
            cosalpha=(re*re+(ht1+re)*(ht1+re)-rho*rho)/(2.D0*re*(ht1+re))
            sinalpha=sqrt(1-cosalpha**2)

            !Doppler centroid at given range
            f0 = fd + fdd*rho + fddd*rho*rho


            if(abs(f0).gt.1.e-1) then   ! If the doppler centroid is not negligible
               !Estimate beta using Equation 10.
               !Beta depends on sign of doppler not on look side.
               tanbeta=-f0*wvl*rho/(2.D0*re*cosalpha*vel)
               cosbeta=cos(atan(tanbeta))
               sinbeta=sin(atan(tanbeta))

               !Estimate gamma using Equation 6.
               !Gamma is also independent of look side.
               cosgamma=cosalpha/cosbeta
               singamma=sqrt(1-cosgamma**2)

               !Estimate delta using Equation 25
               !Delta depends on look side
               sindelta=ilrl*(cosgamma-cosbeta*cosalpha)/sinbeta/sinalpha ! Equation 25 doesn't work for fd=0
               tandelta=tan(asin(sindelta))
           else
               tandelta=0.D0
           end if

        !The projected position of the ideal satellite.
        !Change in sign of delta accounts for change in look side.
        s_sc=s0-re*asin(tandelta*tan(c0/re)) ! Equation 24

        !Save the ideal position of satellite for midrange
        if(irange.eq.nlinesaz/2)s_mocomp(i)=s_sc

        !c If the doppler is really small. 
        if(abs((s_sc-s0)/re).gt.1.e-6)then
            ! Law of spherical cosines
            ! Independent of look side
            cosepsilon=cos((s_sc-s0)/re)*cos(c0/re)

            ! Account for the sign of C-component
            ! Also account for look side
            if(c0.ge.0)then
            sinepsilon=-ilrl*sqrt(1-cosepsilon**2)
            else
            sinepsilon=ilrl*sqrt(1-cosepsilon**2)
            end if
        else
            !The angle corresponds to the C component only.
            cosepsilon=cos(c0/re)
            sinepsilon=-ilrl*sin(c0/re)
        end if

        ! Estimate the angle from the actual satellite
        cosalphaprime=cosalpha*cosepsilon-sinalpha*sinepsilon ! Equation 27

        ! Target at rho to ideal satellite appears at rhoprime for 
        ! the actual satellite. Assumption: Target is on local sphere
        rhoprime=sqrt((re+h0)**2+re**2-2.d0*(re+h0)*re*cosalphaprime) ! Equation 28


        !c  solve for baseline b and frequency offset
        ! Store the mocomp baseline values at mid range
        if(irange.eq.nlinesaz/2)then
            sinalphaprime=sqrt(1.-cosalphaprime**2)
            cosdeltaalpha=cosalpha*cosalphaprime+sinalpha*sinalphaprime

            !Law of cosines
            b=sqrt((rho+ht1)**2+(rhoprime+h0)**2-2.*(rho+ht1)* &
                   (rhoprime+h0)*cosdeltaalpha)
            cosarg=(rho**2+rhoprime**2-b**2)/2./rho/rhoprime

            !Frequency offset due to the baseline
            freq=sol/wvl*acos(cosarg)   !Not in paper. Added later.
        end if


        !c sample echo line at rhoprime
        !Offset in number of pixels
        bin=(rhoprime-rc01)/delr ! note interpolation routine assumes array is zero-based
        phase=(rhoprime-rho)*4.d0*pi/wvl  !Phase adjustment 
        if(line.eq.nnn/2) then    ! Save value at mid azimuth
            phasemoc(irange)=phase
        end if
        
        ! Save correction factor at mid patch
        if(irange.eq.nlinesaz/2.and.line.eq.nnn/2) then 
            focuscorr=(rhoprime-rho)/rho
        end if

        !Save midrange for each line
        if(irange.eq.nlinesaz/2)then
            s_scsave(line)=s_sc     !Ideal satellite position
            b_save(line)=rhoprime-rho   !Mocomp baseline
            rho_save(line)=rho      !Range to ideal satellite
            time_save(line)=timeMoc(i)  !Azimuth time UTC
        end if

        !If mocomp range change is small
        if(bin.le.1.0) bin=1.0

        !If mocomp range change is really large
        if(bin.gt.nlinesaz-1)bin=nlinesaz-1

        !Resample the range bin
        ibin=int(bin+r_delay)
        frac=bin+r_delay-ibin
        c = sinc_eval(rangeline,nlinesaz,fintp,i_decfactor,i_intplength, &
                     ibin,frac)
        shiftphase=2.d0*pi*freq*2.d0*rho/sol   !Add carrier back
        trans1(line,irange)=c*cmplx(cos(phase),sin(phase))
         end do
         t_mocomp(i)=timeMoc(i) !Azimuth time UTC
         i_mocomp(i)=i      !Index
      end do
!$omp end do
      deallocate(rangeline)
!$omp end parallel 

!c  compute phase gradient for migration focus correction
      do irange=1,nlinesaz-1
         phasegrad(irange)=phasemoc(irange+1)-phasemoc(irange)
      end do
      phasegrad(nlinesaz)=phasegrad(nlinesaz-1)

      !Deallocate memory from temporary variables
      deallocate(phasemoc)
!c      deallocate(rec)
      deallocate(s_scsave)
      deallocate(b_save)
      deallocate(rho_save)
      deallocate(time_save)
      return
      end


      subroutine getIdealRange(s0, c0, h0,rawrng,ht1,re,wvl,vel, &
          fd,ilrl,newrng)

            !!Returns approximate range to ideal satellite
            !! Does not need to be precise. Just to center the mocomp image.
            double precision :: rawrng, newrng
            double precision :: ht1, re, wvl, vel, fd
            integer :: ilrl, i, npts
            parameter(npts=2001)

            double precision :: s0, c0, h0
            double precision :: rng(npts), drng, dist(npts), rprime(npts)
            double precision :: rho
            double precision :: cosalpha, sinalpha
            double precision :: tanbeta, cosbeta, sinbeta
            double precision :: cosgamma, singamma
            double precision :: sindelta, tandelta
            double precision :: s_sc, deltah
            double precision :: sinepsilon, cosepsilon

            deltah = h0 - ht1
            drng = 4.0d0*c0/(1.0d0 * npts)

!!            print *, 'Position: ', s0, c0, h0
!!            print *, 'Spacing: ' , drng, npts
            do i=1, npts
                rho = rawrng-deltah + (i -npts/2-1)*drng

                cosalpha=(re*re+(ht1+re)*(ht1+re)-rho*rho)/(2.D0*re*(ht1+re))
                sinalpha=sqrt(1-cosalpha**2)



                if(abs(fd).gt.1.e-1) then   ! If the doppler centroid is not negligible
                    !Estimate beta using Equation 10.
                    !Beta depends on sign of doppler not on look side.
                    tanbeta=-fd*wvl*rho/(2.D0*re*cosalpha*vel)
                    cosbeta=cos(atan(tanbeta))
                    sinbeta=sin(atan(tanbeta))

                    !Estimate gamma using Equation 6.
                    !Gamma is also independent of look side.
                    !Again an approximation since beta is an approximation.
                    cosgamma=cosalpha/cosbeta
                    singamma=sqrt(1-cosgamma**2)

                    !Estimate delta using Equation 25
                    !Delta depends on look side
                    sindelta=ilrl*(cosgamma-cosbeta*cosalpha)/sinbeta/sinalpha ! Equation 25 doesn't work for fd=0
                    tandelta=tan(asin(sindelta))
                else
                    tandelta=0.D0
                end if

                !The projected position of the ideal satellite.
                !Change in sign of delta accounts for change in look side.
                s_sc=s0-re*asin(tandelta*tan(c0/re)) ! Equation 24

                !c If the doppler is really small. 
                if(abs((s_sc-s0)/re).gt.1.e-6)then
                    ! Law of spherical cosines
                    ! Independent of look side
                    cosepsilon=cos((s_sc-s0)/re)*cos(c0/re)

                    ! Account for the sign of C-component
                    ! Also account for look side
                    if(c0.ge.0)then
                        sinepsilon=-ilrl*sqrt(1-cosepsilon**2)
                    else
                        sinepsilon=ilrl*sqrt(1-cosepsilon**2)
                    end if
                else
                    !The angle corresponds to the C component only.
                    cosepsilon=cos(c0/re)
                    sinepsilon=-ilrl*sin(c0/re)
                end if

                cosalphaprime=cosalpha*cosepsilon - sinalpha*sinepsilon
                rng(i) =sqrt((re+h0)**2+re**2-2.d0*(re+h0)*re*cosalphaprime)
                dist(i) = abs(rng(i) - rawrng)
                rprime(i) = rho

!!                print *, i, rng(i), dist(i), rprime(i)
            end do

            !!Min loc returns array
            i = minloc(dist, dim=1)

            newrng = rprime(i)
        end subroutine getIdealRange

