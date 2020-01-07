!c  topocorrect - approximate topo correction
      subroutine correct(intAccessor,zschAccessor,topophaseMphAccessor,topophaseFlatAccessor)
      use correctState
      use fortranUtils

      implicit none
      include 'omp_lib.h'
      integer*8 zschAccessor,intAccessor,topophaseMphAccessor,topophaseFlatAccessor
      integer lineFile
      !integer width, length
      real*4, allocatable ::zsch(:)
      real*4  r_phase,r_phase_zero
      real*8, allocatable :: rho(:),squintshift(:)
      complex, allocatable::c_int(:),c_flat(:),c_topo(:),c_topomht(:)
      real*8 sch(3)
      real*8 r2d,refhgt
      integer pixel
      real*8 beta,fd, temp
      character*1 num(9)
      character*2 numnum(10)
      real*8 b1(3),b2(3),b1mag,b2mag,s1mag,s2mag,smmag,rm1,rm2
      real*8 rho1,rho2,r_los(3),r_schp(3)
      real*8 smxyz(3),s1xyz(3),s2xyz(3)
      real*8 dot,tanbeta,cosalpha
      real*8 arg,re,rminoraxis,rlatg,st,ct
      real*8 sinalpha,t(3),tprime(3),moc(3),cosmu,sat1(3),sat2(3)
      integer line,j
      real*8 flat,phresid
      real*8 tflat(3),coschi,sinchi
      real*8 eta1,eta2
      real*8 coseta1,coseta2
      real*8 pi 
      real*8 q,q0

      data num/'1','2','3','4','5','6','7','8','9'/
      data numnum/'10','11','12','13','14','15','16','17','18','19'/

!c  types needed

        type :: ellipsoid 
           real*8 r_a           ! semi-major axis
           real*8 r_e2          ! eccentricity-squared of earth ellisoid
        end type ellipsoid
        type(ellipsoid) :: elp

        type :: pegpoint 
           real*8 r_lat         ! peg latitude
           real*8 r_lon         ! peg longitude
           real*8 r_hdg         ! peg heading
        end type pegpoint
        type(pegpoint) :: peg
   
        type :: pegtrans 
           real*8 r_mat(3,3)    !transformation matrix SCH->XYZ
           real*8 r_matinv(3,3) !transformation matrix XYZ->SCH
           real*8 r_ov(3)       !Offset vector SCH->XYZ
           real*8 r_radcur      !peg radius of curvature
        end type pegtrans
        type(pegtrans) :: ptm

        pi = getPI()

        lineFile  = 0



!$omp parallel
        if(omp_get_thread_num().eq.1) then
            print *, 'Max threads used: ', omp_get_num_threads()
        end if
!$omp end parallel
!c this should be fixed by decoupling the mocomp array length from the interferogram length
!c	
        print *,'start sample, length : ',is_mocomp,length
        length=min(length,(dim1_s_mocompArray+Nazlooks/2-is_mocomp)/Nazlooks)
        print *, 'reset length: ',length

!c  allocate variable arrays
        allocate (zsch(width))
        allocate (rho(width))
        allocate (c_int(width))
        allocate (c_flat(width))
        allocate (c_topo(width))
        allocate (c_topomht(width))
        allocate (squintshift(width))

!c  some constants
      
      refhgt=0
      r2d=180.d0/pi
      elp%r_a = major
      elp%r_e2 = eccentricitySquared
      
      peg%r_lat =  peglat
      peg%r_lon =  peglon
      peg%r_hdg =  peghdg

!c  get re and insert it into database
      rminoraxis=sqrt(1.-elp%r_e2)*elp%r_a
      rlatg = atan(tan(peg%r_lat)*elp%r_a*elp%r_a/(rminoraxis*rminoraxis));
      st = sin(rlatg);
      ct = cos(rlatg);
      arg = (ct*ct)/(elp%r_a*elp%r_a) + (st*st)/(rminoraxis*rminoraxis);
      re = 1./(sqrt(arg));

      print *,'re, rminoraxis',re,rminoraxis
      print *,'Local earth radius of curvature: ',rcurv


      print *, 'Ncoeff : ', ndop
      print *, 'Coeffs: ', dopcoeff
