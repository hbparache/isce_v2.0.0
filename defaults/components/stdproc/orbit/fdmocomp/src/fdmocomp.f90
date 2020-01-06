!<
!!  Compute the Doppler centroid needed for motion compensation
!!  processor. 
!!  The Doppler centroid needs to be modified because motion
!!  compensation assumes perfect reference orbit, which has vc = 0
!!  and vh = 0 this routine compensates for real orbits that deviate 
!!  from ideal path and have these other Doppler terms
!!

      subroutine fdmocomp
      use fdmocompState
      use fortranUtils

      implicit none
      real*8       vsavg(3) 
      real*8       cosalp,sinalp,delfd  
      integer*8    db, itmp, i
      real*8       r, delr,ht2, re
      double precision sol
      double precision :: fd1, fdd1, fddd1
    
      fd1 = fdArray(1) 
      fdd1 = fdArray(2) 
      fddd1 = fdArray(3) 
      sol = getSpeedOfLight()
      write(6,*) sol
!c  put fd into hz instead of cycles
      fd1=fd1*prf
      fdd1=fdd1*prf
      fddd1=fddd1*prf

      delr=sol/fs/2.D0

!c    reference doppler coefficients to range

      call radopp(fd1,fdd1,fddd1,r001,delr)

!c New code added by Piyush. Global change to Doppler Centroid.
!c *************************************************************
    
     vsavg=sum(vsch(:,1:nlines),2)/nlines

     print *, 'Average Velocities (S,C,H): ',vsavg
     
     r = r001 + 0.5 * delr*(nlinesaz-1) !c Average range for the image.
     print *, 'Average Range of image: ', r
     print *, 'Curvature: ', rcurv
     print *, 'Height: ', ht1
     cosalp = (rcurv*rcurv+(ht1+rcurv)*(ht1+rcurv)-r*r)/(2.*rcurv*(ht1+rcurv))
     sinalp = sqrt(1-cosalp*cosalp)
     
     print *,'Cos and Sin: ', cosalp, sinalp 
   
     delfd = -ilrl*vsavg(2)*rcurv*sinalp/r + vsavg(3)*((rcurv+ht1)-rcurv*cosalp)/r
     delfd = -2*delfd/wavl 

!c Notes: 
!c  sinalp should be singamma but this is a good approximation.
!c  there could be a sign error in front of each of the two terms.
!c  The avg_vc term in particular could have an error sign.
!c   right now fixing the constant doppler term only.
     print *,'Change in Doppler ', delfd, fd1
     print *,'**************************'
     fdnew = fd1 - delfd

     print *,'Old Doppler               : ',fd1
     print *,'New Doppler for processing: ',fdnew

!c End of code added by Piyush for changing Doppler.
 
     fdnew = fdnew/prf

   end subroutine fdmocomp


   subroutine radopp(fd, fdd, fddd, r, del)
     
     double precision fd, fdd, fddd, r, del, temp1, temp2, temp3
     
     temp1 = fd - fdd * (r/del) + fddd * (r/del)**2
     temp2 = fdd/del - 2.d0 * fddd*(r/del)/del
     temp3 = fddd / del**2
     
     fd   = temp1
     fdd  = temp2
     fddd = temp3
     
     return
   end subroutine radopp
 
