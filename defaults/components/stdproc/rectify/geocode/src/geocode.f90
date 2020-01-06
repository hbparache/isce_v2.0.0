subroutine geocode(demAccessor,topophaseAccessor,demCropAccessor,losAccessor,geoAccessor,inband,outband,iscomplex,method)
  use coordinates
  use uniform_interp
  use geocodeState
  use geocodeReadWrite
  use geocodeMethods
  use fortranUtils

  implicit none
  include 'omp_lib.h'


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !! DECLARE LOCAL VARIABLES
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  integer inband,outband,iscomplex,method
  integer*8 topophaseAccessor,demAccessor
  integer*8 losAccessor,geoAccessor,demCropAccessor
  real*4, dimension(:,:),allocatable :: dem
  integer*2, dimension(:,:),allocatable :: dem_crop
  !integer*2, dimension(:), allocatable :: demi2
  !jng linearize array to use it directly in the image api and avoid memory copy
  real*8 :: sch_p(3),xyz_p(3),llh(3),sch(3),xyz(3)
  integer :: pixel,line,min_lat_idx,max_lat_idx,min_lon_idx,max_lon_idx,ith
  real*8,allocatable,dimension(:) :: gnd_sq_ang,cos_ang,sin_ang,rho,squintshift
  complex,allocatable,dimension(:,:) :: geo
  real*4, allocatable, dimension(:,:) :: losang

  !!!Debugging - PSA
  !real*4, allocatable, dimension(:,:) :: distance

  !jng linearize array to use it directly in the image api and avoid memory copy
  real*8 :: lat0,lon0
  integer :: geo_len, geo_wid,i_type,k
  real*8 :: s, rng, s_idx, rng_idx,dlon_out,dlat_out,idxlat,idxlon
  complex, allocatable,dimension(:,:) :: ifg
  complex z
  integer :: int_rdx,int_rdy
  real*8 :: fr_rdx,fr_rdy
  integer,parameter :: plen = 128 !patch size
  integer :: npatch,patch,pline,cnt !number of patches
  integer :: i,j,lineNum
  real*8 :: ds
  real*8 :: max_rho,ds_coeff,hpra,rapz

  real*8 :: min_latr,min_lonr,max_latr,max_lonr
  real*8 :: lat_firstr,lon_firstr,dlonr,dlatr
  real*8 :: alpha,beta,rnggeom
  
  real*4 :: fd,t0,t1
  type(ellipsoid) :: elp
  type(pegpoint) :: peg
  type(pegtrans) :: ptm

  character*20000 MESSAGE
  
  real*8 :: rhomin,rhomax,f,df,rhok,T, cosphi,dssum

  ! declare constants
  real*8 pi,rad2deg,deg2rad 

    procedure(readTemplate), pointer :: readBand => null()
    procedure(writeTemplate), pointer :: writeBand => null()
    procedure(intpTemplate), pointer :: intp_data => null()

    !!Set up the correct readers and writers
    if(iscomplex.eq.1) then
        readBand => readCpxLine
        writeBand => writeCpxLine
    else
        readBand => readRealLine
        writeBand => writeRealLine
    endif


    if (method.eq.SINC_METHOD) then
        intp_data => intp_sinc
    else if (method.eq.BILINEAR_METHOD) then
        intp_data => intp_bilinear
    else if (method.eq.BICUBIC_METHOD) then
        intp_data => intp_bicubic
    else if (method.eq.NEAREST_METHOD) then
        intp_data => intp_nearest
    else
        print *, 'Undefined interpolation method.'
        stop
    endif
  
  pi = getPi()
  rad2deg = 180.d0/pi
  deg2rad = pi/180.d0
  ! get starting time
  t0 = secnds(0.0)
  cnt = 0

  !$OMP PARALLEL
  !$OMP MASTER
  ith = omp_get_num_threads() !total num threads
  !$OMP END MASTER
  !$OMP END PARALLEL
    write(MESSAGE,*) "threads",ith
    call write_out(ptStdWriter,MESSAGE)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !! READ DATABASE AND COMMAND LINE ARGS
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

  elp%r_a= majorSemiAxis
  elp%r_e2= eccentricitySquared
  peg%r_lat = peglat
  peg%r_lon = peglon
  peg%r_hdg = peghdg

  fd=fdprfs * prf

  print *, 'Scaling : ', ipts
  print *,'start sample, length : ',is_mocomp,length
  length=min(length,(dim1_s_mocomp+Nazlooks/2-is_mocomp)/Nazlooks)
  print *, 'reset length: ',length

  print *, 'Length comparison: ', length*nazlooks+is_mocomp, dim1_s_mocomp 

  ! compute avg along-track spacing, update daz and s0
  write(MESSAGE,'(4x,a)'), "computing avg. along-track spacing..."
  call write_out(ptStdWriter,MESSAGE)
  dssum = 0.d0
  !!Added a cushion of 3 nazlooks - PSA
  do line = nazlooks+1,(length-2)*nazlooks
     dssum = dssum + (s_mocomp(is_mocomp+line)-&
          s_mocomp(is_mocomp+(line-1)))
  enddo

  !jng no idea why they get them from database and then don't use them
  daz = dssum/((length-2)*nazlooks-nazlooks)
  s0 = s_mocomp(is_mocomp+1*nazlooks-nazlooks/2)
  print *,daz,s0,length,nazlooks,is_mocomp,dssum,s_mocomp(is_mocomp+length*nazlooks)-s_mocomp(is_mocomp+nazlooks/2)

  ! for now output lat/lon is the same as DEM
  dlonr = dlon*deg2rad
  dlatr = dlat*deg2rad
  lon_firstr = lon_first*deg2rad
  lat_firstr = lat_first*deg2rad
  dlon_out = dlonr/float(ipts)
  dlat_out = dlatr/float(ipts)

  write(MESSAGE, *) 'lat, lon spacings: ',dlat_out,dlon_out
  call write_out(ptStdWriter,MESSAGE)

  ! allocate
  allocate(gnd_sq_ang(width),cos_ang(width),sin_ang(width),rho(width),squintshift(width))
  allocate(dem(demwidth,demlength))
