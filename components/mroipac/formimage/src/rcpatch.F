#ifndef PARALLELIZED_RCPATCH
# ifndef TUNED_RCPATCH
      subroutine rcpatch(ptImageRaw,dataLineGet,nnn,nlinesaz,trans,unpacki,unpackq,
     1     ref,irec,ifrst,nbytes,ngood,nr_fftf,nr_fftr,iq,iflip,agc,dwp,nagc,ndwp, ROMIO)

c      subroutine rcpatch(fdsc,nnn,nlinesaz,trans,unpacki,unpackq,
c     1     ref,irec,ifrst,nbytes,ngood,nr_fftf,nr_fftr,iq,iflip,agc,dwp,nagc,ndwp, ROMIO)
      implicit none
#ifdef MPI_PARA
      include 'mpif.h'
#endif
      integer inbuflen
      parameter (inbuflen=32768)
c      integer*1      inbuf(inbuflen)
      integer*1, dimension(*) :: dataLineGet
      integer*4 nnn,irec,ifrst,nbytes,ngood,fdsc,nlinesaz,i,j,k, iq,iflip
      integer*4 ptImageRaw, offsetGet
      integer*4 nr_fftf, nr_fftr
      real*4    unpacki(256),unpackq(256)

      complex*8 trans(nnn,nlinesaz),ref(nr_fftf),tmp(nr_fftf)
      integer*4 nagc, ndwp, dwpval, nrec
      real*4    dwp(2,ndwp),agc(2,nagc), agcval
      integer*4 line,ii, ierr
      character*4 ROMIO

#ifdef MPI_PARA
      integer status(MPI_STATUS_SIZE)
      integer(KIND=MPI_OFFSET_KIND) offset
      integer count
#endif

      agcval = 1.
      dwpval = 0
      if(iq.eq.0) then
         write(6,*) 'Offset Video: Range starting record, pixel: ',irec,ifrst
         offsetGet = 0
	 do j = 1, nnn
            line=j-1+irec-1
            if(mod(line,1024).eq.1)write(6,*) 'Line ',line
            if(j-1+irec .lt. 1) goto 777
#ifdef MPI_PARA
           if(ROMIO .eq. "yes") then
            offset = (j-1+irec-1)*nbytes
            call MPI_FILE_READ_AT(fdsc,offset,inbuf,nbytes,MPI_BYTE,
     &                            status, ierr)
            call MPI_GET_COUNT(status, MPI_BYTE,count, ierr)
            if(count .eq. 0) goto 777
cc            write(6,*) 'XXX at j:', j, 'read ',count,' bytes (in rcpatch)'
           else
            read(fdsc,rec=j-1+irec,iostat=ierr) (inbuf(k),k=1,nbytes)
            if(ierr .ne. 0) goto 777
           endif
#else
	    offsetGet = j-1+irec
            call getLine(ptImageRaw,dataLineGet,offsetGet)
c            read(fdsc,rec=j-1+irec,iostat=ierr) (inbuf(k),k=1,nbytes)
c            if(ierr .ne. 0) goto 777
            if(offsetGet .lt. 0) goto 777
#endif

c Handle gain change and dwp change of raw data
c
            nrec = j-1+irec
            agcval = 1.
            do i = nagc, 1, -1
               if (nrec .ge. agc(1,i)) then
                 agcval = 10. ** (agc(2,i)/20.)
                 goto 180
               endif
            enddo

180         dwpval = 0
            do i = ndwp, 1, -1
               if (nrec .ge. dwp(1,i)) then
                  dwpval = dwp(2,i)
                  goto 181
               endif
            enddo

181         do i=max(1,dwpval+1),ngood-ifrst+max(0,dwpval)
               tmp(i)=cmplx(unpacki(1+(iand(int(dataLineGet(offsetGet + i+ifrst-dwpval)),255))),0.)
c               tmp(i)=cmplx(unpacki(1+(iand(int(inbuf(i+ifrst-dwpval)),255))),0.)
c              int() above is used to promote inbuf elements 
c              to be a default integer
c              so they are the same type/kind as the constant 255.
c              Some compilers enforce that both parameters to iand()
c              be the same type/kind.
            end do
            do i=ngood-ifrst+1+max(0,dwpval),nr_fftf
               tmp(i)=cmplx(0.,0.)
            end do
            do i=1,max(0,dwpval)
               tmp(i)=cmplx(0.,0.)
            enddo
            goto 778

