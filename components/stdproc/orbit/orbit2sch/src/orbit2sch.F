c  orbit2sch - convert from orbit xyz to sch coordinates
c   use given peg point file if available
      subroutine orbit2sch
      use orbit2schState 
      use fortranUtils
      implicit none
      character*20000 MESSAGE
      double precision, allocatable, dimension(:,:) :: llhv
      double precision rs, rsave
      double precision heading
      double precision pi
      double precision axyz(3),aschTmp(3),xyzschmat(3,3),schxyzmat(3,3)
      integer i,i_type,lines


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
    
      allocate(llhv(dim1_xyz,dim2_xyz)) 
      pi= getPi()

!c  set reference ellipsoid

        !jng defined in the setmocomppath module
        elp%r_a=major
        elp%r_e2=eccentricitySquared
        
        do i=1,dim2_xyz
            call latlon(elp,xyz(1,i),llhv(1,i),2)
        end do
        lines=dim2_xyz
        write(MESSAGE,*),'Lines: ',lines
        call write_out(ptStdWriter,MESSAGE)

c  get average altitude
        rsave=0.d0
        if(computePegInfoFlag .eq. 1) then
            have =0.d0
        endif
        do i=1,lines
            rs=sqrt(xyz(1,i)**2+xyz(2,i)**2+xyz(3,i)**2)
            rsave=rsave+rs
            if(computePegInfoFlag .eq. 1) then
                have = have + llhv(3,i)
            endif
        end do
        rsave=rsave/lines
        if(computePegInfoFlag .eq. 1) then
            have = have/lines
        endif

        write(MESSAGE,*), 'rsave, have = ',rsave,have
        call write_out(ptStdWriter,MESSAGE)

c  compute heading
         call geo_hdg(elp%r_a,elp%r_e2,llhv(1,lines/2+1),llhv(2,lines/2+1),llhv(1,lines),llhv(2,lines),heading)

        write(MESSAGE,*),'Heading ',heading*180/3.14159265359
        call write_out(ptStdWriter,MESSAGE)
        if(computePegInfoFlag .eq. 1) then
c  define peg point
            peg%r_lat =  llhv(1,lines/2+1)
            peg%r_lon =  llhv(2,lines/2+1)
            peg%r_hdg =  heading

            write(MESSAGE,*),'Peg point ',peg%r_lat,peg%r_lon,peg%r_hdg
            call write_out(ptStdWriter,MESSAGE)
        else
!in this case the info have been set from python
            peg%r_lat = pegLatitude
            peg%r_lon = pegLongitude
            peg%r_hdg = pegHeading

            ! jng the quantity "have" is already set while earth radius is not used so it was not passed
      
        endif

c  first initialize the transformations using sh routines
      call radar_to_xyz(elp,peg,ptm)
c  sch of spacecraft
      write(MESSAGE,*),' '
      call write_out(ptStdWriter,MESSAGE)
      write(MESSAGE,*),'sch coordinates of satellite points'
      call write_out(ptStdWriter,MESSAGE)
      i_type=1
      call convert_sch_to_xyz(ptm,sch(1,1),xyz(1,1),i_type)
      write(MESSAGE,*),'Line 1:    ',sch(1,1),sch(2,1),sch(3,1)
      call write_out(ptStdWriter,MESSAGE)
      call convert_sch_to_xyz(ptm,sch(1,lines/2+1),xyz(1,lines/2+1),i_type)
      write(MESSAGE,*),'Middle:    ',sch(1,lines/2+1),sch(2,lines/2+1),sch(3,lines/2+1)
      call write_out(ptStdWriter,MESSAGE)
      call convert_sch_to_xyz(ptm,sch(1,lines),xyz(1,lines),i_type)
      write(MESSAGE,*),'Last line: ',sch(1,lines),sch(2,lines),sch(3,lines)
      call write_out(ptStdWriter,MESSAGE)

c  lat/lon of spacecraft

      write(MESSAGE,*),' '
      call write_out(ptStdWriter,MESSAGE)
      write(MESSAGE,*),'lat/lon/hgt coordinates of satellite points'
      call write_out(ptStdWriter,MESSAGE)
      write(MESSAGE,*),'Line 1:    ',180./pi*llhv(1,1),180./pi*llhv(2,1),llhv(3,1)
      call write_out(ptStdWriter,MESSAGE)
      write(MESSAGE,*),'Middle:    ',180./pi*llhv(1,lines/2+1),180./pi*llhv(2,lines/2+1),llhv(3,lines/2+1)
      call write_out(ptStdWriter,MESSAGE)
      write(MESSAGE,*),'Last line: ',180./pi*llhv(1,lines),180./pi*llhv(2,lines),llhv(3,lines)
      call write_out(ptStdWriter,MESSAGE)

c  write out orbit in sch

      i_type=1
      do i=1,lines
         call convert_sch_to_xyz(ptm,sch(1,i),xyz(1,i),i_type)
         call convert_schdot_to_xyzdot(ptm,sch(1,i),vsch(1,i),vxyz(1,i),i_type)
         rs=sqrt(xyz(1,i)**2+xyz(2,i)**2+xyz(3,i)**2)
         axyz(1)=-GM*xyz(1,i)/rs**3
         axyz(2)=-GM*xyz(2,i)/rs**3
         axyz(3)=-GM*xyz(3,i)/rs**3
         call schbasis(ptm,sch(1,i),xyzschmat,schxyzmat)
         call matvec(xyzschmat,axyz,aschTmp)
         asch(:,i) = aschTmp(:)
         !write(31,'(i8,1x,f17.10,3(1x,f13.4),3(1x,f11.5),3(1x,f11.8))')i,time(i),sch(1,i),sch(2,i),sch(3,i),vsch(1,i),vsch(2,i),vsch(3,i),asch
      end do

c  print out some useful processing parameters
      write(MESSAGE,*),' '
      call write_out(ptStdWriter,MESSAGE)
      write(MESSAGE,*),'Re        ',ptm%r_radcur
      call write_out(ptStdWriter,MESSAGE)
      write(MESSAGE,*),'Altitude  ',have
      call write_out(ptStdWriter,MESSAGE)


      write(MESSAGE,*),'velocity ',vsch(1,lines/2+1),vsch(2,lines/2+1),vsch(3,lines/2+1),
     $  sqrt(vsch(1,lines/2+1)**2+vsch(2,lines/2+1)**2+vsch(3,lines/2+1)**2)
      call write_out(ptStdWriter,MESSAGE)

      deallocate(llhv) 
      end


