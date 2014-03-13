#ROC AREA
##########################################################################
##########################################################################
#Computes ROC area for 3d fields
# function that computes ROC area for two given fields (observations
# and forecasts)
#
# Usage: rocareatwo3d(data1,data2,u,threshold)
#
# Inputs:
#
# data1: 4d array of ensemble forecasts with 
#        first dimension nlon (number of longitude points)
#        second dimension nlat (number of latitude points)
#        third dimension n (number of time slices) and
#        forth dimension m (number of members of the ensemble)
#
# data2: 3d array with the observed values with
#        first dimension nlon (number of longitude points)
#        second dimension nlat (number of latitude points) and
#        third dimension n (number of time slices) and
#
#     u: threshold for which the probabilities will be computed     
#
#    threshold: Logical. If TRUE (Default) uses the value u as threshold, if
#               FALSE u should have the value of the quantile to be computed
#               (e.g. 50 for the median, 90 for the 90th quantile, etc...)
#  Output:
#
#    ra: ROC area map with
#        first dimension nlon (number of longitude points) and
#        second dimension nlat (number of latitude points) 
#
# Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>
#
# Example: dim1 <- c(7,9,60,3)
#          data1 <- array(rnorm(prod(dim1)), dim1)
#          dim2 <- c(7,9,60)
#          data2 <- array(rnorm(prod(dim2)), dim2)
#          rocareatwo3d(data1,data2,0)
#          rocareatwo3d(data1,data2,0,threshold=TRUE)

rocareatwo3d <- function(data1,data2,u,threshold=TRUE) {
data1[data1 == -999.9] <- NA
nlon<-dim(data2)[1]
nlat<-dim(data2)[2]
ra<-data2[,,1]

.Fortran("rkeepalive",i=as.integer(0),n=as.integer(2))
if(threshold) {

binobs<- (data2<= u)
pf <- apply( data1<= u, c(1,2,3), mean,na.rm=TRUE)

} # end of if

else{

#source("applyfieldclimexp.r")
thresh<-applyfieldclimexp(data2,quantil,p=u/100)$out
binobs<-data2
for (i in 1:dim(data2)[3]){
  binobs[,,i]<-(data2[,,i]<=thresh)
}
.Fortran("rkeepalive",i=as.integer(1),n=as.integer(2))

binfcst<-data1
for (i in 1:dim(data2)[3]){
     for(j in 1:dim(data1)[4]){
         binfcst[,,i,j]<-(data1[,,i,j]<=thresh)
     }
}
.Fortran("rkeepalive",i=as.integer(2),n=as.integer(2))

pf<-apply(binfcst,c(1,2,3),mean,na.rm=TRUE)

} #end of else

library(verification)
for (i in 1:nlon){
.Fortran("rkeepalive",i=as.integer(i),n=as.integer(nlon))
      for(j in 1:nlat){    
      index <- !(is.na(pf[i,j,]) | is.na(binobs[i,j,]))
      ra[i,j]<-roc.area(binobs[i,j,index],pf[i,j,index])$A.tild
      }
}
ra[is.na(ra)] <- -999.99
list(ra=ra)
}
