!c  crossmul - cross multiply two files, one conjugated, form int and amp file
      subroutine crossmul(cst, slcAccessor1, slcAccessor2, ifgAccessor, ampAccessor) BIND(C,name='crossmul_f')

      use, intrinsic :: iso_c_binding
      use crossmulState

      implicit none

      include 'omp_lib.h'
      type(crossmulType):: cst
      integer (C_INT64_T) slcAccessor1
      integer (C_INT64_T) slcAccessor2
      integer (C_INT64_T) ifgAccessor
      integer (C_INT64_T) ampAccessor
      complex*8, allocatable:: in1(:,:),in2(:,:),igram(:,:),amp(:,:)
      complex*8, allocatable:: up1(:,:),up2(:,:),inline1(:),inline2(:)
      complex*8, allocatable:: igramacc(:),ampacc(:)
      complex*8, allocatable:: igramtemp(:,:),amptemp(:,:)
      integer n, i, j, k, nnn, line
      integer nblocks, iblk, nl


      !!!!!!For now, making local copies
      !!!!!!Could access anywhere in code using cst%
      integer :: na, nd, looksac, looksdn, blocksize
      double precision:: scale

      na = cst%na
      nd = cst%nd
      looksac = cst%looksac
      looksdn = cst%looksdn
      blocksize = cst%blocksize
      scale = cst%scale

      !$omp parallel
      n=omp_get_num_threads()
      !$omp end parallel
      print *, 'Max threads used: ', n

!c  get ffts lengths for upsampling
      do i=1,16
         nnn=2**i
         if(nnn.ge.na)go to 11
      end do
11    print *,'FFT length: ',nnn

      call cfft1d_jpl(nnn, igramacc, 0)  !c Initialize FFT plan
      call cfft1d_jpl(2*nnn, igramacc, 0)

      !c Number of blocks needed
      nblocks = CEILING(nd/(1.0*blocksize*looksdn))
      print *, 'Overall:', nd, blocksize*looksdn, nblocks
      allocate(in1(na,looksdn*blocksize), in2(na,looksdn*blocksize))
      allocate(igramtemp(na/looksac,blocksize), amptemp(na/looksac,blocksize))


      do iblk=1, nblocks
          k = (iblk-1)*blocksize*looksdn+1
          in1 = cmplx(0., 0.)
          in2 = cmplx(0., 0.)
          igramtemp = cmplx(0., 0.)
          amptemp = cmplx(0., 0.)

          if (iblk.ne.nblocks) then
              nl = looksdn*blocksize
          else
              nl = (nd - (nblocks-1)*blocksize*looksdn)
          endif

!c          print *, 'Block: ', iblk, k, nl
       
          do j=1, nl
            call getLineSequential(slcAccessor1,in1(:,j),k)
          end do


          if (slcAccessor1.ne.slcAccessor2) then
              do j=1, nl
                call getLineSequential(slcAccessor2,in2(:,j),k)
              end do
          else
            in2 = in1
          endif
          in1 = in1*scale
          in2 = in2*scale

          !$omp parallel do private(up1,up2,inline1,inline2,igram,amp) &
          !$omp private(igramacc,ampacc,j,k,i,line) &
          !$omp shared(in1,in2,igramtemp,amptemp) &
          !$omp shared(looksdn,looksac,scale,na,nnn, nd) 

          do line=1,nl/looksdn
                !c  allocate the local arrays
                allocate (igram(na*2,looksdn),amp(na*2,looksdn))
                allocate (igramacc(na),ampacc(na))
                allocate (up1(nnn*2,looksdn),up2(nnn*2,looksdn),inline1(nnn),inline2(nnn))
    

                up1=cmplx(0.,0.)  ! upsample file 1
                do i=1,looksdn
                    inline1(1:na)=in1(:,i+(line-1)*looksdn)
                    inline1(na+1:nnn)=cmplx(0.,0.)
                    call cfft1d_jpl(nnn, inline1, -1)

        
                    up1(1:nnn/2,i)=inline1(1:nnn/2)
                    up1(2*nnn-nnn/2+1:2*nnn,i)=inline1(nnn/2+1:nnn)
                    call cfft1d_jpl(2*nnn, up1(1,i), 1)
                end do
                up1=up1/nnn

                up2=cmplx(0.,0.)  ! upsample file 2
                do i=1,looksdn
                    inline2(1:na)=in2(:,i+(line-1)*looksdn)
                    inline2(na+1:nnn)=cmplx(0.,0.)
                    call cfft1d_jpl(nnn, inline2, -1)

                    up2(1:nnn/2,i)=inline2(1:nnn/2)
                    up2(2*nnn-nnn/2+1:2*nnn,i)=inline2(nnn/2+1:nnn)
                    call cfft1d_jpl(2*nnn, up2(1,i), 1)
               end do
               up2=up2/nnn

               igram(1:na*2,:)=up1(1:na*2,:)*conjg(up2(1:na*2,:))
               amp(1:na*2,:)=cmplx(cabs(up1(1:na*2,:))**2,cabs(up2(1:na*2,:))**2)

               !c  reclaim the extra two across looks first
               do j=1,na
                   igram(j,:) = igram(j*2-1,:)+igram(j*2,:)
                   amp(j,:) = amp(j*2-1,:)+amp(j*2,:)
               end do

               !c     looks down 
               igramacc=sum(igram(1:na,:),2)
               ampacc=sum(amp(1:na,:),2)

               !c     looks across
               do j=0,na/looksac-1
                  do k=1,looksac
                      igramtemp(j+1,line)=igramtemp(j+1,line)+igramacc(j*looksac+k)
                      amptemp(j+1, line)=amptemp(j+1, line)+ampacc(j*looksac+k)
                  end do
                  amptemp(j+1, line)=cmplx(sqrt(real(amptemp(j+1, line))),sqrt(aimag(amptemp(j+1, line))))
               end do

              deallocate (up1,up2,igramacc,ampacc,inline1,inline2,igram,amp)
         end do
         !$omp end parallel do
        
         do line=1, nl/looksdn
            call setLineSequential(ifgAccessor,igramtemp(1,line))
            call setLineSequential(ampAccessor,amptemp(1,line))
         end do

      enddo
      deallocate(in1, in2, igramtemp, amptemp)
      call cfft1d_jpl(nnn, igramacc, 2)  !c Uninitialize FFT plan
      call cfft1d_jpl(2*nnn, igramacc, 2) 

      end