!jng zeros everything
     gnd_sq_ang = 0
     cos_ang = 0
     sin_ang = 0
     rho = 0
     squintshift = 0
     dem = 0

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !! PROCESSING STEPS
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !allocate(demi2(demwidth))
  lineNum = 1
  do i = 1,demlength
      call getLineSequential(demAccessor,dem(:,i),lineNum)
      !do j=1,demwidth
      !   dem(j,i) = demi2(j)
      !enddo
  enddo
  !deallocate(demi2)


  write(MESSAGE, *) "reading interferogram ..."
  call write_out(ptStdWriter,MESSAGE)

  allocate(ifg(width,length))
  ifg = 0


  ! convert deg to rad
  min_latr = min_lat*deg2rad
  max_latr = max_lat*deg2rad
  min_lonr = min_lon*deg2rad
  max_lonr = max_lon*deg2rad
  min_lat_idx=(min_latr-lat_firstr)/dlatr + 1
  min_lon_idx=(min_lonr-lon_firstr)/dlonr + 1
  max_lat_idx=(max_latr-lat_firstr)/dlatr + 1
  max_lon_idx=(max_lonr-lon_firstr)/dlonr + 1
  geo_len = ceiling((max_latr-min_latr)/abs(dlat_out)) + 1
  geo_wid = ceiling((max_lonr-min_lonr)/abs(dlon_out)) + 1
  npatch = ceiling(real(geo_len)/plen) !total number of patches

  write(MESSAGE, *) 'npatches: ', npatch, geo_len, geo_wid
  call write_out(ptStdWriter,MESSAGE)

  call init_RW(max(width,geo_wid),iscomplex)

   ! Read in the data
    do i=1,length
      call readBand(topophaseAccessor,ifg(:,i),inband,lineNum,width)
    enddo


  ! allocate a patch of the output geocoded image
  allocate(geo(geo_wid,plen),dem_crop(geo_wid,plen))
  allocate(losang(2*geo_wid,plen))

  !!!!Debugging - PSA