c     if there is a read error, assume user is requesting a line 
c     from either before or after the file extent.  Fill with zeros.

 777        do ii=1,nr_fftf
               tmp(ii)=cmplx(0.,0.)
            enddo

 778        call cfft1d_jpl(nr_fftf,tmp,-1)
         
c  baseband the resulting spectrum since input is offset video

            do i=1,nr_fftf/4
               tmp(i)=tmp(i+3*nr_fftf/4)*ref(i+3*nr_fftf/4)*agcval
            end do
            do i=1,nr_fftf/4
               tmp(i+nr_fftf/4)=tmp(i+nr_fftf/2)*ref(i+nr_fftf/2)*agcval
            end do

            call cfft1d_jpl(nr_fftr,tmp,1)

            do i=1,nlinesaz
               trans(j,i)=tmp(i)
            end do
         end do
      else

         write(6,*) 'I/Q: Range starting record, pixel: ',irec,ifrst
         offsetGet = 0
         do j = 1, nnn
            line=j-1+irec-1
            if(mod(line,1024).eq.1)write(6,*) 'Line ',line
            if(j-1+irec .lt. 1) goto 779
#ifdef MPI_PARA
           if(ROMIO .eq. "yes") then
            offset = (j-1+irec-1)*nbytes
            call MPI_FILE_READ_AT(fdsc,offset,inbuf,nbytes,MPI_BYTE,
     &                            status, ierr)
            call MPI_GET_COUNT(status, MPI_BYTE,count, ierr)
            if(count .eq. 0) goto 779
cc            write(6,*) 'XXX at j:', j, 'read ',count,' bytes (in rcpatch)'
           else
            read(fdsc,rec=j-1+irec,iostat=ierr) (inbuf(k),k=1,nbytes)
            if(ierr .ne. 0) goto 779
           endif
#else
	    offsetGet = j-1+irec
            call getLine(ptImageRaw,dataLineGet,offsetGet)

c            read(fdsc,rec=j-1+irec,iostat=ierr) (inbuf(k),k=1,nbytes)
c            if(ierr .ne. 0) goto 779
	    if(offsetGet .lt. 0) goto 779
#endif
c
c Handle gain change and dwp change of raw data
c
            nrec = j-1+irec
            agcval = 1.
            do i = nagc, 1, -1
               if (nrec .ge. agc(1,i)) then
                  agcval = 10. ** (agc(2,i)/20.)
                  goto 280
               endif
            enddo

280         dwpval = 0
            do i = ndwp, 1, -1
               if (nrec .ge. dwp(1,i)) then
                  dwpval = dwp(2,i)
                  goto 281
               endif
            enddo

281         do i=max(1,dwpval+1),ngood/2-ifrst+max(0,dwpval)
	       tmp(i)=
     1              cmplx(unpacki(1+(iand(255,int(dataLineGet((i+ifrst-dwpval)*2-1))))),
     $                    unpackq(1+(iand(255,int(dataLineGet((i+ifrst-dwpval)*2))))))
c     1              cmplx(unpacki(1+(iand(255,int(inbuf((i+ifrst-dwpval)*2-1))))),
c     $                    unpackq(1+(iand(255,int(inbuf((i+ifrst-dwpval)*2))))))


            end do

            do i=ngood/2-ifrst+1+max(0,dwpval),nr_fftf
               tmp(i)=cmplx(0.,0.)
            end do
            do i=1,max(0,dwpval)
               tmp(i)=cmplx(0.,0.)
            enddo
            goto 780

