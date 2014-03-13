xdependenceclimexp <- function(lon,lat,array3d,ts,u,fun,upper=T,nonmissing=0.5) {

# Compute extreme dependence measures between a given three-dimensional array
# with first two space dimensions (e.g. longitude and latitude) and third
# time dimension, and a given time series with the same length as the time
# dimension of the three dimensional array
#
# Note: This function allows the user to specify through the parameter
#       nonmissing (defaul is 0.5) the acceptable percentage of nonmissing
#       values in the time series of each grid point of the three-dimensional
#       array. This is the main difference between this function and
#       xdependence.r
#
# Description:
#
#      Returns a map (matrix) of the extreme dependence measures described in
#      Coles et al. (1999) and in section 8.4 of Coles (2001)
#
# Usage:
#
#      xdependence1(lon,lat,array3d,ts,u,fun,nonmissing)
#
# Input:
#
#          lon: vector with p longitude values
#   
#          lat: vector with q latitude values 
#
#      array3d: three-dimensional array with p longitude points and q latitude
#               points as the first two dimensions and n as the third time 
#               dimension 
#
#          ts: time series of data with the same length as the time dimension
#              of array3d for which extreme dependence with each grid point of
#              array3d will be computed
#
#           u: high threshold between 0 and 1 that will define the extreme 
#              level to compute dependence. Must be a high quantile (e.g. 0.95)
#
#         fun: String of characters that defines which extreme dependence 
#              measure is computed (e.g. "chi", "chibar" or "chicount").
#              If fun is "chi", computes chi(u) as in Eq.(3.2) of 
#              Coles et al. 1999 and in section 8.4 of Coles (2001). 
#              If fun is "chibar", computes chibar(u) as in section 3.3.2 of 
#              Coles et al. 1999 and in section 8.4 of Coles (2001).
#              If fun is "chicount", computes the conditional probability of
#              each grid point variable of array3d to be large (above a large 
#              threshold u) conditional on (given that) the variable ts is 
#              also large (with value above the same large threshold u)
#              by counting values above threshold and computing relative 
#              frequencies    
#
#nonmissing: Only grid points with fraction given by this fraction 
#            (between 0 and 1) of non-missing values are used to compute 
#            the statistics specified in fun. Default is 0.5.
#          
# Output:
#
#      $out: an map (matrix) of the extreme dependence measure for each grid
#            point of array3d. 
#
# Authors:
#
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 21 Dec 2005
#      Christopher Ferro <c.a.t.ferro@reading.ac.uk>
#
# References: Coles, S., Heffernan, J., and Tawn, J., 1999: Dependence measures
#             of extreme value analyses. Extremes 2:4, 339-365.
#
#             Coles, S., 2001: An introduction to statistical modeling of 
#             extreme values. Spring series in statistics. 208pp.
#
# Examples:
#
#      x <- seq(-20, 20, 5)
#      y <- seq(30, 60, 5)
#      dim <- c(length(x), length(y), 1000)
#      data <- array(rnorm(prod(dim)), dim)
#      xdependence1(x,y,data,data[4,5,],u=0.95,fun="chi")$out
#      xdependence1(x,y,data,data[4,5,],u=0.95,fun="chibar")$out
#      xdependence1(x,y,data,data[4,5,],u=0.95,fun="chicount")$out


if (all(is.na(ts))) stop("all missing values for ts")


if(upper){
data <- reshapefield(lon,lat,array3d)$out
}
if(!upper){
data <- reshapefield(lon,lat,-array3d)$out
array3d<--array3d
ts<--ts
u<-1-u
}

# compute percentage of non-missing values at each grid point
aux <- apply(data,2,function(x)sum(!is.na(x))/(length(x)))

# identify grid points with more than 50% missing values
index <- (1:length(aux))[aux < nonmissing]

data[,index]<-NA

array3d<-reshapefield(lon,lat,as.matrix(data))$out
out1<-aperm(apply(array3d,c(1,2),rank, na.last = "keep"),c(2,3,1))
aux<-apply(array3d,c(1,2),function(x)sum(!is.na(x)))
aux1<-array(NA,c(dim(out1)))

for (i in 1:(dim(array3d)[3])){
aux1[,,i] <- out1[,,i]/aux
}

if (fun == "chi"){
ts<-rank(ts, na.last = "keep")/sum(!is.na(ts))
chi <- function(y){
index <- !(is.na(y) | is.na(ts))
if(sum(index)==0) return(NA)
2-(log((sum(ts[index]<=u & y[index]<=u)+0.5)/(length(ts[index])+1))/(log((sum(ts[index]<=u)+0.5)/(length(ts[index])+1))))
}
out<-apply(aux1,c(1,2),chi)
out[out<0]<-0
out[is.na(out)]<--999.99
}

if (fun == "chibar"){
ts<-rank(ts, na.last = "keep")/sum(!is.na(ts))
chibar <- function(y){
index <- !(is.na(y) | is.na(ts))
if(sum(index)==0) return(NA)
((2*log((sum(ts[index]>=u)+0.5)/(length(ts[index])+1)))/log((sum(ts[index]>=u & y[index]>=u)+0.5)/(length(ts[index])+1)))-1
}
out<-apply(aux1,c(1,2),chibar)
out[is.na(out)]<--999.99
}

if (fun == "chicount"){
chicount <- function(y){
index <- !(is.na(y) | is.na(ts))
if(sum(index)==0) return(NA)
length(y[index][ts[index]>=quantile(ts[index],u)][y[index][ts[index]>=quantile(ts[index],u)]>=quantile(y[index],u)])/length(y[index][ts[index]>=quantile(ts[index],u)])
}
out<-apply(array3d,c(1,2),chicount)
out[is.na(out)]<--999.99
}

invisible(list(out=out))
}

