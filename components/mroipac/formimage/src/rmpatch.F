#ifndef PARALLELIZED_RMPATCH
# ifndef TUNED_RMPATCH
      subroutine rmpatch(trans,slope,inter,nnn,nl,nls,r0,delr,wavl,vel
     $     ,ht,re,fd,fdd,fddd,fdddd,prf,ideskew)

        implicit none
        real*4 pi, pi2
        parameter (pi=3.14159625265359,pi2=6.28318530718)
        real*8     r0,delr,wavl,fd,fdd,fddd,fdddd, slope, inter, tmpd
        real*8     rd0v1(nl),ht,re, gm, th, sinsqref, acc
        real*4        vel,prf, v1, veleff
        integer*4     nfilter, nnn, nl, nls,ideskew
        real*4        xintp, freq
	real*4        frac, ratio
	integer*4     na,i,ifrac, n, k
	complex*8     trans(nnn,nl)

        integer firsttime
        real*4 f0(nl), f_rate(nl),bdel(nl)
	real*8 r(nl)
        real*4 vtmp(nl)
        integer nvtmp(nl)

        complex*8 c_ctmpb(8)
        real*4    c_xintp(8)
        complex*8 c_ctmpa(nl)

        common /intp/ xintp(0:65544), nfilter

        data gm/3.9858528e14/
        data firsttime/1/
        save firsttime

c initializations        

c     load the interpolation array

        if(firsttime .eq. 1) then
           nfilter = 8192
           call intp_coef(nfilter,xintp)
           firsttime=0
c          write(6,*) 'sinc initialized '
        end if

        acc = gm/(re+ht)**2

        do i = 1, nl
           r(i)      = r0 + (i-1)*delr !range to the line
           f0(i) = fd + ( fdd + ( fddd+fdddd*r(i) ) *r(i) )*r(i)
           th=dacos(((ht+re)**2+r(i)*r(i)-re**2)/(2.d0*r(i)*(re
     $          +ht)))
           sinsqref = f0(i) * wavl/(2.d0*vel*sqrt(re/(re+ht))*sin(th))
           f_rate(i) = (2.d0/wavl)*(acc*cos(th)+((vel*sinsqref)**2-vel
     $          **2)/r(i))
           veleff = sqrt(wavl*abs(f_rate(i))*r(i)/(2.d0))
           v1 =wavl**2/(8.*(veleff/prf)**2)
           rd0v1(i)    = v1*r(i)/(1 + v1*(f0(i)/prf)**2)
c f_rate replaced with a more exact expression for chirp rate
c           f_rate(i) = -2.d0 * vel**2*(rd0v1(i)/v1/r(i))**2/(wavl*r(i))

c           write(6,*) 'f_rates ', f_rate(i), -2.d0 * (vel*sqrt(re/(re+ht)))
c     $          **2*(rd0v1(i)/v1/r(i))**2/(wavl*r(i)),veleff

           bdel(i)   = slope * r(i) + inter
        end do
        
c        write(6,*) 'linear arrays computed '
	do na = 1,nnn

c get the interpolation amounts for a given azimuth pixel na as f(line)
              freq=(na-1)/float(nnn)*prf 
              do i = 1,nl
c     frequencies must be within 0.5*prf of centroid
                 ratio = (freq-f0(i))/prf
                 n = nint(ratio)
                 freq = freq - n * prf
c     range of a pixel at freq f, bdel is range correction for interferogram
                 
                 if(ideskew.eq.1)then
c  deskewing
                    tmpd = bdel(i)+ ((r(i)-(wavl/4.)*f0(i)**2/
     $                f_rate(i))-r(1))/delr +
     $                rd0v1(i)*(1.d0/delr)*(freq**2-f0(i)**2)/prf**2
                 else
c  not deskewing
                    tmpd  = i + rd0v1(i)*(1.d0/delr)*(freq**2-f0(i)**2)/prf**2
     $                + bdel(i)
                 end if
                 nvtmp(i) = int(tmpd)
                 vtmp(i) = tmpd - int(tmpd)
              enddo
c           write(6,*) 'vtmp computed'

