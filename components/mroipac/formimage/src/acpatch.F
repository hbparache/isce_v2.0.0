#ifndef PARALLELIZED_ACPATCH
      subroutine ACpatch(trans,nnn,nl,r0,delr,
     .     wavl,vel,fd,fdd,fddd,fdddd,prf,ht,re,
     .     gm,r_platvel,r_platacc,i_lrl,
     .     npfin,a2,a4,slope,inter,ideskew,na_valid)
      
      implicit none
      REAL*8       PI,PI2
      integer nnn,nl,ideskew,npfin,na_valid
      real*4 vel, prf,a2,a4, y2, phi, dx
      real*8 r0, delr,wavl,fd,fdd,fddd, fdddd, ht,slope,inter
      real*8 r(nl), phase, az, re, gm, th, thaz, sinsqref, acc, dot
      real*8 r_platvel(3), r_platacc(3), r_lookvec(3), r_vdotl, r_adotl,r_veln
      integer*4 i, j, k, i_lrl
      integer*4 n, nfc, nf0
      complex*8 trans(nnn,nl),ref(nnn)
      real*4 t, scl
      real*4 a2p, y(nl),f0(nl),f_rate(nl), sinsq
      integer*4  np(nl)
#ifdef TUNED_ACPATCH
      real*4 phase_arr1(  nnn), cos_arr1(  nnn), sin_arr1(  nnn)
      real*4 phase_arr2(2,nnn), cos_arr2(2,nnn), sin_arr2(2,nnn)
c      equivalence (phase_arr1,phase_arr2)
c      equivalence (cos_arr1,cos_arr2)
c      equivalence (sin_arr1,sin_arr2)
#endif
      
c note: - on y1 because chirp is conjugated below

c both ref and trans are forward transformed and need scaling down

        pi=4.d0*atan2(1.d0,1.d0)
        pi2=2.d0*pi

      scl = 1./float(nnn)**2

      a2p = a2
      if(ideskew .eq. 0) a2p = 0.

      dx = vel/prf

      acc = gm/(re+ht)**2

      call norm(r_platvel,r_veln)
      
      do i = 1 , nl
         r(i) = r0 + float(i-1)*delr
         f0(i) = fd + ( fdd + ( fddd+fdddd*r(i) ) *r(i) )*r(i)
         th=dacos(((ht+re)**2+r(i)*r(i)-re**2)/(2.d0*r(i)*(re+ht)))
         if(i_lrl .eq. 0) then
            sinsqref = f0(i) * wavl/(2.d0*vel*sin(th))
            f_rate(i) = (2.d0/wavl)*(acc*cos(th)+((vel*sinsqref)**2-vel**2)/r(i))
         else
c replace with an even more exact expression for chirp rate
            thaz = asin(((wavl*f0(i)/(2.d0*sin(th)))+(r_platvel(3)/tan(th)))/
     $           sqrt(r_platvel(1)**2+r_platvel(2)**2))-i_lrl*atan(r_platvel(2)/r_platvel(1))
            r_lookvec(1) =  sin(th)*sin(thaz)
            r_lookvec(2) =  sin(th)*cos(thaz)*i_lrl
            r_lookvec(3) = -cos(th)

            r_vdotl = dot(r_lookvec,r_platvel)
            r_adotl = dot(r_lookvec,r_platacc)
            
            f_rate(i) = 2.d0*(r_adotl + (r_vdotl**2 - r_veln**2)/r(i))/(wavl)
         end if
         np(i) = int(r(i)*a4)/2
         phi = 0.
         if(ht .lt. r(i)) phi = acos(ht/r(i))
         az = slope * r(i) + inter
         y2 = pi2 * az / float(nnn)
         sinsq = wavl*f0(i)/2./vel
         y(i) =  r(i) * a2p * sinsq + y2

c  zero out ref
         do  j = 1, nnn
            ref(j) = cmplx(0.,0.)
         end do
c  create reference function
#ifndef TUNED_ACPATCH
c         phase = pi * f0(i)**2 /f_rate(i)
         phase = 0.d0
         ref(1) = cmplx(cos(phase),sin(phase))*scl
         do  j = 1, np(i)
            t = float(j)/prf
            phase = pi * f_rate(i)*t*t + pi2*f0(i)*t
            ref(j+1) = cmplx(cos(phase),sin(phase))*scl
            phase = pi * f_rate(i)*t*t - pi2*f0(i)*t
            ref(-j+nnn+1) = cmplx(cos(phase),sin(phase))*scl
         end do