c     if there is a read error, assume user is requesting a line 
c     from either before or after the file extent.  Fill with zeros.

 779        do ii=1,nr_fftf
               tmp(ii)=cmplx(0.,0.)
            enddo

 780        if(iflip .eq. 1) then
               do i = 1 , nr_fftf
                  tmp(i) = cmplx(aimag(tmp(i)),real(tmp(i)))
               end do
            end if
            call cfft1d_jpl(nr_fftf,tmp,-1)
            
            do i=1,nr_fftf
               tmp(i)=tmp(i)*ref(i)*agcval
            end do
            
            call cfft1d_jpl(nr_fftf,tmp,1)
            
            do i=1,nlinesaz
               trans(j,i)=tmp(i)
            end do
         end do
      end if
         
      return
      end
#else /* TUNED_RCPATCH */
c      subroutine rcpatch(fdsc,nnn,nlinesaz,trans,unpacki,unpackq,
c     1     ref,irec,ifrst,nbytes,ngood,nr_fftf,nr_fftr,iq,iflip,agc,dwp,nagc,ndwp)

      subroutine rcpatch(ptImageRaw,dataLineGet,nnn,nlinesaz,trans,unpacki,unpackq,
     1     ref,irec,ifrst,nbytes,ngood,nr_fftf,nr_fftr,iq,iflip,agc,dwp,nagc,ndwp)
      
      implicit none
      integer*4 nnn,irec,ifrst,nbytes,ngood,fdsc,nlinesaz,i,j,k,jb,jbmax,iq,iflip
      integer*4 nr_fftf, nr_fftr
      integer inbuflen
      parameter (inbuflen=32768)
c      integer*1      inbuf(inbuflen)
      integer*1, dimension(*) :: dataLineGet
      integer*4 ptImageRaw, offsetGet
      real*4    unpacki(256),unpackq(256)
      complex*8 trans(nnn,nlinesaz),ref(nr_fftf)
      complex*8 tmp(nr_fftf,0:3)
      integer*4 nagc, ndwp, dwpval, nrec
      real*4    dwp(2,ndwp),agc(2,nagc), agcval
      integer*4 line,ii,jj, ierr

      write(6,*) 'Range starting record, pixel: ',irec,ifrst

      agcval = 1.
      dwpval = 0
c      if(nbytes .gt. inbuflen) then
c         stop 'rcpatch tuned: input buffer must be enlarged'
c      end if
      if(iq.eq.0) then
         write(6,*) 'Offset Video: Range starting record, pixel: ',irec,ifrst
         offsetGet = 0
	 do j = 1, nnn, 4
            jbmax = min(3,nnn-j)
            do jb = 0, jbmax
               line=j+jb-1+irec-1
               if(mod(line,1024).eq.1)write(6,*) 'Line ',line
               if(j+jb-1+irec .lt. 1) goto 877
		offsetGet = j + jb -1+irec
		call getLine(ptImageRaw,dataLineGet,offsetGet)
               if(offsetGet .lt. 0) goto 877
c               read(fdsc,rec=j+jb-1+irec,iostat=ierr) (inbuf(k),k=1,nbytes)
c               if(ierr .ne. 0) goto 877
c
c Handle gain change and dwp change of raw data
c
               nrec = j+jb-1+irec
               agcval = 1.
               do i = nagc, 1, -1
                  if (nrec .ge. agc(1,i)) then
                     agcval = 10. ** (agc(2,i)/20.)
                     goto 380
                  endif
               enddo

380            dwpval = 0
               do i = ndwp, 1, -1
                  if (nrec .ge. dwp(1,i)) then
                     dwpval = dwp(2,i)
                     goto 381
                  endif
               enddo

381            do i=max(1,dwpval+1),ngood-ifrst+max(0,dwpval)
c                  tmp(i,jb)=cmplx(unpacki(1+(inbuf(i+ifrst-dwpval).and.255)),0.)
                  tmp(i,jb)=cmplx(unpacki(1+(dataLineGet(offsetGet + i+ifrst-dwpval).and.255)),0.)
               end do
               do i=ngood-ifrst+1+max(0,dwpval),nr_fftf
                  tmp(i,jb)=cmplx(0.,0.)
               end do
               do i=1,max(0,dwpval)
                  tmp(i,jb)=cmplx(0.,0.)
               enddo
               goto 878

