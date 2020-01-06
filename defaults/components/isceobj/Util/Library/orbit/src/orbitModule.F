        module orbitModule
            use, intrinsic:: iso_c_binding
            implicit none

            type, bind(C) :: orbitType
                integer(C_INT) :: nVectors 
                character(C_CHAR), dimension(256) :: yyyymmdd
                type(C_PTR) :: pos
                type(C_PTR) :: vel
                integer(C_INT) :: basis
            end type orbitType

            integer, parameter :: WGS84_ORBIT = 1
            integer, parameter :: SCH_ORBIT = 2


            interface

                subroutine initOrbit_f(orb, nvec)BIND(C,NAME='initOrbit')
                    use, intrinsic :: iso_c_binding
                    import :: orbitType
                    type(orbitType) :: orb
                    integer(C_INT), value :: nvec
                end subroutine initOrbit_f

                subroutine cleanOrbit_f(orb)BIND(C,NAME='cleanOrbit')
                    use, intrinsic :: iso_c_binding
                    import :: orbitType
                    type(orbitType) :: orb
                end subroutine cleanOrbit_f

                subroutine printOrbit_f(orb)BIND(C,NAME='printOrbit')
                    use, intrinsic :: iso_c_binding
                    import :: orbitType
                    type(orbitType) :: orb
                end subroutine printOrbit_f

                subroutine getStateVector_f(orb,ind,t,pos,vel)BIND(C,NAME='getStateVector')
                    use, intrinsic :: iso_c_binding
                    import :: orbitType
                    type(orbitType) :: orb
                    integer(C_INT), value :: ind
                    real(C_DOUBLE) :: t
                    real(C_DOUBLE), dimension(3) :: pos
                    real(C_DOUBLE), dimension(3) :: vel
                end subroutine getStateVector_f

                subroutine setStateVector_f(orb,ind,t,pos,vel)BIND(C,NAME='setStateVector')
                    use, intrinsic :: iso_c_binding
                    import :: orbitType
                    type(orbitType) :: orb
                    integer(C_INT), value :: ind
                    real(C_DOUBLE), value :: t
                    real(C_DOUBLE), dimension(3) :: pos
                    real(C_DOUBLE), dimension(3) :: vel
                end subroutine setStateVector_f

                subroutine interpolateWGS84Orbit_f(orb,t,pos,vel)BIND(C,NAME='interpolateWGS84Orbit')
                    use, intrinsic :: iso_c_binding
                    import :: orbitType
                    type(orbitType) :: orb
                    real(C_DOUBLE), value :: t
                    real(C_DOUBLE), dimension(3) :: pos
                    real(C_DOUBLE), dimension(3) :: vel
                end subroutine interpolateWGS84Orbit_f

                subroutine interpolateSCHOrbit_f(orb,t,pos,vel)BIND(C,NAME='interpolateSCHOrbit')
                    use, intrinsic :: iso_c_binding
                    import :: orbitType
                    type(orbitType) :: orb
                    real(C_DOUBLE), value :: t
                    real(C_DOUBLE), dimension(3) :: pos
                    real(C_DOUBLE), dimension(3) :: vel
                end subroutine interpolateSCHOrbit_f

            end interface

            contains
                function loadFromHDR_f(filename, basis)
                    character(len=*) filename
                    character(len=256) line
                    integer :: basis
                    type(orbitType) :: loadFromHDR_f, orb
                    double precision, dimension(3) :: pos, vel
                    double precision :: t
                    integer :: nLines, i, unit

                    unit = 11
                    open(unit, file=filename)
                    nLines = 0
                    do
                        read(unit,'(a)',end=20)line
                        nLines = nLines+1
                    enddo

20                  close(unit)
                    
                    unit = 11
                    call initOrbit_f(orb, nLines)
                    unit = 11
                    open(unit, file=filename)
                    do i=1,nLines
                        read(unit,'(a)') line
                        read(line,*) t,pos(1),pos(2),pos(3),vel(1),vel(2),vel(3)
                        call setStateVector_f(orb, i-1, t, pos, vel)
                    end do
                    close(unit)
                    loadFromHDR_f = orb
                end function loadFromHDR_f

        end module orbitModule



