# Computes basic statistics (e.g. mean, variance, min, max, skewness, quantile) for
# a given three-dimentional array
#
# Description:
#
#      Returns a matrix with the statistics of interest specified by the user
#      (see below the list of statistics that can be computed by this funtion).
#
# Usage:
#
#      applyfieldclimexp(lon,lat,array3d,fun, ...,nonmissing)
#
# Input:
#
#      array3d: a 3-dementional array with p longitude points and q latitude
#               points as the first 2 dimentions and n as the third time 
#               dimention 
#
#      fun: Name of the statistics to be computed
#           that must be one of the following options mean, var,
#           min, max, momentskew, ykskew or quantil, 
#           where  momentskew is a moment measure of skewness and
#           ykskew is the Yule-Kendall skewness statistics
#      
#      ...: Additional argument passed to `fun' (e.g. the quantile p to be 
#           computed). The default quantile p to be computed is 0.5 (i.e. 
#           the median).
#
#nonmissing: Only grid points with fraction given by this fraction 
#            (between 0 and 1) of non-missing values are used to compute 
#            the statistics specified in fun. Default is 0.5.
#
# Output:
#
#      $out: a matrix of the computed statistics
#
# Authors:
#
#      Dag Johan Steinskog <dag.johan.steinskog@nersc.no> 9 June 2005
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 
#
#      applyfieldclimexp(data, quantil,p=0.9)$out # computes the 90th quantile field

applyfieldclimexp <- function(lon,lat,array3d,fun = mean, ...,nonmissing=0.5) {

data <- reshapefield(lon,lat,array3d)$out

# compute percentage of non-missing values at each grid point
aux <- apply(data,2,function(x)sum(!is.na(x))/(length(x)))

# identify grid points with more than 50% missing values
index <- (1:length(aux))[aux < nonmissing]

data[,index]<-NA

array3d<-reshapefield(lon,lat,as.matrix(data))$out

out<-apply(array3d,c(1,2),fun, ...)
out[out==-Inf]<--999.99
out[out==Inf]<--999.99
out[is.na(out)]<--999.99

invisible(list(out=out))

}

momentskew <- function(z) {mean(((z-mean(z))/sd(z))^3)}

ykskew <- function(z) {q<-quantile(z) 
(q[2]-2*q[3]+q[4])/(q[4]-q[2]) }

quantil <- function(w,p=0.5) {quantile(w,p,na.rm=T)}
