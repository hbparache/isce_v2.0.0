c  getpeg - estimate the peg point for a single frame
c    derived from: orbit2sch - convert from orbit xyz to sch coordinates
      subroutine getpeg
      use getpegState
      implicit none
      character*20000 MESSAGE
      double precision,allocatable, dimension(:,:) :: llhv
      double precision,allocatable, dimension(:) :: sch, vsch
      double precision minor,lat,lon,glat,rs,rsave,re,track(3)
      double precision refpt(3),heading,llh(3),trans(3),scht(3),ts
      double precision pole(3),north(3),ps,sidea,sideb,sidec,q,pi
      double precision asch(3),axyz(3),xyzschmat(3,3),schxyzmat(3,3)
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
        type(pegpoint) :: peg
   
        type :: pegtrans 
           real*8 r_mat(3,3)    !transformation matrix SCH->XYZ
           real*8 r_matinv(3,3) !transformation matrix XYZ->SCH
           real*8 r_ov(3)       !Offset vector SCH->XYZ
           real*8 r_radcur      !peg radius of curvature
        end type pegtrans
        type(pegtrans) :: ptm
      ! jng use the fact that now we know the dimension of xyz to allocate in the heap
      


      maxDim = dim2_xyz
      
! copy the position vectors in the local arrays
      allocate(sch(3))
      allocate(vsch(3))
      allocate(llhv(3,maxDim))

      pi=4.d0*datan2(1.d0,1.d0)

!c  set reference ellipsoid

        !jng defined in the setmocomppath module
        elp%r_a=major
        elp%r_e2=eccentricitySquared

!c  Convert to lat lon
	do i=1,dim2_xyz
           call latlon(elp,xyz(1,i),llhv(1,i),2)
        end do
        lines=i-1
        write(MESSAGE,'(a,1x,I10)') 'Lines: ',lines
        call write_out(ptStdWriter,MESSAGE)
c  satellite height

c  get average altitude for first scene
        rsave=0.d0
        have =0.d0
        do i=1,lines
           rs=sqrt(xyz(1,i)**2+xyz(2,i)**2+xyz(3,i)**2)
           rsave=rsave+rs
           have = have + llhv(3,i)
        end do
        rsave=rsave/lines
        have = have/lines


        write(MESSAGE,'(a,1x,f15.7,1x,f15.7)') 'rsave, have = ',rsave,have        
        call write_out(ptStdWriter,MESSAGE)
c  compute heading
        call geo_hdg(elp%r_a,elp%r_e2,llhv(1,lines/2+1),llhv(2,lines/2+1),llhv(1,lines),llhv(2,lines),heading)

        write(MESSAGE,'(a,1x,f15.7)') 'Heading: ',heading*180/3.14159265359       
        call write_out(ptStdWriter,MESSAGE)

c  define peg point
        peg%r_lat =  llhv(1,lines/2+1)
        peg%r_lon =  llhv(2,lines/2+1)
        peg%r_hdg =  heading

	write(MESSAGE,'(a,1x,f15.7,1x,f15.7,1x,f15.7)') 'Peg point: ',peg%r_lat,peg%r_lon,peg%r_hdg
	call write_out(ptStdWriter, MESSAGE)

c  initialize the transformations using sh routines to get radius of curvature
      call radar_to_xyz(elp,peg,ptm)

c  velocity estimate from file 
      i_type=1
      call convert_sch_to_xyz(ptm,sch,xyz(1,lines/2+1),i_type)
      call convert_schdot_to_xyzdot(ptm,sch,vsch,vxyz(1,lines/2+1),i_type)
      write(MESSAGE,'(a,1x,f15.7,1x,f15.7,1x,f15.7,1x,f15.7)') 'Image velocity ',vsch(1),vsch(2),vsch(3),
     $ sqrt(vsch(1)**2+vsch(2)**2+vsch(3)**2)
      call write_out(ptStdWriter,MESSAGE)
      vel=vsch(1)


      write(MESSAGE,'(a,1x,f15.7,1x,f15.7,1x,f15.7)') 'Mean peg point: ',peg%r_lat,peg%r_lon,peg%r_hdg
      call write_log(ptStdWriter,MESSAGE)
      write(MESSAGE,'(a,1x,f15.7)') 'Mean altitude  ',have 
      call write_log(ptStdWriter,MESSAGE)
      write(MESSAGE,'(a,1x,f15.7)') 'Suggested processing velocity (vsch(1)): ',vel
      call write_log(ptStdWriter,MESSAGE)

      ! return variables to python
      pegLatitude = peg%r_lat
      pegLongitude = peg%r_lon
      pegHeading = peg%r_hdg
      pegRadiusOfCurvature = ptm%r_radcur

      deallocate(sch)
      deallocate(llhv)
      deallocate(vsch)
      end


