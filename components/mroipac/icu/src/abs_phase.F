!c***************************************************************************
      subroutine abs_phase(r_unw, c_ampb, r_amp, b_all_unwrap,r_bphase,
     $          r_bamp, i_complist, i_patch)

      use icuState  
      implicit none


!C   INPUT VARIABLES:

      real*4 r_xofr(0:infp%i_rsamps-1)	!azimuth offsets (pixels) for the bootstrap phase
      complex*8 c_ampb(0:infp%i_rsamps-1, 0:infp%i_azbufsize-1)		!amplitude of the two SLCs used to form the interferogram
      real*4 r_unw(0:infp%i_rsamps-1, 0:infp%i_azbufsize-1)		!unwrapped phase
      integer*1 b_all_unwrap(0:infp%i_rsamps-1, 0:infp%i_azbufsize-1) !flag array marking all samples unwrapped in the patch
      real*4 r_bphase(0:infp%i_rsamps-1,0:NBL-1)             !bootstrap phase data
      real*4 r_bamp(0:infp%i_rsamps-1,0:NBL-1)		!bootstrap amplitude data
      integer*4 i_complist(0:1,MAXCCOMP)
      integer*4 i_patch, ml


!c   OUTPUT VARIABLES:

      real*4 r_amp(0:infp%i_rsamps-1, 0:infp%i_azbufsize-1)		!image amplitude (0 where not unwrapped)c

!c   LOCAL VARIABLES:
         
      integer*4 i_ccc           !connected component counter
      integer*4 ir, ia, ind, i_bcnt
      integer*4 i_abs_phase, i_printfreq, i_abs_phase_index

!c     external rt_cc

!c     DATA STATEMENTS:

      data i_abs_phase_index /0/

                
!c     PROCESSING STEPS:

      if(i_patch .eq. 1) then
         ml = 0
         ia = 0
         do ir = 1, MAXCCOMP
            if(i_complist(0,ir) .gt. ml) then
               ml = i_complist(0,ir)
               ia = ir
            end if
         end do
         if(ia .ne. 0) then
            i_complist(1,ia) = BOOT
         end if
      end if
      do ia = unwp%i_sunw, unwp%i_eunw !initialize unwrap data arrays
         do ir = unwp%i_spixel, unwp%i_epixel
            r_amp(ir,ia) = 0.
            if(b_all_unwrap(ir,ia) .ne. 0)then
               ind = b_all_unwrap(ir,ia)
!c               write(*,*) 'ind ', ind
               if(i_complist(1,ind) .eq. NOBOOT) then
                  r_unw(ir,ia) = 0.
               else
!c                 r_amp(ir,ia) = real(c_ampb(ir,ia))
                  r_amp(ir,ia) = sqrt(real(c_ampb(ir,ia))
     $                 *aimag(c_ampb(ir,ia)))
               end if
            end if
         end do
      end do

!c* set the bootstrap phase

      i_bcnt = 0                !initialize counter of bootstrap points
      do ind = 0, NBL-1
         do ir = unwp%i_spixel, unwp%i_epixel
            ia = infp%i_azbufsize - unwp%i_ovloff - NBL/2 + ind
            r_bamp(ir,ind)   = r_amp(ir,ia)
            r_bphase(ir,ind) = r_unw(ir,ia)
            if(r_amp(ir,ia) .ne. 0) then
               i_bcnt = i_bcnt + 1
            end if
         end do
      end do

!c      if(i_bcnt .eq. 0) then
!c        write(6,'(1x,a)')'WARNING: UNW_RT: no points for phase bootstap of next patch' 
!c      else 
!c        write(6,'(1x,a,i10)')'UNW_RT: phase bootstrap points for next patch: ',i_bcnt	
!c      end if
      

      end

