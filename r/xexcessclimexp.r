xexcessclimexp <- function(lon,lat,array3d,fun = 'meanexcess',p=0.9,threshold = FALSE, upper=TRUE,nonmissing=0.5) {

# Compute mean excess and variance of excess for a given three-dimensional 
# array with first two space dimensions and third time dimension.
#
# Description:
#
#      Returns a matrix with the mean excess or the variance of excess for a 
#      given quantile or user defined threshold.
#
# Usage:
#
#      xexcess(array3d,fun,p=0.9,threshold = FALSE, upper=TRUE)
#
# Input:
#
#       lon: vector of longitudes
#
#       lat: vector of latitudes
#
#      array3d: three-dimensional array with p longitude points and 
#               q latitude points as the first 2 dimensions and n as the 
#               third time dimension 
#
#      fun: String containing the name of the statistics to be computed
#           that must be one of the following options "meanexcess",  
#           "stdevexcess", or "medianexcess".
#
#      p: The quantile to be computed (Default is 0.9) or a particular threshold
#         chosen by the user. If p is a threshold then the argument threshold 
#         (see below) must be set to TRUE.
#
#      threshold: Logic argument. Default is FALSE. If TRUE p must be a given 
#                 threshold value.
#
#      upper: Logic argument. Defalts is TRUE (examines upper tail of the 
#             distribution).If FALSE lower tail is examined.
#
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
#      Dag Johan Steinskog <dag.johan.steinskog@nersc.no> 14 June 2005
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 
#      Christopher Ferro <c.a.t.ferro@reading.ac.uk>
#
# Examples:
#
#      x <- seq(-20, 20, 5)
#      y <- seq(30, 60, 5)
#      dim <- c(length(x), length(y), 100)
#      data <- array(rnorm(prod(dim)), dim)
#      xexcess(data,"meanexcess")$out
#      xexcess(data,"stdevexcess")$out
#      xexcess(data,"meanexcess",p=1.5,threshold =TRUE)$out
#      xexcess(data,"meanexcess",p=1.5,threshold =TRUE,upper=FALSE)$out
#

data <- reshapefield(lon,lat,array3d)$out

# compute percentage of non-missing values at each grid point
aux <- apply(data,2,function(x)sum(!is.na(x))/(length(x)))

# identify grid points with more than 50% missing values
index <- (1:length(aux))[aux < nonmissing]

data[,index]<-NA

array3d<-reshapefield(lon,lat,as.matrix(data))$out

if(fun=="meanexcess"){
mean.excess <- function(y,p) {
if(threshold) u<- p
else u<-quantile(y,p,na.rm=T)

if(upper) mean(y[y>u]-u,na.rm=T)
else mean(y[y<u]-u,na.rm=T)

}
out<-apply(array3d,c(1,2),mean.excess,p)
out[is.na(out)]<--999.99
}

if(fun=="stdevexcess"){
stdev.excess <- function(y,p) {
if(threshold) u<- p
else u<-quantile(y,p,na.rm=T)

if(upper) sqrt(var(y[y>u]-u,na.rm=T))
else sqrt(var(y[y<u]-u,na.rm=T))

}

out<-apply(array3d,c(1,2),stdev.excess,p)
out[is.na(out)]<--999.99
}


if(fun=="medianexcess"){
median.excess <- function(y,p) {
if(threshold) u<- p
else u<-quantile(y,p,na.rm=T)

if(upper) median(y[y>u]-u,na.rm=T)
else median(y[y<u]-u,na.rm=T)

}
out<-apply(array3d,c(1,2),median.excess,p)
out[is.na(out)]<--999.99
}

invisible(list(out=out))

}

