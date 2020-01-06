!c  dismphfile - fortran version
      
      subroutine dismphfile(accessorIn,accessorOut)
      use dismphfileState
      implicit none
      integer*8 accessorIn, accessorOut
      !character*60 str,file
      integer statb(13),fstat
      complex, allocatable :: cdata(:)
      real r(360), g(360), b(360)
      integer*1, allocatable :: rgb(:,:,:)
      integer i,j,iphase,ival,isum
      real*4 amp,scalemag,sum,phase

     
!      if(iargc().lt.2)then
!         print *,'Usage: dismphfile infile length <firstline=1> <nlines> <scale=1.> <exponent=0.3> <flipflag=0>'
!         stop
!      end if

!      call getarg(1,file)
!      call getarg(2,str)
!      read(str,*)len
!      ifirst=1
!      if(iargc().ge.3)then
!         call getarg(3,str)
!         read(str,*)ifirst
!      end if
!      lines=10000000
!      if(iargc().ge.4)then
!         call getarg(4,str)
!         read(str,*)lines
!      end if
!      scale=1.0
!      if(iargc().ge.5)then
!         call getarg(5,str)
!         read(str,*)scale
!      end if
!      expo=0.3
!      if(iargc().ge.6)then
!         call getarg(6,str)
!         read(str,*)expo
!      end if
!      iflip=0

!      open(21,file=file,access='direct',recl=len*8)
!      ierr=fstat(21,statb)
!      nd=statb(8)/8/len
!      write(*,*)'Lines in file: ',nd
!      if(nd.lt.ifirst+lines-1)lines=nd-ifirst+1

!c  allocate rgb array
      allocate (rgb(len,lines,4))
      allocate(cdata(len))
!c  set up color tables
      do i=1,120
         r(i) = float(i) * 2.13 * 155./255. + 100 
         g(i) = float (120 -i) * 2.13 * 155./255. + 100
         b(i) = 255
      end do
      do i=121,240
         ival = i - 121
         r(i)= 255. 
         g(i) = float (ival) *  2.13 * 155./255. + 100. 
         b(i) = float (239 - i) * 2.13 * 155./ 255. + 100. 
      end do
      do i=241,360
         ival = i - 241.
         r(i) = float (359 - i)  * 2.13 * 155. / 255. + 100.
         g(i) = 255. ;
         b(i) = float (ival) * 2.13 * 155. / 255. + 100.
      end do

!c  scale for amplitude as in c++ version
      sum=0.
      isum=0
      do i=ifirst,ifirst+lines-1,32
      !  read(21,rec=i)(cdata(k),k=1,len)
         call getLine(accessorIn,cdata,i)
         do j=32,len-32,32
            isum=isum+1
            sum=sum+cabs(cdata(j))**expo
         end do
      end do
      scalemag = scale*150/(sum/isum)
      print *,'scale factor: ',scalemag

!c  now process each line
      do i=ifirst,ifirst+lines-1

         call getLine(accessorIn,cdata,i)
         !read(21,rec=i)(cdata(k),k=1,len)
         do j=1,len
            amp=cabs(cdata(j))**expo * scalemag/255.
            if(amp.gt.0.999)amp=0.999
            phase=atan2(aimag(cdata(j)),real(cdata(j)))*180/atan(1.)/4.
            iphase=nint(phase)
            if(iphase.lt.1)iphase=iphase+360
            if(iphase.gt.360)iphase=360
!c            print *,amp,iphase,phase
            rgb(j,i,1)=r(iphase)*amp
            rgb(j,i,2)=g(iphase)*amp
            rgb(j,i,3)=b(iphase)*amp
            rgb(j,i,4)=255
            if(amp.le.1.e-10)rgb(j,i,4)=0
         end do
      end do

!c  save as a tiff
      call writetiff(accessorOut,rgb,len,lines)

      deallocate(rgb)
      deallocate(cdata)
      end


