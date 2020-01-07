  subroutine mocompTSX(imageInAccessor,imageOutAccessor)
  use tsxmocomp
  use omp_lib
  use fortranUtils
  use mocompTSXstate
  use arraymodule
  implicit none   ! this statement forces all variables to the defined
  !! PROGRAM DESCRIPTION
  ! reads TerraSAR raw image data(.cos)
  ! Convert it to a slc image
  ! Motion compensation is included

  integer*8 imageInAccessor, imageOutAccessor
  real*8::dr
  real::t0,t1
  
  integer :: i,j,k,lineNumber  ! counter variable
  integer,allocatable::rangeline(:)
  integer,allocatable::rs(:,:),as(:,:) !the validity annotation 
  real*8::fd,fdd,fddd
  real,allocatable::slc(:,:)
  double precision :: pi,sol
  double precision :: midsch(3)
  !$omp parallel
      if(omp_get_thread_num().eq.1)&
      print *, 'Max threads used: ', omp_get_num_threads()
  !$omp end parallel

  t0=secnds(0.0)
  !Read data, byte swap for little endian machine
  allocate(trans1(nr,naz))
  allocate(rangeline((nr+2)))
  allocate(rs(2,naz))
  allocate(as(3,nr+2))
  allocate(schMoc(dim1_sch,dim2_sch))
  allocate(timeMoc(dim1_time))
  !!!!!!!!!!    NOTE !!!!!!!!!!!
  !!!!!!!!!  the deallocation of the next 3 is done in the getState
  !!!!!!!!!  since they need to be accessed after the main is done
  allocate(s_mocomp(naz))
  allocate(t_mocomp(naz))
  allocate(i_mocomp(naz))
   
  !copy the sch position into an array share in arraymodule 
  do i = 1,dim1_sch
    do j = 1,dim2_sch
      schMoc(i,j) = sch(i,j)
    enddo
  enddo
  do j = 1,dim2_sch
    timeMoc(j) = time(j)
  enddo

  t0=secnds(0.0)
  pi = getPI()
  sol = getSpeedOfLight()

  fd = dopplerCentroidCoefficients(1)
  fdd = dopplerCentroidCoefficients(2)
  fdd = dopplerCentroidCoefficients(3)

  dr=sol/fs/2.
  fd=fd*prf
  fdd=fdd*prf
  fddd=fdd*prf
  do j=1,naz
     call getLineSequential(imageInAccessor,trans1(:,j),lineNumber)
  enddo


  midsch = schMoc(1:3, dim2_sch/2)
  call getIdealRange(midsch(1), midsch(2), midsch(3), &
      r0, ht, rcurv, wvl, vel, fd, ilrl, adjustr0)

  print *, 'Original Starting Range: ', r0
  print *, 'Adjusted Starting Range: ', adjustr0


  call mocomp(naz,nr,adjustr0,dr,ht,rcurv,wvl,vel,fd,fdd,fddd,ilrl,r0)
  t1=secnds(t0)
  print *,'Motion compensation uses',t1,'seconds'

  !Write data as slc
  t0=secnds(0.0)
  !print *,'Writing the slc file...'
  !open(22,file=slcfile,access='direct',form='unformatted',recl=nr*2*4)
  !do j=1,naz
     !write(22,rec=j) slc(:,j)
  !enddo
  !close(22)
  
  do j=1,naz
    !call setLineSequential(imageOutAccessor,slc(:,j))

    call setLineSequential(imageOutAccessor,trans1(:,j))
  enddo 
  !the mocompPositionSize is passed back to the python module so it can allocate the
  !right dimension when retrieving the data from fortran
  do k=1,dim2_sch
     if(i_mocomp(k).eq.0)exit
     mocompPositionSize = k
  end do
  t1=secnds(t0)
  print *,'Writing slc file uses',t1,'seconds'
  deallocate(schMoc)
  deallocate(timeMoc)
  deallocate(trans1)
  deallocate(rangeline)
  deallocate(rs)
  deallocate(as)


end subroutine 