c  interpolate that line according to coeffs determined above
              do i=1,nl
                 c_ctmpa(i)=cmplx(0.,0.)
                 if(nvtmp(i).ge.4 .and. nvtmp(i).lt.(nl-4)) then
                       frac = vtmp(i)
                       ifrac= 8*nint(frac*float(nfilter))
                       do k = 1 , 8
                          c_xintp(k) = xintp(ifrac+k-1)
                          c_ctmpb(k) = trans(na,nvtmp(i)-3+k-1)
                      end do
                       c_ctmpa(i)=c_ctmpb(1)*c_xintp(1)
     2                      +c_ctmpb(2)*c_xintp(2)
     3                      +c_ctmpb(3)*c_xintp(3)
     4                      +c_ctmpb(4)*c_xintp(4)
     5                      +c_ctmpb(5)*c_xintp(5)
     6                      +c_ctmpb(6)*c_xintp(6)
     7                      +c_ctmpb(7)*c_xintp(7)
     8                      +c_ctmpb(8)*c_xintp(8)
                    endif
              enddo
              do i = 1, nl
                 trans(na,i) = c_ctmpa(i)
              end do
c           write(6,*) 'interpolation computed'

	enddo                   ! na-loop

        return
	end
# else /* TUNED_RMPATCH */
        subroutine rmpatch(trans,slope,inter,nnn,nl,nls,r0,delr,wavl,vel
     $     ,ht,re,fd,fdd,fddd,fdddd,prf,ideskew)

        implicit none
        real*4 pi, pi2
        parameter (pi=3.14159625265359,pi2=6.28318530718)
        real*8     r0,delr,wavl,fd,fdd,fddd,fdddd, slope, inter, tmpd
        real*8     rd0v1(nl), ht, re, gm, th, sinsqref, acc
        real*4        vel,prf,v1, veleff
        integer*4     nfilter, nnn, nl, nls,ideskew
        real*4        xintp
	integer*4     i, n, k
	complex*8     trans(nnn,nl)

        integer firsttime
        real*4 f0(nl), f_rate(nl),bdel(nl)
	real*8 r(nl)

#define	CACHE_LINE	(128)
        integer*8 linesz
        integer*4 ioff, iblock, iblockbeg, iblockend, ib
        complex*8 tmp_cache((CACHE_LINE/8)*(nl+1))
 
        data gm/3.9858528e14/
        data firsttime/1/
        save firsttime

        common /intp/ xintp(0:65544), nfilter

c initializations        

c     load the interpolation array

        if(firsttime .eq. 1) then
           nfilter = 8192
           call intp_coef(nfilter,xintp)
           firsttime=0
c          write(6,*) 'sinc initialized '
        end if

        acc = gm/(re+ht)**2

        do i = 1, nl
           r(i)      = r0 + (i-1)*delr !range to the line
           f0(i) = fd + ( fdd + ( fddd+fdddd*r(i) ) *r(i) )*r(i)
           th=dacos(((ht+re)**2+r(i)*r(i)-re**2)/(2.d0*r(i)*(re
     $          +ht)))
           sinsqref = f0(i) * wavl/(2.d0*vel*sqrt(re/(re+ht))*sin(th))
           f_rate(i) = (2.d0/wavl)*(acc*cos(th)+((vel*sinsqref)**2-vel
     $          **2)/r(i))
           veleff = sqrt(wavl*abs(f_rate(i))*r(i)/(2.d0))
           v1 =wavl**2/(8.*(veleff/prf)**2)
           rd0v1(i)    = v1*r(i)/(1 + v1*(f0(i)/prf)**2)
c f_rate replaced with a more exact expression for chirp rate
c           f_rate(i) = -2.d0 * vel**2*(rd0v1(i)/v1/r(i))**2/(wavl*r(i))

c           write(6,*) 'f_rates ', f_rate(i), -2.d0 * (vel*sqrt(re/(re+ht)))
c     $          **2*(rd0v1(i)/v1/r(i))**2/(wavl*r(i)), veleff
           bdel(i)   = slope * r(i) + inter
        end do
        