#else
c         phase_arr2(1,1) =  pi * f0(i)**2 /f_rate(i)
         phase_arr2(1,1) =  0.0d0
         phase_arr2(2,1) =  0.0d0
         do j = 1, np(i)
            t = float(j)/prf
            phase_arr2(1,j+1) = pi * f_rate(i)*t*t + pi2*f0(i)*t
            phase_arr2(2,j+1) = pi * f_rate(i)*t*t - pi2*f0(i)*t
         enddo
         call vfcos$(phase_arr2(1,1),cos_arr2(1,1),%val(2*(np(i)+1)),%val(1),%val(1))
         call vfsin$(phase_arr2(1,1),sin_arr2(1,1),%val(2*(np(i)+1)),%val(1),%val(1))
         ref(1) = cmplx(cos_arr2(1,1),sin_arr2(1,1))*scl
         do j = 1, np(i)
            ref(j+1)      = cmplx(cos_arr2(1,j+1),sin_arr2(1,j+1))*scl
            ref(-j+nnn+1) = cmplx(cos_arr2(2,j+1),sin_arr2(2,j+1))*scl
         enddo
#endif

c  transform the reference
         call cfft1d_jpl(nnn,ref,-1)

c  multiply the reference by the data
         n = nint(f0(i)/prf)
         nf0 = nnn*(f0(i)-n*prf)/prf
         nfc = nf0 + nnn/2
         if(nfc .gt. nnn) nfc = nfc - nnn
#ifndef TUNED_ACPATCH
         phase = - y(i) * nf0
         do k = 1, nfc
            trans(k,i)=trans(k,i)*conjg(ref(k))*cmplx(cos(phase),sin(phase))
            phase = phase + y(i)
         end do
           
         phase = - y(i) * (nf0+1)
         do k = nnn, nfc+1,-1
            trans(k,i)=trans(k,i)*conjg(ref(k))*cmplx(cos(phase),sin(phase))
            phase = phase - y(i)
         end do
#else
         do k = 1, nfc
            phase_arr1(k) = - y(i) * nf0 + (k-1)*y(i)
         enddo
         call vfcos$(phase_arr1(1),cos_arr1(1),%val(nfc),%val(1),%val(1))
         call vfsin$(phase_arr1(1),sin_arr1(1),%val(nfc),%val(1),%val(1))
         do k = 1, nfc
            trans(k,i)=trans(k,i)*conjg(ref(k))*cmplx(cos_arr1(k),sin_arr1(k))
         enddo

         do k = nnn, nfc+1, -1
            phase_arr1(nnn-k+1) = - y(i) * (nf0+1) - (nnn-k)*y(i)
         enddo
         call vfcos$(phase_arr1(1),cos_arr1(1),%val(nnn-nfc),%val(1),%val(1))
         call vfsin$(phase_arr1(1),sin_arr1(1),%val(nnn-nfc),%val(1),%val(1))
         do k = nnn, nfc+1, -1
            trans(k,i)=trans(k,i)*conjg(ref(k))*cmplx(cos_arr1(nnn-k+1),sin_arr1(nnn-k+1))
         enddo
#endif
c  inverse transform the product
         call cfft1d_jpl(nnn,trans(1,i),1)

      end do

      return
      end
#else
      subroutine ACpatch(trans,nnn,nl,r0,delr,
     .     wavl,vel,fd,fdd,fddd,fdddd,prf,ht,re,gm,
     .     r_platvel,r_platacc,i_lrl,
     .     npfin,a2,a4,slope,inter,ideskew,na_valid)
      
      implicit none
      integer nnn,nl,ideskew,npfin,na_valid
      real*4 vel, prf,a2,a4,dx
      real*8 r0, delr,wavl,fd,fdd,fddd,fdddd, ht,slope,inter,re, gm
      real*8 r_platvel(3), r_platacc(3)
      integer*4 i, n_threads, iblock, iend,i_lrl
      complex*8 trans(nnn,nl)
      real*4 scl, a2p
c$    integer*4 mp_numthreads      

