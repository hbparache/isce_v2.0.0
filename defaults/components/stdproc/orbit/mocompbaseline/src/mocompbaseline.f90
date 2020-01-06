!c  mocompbaseline - get insar baseline from mocomp and position files
      subroutine mocompbaseline
      use mocompbaselineState

      implicit none
      character*20000 MESSAGE
      character*60 moc_pos1,moc_pos2,schfile1,schfile2,baselinefile
      character*60 dbname,tablename,units,type
      !real*8 s1(100000),s2(100000),time,sch1(3,100000),sch2(3,100000)
      real*8 sch(3),baseline(3),midpoint(3),base1(3),base2(3),sc(3),mid1(3),mid2(3)
      !real*8 peglat,peglon,peghdg
      integer*8 db
      !integer is1(100000),is2(100000),lines1,lines2,i,j,ibin
      integer lines1,lines2,i,j,ibin
      integer schlines1,schlines2,irec
      real frac

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


      !if(iargc().lt.3)then
      !   print *,'Usage: mocompbaseline database table baselinefile'
      !   stop
      !end if
      lines1 = dim1_s1
      lines2 = dim1_s2
      schlines1 = dim2_sch1
      schlines2 = dim2_sch2
      peg%r_lat=peglat
      peg%r_lon=peglon
      peg%r_hdg=peghdg
      !call getarg(1,dbname)
      !call getarg(2,tablename)
!!$      call getarg(3,moc_pos1)
!!$      call getarg(4,moc_pos2)
!!$      call getarg(5,schfile1)
!!$      call getarg(6,schfile2)
      !call getarg(3,baselinefile)

!c  initialize the transformation matrices
        !call open_db(db,dbname)
        !call get_paramd(db,tablename,'peg_latitude',peglat,units,type)
        !call get_paramd(db,tablename,'peg_longitude',peglon,units,type)
        !call get_paramd(db,tablename,'peg_heading',peghdg,units,type)
        !call get_paramc(db,tablename,'orbit_sch1',schfile1,units,type)
        !call get_paramc(db,tablename,'orbit_sch2',schfile2,units,type)
        !call get_paramc(db,tablename,'mocomp_position_file1',moc_pos1,units,type)
        !call get_paramc(db,tablename,'mocomp_position_file2',moc_pos2,units,type)
        !call close_db(db)

      elp%r_a = major !6378137.0
      elp%r_e2 = eccentricitySquared !0.0066943799901499996

      write(MESSAGE,*) peg%r_lat,peg%r_lon,peg%r_hdg,elp%r_a,elp%r_e2
      call write_out(ptStdWriter,MESSAGE)
      call radar_to_xyz(elp,peg,ptm)
      write(MESSAGE,*),'Local Earth radius of curvature: ',ptm%r_radcur
      call write_out(ptStdWriter,MESSAGE)

!c  read in mocomp reference track positions
      !open(21,file=moc_pos1)
      !do i=1,100000
       !  read(21,*,end=11)is1(i),time,s1(i)
      !end do
!11    lines1=i-1
!      close(21)
!      open(21,file=moc_pos2)
!      do i=1,100000
!         read(21,*,end=21)is2(i),time,s2(i)
!      end do
!21    lines2=i-1
!      close(21)
!      print *,'Lines read: ',lines1,lines2

!c  read in satellite locations in sch coords
!      open(21,file=schfile1)
!      do i=1,100000
!         read(21,*,end=31)irec,time,sch1(1,i),sch1(2,i),sch1(3,i)
!      end do
!31    schlines1=i-1
!      close(21)
!      open(21,file=schfile2)
!      do i=1,100000
!         read(21,*,end=41)irec,time,sch2(1,i),sch2(2,i),sch2(3,i)
!      end do
!41    schlines2=i-1
!      close(21)

!c  open baseline output file
!      open(22,file=baselinefile)

!c  for each line in master image, find corresponding location in file 2
      ibin=1
      do i=1,lines1
         do j=ibin,lines2
!c            print *,s2(j),s1(i)
            if(s2(j).gt.s1(i))go to 30
         end do
         !if we get here, then there is no location in file 2 that
         !corresponds to the location in file1.  Set dim1_s1 to previous
         !value that had a corresponding point in file 2
         dim1_s1 = i-1
         return
30       if(j.gt.1)then
!c            print *,i,j
            frac=(s1(i)-s2(j-1))/(s2(j)-s2(j-1))
            ibin=j-1
         end if
         if(ibin.gt.schlines2-1)then
            ibin=schlines2-1
            frac=0.
         end if
!c         print *,i,s1(i),ibin,frac,s2(ibin),s2(ibin+1)
!c  interpolate file 2 to correct spot
         sch(1)=sch2(1,ibin)+frac*(sch2(1,ibin+1)-sch2(1,ibin))
         sch(2)=sch2(2,ibin)+frac*(sch2(2,ibin+1)-sch2(2,ibin))
         sch(3)=sch2(3,ibin)+frac*(sch2(3,ibin+1)-sch2(3,ibin))
         !write(6,*) 'a',i
         call get_tpsch(ptm,sch1(1,i),ptm,sch,baseline)
         call ave_tpsch(ptm,sch1(1,i),ptm,sch,midpoint)
         sc(1)=s1(i)
         sc(2)=0.
         sc(3)=height
!         base1=sch1(:,i)-sc
         call get_tpsch(ptm,sch1(1,i),ptm,sc,base1)
         call ave_tpsch(ptm,sch1(1,i),ptm,sc,mid1)
!         base2=sch-sc
         call get_tpsch(ptm,sch,ptm,sc,base2)
         call ave_tpsch(ptm,sch,ptm,sc,mid2)
          baselineArray(:,i) = baseline(:)
          baselineArray1(:,i) = base1(:)
          baselineArray2(:,i) = base2(:)
          midpointArray(:,i) = midpoint(:)
          midpointArray1(:,i) = mid1(:)
          midpointArray2(:,i) = mid2(:)
          schArray(:,i) = sch(:)
          scArray(:,i) = sc(:)
      end do
!      close(22)
      end