c     if there is a read error, assume user is requesting a line 
c     from either before or after the file extent.  Fill with zeros.

 877           do ii=1,nr_fftf
                  tmp(ii,jb)=cmplx(0.,0.)
               enddo

 878           call cfft1d_jpl(nr_fftf,tmp(1,jb),-1)
               
c     baseband the resulting spectrum since input is offset video

               do i=1,nr_fftf/4
                  tmp(i,jb)=tmp(i+3*nr_fftf/4,jb)*ref(i+3*nr_fftf/4)*agcval
               end do
               do i=1,nr_fftf/4
                  tmp(i+nr_fftf/4,jb)=tmp(i+nr_fftf/2,jb)*ref(i+nr_fftf/2)*agcval
               end do
               
               call cfft1d_jpl(nr_fftr,tmp(1,jb),1)
            enddo
            
            if (jbmax.eq.3) then
               do i=1,nlinesaz
                  trans(j+ 0,i)=tmp(i, 0)
                  trans(j+ 1,i)=tmp(i, 1)
                  trans(j+ 2,i)=tmp(i, 2)
                  trans(j+ 3,i)=tmp(i, 3)
               end do
            elseif (jbmax.eq.2) then
               do i=1,nlinesaz
                  trans(j+ 0,i)=tmp(i, 0)
                  trans(j+ 1,i)=tmp(i, 1)
                  trans(j+ 2,i)=tmp(i, 2)
               end do
            elseif (jbmax.eq.1) then
               do i=1,nlinesaz
                  trans(j+ 0,i)=tmp(i, 0)
                  trans(j+ 1,i)=tmp(i, 1)
               end do
            elseif (jbmax.eq.0) then
               do i=1,nlinesaz
                  trans(j+ 0,i)=tmp(i, 0)
               end do
            endif
         end do
      else
         write(6,*) 'I/Q: Range starting record, pixel: ',irec,ifrst
	 offsetGet = 0
         do j = 1, nnn, 4
            jbmax = min(3,nnn-j)
            do jb = 0, jbmax
               line=j+jb-1+irec-1
               if(mod(line,1024).eq.1)write(6,*) 'Line ',line
               if(j+jb-1+irec .lt. 1) goto 879
		offsetGet = j + jb -1+irec
		call getLine(ptImageRaw,dataLineGet,offsetGet)
               if(offsetGet .lt. 0) goto 879
c               read(fdsc,rec=j+jb-1+irec,iostat=ierr) (inbuf(k),k=1,nbytes)
c               if(ierr .ne. 0) goto 879

c
c Handle gain change and dwp change of raw data
c
               nrec = j+jb-1+irec
               agcval = 1.
               do i = nagc, 1, -1
                  if (nrec .ge. agc(1,i)) then
                     agcval = 10. ** (agc(2,i)/20.)
                     goto 480
                  endif
               enddo

480            dwpval = 0
               do i = ndwp, 1, -1
                  if (nrec .ge. dwp(1,i)) then
                     dwpval = dwp(2,i)
                     goto 481
                  endif
               enddo

481            do i=max(1,dwpval+1),ngood/2-ifrst+max(0,dwpval)
                  tmp(i,jb)=
     1                 cmplx(unpacki(1+(255.and.dataLineGet((i+ifrst-dwpval)*2-1 + offsetGet)))
     $                      ,unpackq(1+(255.and.dataLineGet((i+ifrst-dwpval)*2 + offsetGet))))
c     1                 cmplx(unpacki(1+(255.and.inbuf((i+ifrst-dwpval)*2-1)))
c     $                      ,unpackq(1+(255.and.inbuf((i+ifrst-dwpval)*2))))
               end do
               do i=ngood/2-ifrst+1+max(0,dwpval),nr_fftf
                  tmp(i,jb)=cmplx(0.,0.)
               end do
               do i=1,max(0,dwpval)
                   tmp(i,jb)=cmplx(0.,0.)
               enddo
               goto 880