c        write(6,*) 'linear arrays computed '
        linesz    = CACHE_LINE
        iblock    = CACHE_LINE/8
        ioff      = 1 + iand(%loc(tmp_cache(1)),linesz-1)/8
        if (ioff.ne.1) ioff = iblock - ioff + 2
        iblockbeg = iand(%loc(trans(1,1)),linesz-1)/8
        if (iblockbeg.ne.0) iblockbeg = iblock - iblockbeg
        iblockend = iand(nnn-iblockbeg,iblock-1)

        ib = 1
           call cache_copy(trans(ib,1),nnn,tmp_cache(ioff),iblock,
     &                     iblockbeg,nl)
           call rmpatch_work(ib-1,iblockbeg,tmp_cache(ioff),iblock,nl,nnn,f0,
     &                       bdel,r,f_rate,rd0v1,delr,wavl,prf,ideskew)
           call cache_copy(tmp_cache(ioff),iblock,trans(ib,1),nnn,
     &                     iblockbeg,nl)
        continue

        do ib = iblockbeg+1, nnn-iblockend, iblock
           call cache_copy(trans(ib,1),nnn,tmp_cache(ioff),iblock,
     &                     iblock,nl)
           call rmpatch_work(ib-1,iblock,tmp_cache(ioff),iblock,nl,nnn,f0,
     &                       bdel,r,f_rate,rd0v1,delr,wavl,prf,ideskew)
           call cache_copy(tmp_cache(ioff),iblock,trans(ib,1),nnn,
     &                     iblock,nl)
        enddo

        ib = nnn-iblockend+1
           call cache_copy(trans(ib,1),nnn,tmp_cache(ioff),iblock,
     &                     iblockend,nl)
           call rmpatch_work(ib-1,iblockend,tmp_cache(ioff),iblock,nl,nnn,f0,
     &                       bdel,r,f_rate,rd0v1,delr,wavl,prf,ideskew)
           call cache_copy(tmp_cache(ioff),iblock,trans(ib,1),nnn,
     &                     iblockend,nl)
        continue

999     return
	end

      subroutine rmpatch_work(na0,na_cnt,tmp_cache,ldtc,nl,nnn,f0,bdel,
     &                          r,f_rate,rd0v1,delr,wavl,prf,ideskew)
      implicit none
      integer*4 na0, na_cnt, ldtc, nl, nnn, nfilter, ideskew
      complex*8 tmp_cache(ldtc,nl)
      real*4 f0(nl), bdel(nl), f_rate(nl), prf
      real*8 r(nl), rd0v1(nl), delr, wavl

      real*4 xintp
      common /intp/ xintp(0:65544), nfilter

      integer na, i, k, nvtmp(nl), knt, ii, index(nl), ifrac_arr(nl)
      integer*4 n, ifrac
      real freq
      real*4 ratio, vtmp(nl), frac, c_xintp(8)
      real*8 tmpd
      complex*8 c_ctmpa(nl), c_ctmpb(8)

      do na = 1, na_cnt

c get the interpolation amounts for a given azimuth pixel na as f(line)
         freq=(na0+na-1)/float(nnn)*prf 
         do i = 1,nl
c     frequencies must be within 0.5*prf of centroid
            ratio = (freq-f0(i))/prf
            n = nint(ratio)
            freq = freq - n * prf
c     range of a pixel at freq f, bdel is range correction for interferogram
                 
            if(ideskew.eq.1)then
c  deskewing
               tmpd = bdel(i)+ ((r(i)-(wavl/4.)*f0(i)**2/
     $              f_rate(i))-r(1))/delr +
     $              rd0v1(i)*(1.d0/delr)*(freq**2-f0(i)**2)/prf**2
            else
c  not deskewing
               tmpd  = i + rd0v1(i)*(1.d0/delr)*(freq**2-f0(i)**2)/prf**2
     $              + bdel(i)
            end if
            nvtmp(i) = int(tmpd)
            vtmp(i) = tmpd - int(tmpd)
         enddo
c     write(6,*) 'vtmp computed'

c  interpolate that line according to coeffs determined above
         knt = 0
         do i=1,nl
            c_ctmpa(i)=cmplx(0.,0.)
            if (nvtmp(i).ge.4 .and. nvtmp(i).lt.(nl-4)) then
               knt        = knt + 1
               index(knt) = i
            endif
         enddo