!!  allocate(distance(geo_wid,plen))

  geo = 0;
  dem_crop = 0

  ! initialize sch transformation matrices
  call radar_to_xyz(elp,peg,ptm)


  write(MESSAGE,'(4x,a)') 'computing sinc coefficients...'
  call write_out(ptStdWriter,MESSAGE)

  !!!!Allocate arrays if needed 
  call prepareMethods(method)

  ! precompute some constants
  ds_coeff = 1.0
  if(abs(fd).gt.0.1)ds_coeff = 2.d0*vel/fd/wvl
  max_rho = rho0 + (width-1)*drho*nrnglooks
  lat0 = lat_firstr + dlatr*(max_lat_idx-1)
  lon0 = lon_firstr + dlonr*(min_lon_idx-1)
  hpra = h + ra

  !!!!Distance file for debugging - PSA
  !!!open(31, file='distance',access='direct',recl=4*geo_wid,form='unformatted')

  write(MESSAGE,'(4x,a,i2,a)'), "geocoding on ",ith,' threads...'
  call write_out(ptStdWriter,MESSAGE)
  do patch = 1,npatch
     geo = cmplx(0.,0.)
     dem_crop = 0
     losang = 0.

     !!!!Add distance to shared for debugging - PSA
     !$OMP PARALLEL DO private(line,pixel,llh,i_type)&
     !$OMP private(sch,xyz,s,rng,sch_p,xyz_p,s_idx,rng_idx,z,idxlat,idxlon,rapz)&
     !$OMP private(int_rdx,int_rdy,fr_rdx,fr_rdy,pline)&
     !$OMP private(rhomin,rhomax,f,df,rhok,T,k,cosphi,ds) &
     !$OMP shared(patch,geo_len,lat0,dlat_out,lon0,dlon_out,dlat,dlon,f_delay) &
     !$OMP shared(dem,fintp,demwidth,demlength,ra,ds_coeff,rho0,max_rho,hpra) &
     !$OMP shared(lat_first,lon_first,ptm,fd,elp,ilrl,losang) &
     !$OMP shared(max_lat_idx,min_lon_idx,s0,daz,nazlooks) &
     !$OMP shared(lat_firstr,lon_firstr,dlatr,dlonr,nrnglooks)

     do line= 1+(patch-1)*plen,min(plen+(patch-1)*plen,geo_len)
        pline = line - (patch-1)*plen !the line of this patch

        do pixel = 1,geo_wid

           z = cmplx(0.,0.)
           llh(3) = 0.
           ! dem pixel to sch
           llh(1) = lat0 + dlat_out*(line-1)
           llh(2) = lon0 + dlon_out*(pixel-1)

           ! interpolate DEM if necessary...
           if (dlatr.ne.dlat_out.or.dlonr.ne.dlon_out) then
              print *, 'Interpolating DEM'
              idxlat=(llh(1)-lat_firstr)/dlatr ! note interpolation routine assumes array is zero-based
              idxlon=(llh(2)-lon_firstr)/dlonr ! note interpolation routine assumes array is zero-based

              llh(3) = 0.
              if(idxlon.lt.f_delay) goto 200
              if(idxlon.gt.demwidth-f_delay) goto 200
              if(idxlat.lt.f_delay) goto 200
              if(idxlat.gt.demlength-f_delay) goto 200


              int_rdx=int(idxlon+f_delay)
              fr_rdx=idxlon+f_delay-int_rdx
              int_rdy=int(idxlat+f_delay)
              fr_rdy=idxlat+f_delay-int_rdy

              llh(3) = sinc_eval_2d_f(dem,fintp,sinc_sub,sinc_len,int_rdx,int_rdy,&
                   fr_rdx,fr_rdy,demwidth,demlength)
        
              ! this should catch bad SRTM points, even if interpolated with
              ! good surrounding points
              if(llh(3).lt.-1000.) then
                 ! llh(3) = 0.
                 goto 100
              end if

           else

              idxlat = max_lat_idx + (line-1)
              idxlon = min_lon_idx + (pixel-1)