c note: - on y1 because chirp is conjugated below

c both ref and trans are forward transformed and need scaling down

      scl = 1./float(nnn)**2

      a2p = a2
      if(ideskew .eq. 0) a2p = 0.

      dx = vel/prf
      n_threads = 1
c$    n_threads = mp_numthreads()
      iblock    = (nl + n_threads-1)/n_threads
c$doacross local(i,iend), share(scl,a2p,dx,trans,nnn,nl,r0,delr
c$&,                            wavl,vel,fd,fdd,fddd,fdddd,prf,ht,gm
c&&,                            r_platvel,r_platacc,i_lrl
c$&,                            npfin,a2,a4,slope,inter,ideskew,na_valid)
      do i = 1, nl, iblock
         iend = min(i+iblock-1,nl)
         call acpatch_work(i,iend,scl,a2p,dx,trans,nnn,nl,r0,delr,
     .     wavl,vel,fd,fdd,fddd,fdddd,prf,ht,re,gm,
     .     r_platvel,r_platacc,i_lrl,
     .     npfin,a2,a4,slope,inter,ideskew,na_valid)
      enddo

      return
      end

      subroutine acpatch_work(ibeg,iend,scl,a2p,dx,trans,nnn,nl,
     .     r0,delr,wavl,vel,fd,fdd,fddd,fdddd,prf,ht,re,gm,
     .     r_platvel,r_platacc,i_lrl,
     .     npfin,a2,a4,slope,inter,ideskew,na_valid)
      
      implicit none
      REAL*8       PI,PI2
      integer nnn,nl,ideskew,npfin,na_valid
      real*4 vel, prf,a2,a4, y2, phi, dx
      real*8 r0, delr,wavl,fd,fdd,fddd,fdddd, ht,slope,inter, rt,ft
      real*8 r(nl), phase, az, re, gm, th, thaz, sinsqref, acc, dot
      real*8 r_platvel(3), r_platacc(3), r_lookvec(3), r_vdotl, r_adotl,r_veln
      integer*4 i, j, k, l, i_lrl
      integer*4 n, nfc, nf0, ibeg, iend
      complex*8 trans(nnn,nl),ctmp,ref(nnn)
      real*4 Dm,t, scl
      real*4 a2p, y(nl),f0(nl),f_rate(nl), sinsq
      integer*4 firsttime, np(nl), in

      real*4 phase_arr1(  nnn), cos_arr1(  nnn), sin_arr1(  nnn)
      real*4 phase_arr2(2,nnn), cos_arr2(2,nnn), sin_arr2(2,nnn)
c      equivalence (phase_arr1,phase_arr2)
c      equivalence (cos_arr1,cos_arr2)
c      equivalence (sin_arr1,sin_arr2)

      acc = gm/(re+ht)**2

      pi=4.d0*atan2(1.d0,1.d0)
      pi2=2.d0*pi
      call norm(r_platvel,r_veln)

      do i = ibeg, iend
         r(i) = r0 + float(i-1)*delr
         f0(i) = fd + ( fdd + ( fddd+fdddd*r(i) ) *r(i) )*r(i)
         th=dacos(((ht+re)**2+r(i)*r(i)-re**2)/(2.d0*r(i)*(re
     $     +ht)))
         if(i_lrl .eq. 0) then
            sinsqref = f0(i) * wavl/(2.d0*vel*sin(th))
            f_rate(i) = (2.d0/wavl)*(acc*cos(th)+((vel*sinsqref)**2-vel**2)/r(i))
         else
            thaz = asin(((wavl*f0(i)/(2.d0*sin(th)))+(r_platvel(3)/tan(th)))/
     $           sqrt(r_platvel(1)**2+r_platvel(2)**2))-i_lrl*atan(r_platvel(2)/r_platvel(1))
            r_lookvec(1) =  sin(th)*sin(thaz)
            r_lookvec(2) =  sin(th)*cos(thaz)*i_lrl
            r_lookvec(3) = -cos(th)
            r_vdotl = dot(r_lookvec,r_platvel)
            r_adotl = dot(r_lookvec,r_platacc)
            
            f_rate(i) = 2.d0*(r_adotl + (r_vdotl**2 - r_veln**2)/r(i))/(wavl)
         end if

         np(i) = int(r(i)*a4)/2
         phi = 0.
         if(ht .lt. r(i)) phi = acos(ht/r(i))
         az = slope * r(i) + inter
         y2 = pi2 * az / float(nnn)
         sinsq = wavl*f0(i)/2./vel
         y(i) =  r(i) * a2p * sinsq + y2