cdir$ ivdep
         do ii = 1, knt
            i     = index(ii)
            frac  = vtmp(i)
            ifrac = 8*nint(frac*float(nfilter))
            c_ctmpa(i) = tmp_cache(na,nvtmp(i)-3)*xintp(ifrac+0)
     2                 + tmp_cache(na,nvtmp(i)-2)*xintp(ifrac+1)
     3                 + tmp_cache(na,nvtmp(i)-1)*xintp(ifrac+2)
     4                 + tmp_cache(na,nvtmp(i)+0)*xintp(ifrac+3)
     5                 + tmp_cache(na,nvtmp(i)+1)*xintp(ifrac+4)
     6                 + tmp_cache(na,nvtmp(i)+2)*xintp(ifrac+5)
     7                 + tmp_cache(na,nvtmp(i)+3)*xintp(ifrac+6)
     8                 + tmp_cache(na,nvtmp(i)+4)*xintp(ifrac+7)
         enddo
         do i = 1, nl
            tmp_cache(na,i) = c_ctmpa(i)
         end do

c     write(6,*) 'interpolation computed'

      enddo                     ! na-loop

      return
      end


        subroutine cache_copy(from,ldf,to,ldt,nrf,ncf)
        complex*8 from(ldf,ncf), to(ldt,nrf)
        integer ldf, ldt, nrf, ncf

        integer i, j

        if (nrf.eq.1) then
           do j = 1, ncf
              to(1,j) = from(1,j)
           enddo
        else if (nrf.eq.2) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
           enddo
        else if (nrf.eq.3) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
              to(3,j) = from(3,j)
           enddo
        else if (nrf.eq.4) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
              to(3,j) = from(3,j)
              to(4,j) = from(4,j)
           enddo
        else if (nrf.eq.5) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
              to(3,j) = from(3,j)
              to(4,j) = from(4,j)
              to(5,j) = from(5,j)
           enddo
        else if (nrf.eq.6) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
              to(3,j) = from(3,j)
              to(4,j) = from(4,j)
              to(5,j) = from(5,j)
              to(6,j) = from(6,j)
           enddo
        else if (nrf.eq.7) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
              to(3,j) = from(3,j)
              to(4,j) = from(4,j)
              to(5,j) = from(5,j)
              to(6,j) = from(6,j)
              to(7,j) = from(7,j)
           enddo
        else if (nrf.eq.16) then
           do j = 1, ncf
              to( 1,j) = from( 1,j)
              to( 2,j) = from( 2,j)
              to( 3,j) = from( 3,j)
              to( 4,j) = from( 4,j)
              to( 5,j) = from( 5,j)
              to( 6,j) = from( 6,j)
              to( 7,j) = from( 7,j)
              to( 8,j) = from( 8,j)
              to( 9,j) = from( 9,j)
              to(10,j) = from(10,j)
              to(11,j) = from(11,j)
              to(12,j) = from(12,j)
              to(13,j) = from(13,j)
              to(14,j) = from(14,j)
              to(15,j) = from(15,j)
              to(16,j) = from(16,j)
           enddo
        else
           do j = 1, ncf
              do i = 1, nrf
                 to(i,j) = from(i,j)
              enddo
           enddo
        endif

        return
        end

# endif  /* TUNED_RMPATCH */
#else /* PARALLELIZED_RMPATCH */
        subroutine rmpatch(trans,slope,inter,nnn,nl,nls,r0,delr,wavl,vel
     $     ,ht,re,fd,fdd,fddd,fdddd,prf,ideskew)

        implicit none
        real*4 pi, pi2
        parameter (pi=3.14159625265359,pi2=6.28318530718)
        real*8     r0,delr,wavl,fd,fdd,fddd,fdddd, slope, inter, tmpd
        real*8     rd0v1(nl), ht,re, gm, th, sinsqref, acc
        real*4        vel,prf,v1, veleff
        integer*4     nfilter, nnn, nl, nls,ideskew
        real*4        xintp
	integer*4     i, j, n, k
	complex*8     trans(nnn,nl)

        integer firsttime
        real*4 f0(nl), f_rate(nl),bdel(nl)
	real*8 r(nl)

