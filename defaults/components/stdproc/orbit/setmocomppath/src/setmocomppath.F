c  setmocomppath - pick a mocomp trajectory from two insar scenes
c    derived from: orbit2sch - convert from orbit xyz to sch coordinates
      subroutine setmocomppath
      use setmocomppathState
      implicit none
      character*20000 MESSAGE
      double precision,allocatable, dimension(:,:) :: sch,llhv,vsch
      double precision ,allocatable, dimension(:) :: time
      double precision minor,lat,lon,glat,rs,rsave,re,track(3)
      double precision refpt(3),heading,llh(3),trans(3),scht(3),ts,have
      double precision pole(3),north(3),ps,sidea,sideb,sidec,q,pi
      double precision prf,vel,asch(3),axyz(3),xyzschmat(3,3),schxyzmat(3,3)
      integer i,j,i_type,lines,maxDim

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
        type(pegpoint) :: peg1
        type(pegpoint) :: peg2
        type(pegpoint) :: peg
   
        type :: pegtrans 
           real*8 r_mat(3,3)    !transformation matrix SCH->XYZ
           real*8 r_matinv(3,3) !transformation matrix XYZ->SCH
           real*8 r_ov(3)       !Offset vector SCH->XYZ
           real*8 r_radcur      !peg radius of curvature
        end type pegtrans
        type(pegtrans) :: ptm
      ! jng use the fact that now we know the dimension of xyz to allocate in the heap
      


      maxDim = dim2_xyz2
      if(dim2_xyz1 .gt. dim2_xyz2) then
          maxDim = dim2_xyz1
      endif
      ! copy the position vectors in the local arrays
      allocate(sch(3,maxDim))
      allocate(llhv(3,maxDim))
      allocate(vsch(3,maxDim))
      allocate(time(maxDim))


      pi=4.d0*datan2(1.d0,1.d0)

!c  set reference ellipsoid

        !jng defined in the setmocomppath module
        elp%r_a=major
        elp%r_e2=eccentricitySquared
c  parameters for first scene
        do i=1,dim2_xyz1
           call latlon(elp,xyz1(1,i),llhv(1,i),2)
        end do
        lines=i-1
        write(MESSAGE,'(a,1x,I10)') 'Lines, image 1: ',lines
        call write_out(ptStdWriter,MESSAGE)
c  satellite height

c  get average altitude for first scene
        rsave=0.d0
        have1 =0.d0
        do i=1,lines
           rs=sqrt(xyz1(1,i)**2+xyz1(2,i)**2+xyz1(3,i)**2)
           rsave=rsave+rs
           have1 = have1 + llhv(3,i)
        end do
        rsave=rsave/lines
        have1 = have1/lines


        write(MESSAGE,'(a,1x,f15.7,1x,f15.7)') 'Image 1 rsave, have = ',rsave,have1        
        call write_out(ptStdWriter,MESSAGE)
c  compute heading
        call geo_hdg(elp%r_a,elp%r_e2,llhv(1,lines/2+1),llhv(2,lines/2+1),llhv(1,lines),llhv(2,lines),heading)

        write(MESSAGE,'(a,1x,f15.7)') 'Heading, image 1: ',heading*180/3.14159265359       
        call write_out(ptStdWriter,MESSAGE)

c  define peg point
        peg1%r_lat =  llhv(1,lines/2+1)
        peg1%r_lon =  llhv(2,lines/2+1)
        peg1%r_hdg =  heading

        write(MESSAGE,'(a,1x,f15.7,1x,f15.7,1x,f15.7)') 'Peg point, image 1: ',peg1%r_lat,peg1%r_lon,peg1%r_hdg

        call write_out(ptStdWriter,MESSAGE)
c  repeat for file 2
        do i=1,dim2_xyz2
           call latlon(elp,xyz2(1,i),llhv(1,i),2)
        end do
        lines=i-1

        write(MESSAGE,'(a,1x,I10)') 'Lines, image 2: ',lines
        call write_out(ptStdWriter,MESSAGE)

c  get average altitude for first scene
        rsave=0.d0
        have2 =0.d0
        do i=1,lines
           rs=sqrt(xyz2(1,i)**2+xyz2(2,i)**2+xyz2(3,i)**2)
           rsave=rsave+rs
           have2 = have2 + llhv(3,i)
        end do
        rsave=rsave/lines
        have2 = have2/lines

        write(MESSAGE,'(a,1x,f15.7,1x,f15.7)') 'Image 2 rsave, have = ',rsave,have2        
        call write_out(ptStdWriter,MESSAGE)

