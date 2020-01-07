      subroutine rcov(rawAccessor,nnn,nlinesaz,unpacki,unpackq, &
          irec,ifrst,nbytes,ngood, ranfft)

      !rawAccessor    -> File pointer
      !nnn            -> Number of azimuth lines in a patch
      !nlinesaz       -> Size of the output array in range
      !unpacki        -> Unpacking I channel array
      !unpackq        -> Unpacking Q channel array
      !irec           -> First line in the file to read
      !ifrst          -> First pixel to read
      !nbytes         -> Number of bytes in a line in raw file
      !ngood          -> Number of good bytes in a line in raw file
      !iflip          -> If the I/Q channels are flipped
      !ranfft         -> FFT size for range
      
      use arraymodule
      implicit none
      include 'omp_lib.h'
      
      integer*8 rawAccessor		!File pointer
      integer*4 ranfft			!Size of FFT
      integer*4 nnn,irec                !Number of lines, First line to read
      integer*4 ifrst,nbytes            !First pixel to read, Number of bytes per line
      integer*4 ngood,nlinesaz          !Number of good bytes, Number of range pixels
      integer*4 i,j			!Local variables
      integer*1,allocatable:: inbuf(:)  !Contiguous Input Buffer
      real*4    unpacki(256),unpackq(256) !Unpacking arrays

      complex*8 tmp(ranfft)		!Array for storing one line of complex data
      integer*8 iplanfranfft,iplaniranfft2   !FFTW plans 
      real*4, allocatable :: planfranfft(:),planiranfft2(:)   !FFTW arrays
      integer colPos,rowPos,numEl

      write(*,*)'O/V range starting record, pixel: ',irec,ifrst

!c  init the ffts for both transform lengths
      call cfft1d_jpl(ranfft,tmp,0)     !Create FFTW plans
      call cfft1d_jpl(ranfft/2,tmp,0)

!c   Initialize buffers
      allocate(inbuf(nnn*nbytes))  !Allocate memory for an entire patch of data
      trans1 = 0		   !Initialize O/P buffer to zero
      inbuf = 0			   !Initialize I/P buffer to zero   
      tmp = 0			   !Initialize temporary buffer to zero

!c    Actually read in the data
      rowPos = irec + 1		    !First line starts from irec+1
      colPos =  1		    !Starting from first column
      numEl = nbytes*nnn	    !Number of bytes to read
      !Read
      call getSequentialElements(rawAccessor,inbuf,rowPos,colPos,numEl)

!c    Report if fewer elements are read in
      if(numEl .ne. nbytes*nnn) then
           write(6,*) "Warning. Number of elements requested is ", nbytes*nnn ,"while the number of elements read is", numEl 
      endif


!c  Start of the openmp parallel loop

!$omp parallel  private(tmp,planfranfft,planiranfft2) &
!$omp shared(nnn,unpacki,unpackq,ifrst,nbytes,ngood,numEl,trans1,iplanfranfft,iplaniranfft2)
!$omp do
      do j = 1, min(numEl/nbytes,nnn)	!For each line read in
         do i=1,ngood-ifrst             !For each good pixel
            tmp(i)=cmplx(unpacki(iand(1+inbuf(i+ifrst+(j-1)*nbytes),255)),0.)
	 end do   !Done unpacking the line

	 !Fill the rest of the lines with zeros
         do i=ngood-ifrst+1,ranfft
            tmp(i)=cmplx(0.,0.)
         end do

	 !Forward transform the data line
         call cfft1d_jpl(ranfft,tmp,-1)

!c   Transform the spectrum to baseband since the input is offset video
!c   Only the first and the far ends of the spectrum are relevant
!c   Multiply with the FFT of the reference chirp as well
         do i=1,ranfft/4
            tmp(i)=tmp(i+3*ranfft/4)*ref1(i+3*ranfft/4)
         end do
         do i=1,ranfft/4
            tmp(i+ranfft/4)=tmp(i+ranfft/2)*ref1(i+ranfft/2)
         end do

!c   Inverse Fourier Transform - Only half the spectrum is relevant.
         call cfft1d_jpl(ranfft/2,tmp,1)

!c   Number of valid samples copied to output
         do i=1,nlinesaz
            trans1(j,i)=tmp(i)
         end do
      end do

!$omp end do
!$omp end parallel 

      !Deallocate the temporary input buffer
      deallocate(inbuf)

      !Destroy FFTW plans
      call cfft1d_jpl(ranfft,tmp,2)
      call cfft1d_jpl(ranfft/2,tmp,2)

      return
      end