#define	CACHE_LINE	(128)
        integer*8 linesz
        integer*4 ioff, iblock, iblockbeg, iblockend, ib
        integer*4 nb, nt, ntblock, intblock, intblock_end
        integer*4 mp_numthreads
        external  mp_numthreads
        complex*8 tmp_cache((CACHE_LINE/8)*(nl+1))
 
        data gm/3.9858528e14/
        data firsttime/1/
        save firsttime

        common /intp/ xintp(0:65544), nfilter

c initializations

c     load the interpolation array

        if(firsttime .eq. 1) then
           nfilter = 8192
           call intp_coef(nfilter,xintp)
           firsttime=0
c          write(6,*) 'sinc initialized '
        end if

        acc = gm/(re+ht)**2
        do i = 1, nl
           r(i)      = r0 + (i-1)*delr !range to the line
           f0(i) = fd + ( fdd + ( fddd+fdddd*r(i) ) *r(i) )*r(i)
           th=dacos(((ht+re)**2+r(i)*r(i)-re**2)/(2.d0*r(i)*(re
     $          +ht)))
           sinsqref = f0(i) * wavl/(2.d0*vel*sqrt(re/(re+ht))*sin(th))
           f_rate(i) = (2.d0/wavl)*(acc*cos(th)+((vel*sinsqref)**2-vel
     $          **2)/r(i))
           veleff = sqrt(wavl*abs(f_rate(i))*r(i)/(2.d0))
           v1 =wavl**2/(8.*(veleff/prf)**2)
           rd0v1(i)    = v1*r(i)/(1 + v1*(f0(i)/prf)**2)
c f_rate replaced with a more exact expression for chirp rate
c           f_rate(i) = -2.d0 * vel**2*(rd0v1(i)/v1/r(i))**2/(wavl*r(i))

c         write(6,*) 'f_rates ', f_rate(i), -2.d0 * (vel*sqrt(re/(re+ht)))**2
c     $        *(rd0v1(i)/v1/r(i))**2/(wavl*r(i))
           bdel(i)   = slope * r(i) + inter
        end do
        
c        write(6,*) 'linear arrays computed '
        linesz    = CACHE_LINE
        iblock    = CACHE_LINE/8
        ioff      = 1 + iand(%loc(tmp_cache(1)),linesz-1)/8
        if (ioff.ne.1) ioff = iblock - ioff + 2
        iblockbeg = iand(%loc(trans(1,1)),linesz-1)/8
        if (iblockbeg.ne.0) iblockbeg = iblock - iblockbeg
        iblockend = iand(nnn-iblockbeg,iblock-1)

        ib = 1
           call cache_copy(trans(ib,1),nnn,tmp_cache(ioff),iblock,
     &                     iblockbeg,nl)
           call rmpatch_work(ib-1,iblockbeg,tmp_cache(ioff),iblock,nl,nnn,f0,
     &                       bdel,r,f_rate,rd0v1,delr,wavl,prf,ideskew)
           call cache_copy(tmp_cache(ioff),iblock,trans(ib,1),nnn,
     &                     iblockbeg,nl)
        continue

        nb = (nnn-iblockend - iblockbeg)/iblock
        nt = 1
c$      nt = mp_numthreads()
        ntblock = ((nb + nt-1)/nt)*iblock
c$doacross local(intblock,intblock_end)
c&,        share(iblockbeg,ntblock,iblock,trans,nl,nnn,f0,bdel,r,
c&               f_rate,rd0v1,delr,wavl,prf,ideskew)
        do intblock = iblockbeg+1, nnn-iblockend, ntblock
           intblock_end = min(intblock+ntblock-1,nnn-iblockend)
           call rmpatch_parallel(intblock,intblock_end,iblock,
     &                           trans,nl,nnn,f0,bdel,r,f_rate,rd0v1,
     &                           delr,wavl,prf,ideskew)
        enddo

        ib = nnn-iblockend+1
           call cache_copy(trans(ib,1),nnn,tmp_cache(ioff),iblock,
     &                     iblockend,nl)
           call rmpatch_work(ib-1,iblockend,tmp_cache(ioff),iblock,nl,nnn,f0,
     &                       bdel,r,f_rate,rd0v1,delr,wavl,prf,ideskew)
           call cache_copy(tmp_cache(ioff),iblock,trans(ib,1),nnn,
     &                     iblockend,nl)
        continue