c     if there is a read error, assume user is requesting a line 
c     from either before or after the file extent.  Fill with zeros.

 879           do ii=1,nr_fftf
                  tmp(ii,jj)=cmplx(0.,0.)
               enddo

 880           if(iflip .eq. 1) then
                  do i = 1 , nr_fftf
                     tmp(i,jb) = cmplx(aimag(tmp(i,jb)),real(tmp(i,jb)))
                  end do
               end if

               call cfft1d_jpl(nr_fftf,tmp(1,jb),-1)
               
               do i=1,nr_fftf
                  tmp(i,jb)=tmp(i,jb)*ref(i)*agcval
               end do

               call cfft1d_jpl(nr_fftf,tmp(1,jb),1)

            enddo
            
            if (jbmax.eq.3) then
               do i=1,nlinesaz
                  trans(j+ 0,i)=tmp(i, 0)
                  trans(j+ 1,i)=tmp(i, 1)
                  trans(j+ 2,i)=tmp(i, 2)
                  trans(j+ 3,i)=tmp(i, 3)
               end do
            elseif (jbmax.eq.2) then
               do i=1,nlinesaz
                  trans(j+ 0,i)=tmp(i, 0)
                  trans(j+ 1,i)=tmp(i, 1)
                  trans(j+ 2,i)=tmp(i, 2)
               end do
            elseif (jbmax.eq.1) then
               do i=1,nlinesaz
                  trans(j+ 0,i)=tmp(i, 0)
                  trans(j+ 1,i)=tmp(i, 1)
               end do
            elseif (jbmax.eq.0) then
               do i=1,nlinesaz
                  trans(j+ 0,i)=tmp(i, 0)
               end do
            endif
         end do
      end if
      return
      end
#endif /* TUNED_RCPATCH */
#else /* PARALLELIZED_RCPATCH */
      subroutine rcpatch(fdsc,nnn,nlinesaz,trans,unpacki,unpackq,
     1     ref,irec,ifrst,nbytes,ngood,nr_fftf,nr_fftr,iq,iflip,agc,dwp,nagc,ndwp)

      implicit none
      integer*4 nnn,irec,ifrst,nbytes,ngood,fdsc,nlinesaz,i,j,iq,iflip
      integer*4 nr_fftf, nr_fftr
      integer*4 nio, jio, jioend, jblock, n_threads, iblock, jend
      integer*4 mp_numthreads, k
      external  mp_numthreads
      parameter (nio = 64*16)	! 64 * # MBytes: 8 or 16 MBytes is good
      integer inbuflen
      parameter (inbuflen=32768)
      integer*1      inbuf(inbuflen,nio)
      real*4    unpacki(256),unpackq(256)
      complex*8 trans(nnn,nlinesaz),ref(nr_fftf)
      integer*4 nagc, ndwp, dwpval, ierr
      real*4    dwp(2,ndwp),agc(2,nagc), agcval

      write(6,*) 'Range starting record, pixel: ',irec,ifrst

      if(nbytes .gt. inbuflen) then
         stop 'rcpatch parallel: input buffer must be enlarged'
      end if
      n_threads = 1
c$    n_threads = mp_numthreads()
c
c     iblock needs to be >= 16 to avoid false sharing problems.
      iblock = (nio + n_threads-1)/n_threads
      do jio = 1, nnn, nio
         jioend = min(jio+nio-1,nnn)
c
c        Since there is only one file to read the data from,
c        it only makes sense to do the IO sequentially. So we
c        do a bunch of it all at once, and then let the CPUs
c        split up the processing work on what has been read.
c

         do j = jio, jioend
            do k = 1 , nlinesaz
               trans(j,k) = cmplx(0.,0.)
            end do
         end do

         do j = jio, jioend
            if (mod(j,1024).eq.1) write(6,*) 'Line ',j
            read(fdsc,rec=j-1+irec,iostat=ierr) (inbuf(k,1+j-jio),k=1,nbytes)
            if(ierr .ne. 0) goto 999
         enddo
            
c
c        Here is the parallel procesing: one iblock per
c        processor.
c
         if(iq .eq. 0) then

c$doacross local(j,jend), share(jio,jioend,iblock,
c$&                             inbuf,nnn,nlinesaz,trans,
c$&                             unpacki,unpackq,ref,ifrst,ngood
c$&                             ,nr_fftf, nr_fftr)
            do j = jio, jioend, iblock
               jend = min(j+iblock-1,jioend)
               call rcpatch_work(j,jend,irec,inbuf(1,1+j-jio),
     &              nnn,nlinesaz,trans,unpacki,unpackq,
     &              ref,ifrst,ngood,nr_fftf, nr_fftr,agc,dwp,nagc,ndwp)
            enddo
         else
