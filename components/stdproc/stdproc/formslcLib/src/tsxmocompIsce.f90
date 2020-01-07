module tsxmocomp
!c mocomp - apply mocomp to move data to a desired reference
implicit none


contains

subroutine mocomp(naz,nr,r0,delr,ht,re,wvl,vel,fd,fdd,fddd,ilrl,slc001)

!c inputs
!c
!c naz - array size in azimuth lines
!c nr - array size in range bins
!c trans - range compressed data array
!c r0 - near range, m
!c delr - range spacing in m
!c ht - height of reference track, m
!c re  - local earth radius, m
!c wvl -wavelength
!c vel - velocity
!c fd,fdd,fddd - Doppler coefficients
!c ilrl - Left [1] / Right [-1] look direction of the satellite
!c slc001 - Starting range of the input SLC

!c outputs
!c
!c trans - distorted input array with shift and mocomp phases applied
!c s,t,i_mocomp - s coord, time, record for each mocomped line
!c focuscorr - focus correction (2nd order) term B/rho
!c phasegrad - phase gradient with respect to range for focus correction

 use omp_lib
 use fortranUtils
 use uniform_interp
 use arraymodule
 
 integer MAXDECFACTOR      ! maximum lags in interpolation kernels
 parameter(MAXDECFACTOR=8192)

 integer MAXINTKERLGH      ! maximum interpolation kernel length
 parameter (MAXINTKERLGH=8)

 integer MAXINTLGH         ! maximum interpolation kernel array size
 parameter (MAXINTLGH=MAXINTKERLGH*MAXDECFACTOR)
 
 complex*8::rangeline(nr),c
 real*8:: time(naz),sch(3,naz)
 real*8:: x(2),sinbeta,cosbeta
 real*8:: sindelta,cosbetaprime,rho,rhoprime
 real*8:: r0,delr,ht,re,phase,wvl
 real*8:: s0, vel, c0, h0, frac
 real*8:: cosalpha,sinalpha,f0,tanbeta,cosgamma,singamma,s_sc
 real*8:: fd,fdd,fddd,tandelta,cosepsilon,sinepsilon,cosalphaprime,pi
 real*8  r_pedestal, r_relfiltlen, r_beta,r_delay
 double precision :: r_filter(0:MAXINTLGH)
 real*4:: poly(3),bin
 integer:: naz,nr,irange,rec(naz),iline,i,j,ibin
 integer :: i_intplength,i_filtercoef, i_decfactor, i_weight
 integer ilrl
 real*8, intent(in), optional :: slc001
 real*8  rc01
 !character*64:: schfile
 real*4 fintp

 integer firsttime
 data firsttime/1/
 save firsttime, r_delay, i_decfactor, i_intplength
 common /fintp/ fintp(0:MAXINTLGH)
 pi = getPI()

 if(present(slc001)) then
     rc01 = slc001
 else
     rc01 = r0
 endif

 if(firsttime .eq. 1) then
     r_beta = 1.d0
     r_relfiltlen = 8.d0
     i_decfactor = 8192
     r_pedestal = 0.d0
     i_weight = 1

     write(6,*) ' '
     write(6,'(a)') 'Computing mocomp sinc coefficients... '
     write(6,*) ' '

     call sinc_coef(r_beta,r_relfiltlen,i_decfactor,r_pedestal,i_weight,i_intplength,i_filtercoef,r_filter)

     r_delay = i_intplength/2.d0

     do i = 0 , i_intplength - 1
         do j = 0 , i_decfactor - 1
             fintp(i+j*i_intplength) = r_filter(j+i*i_decfactor)
         enddo
     enddo
     firsttime=0
 end if


!c assume orbit in sch coords. is present in position.sch
 !open(41,file=schfile)
 !do iline=1,naz
    !read(41,*)rec(iline),time(iline),sch(1,iline),sch(2,iline),sch(3,iline)
 !end do
 !close(41)
 !print *,'Mocomp records read: ',naz