999     return
	end

      subroutine rmpatch_parallel(intblock,intblock_end,iblock,
     &                            trans,nl,nnn,f0,bdel,r,f_rate,rd0v1,
     &                            delr,wavl,prf,ideskew)

      implicit none
      integer*4 intblock, intblock_end, iblock
      complex*8 trans(nnn,nl)
      integer*4 nl, nnn, ideskew
      real*4 f0(nl), bdel(nl), f_rate(nl), prf
      real*8 r(nl), rd0v1(nl), delr, wavl

      integer*4 ioff, ib
      complex*8 tmp_cache((CACHE_LINE/8)*(nl+1))
 
      ioff = 1 + iand(%loc(tmp_cache(1)),iblock*8-1)/8
      if (ioff.ne.1) ioff = iblock - ioff + 2

      do ib = intblock, intblock_end, iblock
         call cache_copy(trans(ib,1),nnn,tmp_cache(ioff),iblock,
     &                   iblock,nl)
         call rmpatch_work(ib-1,iblock,tmp_cache(ioff),iblock,nl,nnn,f0,
     &                     bdel,r,f_rate,rd0v1,delr,wavl,prf,ideskew)
         call cache_copy(tmp_cache(ioff),iblock,trans(ib,1),nnn,
     &                   iblock,nl)
      enddo

      return
      end
      subroutine rmpatch_work(na0,na_cnt,tmp_cache,ldtc,nl,nnn,f0,bdel,
     &                          r,f_rate,rd0v1,delr,wavl,prf,ideskew)
      implicit none
      integer*4 na0, na_cnt, ldtc, nl, nnn, nfilter, ideskew
      complex*8 tmp_cache(ldtc,nl)
      real*4 f0(nl), bdel(nl), f_rate(nl), prf
      real*8 r(nl), rd0v1(nl), delr, wavl

      real*4 xintp
      common /intp/ xintp(0:65544), nfilter

      integer na, i, k, nvtmp(nl), knt, ii, index(nl), ifrac_arr(nl)
      integer*4 n, ifrac
      real freq
      real*4 ratio, vtmp(nl), frac, c_xintp(8)
      real*8 tmpd
      complex*8 c_ctmpa(nl), c_ctmpb(8)

      do na = 1, na_cnt

c get the interpolation amounts for a given azimuth pixel na as f(line)
         freq=(na0+na-1)/float(nnn)*prf 
         do i = 1,nl
c     frequencies must be within 0.5*prf of centroid
            ratio = (freq-f0(i))/prf
            n = nint(ratio)
            freq = freq - n * prf
c     range of a pixel at freq f, bdel is range correction for interferogram
                 
            if(ideskew.eq.1)then
c  deskewing
               tmpd = bdel(i)+ ((r(i)-(wavl/4.)*f0(i)**2/
     $              f_rate(i))-r(1))/delr +
     $              rd0v1(i)*(1.d0/delr)*(freq**2-f0(i)**2)/prf**2
            else
c  not deskewing
               tmpd  = i + rd0v1(i)*(1.d0/delr)*(freq**2-f0(i)**2)/prf**2
     $              + bdel(i)
            end if
            nvtmp(i) = int(tmpd)
            vtmp(i) = tmpd - int(tmpd)
         enddo
c     write(6,*) 'vtmp computed'

c  interpolate that line according to coeffs determined above
         knt = 0
         do i=1,nl
            c_ctmpa(i)=cmplx(0.,0.)
            if (nvtmp(i).ge.4 .and. nvtmp(i).lt.(nl-4)) then
               knt        = knt + 1
               index(knt) = i
            endif
         enddo