c  zero out ref
         do  j = 1, nnn
            ref(j) = cmplx(0.,0.)
         end do
c  create reference function
#ifndef TUNED_ACPATCH
c         phase = pi * f0(i)**2 /f_rate(i)
         phase = 0.d0
         ref(1) = cmplx(cos(phase),sin(phase))*scl
         do  j = 1, np(i)
            t = float(j)/prf
            phase = pi * f_rate(i)*t*t + pi2*f0(i)*t
            ref(j+1) = cmplx(cos(phase),sin(phase))*scl
            phase = pi * f_rate(i)*t*t - pi2*f0(i)*t
            ref(-j+nnn+1) = cmplx(cos(phase),sin(phase))*scl
         end do
#else
c         phase_arr2(1,1) =  pi * f0(i)**2 /f_rate(i)
         phase_arr2(1,1) =  0.d0
         phase_arr2(2,1) =  0.0d0
         do j = 1, np(i)
            t = float(j)/prf
            phase_arr2(1,j+1) = pi * f_rate(i)*t*t + pi2*f0(i)*t
            phase_arr2(2,j+1) = pi * f_rate(i)*t*t - pi2*f0(i)*t
         enddo
         call vfcos$(phase_arr2(1,1),cos_arr2(1,1),%val(2*(np(i)+1)),%val(1),%val(1))
         call vfsin$(phase_arr2(1,1),sin_arr2(1,1),%val(2*(np(i)+1)),%val(1),%val(1))
         ref(1) = cmplx(cos_arr2(1,1),sin_arr2(1,1))*scl
         do j = 1, np(i)
            ref(j+1)      = cmplx(cos_arr2(1,j+1),sin_arr2(1,j+1))*scl
            ref(-j+nnn+1) = cmplx(cos_arr2(2,j+1),sin_arr2(2,j+1))*scl
         enddo
#endif
c  transform the reference
         call cfft1d_jpl(nnn,ref,-1)
c  multiply the reference by the data
         n = nint(f0(i)/prf)
         nf0 = nnn*(f0(i)-n*prf)/prf
         nfc = nf0 + nnn/2
         if(nfc .gt. nnn) nfc = nfc - nnn
#ifndef TUNED_ACPATCH
         phase = - y(i) * nf0
         do k = 1, nfc
            trans(k,i)=trans(k,i)*conjg(ref(k))*cmplx(cos(phase),sin(phase))
            phase = phase + y(i)
         end do
           
         phase = - y(i) * (nf0+1)
         do k = nnn, nfc+1,-1
            trans(k,i)=trans(k,i)*conjg(ref(k))*cmplx(cos(phase),sin(phase))
            phase = phase - y(i)
         end do
#else
         do k = 1, nfc
            phase_arr1(k) = - y(i) * nf0 + (k-1)*y(i)
         enddo
         call vfcos$(phase_arr1(1),cos_arr1(1),%val(nfc),%val(1),%val(1))
         call vfsin$(phase_arr1(1),sin_arr1(1),%val(nfc),%val(1),%val(1))
         do k = 1, nfc
            trans(k,i)=trans(k,i)*conjg(ref(k))*cmplx(cos_arr1(k),sin_arr1(k))
         enddo

         do k = nnn, nfc+1, -1
            phase_arr1(nnn-k+1) = - y(i) * (nf0+1) - (nnn-k)*y(i)
         enddo
         call vfcos$(phase_arr1(1),cos_arr1(1),%val(nnn-nfc),%val(1),%val(1))
         call vfsin$(phase_arr1(1),sin_arr1(1),%val(nnn-nfc),%val(1),%val(1))
         do k = nnn, nfc+1, -1
            trans(k,i)=trans(k,i)*conjg(ref(k))*cmplx(cos_arr1(nnn-k+1),sin_arr1(nnn-k+1))
         enddo
#endif
c  inverse transform the product
         call cfft1d_jpl(nnn,trans(1,i),1)
      enddo

      return
      end
#endif