!c  set up coordinates
!$omp parallel do private(iline,irange,rangeline,rho,&
!$omp cosalpha,sinalpha,f0,cosbeta,sinbeta,&
!$omp tanbeta,cosgamma,singamma,tandelta,sindelta,&
!$omp s_sc,cosepsilon,sinepsilon,cosalphaprime,&
!$omp rhoprime,bin,phase,c,s0,c0,h0,ibin,frac)&
!$omp shared(naz,schMoc,re,trans1,r0,delr,ht,wvl,nr,r_delay,fd,fdd,fddd)&
!$omp shared(timeMoc,vel,s_mocomp,t_mocomp,i_mocomp,ilrl,rc01,pi,fintp,i_decfactor,i_intplength)
do iline=1,naz
   s0=schMoc(1,iline)
   c0=schMoc(2,iline)
   h0=schMoc(3,iline)
   !c copy line into temporary array
   rangeline=trans1(:,iline)
   !c loop over range pixels
   do irange=1,nr
      !c  we need gamma and alpha for the point to be imaged
      !c  primed coordinates are actual platform location
      rho=r0+(irange-1)*delr

      !!alpha unchanged by look side
      cosalpha=(re*re+(ht+re)*(ht+re)-rho*rho)/(2.*re*(ht+re))
      sinalpha=sqrt(1-cosalpha**2)
      f0 = fd + fdd*rho + fddd*rho*rho 
      if(abs(f0).gt.1.e-1)then
         !!Beta unaffected by look side
         tanbeta=-f0*wvl*rho/(2*re*cosalpha*vel)
         cosbeta=cos(atan(tanbeta))
         sinbeta=sin(atan(tanbeta))

         !!Gamma also unaffected by look side
         cosgamma=cosalpha/cosbeta
         singamma=sqrt(1-cosgamma**2)

         !!Delta depends on look side
         sindelta=ilrl*(cosgamma-cosbeta*cosalpha)/sinbeta/sinalpha !doesn't work for fd=0
         tandelta=tan(asin(sindelta))
      else
         tandelta=0.
      end if

      s_sc=s0-re*asin(tandelta*tan(c0/re))
      if(irange.eq.nr/2)s_mocomp(iline)=s_sc
      if(abs((s_sc-s0)/re).gt.1.e-6)then
         cosepsilon=cos((s_sc-s0)/re)*cos(c0/re)
         if(c0.ge.0)then
            sinepsilon=-ilrl*sqrt(1-cosepsilon**2)
         else
            sinepsilon=ilrl*sqrt(1-cosepsilon**2)
         end if
      else
         cosepsilon=cos(c0/re)
         sinepsilon=-ilrl*sin(c0/re)
      end if
      cosalphaprime=cosalpha*cosepsilon-sinalpha*sinepsilon
      rhoprime=sqrt((re+h0)**2+re**2-2.d0*(re+h0)*re*cosalphaprime)
      !c sample echo line at rhoprime
      bin=(rhoprime-rc01)/delr
      phase=(rhoprime-rho)*4.d0*pi/wvl
      if(bin.le.1.0)bin=1.0
      if(bin.gt.nr-1)bin=nr-1
      ibin=int(bin+r_delay)
      frac=bin+r_delay-ibin
      c = sinc_eval(rangeline,nr,fintp,i_decfactor,i_intplength,ibin,frac)

      !c start with sinc interp
      !call sinc_interp1d_cpx(rangeline,data_params,sinc_value,sinc_value_params,bin,c)
      trans1(irange,iline)=c*cmplx(cos(phase),sin(phase))
   end do
   t_mocomp(iline)=timeMoc(iline)
   i_mocomp(iline)=iline
end do
!$omp end paralleldo
print *,'*****Mocomp uses sinc interpolation*****'
      
end subroutine mocomp


end module tsxmocomp