!              write(6,*) idxlat,max_lat_idx,idxlon,min_lon_idx
              if(idxlat.lt.1.or.idxlat.gt.demlength) goto 200
              if(idxlon.lt.1.or.idxlon.gt.demwidth) goto 200
              llh(3) = dem(int(idxlon),int(idxlat))
              ! catch bad SRTM pixels
              if(llh(3).eq.-32768) then
                 ! llh(3) = 0.
                 goto 100
              endif

           endif


200        continue

           i_type = 1
           call latlon(elp,xyz,llh,i_type)
           i_type = 1
           call convert_sch_to_xyz(ptm,sch,xyz,i_type)
           cnt = cnt + 1

           !if (sch(2).gt.0.d0) goto 100 !uncomment for right-looking
           !if (sch(2).lt.0.d0) goto 100 !uncomment for left-looking
           if ((ilrl*sch(2)).lt.0.d0) goto 100

           ! zero doppler values of s and slant range

           s_idx = (sch(1)-s0)/(daz*nazlooks) + 1

           !if(s_idx.lt.f_delay) goto 100
           !if(s_idx.gt.length-f_delay) goto 100

           sch_p = (/sch(1),0.d0,dble(h)/)
           i_type = 0
           call convert_sch_to_xyz(ptm,sch_p,xyz_p,i_type)
           rng = norm(xyz_p-xyz) !no-squint slant range


           ! skip if outside image
           if(rng.lt.rho0) goto 100
           if(rng.gt.max_rho) goto 100


!!$ ! solve for along-track shift due to squint.
!!$ ! numerically solve for ds:
!!$ ! ((h+re)**2+(h+z)**2-rho**2)/(2*(h+re)*(z+re)) =
!!$ ! cos(c/re)*cos(ds/re)
!!$ !
!!$ ! where:
!!$ ! ds = 2*vel*rho/fd/wvl


           cosphi = cos(sch(2)/ra)
           rapz = ra + sch(3)

           ds=0.
           if(abs(fd).gt.0.1)then
              ds = ra*asin(rng/ra/cosphi/ds_coeff)

              ! use Newton method to solve for ds...
              do k = 1,10
                 
!!$ f = ((hpre)**2+(repz)**2-(ds*ds_coeff)**2)/2.d0/(hpre)/(repz) - &
!!$ cosphi*cos(ds/re)
!!$ df= cosphi*sin(ds/re)/re - ds_coeff**2*ds/hpre/repz

                 f = ((hpra)**2+(rapz)**2-(ra*cosphi*sin(ds/ra)*ds_coeff)**2)/2.d0/(hpra)/(rapz) - &
                      cosphi*cos(ds/ra)
                 df= cosphi*sin(ds/ra)/ra - (ds_coeff*ra*cosphi)**2/hpra/rapz*&
                      sin(ds/ra)*cos(ds/ra)/ra
                 
                 ds = ds - f/df
                 
              enddo
              continue

              ! correct platform location for squint
              sch_p(1) = sch_p(1) - ds
              rng = ds_coeff*ra*cosphi*sin(ds/ra)
              
           end if

           ! compute decimal indices into complex image
!           rng_idx = (rng - rho0)/drho/nrnglooks + 1
           rng_idx = (rng - rho0)/(drho*nrnglooks) ! note interpolation routine assumes array is zero-based

           ! correct s image coordinate, s0 relative to platform
