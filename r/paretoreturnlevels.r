paretoreturnlevels <- function(lon,lat,array3d,p=0.9,rt=10,upper=TRUE,nonmissing=0.5) {

# Description:
#
# Compute return levels of Generalized Pareto Distribution for
# a given three-dimensional array with first two space dimensions and third
# time dimension.
#
# Usage:
#
#      paretoreturnlevels(lon,lat,array3d,p=0.9,rt=10,upper=TRUE,nonmissing)
#
# Input:
#
#      lon: vector of longitudes
#
#      lat: vector of latitudes
#
#      array3d: three-dimensional array with p longitude points and q latitude
#               points as the first 2 dimensions and n as the third time 
#               dimension 
#
#      p:     threshold to define peaks over (Default is 0.9). 
#
#      rt:    the return time (Default is 10 years).
#
#      upper: Logic argument. Default is TRUE (examines upper tail of the 
#             distribution). If FALSE lower tail is examined.
#
#nonmissing: Only grid points with fraction given by this fraction 
#            (between 0 and 1) of non-missing values are used to compute 
#            the statistics specified in fun. Default is 0.5.
#
# Output:
#
#      $out: an array of the computed return levels.
#
#
# Authors:
#
#      Dag Johan Steinskog <dag.johan.steinskog@nersc.no> 16 June 2005
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 
#      Christopher Ferro <c.a.t.ferro@reading.ac.uk>
#      Geert Jan van Oldenborgh <oldenborgh@knmi.nl>
#
# Examples:
#
# (to be added)
#
if ( p >= 1-1/rt ) {
  out = apply(array3d,c(1,2),quantile,p,na.rm=T)
} else {

data <- reshapefield(lon,lat,array3d)$out

# compute percentage of non-missing values at each grid point
aux <- apply(data,2,function(x)sum(!is.na(x))/(length(x)))

.Fortran("rkeepalive",i=as.integer(1),n=as.integer(4))

# identify grid points with more than 50% missing values
index <- (1:length(aux))[aux < nonmissing]

data[,index]<-NA

array3d<-reshapefield(lon,lat,as.matrix(data))$out

.Fortran("rkeepalive",i=as.integer(2),n=as.integer(4))

estim.par <- function(y,p) {

  if ( all(is.na(y)) ) {
    return(c(NA,NA))
  }
  r <- range(y, na.rm=T)
  if ( r[1] == r[2] ) {
    return(c(NA,NA))
  }
  if( upper ) {
    q <- quantile(y, p, na.rm=T)
    if ( q == r[2] ) {
      q <- r[2] - 0.00001*(r[2] - r[1])
    } 
    fpot(y, q, "gpd", std.err = FALSE)$est
  } else {
    q <- quantile(-y, p, na.rm=T)
    r <- range(-y,na.rm=T)
    if ( q == r[2] ) {
      q <- r[2] - 0.00001*(r[2]-r[1])
    }
    fpot(-y, q, "gpd", std.err = FALSE)$est
  }
}

aux<-apply(array3d,c(1,2),estim.par,p)

.Fortran("rkeepalive",i=as.integer(3),n=as.integer(4))

dims<-dim(array3d)

# GJvO bug fix: the return period is defined for the whole distrubution, not the 
# part above the threshold.
t <- (1-p)*rt
out<-matrix(ncol=dims[2],nrow=dims[1])
for (i in 1:dims[1]){
.Fortran("rkeepalive",i=as.integer(i),n=as.integer(dims[1]))
for (j in 1:dims[2]){
val <- aux[1,i,j]/aux[2,i,j]*(((t)^aux[2,i,j])-1)
if ( upper ) {
  out[i,j] <- quantile(array3d[i,j,],p,na.rm=T) + val
} else {
  q <- quantile(-array3d[i,j,],p,na.rm=T)
  if ( is.na(q) ) {
    out[i,j] = NA
  } else if ( q == 0 ) {
    out[i,j] <- 0
  } else {
    out[i,j] <- -(q+val)
  }
}
}
}
}
out[is.na(out)]<--999.99
invisible(list(out=out))

}
