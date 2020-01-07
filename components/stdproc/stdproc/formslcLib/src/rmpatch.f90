!> Range migration and azimuth compression of a single azimuth patch
!!
!! @param nnn
!! @param nl
!! @param r0 starting range [m]
!! @param delr range spacing [m]
!! @param wavl radar wavelength [m]
!! @param fd Doppler centroid [Hz/prf]
!! @param fdd Doppler rate [Hz/s/prf]
!! @param fddd Doppler acceleration [Hz/s/s/prf]
!! @param prfL pulse repetition frequency [Hz]
!! @param ideskew deskew flag
!! @param v satellite velocity [m/s]
!! @param ht satellite height [m]
!! @param focuscorr focus correction from motion compensation
!! @param azresL
!! @param peg the peg point structure
!! @param elp the ellipsoid structure
!! @param planet the planet structure
!! @param left [1] / right [-1] look side of satellite

subroutine rmpatch(nnn,nl,r0,delr,wavl, &
     fd,fdd,fddd,prfL,ideskew,v,ht,re,focuscorr,azresL, &
      peg,elp,planet,lrl)
  
  use arraymodule
  use fortranUtils
  use uniform_interp

  implicit none
  include 'omp_lib.h'

  type peg_type
     double precision :: r_lat                                    !< Peg point latitude
     double precision :: r_lon                                    !< Peg point longitude
     double precision :: r_hdg                                    !< Peg point heading
  end type peg_type
  type ellipsoid
     double precision :: r_a
     double precision :: r_e2
  end type ellipsoid
  type planet_type
     double precision :: r_spindot
     double precision :: r_gm
  end type planet_type

  type(peg_type) :: peg
  type(ellipsoid) :: elp
  type(planet_type) :: planet
  
  integer MAXDECFACTOR      ! maximum lags in interpolation kernels
  parameter(MAXDECFACTOR=8192)                        
    
  integer MAXINTKERLGH      ! maximum interpolation kernel length
  parameter (MAXINTKERLGH=8)
      
  integer MAXINTLGH         ! maximum interpolation kernel array size
  parameter (MAXINTLGH=MAXINTKERLGH*MAXDECFACTOR)

  integer*4 mmm,nmax,mmax
  integer lrl
  parameter (mmm=65536, nmax=4096,mmax= 30)
  real*8     r0,delr           ! Starting range, range pixel spacing
  real*8     wavl              ! Wavelength
  real*8     fd,fdd,fddd, tmpd ! Doppler coefficients
  real*8     ht,re,v,focuscorr ! Height, Earth radius, velocity, correction
  real*8  ,   allocatable :: rdopcent(:),rangezerodop(:) !Doppler, Range to zero doppler

  !Beta is the angle as described in mocomp.f90
  real*8     betadot,tanbeta,sinbeta,cosbeta

  !Alpha, Gamma are the same as defined in mocomp.f90
  real*8   ,  allocatable :: cosalpha(:),cosgamma(:)

  real*8     rhodot,range,tarloc(3) !range rate change, range, target location
  real*8  , allocatable ::squint(:) !Squint as a function of range
  real*8        prfL
  real*4        prf,freq
  integer*4     nnn, nl, ideskew
  real*4        xintp
  real*4        ratio, azres, azimuth_halfbw, loc
  real*8        azresL
  integer*4     na,i,n, k
  complex*8, allocatable ::  phasecpx(:), squintcpx(:)
  real*8 factor
  integer firsttime
  real*8, allocatable :: f0(:), f_rate(:),bdel(:) !Doppler, frate
  real*8 q,a,b,c
  real*8 , allocatable :: r(:),qtmpd(:),phase(:)
  integer ii
  real*8 , allocatable ::r_filter(:)
  real*8 , allocatable :: vtmp(:)
  integer, allocatable :: nvtmp(:)
  real*8 r_beta, r_relfiltlen, r_pedestal
  integer i_decfactor, i_weight, i_intplength, i_filtercoef
  real*8 pi, r_delay
  complex*8 c_b

  data firsttime/1/
  save firsttime,r_delay,i_decfactor,i_intplength
  
  common /xintp/ xintp(0:MAXINTLGH)
  
  complex*8, allocatable ::  c_ctmpa(:)
  
  pi = getPi()

  !c initializations        
