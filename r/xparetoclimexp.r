xparetoclimexp <- function(lon,lat,array3d,p=0.9,upper=TRUE,nonmissing=0.5) {

# Compute shape and scale parameters of a Generalized Pareto Distribution for
# a given three-dimensional array with first two space dimensions and third
# time dimension.
#
# Description:
#
#      Returns an array with the shape and scale parameters of a Generalized 
#      Pareto Distribution for the exceedances above a given quantile that
#      defines the threshold. 
#
# Usage:
#
#      xpareto(lon,lat,array3d,p=0.9, upper=TRUE,nonmissing)
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
#      x <- seq(-20, 20, 5)
#      y <- seq(30, 60, 5)
#      dim <- c(length(x), length(y), 1000)
#      data <- array(rnorm(prod(dim)), dim)
#      xpareto(data)
#      xpareto(data,p=0.95)
#      xpareto(data,p=0.1,upper=FALSE)
#


data <- reshapefield(lon,lat,array3d)$out

# compute percentage of non-missing values at each grid point
aux <- apply(data,2,function(x)sum(!is.na(x))/(length(x)))

# identify grid points with more than 50% missing values
index <- (1:length(aux))[aux < nonmissing]

data[,index]<-NA

array3d<-reshapefield(lon,lat,as.matrix(data))$out


estim.par <- function(y,p,upper) {
  print (c("xparetoclimexp, p=",p,", upper=",upper))
  print(c("y = ",y))
  if ( all(is.na(y)) ) {
    return(c(NA,NA))
  }
  if ( upper ) {
    f <- fpot(y, quantile(y, p, na.rm=T), "gpd", std.err = FALSE)$est
    print(c("p=",p,", f = ",f))
    print(y)
    f
  } else {
    q <- quantile(-y, p,na.rm=T)
    r <- range(-y,na.rm=T)
    if ( q == r[2] ) {
      q <- r[2] - 0.00001*(r[2]-r[1])
    }
    fpot(-y, q, "gpd", std.err = FALSE)$est
  }
}

out<-apply(array3d,c(1,2),estim.par,p,upper)
out[is.na(out)]<--999.99
invisible(list(out=out))

}
