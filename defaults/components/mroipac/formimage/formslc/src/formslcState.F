c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c                                  Giangi Sacco
c                        NASA Jet Propulsion Laboratory
c                      California Institute of Technology
c                        (C) 2009  All Rights Reserved
c
c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	module formslcState
		integer ngood1
		integer nbytes1
		integer iflag
		character*1 deskew
		character*1 srm
		integer ifirstline
		integer npatches
		integer ifirst
		integer nnn
		integer na_valid
		real*4 caltone1
		integer isave
		integer nlinesaz
		real*8, allocatable, dimension(:) ::  dopplerCoefficients
		integer dim1_dopplerCoefficients
		real*8 re
		real*4 vel1
		real*8 ht1
		real*8 gm
		integer i_lrl
		real*8, allocatable, dimension(:) ::  r_platvel1
		integer dim1_r_platvel1
		real*8, allocatable, dimension(:) ::  r_platacc1
		integer dim1_r_platacc1
		real*8 r001
		real*4 prf1
		real*4 xmi1
		real*4 xmq1
		character*1 iqflip
		real*4 azres
		integer nlooks
		real*4 fs
		real*4 slope
		real*4 pulsedur
		integer nextend
		real*8 wavl
		real*4 rhww
		real*4, allocatable, dimension(:) ::  spectralShiftFrac
		integer dim1_spectralShiftFrac
		real*8, allocatable, dimension(:) ::  linearResampCoeff
		integer dim1_linearResampCoeff
		real*8, allocatable, dimension(:) ::  linearResampDeltas
		integer dim1_linearResampDeltas
	end module 