!           s_idx = (sch_p(1)-s0)/daz/nazlooks + 1
           s_idx = (sch_p(1)-s0)/(daz*nazlooks) ! note interpolation routine assumes array is zero-based
           if(rng_idx.lt.f_delay) goto 100
           if(rng_idx.gt.width-f_delay) goto 100
           if(s_idx.lt.f_delay) goto 100
           if(s_idx.gt.length-f_delay) goto 100

           int_rdx=int(rng_idx+f_delay)
           fr_rdx=rng_idx+f_delay-int_rdx
           int_rdy=int(s_idx+f_delay)
           fr_rdy=s_idx+f_delay-int_rdy
           !! The indices are offset by f_delay for sinc
           !! Other methods adjust this bias in intp_call
           z = intp_data(ifg,int_rdx,int_rdy,fr_rdx,fr_rdy,width,length)

           !!!!LOS computations
           alpha = acos(((h+ra)**2 + rapz**2 - rng**2)/(2.*rapz*(h+ra)))
           beta = acos(((h+ra)**2 + rng**2 - rapz**2)/(2.*(h+ra)*rng))
           losang(2*(pixel-1)+1,pline) = (alpha+beta)*rad2deg

           beta = asin(sin(ds/ra)/sin(alpha))
           losang(2*pixel,pline) = (-peghdg+0.5*pi+beta)*rad2deg




100        continue

           !!!!Distance computation for debugging - PSA
!           i_type = 0
!           call convert_sch_to_xyz(ptm,sch_p,xyz_p,i_type)
!           rnggeom = norm(xyz_p-xyz) !geometric slant range
!           distance(pixel, pline) = abs(rng-rnggeom)

           !jng linearized arrays to avoid mem copy
           geo(pixel,pline) = z
           dem_crop(pixel, pline) = llh(3)

        enddo
     enddo
     !$OMP END PARALLEL DO

     ! write output file
     do i=1,plen
        call writeBand(geoAccessor,geo(:,i),outband,geo_wid)
     enddo

     if(demCropAccessor.gt.0) then
         do i=1,plen
            call setLineSequential(demCropAccessor,dem_crop(:,i))
         enddo
     endif

     if(losAccessor.gt.0) then
         do i=1,plen
            call setLineSequential(losAccessor, losang(:,i))
         enddo
     endif

     !!!!Debugging distance write to file - PSA
!     do i=1,plen
!        write(31,rec=i+(patch-1)*plen)(distance(j,i),j=1,geo_wid)
!     enddo

  enddo ! end patch do

  !!!!Close the debug output file - PSA
!  close(31)

  call finalize_RW(iscomplex)
  call unprepareMethods(method)
  ! write params to database
  write(MESSAGE,'(4x,a)'), "writing parameters to the database..."
  call write_out(ptStdWriter,MESSAGE)
! jng pass to python the parameters that were save in the table before 
  geowidth = geo_wid
  geolength = npatch*plen
  latSpacing  = dlat_out*rad2deg
  lonSpacing = dlon_out*rad2deg
  geomin_lat = lat0*rad2deg
  geomax_lat = (lat0 + dlat_out*(npatch*plen-1))*rad2deg
  geomin_lon = lon0*rad2deg
  geomax_lon = (lon0 + dlon_out*(geo_wid-1))*rad2deg
  write(MESSAGE,*) "PIXELS = ",geo_wid
  call write_out(ptStdWriter,MESSAGE)
  write(MESSAGE,*) "LINES = ", npatch*plen
  call write_out(ptStdWriter,MESSAGE)
  deallocate(gnd_sq_ang,cos_ang,sin_ang,rho,squintshift)
  deallocate(dem,geo,dem_crop)
  deallocate(losang)
!!  Debugging - PSA  
!!  deallocate(distance)
  deallocate(ifg)

  nullify(readBand,writeBand,intp_data)

  t1 = secnds(t0)
  write(MESSAGE,*) 'elapsed time = ',t1,' seconds'
  call write_out(ptStdWriter,MESSAGE)
end 