!  lrl = -1  ! Right looking (-1), Left looking (+1)  MUST BE CHANGED TO BE A READ/PASSED PARAMETER
  
  !c     load the interpolation array
 
  !Allocate memory 
  allocate(r(mmm))
  allocate(qtmpd(mmm))
  allocate(rdopcent(mmm))
  allocate(rangezerodop(mmm))
  allocate(cosalpha(mmm))
  allocate(cosgamma(mmm))
  allocate(squint(mmm/2))
  allocate(f0(mmm))
  allocate(f_rate(mmm))
  allocate(bdel(mmm))
  allocate(r_filter(0:MAXINTLGH))
  
  prf = 1.0*prfL
  azres = 1.0*azresL

  !Setting up the sinc interpolator for resampling in range
  if(firsttime .eq. 1) then
      r_beta = 1.d0
      r_relfiltlen = 8.d0
      i_decfactor = 8192
      r_pedestal = 0.d0
      i_weight = 1

      write(6,*) ' '
      write(6,'(a)') 'Computing range migration sinc coefficients...'
      write(6,*) ' '

      call sinc_coef(r_beta,r_relfiltlen,i_decfactor,r_pedestal,i_weight,i_intplength,i_filtercoef,r_filter)

      r_delay = i_intplength/2.d0

      do i = 0 , i_intplength - 1
         do k = 0 , i_decfactor - 1
            xintp(i+k*i_intplength) = r_filter(k+i*i_decfactor)
         enddo
      enddo

     firsttime=0
  end if
 
  !Azimuth half bandwidth 
  azimuth_halfbw=v/azres/2.D0
  if(azimuth_halfbw.ge.prf/2.D0)azimuth_halfbw=prf/2.D0
  print *,"Azimuth Half Bandwidth: ",azimuth_halfbw
  betadot=v/(re+ht)    !Angular velocity


  ! Place the target on the ellipsoid
  do i = 1,3
     tarloc(i) = 0.D0
  enddo

  !Compute parameters as a function of range
  do i = 1, nl
     r(i)      = r0 + (i-1)*delr !range to the line
     f0(i)     = fd+fdd*r(i)+fddd*r(i)*r(i) !Doppler centroid

     !!As described in mocomp.f90 - alpha, beta and gamma are not affected by
     !! look side. Geometry is symmetric on right or left side. - Piyush
     cosalpha(i)=(re*re+(ht+re)*(ht+re)-r(i)*r(i))/(2.*re*(ht+re))
     tanbeta=f0(i)*wavl*r(i)/(2*re*(re+ht)*cosalpha(i)*betadot)
     sinbeta=sin(atan(tanbeta))
     cosbeta=sqrt(1.D0-sinbeta*sinbeta)
     cosgamma(i)=cosalpha(i)/cosbeta
     rhodot=-re*cosgamma(i)*sinbeta*v/r(i)
     f_rate(i)=2.D0*(rhodot**2-re*cosgamma(i)*v*cosbeta*betadot)/r(i)/wavl*(1.D0-focuscorr) ! Original equation from SOI
     squint(i)=-re*asin(-f0(i)*r(i)*wavl/2.D0/re/cosgamma(i)/v)/(v*re/(ht+re)/prf)
  end do


  !$omp parallel  private(freq,ratio,n,tmpd,nvtmp,vtmp,i,na,c_ctmpa,c_b,sinbeta,cosbeta,range,tanbeta,q,a,b,c,phase,ii,phasecpx,squintcpx,loc) & 
  !$omp shared(r,f0,rdopcent,f_rate,bdel,xintp,prf,trans1,nnn,ideskew,wavl,delr,cosgamma,cosalpha,ht,re,rangezerodop,qtmpd,factor,phasegrad,squint,azimuth_halfbw,pi,r_delay,i_intplength,i_decfactor)
  allocate(vtmp(mmm))
  allocate(nvtmp(mmm))
  allocate(c_ctmpa(mmm))
  allocate(phasecpx(mmm))
  allocate(squintcpx(mmm))
  allocate(phase(mmm))
  vtmp = 0
  nvtmp = 0
  phasecpx = 0
  squintcpx = 0
  phase = 0
  !$omp do
  do na = 1,nnn        !For a given azimuth frequency
     
     !c get the interpolation amounts for a given azimuth pixel na as f(line)
     do i = 1,nl
        if(na.le.nnn/2)then
           freq=(na-1)/float(nnn)*prf 
        else
           freq=(na-1)/float(nnn)*prf-prf
        end if
        !c     frequencies must be within 0.5*prf of centroid
        ratio = (freq-f0(i))/prf
        n = nint(ratio)
        freq = freq - n * prf
        !c     range of a pixel at freq f, bdel is range correction for interferogram
        phase(i)=pi/f_rate(i)*freq**2      !The azimuth chirp phase
        range=-wavl/4.D0/pi*phase(i)       !Range computation from phase
        tmpd=i+range/delr - 1 ! note interpolation routine assumes array is zero-based
        ! Deskewing code went here, it was broken
        nvtmp(i) = int(tmpd+r_delay)
        vtmp(i) = tmpd +r_delay - int(tmpd)
        if(na.le.nnn/2)then
           loc = (na-1)/float(nnn)*pi*2.D0-2.D0*pi
        else
           loc = (na-nnn-1)/float(nnn)*pi*2.D0
        end if
        if (freq.ge.0.D0) then
                loc = loc + 2.D0*pi
        endif
        !if (i.eq.2340) then
        !   print *,freq,loc,phase(i),phasegrad(i)*range/delr,squint(i)*loc
        !endif
        phase(i)=phase(i)-phasegrad(i)*range/delr  !remove mocomp resampling phase gradient
        squintcpx(i) = cmplx(cos(squint(i)*loc),sin(squint(i)*loc))  !Squint phase
        phasecpx(i)=cmplx(cos(phase(i)),sin(phase(i)))/float(nnn)    !Range phase
        if(abs(freq-f0(i)).gt.azimuth_halfbw)phasecpx(i)=cmplx(0.,0.)
     enddo
     
     !c  interpolate that line according to coeffs determined above
     !c  temp array index calculation must be one based because that's what sinc_eval expects

     c_b = 0
     do i = 1 , nl
       c_ctmpa(i) = trans1(na,i)
     end do
     do i=1,nl
       c_b = sinc_eval(c_ctmpa,nl,xintp,i_decfactor,i_intplength,nvtmp(i),vtmp(i))
       trans1(na,i) = c_b *phasecpx(i)*squintcpx(i)
     end do
     
  enddo      ! na-loop
  !$omp end do
  deallocate(vtmp)
  deallocate(nvtmp)
  deallocate(c_ctmpa)
  deallocate(phasecpx)
  deallocate(squintcpx)
  deallocate(phase)
  !$omp end parallel 
  deallocate(r)
  deallocate(qtmpd)
  deallocate(rdopcent)
  deallocate(rangezerodop)
  deallocate(cosalpha)
  deallocate(cosgamma)
  deallocate(squint)
  deallocate(f0)
  deallocate(f_rate)
  deallocate(bdel)

  return
end subroutine rmpatch
