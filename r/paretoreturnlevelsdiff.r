paretoreturnlevelsdiff <- function(lon,lat,array3d,pat2d,p=0.9,upper=TRUE,nonmissing=0.5) {

# Description:
#
# Compute return levels of Generalized Pareto Distribution for
# a given three-dimensional array with first two space dimensions and third
# time dimension, corresponding to the values in the 2D array pat.
#
# based on paretoreturnlevels, which is based on xpareto
#
# Usage:
#
#      paretoreturnlevelsdiff(lon,lat,array3d,pat2d,p=0.9,upper=TRUE,nonmissing)
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
#      pat2d: two-dimensional array, assumed (but not yet checked!) to be
#             on the same lat-lon grid as array3d
#
#      p:     quantile to be computed (Default is 0.9). 
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
#      $out: an array of the computed statistics. First dimension contains
#            the estimated parameters. (e.g. $out[1,,] is the scale parameter
#            and $out[2,,] is the shape parameter). Second and third dimensions
#            are the same space dimensions as of array3d. 
#
#
# Authors:
#
#      Dag Johan Steinskog <dag.johan.steinskog@nersc.no> 16 June 2005
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 
#      Christopher Ferro <c.a.t.ferro@reading.ac.uk>
#
# Examples:
#
#  (to be done)
#

# very simple error chacking

stopifnot(dim(array3d$data)[1] == dim(pat2d$data)[1], 
          dim(array3d$data)[2] == dim(pat2d$data)[2])

print(c("p = ",p))

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

out<-matrix(ncol=dims[2],nrow=dims[1])
for (i in 1:dims[1]){
.Fortran("rkeepalive",i=as.integer(i),n=as.integer(dims[1]))
for (j in 1:dims[2]){

if ( upper) {
  q <- quantile(array3d[i,j,],p,na.rm=T)
  z <- pat2d[i,j] - q
} else {
  q <- quantile(-array3d[i,j,],p,na.rm=T)
  if ( is.na(q) ) {
    z <- NA
  } else if ( q == 0 ) {
    z <- NA
  } else {
    z <- -(pat2d[i,j] + q)
  }
}
print(c("pat2d[",i,j,"] = ",pat2d[i,j],", q = ",q,", z = ",z))

if ( z < 0 ) {
  # the value is smaller than the threshold, so just look up it up in the 
  # distribution.  This part of the code has not yet been checked.
  if ( upper ) {
    F <- ecdf(array3d[i,j,])
    out[i,j] <- 1/(1-F(pat2d[i,j]))
  } else {
    F <- ecdf(array3d[i,j,])
    out[i,j] <- 1/F(pat2d[i,j])
  }
} else {
  x <- 1 + z*aux[2,i,j]/aux[1,i,j]
  if ( x > 0.000001 ) {
    # this assumes xi is not too small...
    out[i,j] <- x^(1/aux[2,i,j])
  } else {
    out[i,j] <- NA
  }
out[i,j] = out[i,j]/(1-p)
}

###if ( out[i,j] > 99 && out[i,j] < 101 ) { 
###  out[i,j] <- out[i,j]
###} else {
###  print(c("Curious value for out[",i,j,"]: ",out[i,j]))
###  print(c("sigma,xi = ",aux[1,i,j],aux[2,i,j]))
###  print(c("pat2d,z = ",pat2d[i,j],z))
###  print(c("x = ",x))
###}

# end loops over i,j
}
}

out[is.na(out)]<--999.99
invisible(list(out=out))

}