!c  precalculate squint-related shift for each range location
      line=1
      do pixel=1,width
         temp=1.0d0
         fd=0.0d0
         do j=1,ndop
            fd = fd + dopcoeff(j)*temp
            temp = temp*pixel
         end do
         fd = fd*prf
         rho(pixel)=r0+rspace*(pixel-1)*Nrnglooks
         tanbeta=-fd*(height+rcurv)*wvl*rho(pixel)/vel/(rcurv**2+(height+rcurv)**2-rho(pixel)**2)
         squintshift(pixel) = -rcurv*atan(tanbeta)
      end do


!c  initialize the transformation matrices
      call radar_to_xyz(elp,peg,ptm)

      do line=1,length

         !c Read the height file
         call getLineSequential(zschAccessor,zsch,lineFile)


         r_schp(1) = midpoint(1,is_mocomp+line*Nazlooks-Nazlooks/2)
         r_schp(2) = midpoint(2,is_mocomp+line*Nazlooks-Nazlooks/2)
         r_schp(3) = midpoint(3,is_mocomp+line*Nazlooks-Nazlooks/2)


!c  convert sc position to xyz
         call convert_sch_to_xyz(ptm,smsch(1,is_mocomp+line*Nazlooks-Nazlooks/2),smxyz,0)
         call convert_sch_to_xyz(ptm,s1sch(1,is_mocomp+line*Nazlooks-Nazlooks/2),s1xyz,0)
         call convert_sch_to_xyz(ptm,s2sch(1,is_mocomp+line*Nazlooks-Nazlooks/2),s2xyz,0)

         smmag=height+rcurv
         s1mag=s1sch(3,is_mocomp+line*Nazlooks-Nazlooks/2)+rcurv !from rc 
         s2mag=s2sch(3,is_mocomp+line*Nazlooks-Nazlooks/2)+rcurv !from rc
         b1=s1xyz-smxyz
         b2=s2xyz-smxyz
         b1mag=sqrt(b1(1)**2+b1(2)**2+b1(3)**2)
         b2mag=sqrt(b2(1)**2+b2(2)**2+b2(3)**2)

         coseta1=(smmag**2+s1mag**2-b1mag**2)/(2*smmag*s1mag)
         if(coseta1.ge.1.d0)coseta1=1.d0  ! roundoff errors here create nans
         eta1=acos(coseta1)
         if(s1sch(2,is_mocomp+line*Nazlooks-Nazlooks/2).lt.0.)eta1=-eta1
         coseta2=(smmag**2+s2mag**2-b2mag**2)/(2*smmag*s2mag)
         if(coseta2.ge.1.d0)coseta2=1.d0  ! roundoff errors here create nans
         eta2=acos(coseta2)
         if(s2sch(2,is_mocomp+line*Nazlooks-Nazlooks/2).lt.0.)eta2=-eta2
         sat1(1)=0.
         sat1(2)=s1mag*sin(eta1)
         sat1(3)=s1mag*cos(eta1)
         sat2(1)=0.
         sat2(2)=s2mag*sin(eta2)
         sat2(3)=s2mag*cos(eta2)
         moc(1)=0.
         moc(2)=0.
         moc(3)=rcurv+height
         
         !$omp parallel do private(pixel,beta,cosalpha,sch,r_los,r_phase,r_phase_zero) &
         !$omp private(phresid,flat,q,q0) &
         !$omp private(cosmu,sinmu,rm1,rm2) &
         !$omp private(sinalpha,t,tprime,tflat,coschi,sinchi,rho1,rho2) &
         !$omp shared(eta1,eta2,sat1,sat2,moc) &
         !$omp shared(width,height,rcurv,zsch,rho,s_mocomp)&
         !$omp shared(is_mocomp,line,Nazlooks,squintshift,ptm,r_schp) &
         !$omp shared(pi,wvl,mocbase,c_topo,ilrl)
         do pixel=1,width
!c  first get phase for elevated pixel
!  get sch for pixel under consideration
            cosalpha=((height+rcurv)**2+(rcurv+zsch(pixel))**2-rho(pixel)**2)/2./(height+rcurv)/(rcurv+zsch(pixel))
            sch(1)=s_mocomp(is_mocomp+line*Nazlooks-Nazlooks/2)
            sch(1)=sch(1)+squintshift(pixel)
            beta=-squintshift(pixel)/rcurv 

            !!Accounting for satellite look side
            sch(2)=ilrl*rcurv*acos(cosalpha/cos(beta))
            sch(3)=zsch(pixel)

            call get_tpsch(ptm,r_schp,ptm,sch,r_los)
            call unitvec(r_los,r_los)

            r_phase = -(4.*pi/wvl)*dot(r_los,mocbase(1,is_mocomp+Nazlooks*line+Nazlooks/2))
            q=-r_phase*wvl/4/pi