c  compute heading
        call geo_hdg(elp%r_a,elp%r_e2,llhv(1,lines/2+1),llhv(2,lines/2+1),llhv(1,lines),llhv(2,lines),heading)

        write(MESSAGE,'(a,1x,f15.7)') 'Heading, image 2: ',heading*180/3.14159265359       
        call write_out(ptStdWriter,MESSAGE)

c  define peg point
      peg2%r_lat =  llhv(1,lines/2+1)
      peg2%r_lon =  llhv(2,lines/2+1)
      peg2%r_hdg =  heading

      write(MESSAGE,'(a,1x,f15.7,1x,f15.7,1x,f15.7)') 'Peg point, image 2: ',peg2%r_lat,peg2%r_lon,peg2%r_hdg

      call write_out(ptStdWriter,MESSAGE)

c  average of the two peg points
      peg%r_lat =  (peg1%r_lat+peg2%r_lat)/2.
      peg%r_lon =  (peg1%r_lon+peg2%r_lon)/2.
      peg%r_hdg =  (peg1%r_hdg+peg2%r_hdg)/2.

      have=(have1+have2)/2.

c  initialize the transformations using sh routines to get radius of curvature
      call radar_to_xyz(elp,peg,ptm)

c  velocity estimate from file 1, 2
      i_type=1
      call convert_sch_to_xyz(ptm,sch(1,lines/2+1),xyz1(1,lines/2+1),i_type)
      call convert_schdot_to_xyzdot(ptm,sch(1,lines/2+1),vsch(1,lines/2+1),vxyz1(1,lines/2+1),i_type)
      write(MESSAGE,'(a,1x,f15.7,1x,f15.7,1x,f15.7,1x,f15.7)') 'Image 1 velocity ',vsch(1,lines/2+1),vsch(2,lines/2+1),vsch(3,lines/2+1),
     $ sqrt(vsch(1,lines/2+1)**2+vsch(2,lines/2+1)**2+vsch(3,lines/2+1)**2)
      call write_out(ptStdWriter,MESSAGE)
      vel1=vsch(1,lines/2+1)

      call convert_sch_to_xyz(ptm,sch(1,lines/2+1),xyz2(1,lines/2+1),i_type)
      call convert_schdot_to_xyzdot(ptm,sch(1,lines/2+1),vsch(1,lines/2+1),vxyz2(1,lines/2+1),i_type)
        write(MESSAGE,'(a,1x,f15.7,1x,f15.7,1x,f15.7,1x,f15.7)') 'Image 2 velocity ',vsch(1,lines/2+1),vsch(2,lines/2+1),vsch(3,lines/2+1),
     $ sqrt(vsch(1,lines/2+1)**2+vsch(2,lines/2+1)**2+vsch(3,lines/2+1)**2)
      call write_out(ptStdWriter,MESSAGE)

      vel2=vsch(1,lines/2+1)


      write(MESSAGE,'(a,1x,f15.7,1x,f15.7,1x,f15.7)') 'Mean peg point: ',peg%r_lat,peg%r_lon,peg%r_hdg
      call write_log(ptStdWriter,MESSAGE)
      write(MESSAGE,'(a,1x,f15.7)') 'Mean altitude  ',have 
      call write_log(ptStdWriter,MESSAGE)
      write(MESSAGE,'(a,1x,f15.7)') 'Suggested processing velocity (vsch(1)): ',(vel1+vel2)/2.
      call write_log(ptStdWriter,MESSAGE)
      write(MESSAGE,'(a,1x,f15.7,1x,f15.7)') 'Individual velocities: ',vel1,vel2
      call write_log(ptStdWriter,MESSAGE)

      !jng set the variables that are returned to python. have1,2 and vel1,2 are already defined in the module 
      pegLatitude = peg%r_lat
      pegLongitude = peg%r_lon
      pegHeading = peg%r_hdg
      pegRadiusOfCurvature = ptm%r_radcur

      deallocate(sch)
      deallocate(llhv)
      deallocate(vsch)
      deallocate(time)
      end


