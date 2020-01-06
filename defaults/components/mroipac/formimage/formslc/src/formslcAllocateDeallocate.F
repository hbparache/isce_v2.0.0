c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c
c                                  Giangi Sacco
c                        NASA Jet Propulsion Laboratory
c                      California Institute of Technology
c                        (C) 2009  All Rights Reserved
c
c~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	subroutine allocate_dopplerCoefficients(dim1)
		use formslcState
		implicit none
		integer dim1
		dim1_dopplerCoefficients = dim1
		allocate(dopplerCoefficients(dim1)) 
	end

	subroutine deallocate_dopplerCoefficients()
		use formslcState
		deallocate(dopplerCoefficients) 
	end

	subroutine allocate_r_platvel1(dim1)
		use formslcState
		implicit none
		integer dim1
		dim1_r_platvel1 = dim1
		allocate(r_platvel1(dim1)) 
	end

	subroutine deallocate_r_platvel1()
		use formslcState
		deallocate(r_platvel1) 
	end

	subroutine allocate_r_platacc1(dim1)
		use formslcState
		implicit none
		integer dim1
		dim1_r_platacc1 = dim1
		allocate(r_platacc1(dim1)) 
	end

	subroutine deallocate_r_platacc1()
		use formslcState
		deallocate(r_platacc1) 
	end

	subroutine allocate_spectralShiftFrac(dim1)
		use formslcState
		implicit none
		integer dim1
		dim1_spectralShiftFrac = dim1
		allocate(spectralShiftFrac(dim1)) 
	end

	subroutine deallocate_spectralShiftFrac()
		use formslcState
		deallocate(spectralShiftFrac) 
	end

	subroutine allocate_linearResampCoeff(dim1)
		use formslcState
		implicit none
		integer dim1
		dim1_linearResampCoeff = dim1
		allocate(linearResampCoeff(dim1)) 
	end

	subroutine deallocate_linearResampCoeff()
		use formslcState
		deallocate(linearResampCoeff) 
	end

	subroutine allocate_linearResampDeltas(dim1)
		use formslcState
		implicit none
		integer dim1
		dim1_linearResampDeltas = dim1
		allocate(linearResampDeltas(dim1)) 
	end

	subroutine deallocate_linearResampDeltas()
		use formslcState
		deallocate(linearResampDeltas) 
	end