cdir$ ivdep
         do ii = 1, knt
            i     = index(ii)
            frac  = vtmp(i)
            ifrac = 8*nint(frac*float(nfilter))
            c_ctmpa(i) = tmp_cache(na,nvtmp(i)-3)*xintp(ifrac+0)
     2                 + tmp_cache(na,nvtmp(i)-2)*xintp(ifrac+1)
     3                 + tmp_cache(na,nvtmp(i)-1)*xintp(ifrac+2)
     4                 + tmp_cache(na,nvtmp(i)+0)*xintp(ifrac+3)
     5                 + tmp_cache(na,nvtmp(i)+1)*xintp(ifrac+4)
     6                 + tmp_cache(na,nvtmp(i)+2)*xintp(ifrac+5)
     7                 + tmp_cache(na,nvtmp(i)+3)*xintp(ifrac+6)
     8                 + tmp_cache(na,nvtmp(i)+4)*xintp(ifrac+7)
         enddo
         do i = 1, nl
            tmp_cache(na,i) = c_ctmpa(i)
         end do
c     write(6,*) 'interpolation computed'

      enddo                     ! na-loop

      return
      end
#endif


#if (0)
cdir$ ivdep
         do ii = 1, knt
            i     = index(ii)
            frac  = vtmp(i)
            ifrac = 8*nint(frac*float(nfilter))
            c_ctmpa(i) = tmp_cache(na,nvtmp(i)-3)*xintp(ifrac+0)
     2                 + tmp_cache(na,nvtmp(i)-2)*xintp(ifrac+1)
     3                 + tmp_cache(na,nvtmp(i)-1)*xintp(ifrac+2)
     4                 + tmp_cache(na,nvtmp(i)+0)*xintp(ifrac+3)
         enddo
cdir$ ivdep
         do ii = 1, knt
            i     = index(ii)
            frac  = vtmp(i)
            ifrac = 8*nint(frac*float(nfilter))
            c_ctmpa(i) = c_ctmpa(i)
     5                 + tmp_cache(na,nvtmp(i)+1)*xintp(ifrac+4)
     6                 + tmp_cache(na,nvtmp(i)+2)*xintp(ifrac+5)
     7                 + tmp_cache(na,nvtmp(i)+3)*xintp(ifrac+6)
     8                 + tmp_cache(na,nvtmp(i)+4)*xintp(ifrac+7)
         enddo
#endif

        subroutine cache_copy(from,ldf,to,ldt,nrf,ncf)
        complex*8 from(ldf,ncf), to(ldt,nrf)
        integer ldf, ldt, nrf, ncf

        integer i, j

        if (nrf.eq.1) then
           do j = 1, ncf
              to(1,j) = from(1,j)
           enddo
        else if (nrf.eq.2) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
           enddo
        else if (nrf.eq.3) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
              to(3,j) = from(3,j)
           enddo
        else if (nrf.eq.4) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
              to(3,j) = from(3,j)
              to(4,j) = from(4,j)
           enddo
        else if (nrf.eq.5) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
              to(3,j) = from(3,j)
              to(4,j) = from(4,j)
              to(5,j) = from(5,j)
           enddo
        else if (nrf.eq.6) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
              to(3,j) = from(3,j)
              to(4,j) = from(4,j)
              to(5,j) = from(5,j)
              to(6,j) = from(6,j)
           enddo
        else if (nrf.eq.7) then
           do j = 1, ncf
              to(1,j) = from(1,j)
              to(2,j) = from(2,j)
              to(3,j) = from(3,j)
              to(4,j) = from(4,j)
              to(5,j) = from(5,j)
              to(6,j) = from(6,j)
              to(7,j) = from(7,j)
           enddo
        else if (nrf.eq.16) then
           do j = 1, ncf
              to( 1,j) = from( 1,j)
              to( 2,j) = from( 2,j)
              to( 3,j) = from( 3,j)
              to( 4,j) = from( 4,j)
              to( 5,j) = from( 5,j)
              to( 6,j) = from( 6,j)
              to( 7,j) = from( 7,j)
              to( 8,j) = from( 8,j)
              to( 9,j) = from( 9,j)
              to(10,j) = from(10,j)
              to(11,j) = from(11,j)
              to(12,j) = from(12,j)
              to(13,j) = from(13,j)
              to(14,j) = from(14,j)
              to(15,j) = from(15,j)
              to(16,j) = from(16,j)
           enddo
        else
           do j = 1, ncf
              do i = 1, nrf
                 to(i,j) = from(i,j)
              enddo
           enddo
        endif

        return
        end

