	program null
*
*	make null.dat for map-drwaing GrADS script...
*
	implicit none
#include "recfac.inc"
	open(1,file='null.dat',access='direct',recl=4*recfa4)
	write(1,rec=1) 0.001,0.002,0.003,0.004
	close(1)
	end