c$doacross local(j,jend), share(jio,jioend,iblock,
c$&                             inbuf,nnn,nlinesaz,trans,
c$&                             unpacki,unpackq,ref,ifrst,ngood
c$&                             ,nr_fftf, nr_fftr)
            do j = jio, jioend, iblock
               jend = min(j+iblock-1,jioend)
               call rcpatch_workiq(j,jend,irec,inbuf(1,1+j-jio),
     &              nnn,nlinesaz,trans,unpacki,unpackq,iflip,
     &              ref,ifrst,ngood,nr_fftf,nr_fftr,agc,dwp,nagc,ndwp)
            enddo
            
         end if
         
 999  enddo

      return
      end

      subroutine rcpatch_work(jbeg,jend,irec,inbuf,
     &                        nnn,nlinesaz,trans,unpacki,unpackq,
     &                        ref,ifrst,ngood,nr_fftf,nr_fftr,agc,dwp,nagc,ndwp)

      implicit none
      integer*4 jbeg, jend, nr_fftf, nr_fftr
      integer inbuflen
      parameter (inbuflen=32768)
      integer*1     inbuf(inbuflen,jend-jbeg+1)
      integer*4 nnn, ifrst, ngood, nlinesaz, i, j, jb, jbmax
      real*4    unpacki(256), unpackq(256)
      complex*8 trans(nnn,nlinesaz), ref(nr_fftf)
      complex*8 tmp(nr_fftf,0:3)
      integer*4 nagc, ndwp, dwpval,irec, nrec
      real*4    dwp(2,ndwp),agc(2,nagc), agcval
      
      do j = jbeg, jend, 4
         jbmax = min(3,jend-j)
         do jb = 0, jbmax
c
c Handle gain change and dwp change of raw data
c
            nrec = j+jb-1+irec
            agcval = 1.
            do i = nagc, 1, -1
              if (nrec .ge. agc(1,i)) then
                agcval = 10. ** (agc(2,i)/20.)
                goto 580
              endif
            enddo

580         dwpval = 0
            do i = ndwp, 1, -1
              if (nrec .ge. dwp(1,i)) then
                dwpval = dwp(2,i)
                goto 581
              endif
            enddo

581         do i=max(1,dwpval+1),ngood-ifrst+max(0,dwpval)
               tmp(i,jb)=cmplx(unpacki(1+(inbuf(i+ifrst-dwpval,1+j-jbeg+jb).and.255)),0.)
            end do
            do i=ngood-ifrst+1+max(0,dwpval),nr_fftf
               tmp(i,jb)=cmplx(0.,0.)
            end do
            do i=1,max(0,dwpval)
               tmp(i,jb)=cmplx(0.,0.)
            enddo

            call cfft1d_jpl(nr_fftf,tmp(1,jb),-1)
         
