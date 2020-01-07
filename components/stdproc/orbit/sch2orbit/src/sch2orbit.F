c  orbit2sch - convert from orbit xyz to sch coordinates
c   use given peg point file if available
      subroutine sch2orbit
      use sch2orbitState 
      use fortranUtils
      implicit none
      character*20000 MESSAGE
      double precision rs, rsave
      double precision heading
      double precision pi
      double precision aschTmp(3),xyzschmat(3,3),schxyzmat(3,3)
      integer i,i_type


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
    
        pi= getPi()

!c  set reference ellipsoid

        !jng defined in the setmocomppath module
        elp%r_a=major
        elp%r_e2=eccentricitySquared
        
        write(MESSAGE,*),'Lines: ',len_vec
        call write_out(ptStdWriter,MESSAGE)

!in this case the info have been set from python
        peg%r_lat = pegLatitude
        peg%r_lon = pegLongitude
        peg%r_hdg = pegHeading

            ! jng the quantity "have" is already set while earth radius is not used so it was not passed
      

!c  first initialize the transformations using sh routines
      call radar_to_xyz(elp,peg,ptm)
!c  sch of spacecraft
      write(MESSAGE,*),' '
      call write_out(ptStdWriter,MESSAGE)
      write(MESSAGE,*),'xyz coordinates of satellite points'
      call write_out(ptStdWriter,MESSAGE)
      i_type=0
      call convert_sch_to_xyz(ptm,sch(1,1),xyz(1,1),i_type)
      write(MESSAGE,*),'Line 1:    ',xyz(1,1),xyz(2,1),xyz(3,1)
      call write_out(ptStdWriter,MESSAGE)
      call convert_sch_to_xyz(ptm,sch(1,len_vec/2+1),xyz(1,len_vec/2+1),i_type)
      write(MESSAGE,*),'Middle:    ',xyz(1,len_vec/2+1),xyz(2,len_vec/2+1),xyz(3,len_vec/2+1)
      call write_out(ptStdWriter,MESSAGE)
      call convert_sch_to_xyz(ptm,sch(1,len_vec),xyz(1,len_vec),i_type)
      write(MESSAGE,*),'Last line: ',xyz(1,len_vec),xyz(2,len_vec),xyz(3,len_vec)
      call write_out(ptStdWriter,MESSAGE)

!c  write out orbit in xyz

      i_type=0
      do i=1,len_vec
         call convert_sch_to_xyz(ptm,sch(1,i),xyz(1,i),i_type)
         call convert_schdot_to_xyzdot(ptm,sch(1,i),vsch(1,i),vxyz(1,i),i_type)
         rs=sqrt(xyz(1,i)**2+xyz(2,i)**2+xyz(3,i)**2)
         axyz(1,i)=-GM*xyz(1,i)/rs**3
         axyz(2,i)=-GM*xyz(2,i)/rs**3
         axyz(3,i)=-GM*xyz(3,i)/rs**3
      end do

c  print out some useful processing parameters
      write(MESSAGE,*),' '
      call write_out(ptStdWriter,MESSAGE)
      write(MESSAGE,*),'Re        ',ptm%r_radcur, radius
      call write_out(ptStdWriter,MESSAGE)


      end


