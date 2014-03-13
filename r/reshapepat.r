reshapepat <- function(lon,lat,matr) {

# Reshape a p*q matrix in a two-dimensional p x q array or reshapes 
# a two-dimensional p x q array into a p*q matrix.
#
# Description:
#
#      Returns a p x q array or a (p*q) matrix
#
# Usage:
#
#      reshapepat(lon,lat,matr)
#
# Input:
#
#      matr: a p*q matrix or a p x q array with n time dimension 
#	     and p and q space dimensions
#       lon: vector of longitudes 
#       lat: vector of latitudes 
#
# Output:
#
#      $out: a p x q array or a p x q matrix
#
# Authors:
#
#      Dag Johan Steinskog <dag.johan.steinskog@nersc.no> 7 June 2005
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 
#
# Examples:
#
#      # Reshape a n x p*q matrix in a three-dimensional n x p x q array
#      x <- array(1:4)
#      lon <- seq(50,70,20)
#      lat <- seq(-10,10,20)
#      reshapepat(lon,lat,x)$out
#
#      # Reshape a three-dimensional n x p x q array in a n x p*q matrix
#      y <- array(1:4,dim=c(2,2))
#      lon <- seq(50,70,20)
#      lat <- seq(-10,10,20)
#      reshapepat(lon,lat,y)$out


if (length(dim(matr))==1) {
dims <- dim(matr)
spacedim <- dims[1]

if(spacedim != length(lat)*length(lon)) stop("Incompatible dimensions")

out<-array(t(matr),c(length(lon),length(lat)))
}

if (length(dim(matr))==2) {
dims <- dim(matr)
p <- dims[1]
q <- dims[2]

if(p*q != length(lat)*length(lon)) stop("Incompatible dimensions")

out <- t(array(as.vector(matr),c(p*q)))}

invisible(list(out=out))

}