!c  compute topo correction term for unknown target height
!c
!c  place points in a plane and reference coords to that plane
            sinalpha=sqrt(1-cosalpha**2)

            t(1)=0.  ! true target location in plane
            t(2)=-ilrl*(rcurv+zsch(pixel))*sinalpha
            t(3)=(rcurv+zsch(pixel))*cosalpha

            rho1=sqrt((t(2)-sat1(2))**2+(t(3)-sat1(3))**2)
            rho2=sqrt((t(2)-sat2(2))**2+(t(3)-sat2(3))**2)

            cosmu=(s1mag**2+rcurv**2-rho1**2)/(2*s1mag*rcurv)

            tprime(1)=0.  ! location of zero-height pixel
            tprime(2)=rcurv*sin(eta1-ilrl*acos(cosmu))
            tprime(3)=rcurv*cos(eta1-ilrl*acos(cosmu))
            rm1=sqrt((tprime(2)-moc(2))**2+(tprime(3)-moc(3))**2)
            cosmu=(s2mag**2+rcurv**2-rho2**2)/(2*s2mag*rcurv)
            tprime(1)=0.
            tprime(2)=rcurv*sin(eta2-ilrl*acos(cosmu))
            tprime(3)=rcurv*cos(eta2-ilrl*acos(cosmu))
            rm2=sqrt((tprime(2)-moc(2))**2+(tprime(3)-moc(3))**2)

!c  flat earth correction construction
            coschi=((rcurv+height)**2+rcurv**2-rho(pixel)**2)/(2*(rcurv+height)*rcurv)
            sinchi=sqrt(1-coschi**2)
            tflat(1)=0.
            tflat(2)=-ilrl*rcurv*sinchi
            tflat(3)=rcurv*coschi

            flat=dot(t-tflat,sat2-sat1)/rho(pixel)
            phresid=(rm2-rm1)+flat
            phresid=phresid*4*pi/wvl

!repeat phase calculation for zero-elevation pixel
            cosalpha=((height+rcurv)**2+(rcurv+0.0)**2-rho(pixel)**2)/2./(height+rcurv)/(rcurv+0.0)
            sch(1)=s_mocomp(is_mocomp+line*Nazlooks-Nazlooks/2)
            sch(1)=sch(1)+squintshift(pixel)  
            beta=-squintshift(pixel)/rcurv 
            sch(2)=ilrl*rcurv*acos(cosalpha/cos(beta))
            sch(3)= 0.0

            call get_tpsch(ptm,r_schp,ptm,sch,r_los)
            call unitvec(r_los,r_los)

            r_phase_zero = -(4.*pi/wvl)*dot(r_los,mocbase(1,is_mocomp+Nazlooks*line+Nazlooks/2))
            q0=-r_phase_zero*wvl/4/pi
            c_topo(pixel)=cmplx(cos(r_phase-r_phase_zero),sin(r_phase-r_phase_zero))
!c  apply residual correction from mocomp lack of elevation data
            c_topo(pixel)=c_topo(pixel)*cmplx(cos(phresid),sin(phresid))

         enddo
         !$omp end parallel do
           
         
         call getLineSequential(intAccessor,c_int(:),lineFile)

         !$omp parallel do private(pixel)
         !$omp shared(c_flat,c_topomht,c_topo,c_int)
         do pixel=1,width
              c_flat(pixel)=c_int(pixel)*conjg(c_topo(pixel))
              c_topomht(pixel)=c_topo(pixel)*abs(c_int(pixel))
         end do
         !$omp end parallel do


         call setLineSequential(topophaseMphAccessor,c_topomht(:))
         call setLineSequential(topophaseFlatAccessor,c_flat(:))
      enddo


       deallocate (zsch)
       deallocate (rho)
       deallocate (c_int)
       deallocate (c_flat)
       deallocate (c_topo)
       deallocate (squintshift)
      end

