reshapefield <- function(lon,lat,matr) {

# Reshape a n x p*q matrix in a three-dimensional n x p x q array or reshapes 
# a three-dimensional n x p x q array into a n x p*q matrix.
#
# Description:
#
#      Returns a n x p x q array or a n x (p*q) matrix
#
# Usage:
#
#      reshapefield(lon,lat,matr)
#
# Input:
#
#      matr: a n x p*q matrix or a n x p x q array with n time dimension 
#	     and p and q space dimensions
#       lon: vector of longitudes 
#       lat: vector of latitudes 
#
# Output:
#
#      $out: a n x p x q array or a n x p x q matrix
#
# Authors:
#
#      Dag Johan Steinskog <dag.johan.steinskog@nersc.no> 7 June 2005
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 
#
# Examples:
#
#      # Reshape a n x p*q matrix in a three-dimensional n x p x q array
#      x <- array(1:8,dim=c(2,4))
#      lon <- seq(50,70,20)
#      lat <- seq(-10,10,20)
#      reshapefield(lon,lat,x)$out
#
#      # Reshape a three-dimensional n x p x q array in a n x p*q matrix
#      y <- array(1:8,dim=c(2,2,2))
#      lon <- seq(50,70,20)
#      lat <- seq(-10,10,20)
#      reshapefield(lon,lat,y)$out


if (length(dim(matr))==2) {
dims <- dim(matr)
n <- dims[1]
spacedim <- dims[2]

if(spacedim != length(lat)*length(lon)) stop("Incompatible dimensions")

out<-array(t(matr),c(length(lon),length(lat),n))
}

if (length(dim(matr))==3) {
dims <- dim(matr)
n <- dims[3]
p <- dims[1]
q <- dims[2]

if(p*q != length(lat)*length(lon)) stop("Incompatible dimensions")

out <- t(array(as.vector(matr),c(p*q,n)))}
invisible(list(out=out))

}