c  baseband the resulting spectrum since input is offset video
            do i=1,nr_fftf/4
               tmp(i,jb)=tmp(i+3*nr_fftf/4,jb)*ref(i+3*nr_fftf/4)*agcval
            end do
            do i=1,nr_fftf/4
               tmp(i+nr_fftf/4,jb)=tmp(i+nr_fftf/2,jb)*ref(i+nr_fftf/2)*agcval
            end do

            call cfft1d_jpl(nr_fftr,tmp(1,jb),1)
         enddo

         if (jbmax.eq.3) then
            do i=1,nlinesaz
               trans(j+ 0,i)=tmp(i, 0)
               trans(j+ 1,i)=tmp(i, 1)
               trans(j+ 2,i)=tmp(i, 2)
               trans(j+ 3,i)=tmp(i, 3)
            end do
         elseif (jbmax.eq.2) then
            do i=1,nlinesaz
               trans(j+ 0,i)=tmp(i, 0)
               trans(j+ 1,i)=tmp(i, 1)
               trans(j+ 2,i)=tmp(i, 2)
            end do
         elseif (jbmax.eq.1) then
            do i=1,nlinesaz
               trans(j+ 0,i)=tmp(i, 0)
               trans(j+ 1,i)=tmp(i, 1)
            end do
         elseif (jbmax.eq.0) then
            do i=1,nlinesaz
               trans(j+ 0,i)=tmp(i, 0)
            end do
         endif
      end do

      return
      end
      subroutine rcpatch_workiq(jbeg,jend,irec,inbuf,
     &                        nnn,nlinesaz,trans,unpacki,unpackq,iflip,
     &                        ref,ifrst,ngood,nr_fftf,nr_fftr,agc,dwp,nagc,ndwp)

      implicit none
      integer*4 jbeg, jend, nr_fftf, nr_fftr,iflip
      integer inbuflen
      parameter (inbuflen=32768)
      integer*1     inbuf(inbuflen,jend-jbeg+1)
      integer*4 nnn, ifrst, ngood, nlinesaz, i, j, jb, jbmax
      real*4    unpacki(256), unpackq(256)
      complex*8 trans(nnn,nlinesaz), ref(nr_fftf)
      complex*8 tmp(nr_fftf,0:3)
      integer*4 nagc, ndwp, dwpval, irec, nrec
      real*4    dwp(2,ndwp),agc(2,nagc), agcval
      
      do j = jbeg, jend, 4
         jbmax = min(3,jend-j)
         do jb = 0, jbmax
c
c Handle gain change and dwp change of raw data
c
            nrec = j+jb-1+irec
            agcval = 1.
            do i = nagc, 1, -1
              if (nrec .ge. agc(1,i)) then
                agcval = 10. ** (agc(2,i)/20.)
                goto 680
              endif
            enddo

680         dwpval = 0
            do i = ndwp, 1, -1
              if (nrec .ge. dwp(1,i)) then
                dwpval = dwp(2,i)
                goto 681
              endif
            enddo

681         do i=max(1,dwpval+1),ngood/2-ifrst+max(0,dwpval)
               tmp(i,jb)=cmplx(
     .              unpacki(1+(inbuf(2*(i+ifrst-dwpval)-1,1+j-jbeg+jb).and.255)),
     .              unpackq(1+(inbuf(2*(i+ifrst-dwpval)  ,1+j-jbeg+jb).and.255)))
            end do
            do i=ngood/2-ifrst+1+max(0,dwpval),nr_fftf
               tmp(i,jb)=cmplx(0.,0.)
            end do
            do i=1,max(0,dwpval)
               tmp(i,jb)=cmplx(0.,0.)
            enddo

            if(iflip .eq. 1) then
               do i = 1 , nr_fftf
                  tmp(i,jb) = cmplx(aimag(tmp(i,jb)),real(tmp(i,jb)))
               end do
            end if
            call cfft1d_jpl(nr_fftf,tmp(1,jb),-1)
         
            do i=1,nr_fftf
               tmp(i,jb)=tmp(i,jb)*ref(i)*agcval
            end do

            call cfft1d_jpl(nr_fftf,tmp(1,jb),1)
         enddo

         if (jbmax.eq.3) then
            do i=1,nlinesaz
               trans(j+ 0,i)=tmp(i, 0)
               trans(j+ 1,i)=tmp(i, 1)
               trans(j+ 2,i)=tmp(i, 2)
               trans(j+ 3,i)=tmp(i, 3)
            end do
         elseif (jbmax.eq.2) then
            do i=1,nlinesaz
               trans(j+ 0,i)=tmp(i, 0)
               trans(j+ 1,i)=tmp(i, 1)
               trans(j+ 2,i)=tmp(i, 2)
            end do
         elseif (jbmax.eq.1) then
            do i=1,nlinesaz
               trans(j+ 0,i)=tmp(i, 0)
               trans(j+ 1,i)=tmp(i, 1)
            end do
         elseif (jbmax.eq.0) then
            do i=1,nlinesaz
               trans(j+ 0,i)=tmp(i, 0)
            end do
         endif
      end do

      return
      end
#endif /* PARALLELIZED_RCPATCH */

