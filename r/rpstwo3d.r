##########################################################################
##########################################################################
#Ranked probability score for 3d fields (for tercile categories)
# function that computes Ranked probability score for two given fields 
# (observations and forecasts)
#
# Usage: rpstwo3d(data1,data2)
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
#  Output:
#
#   rps: Ranked probability score map with
#        first dimension nlon (number of longitude points) and
#        second dimension nlat (number of latitude points) 
#
# Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>
#
# Example: dim1 <- c(7,9,60,3)
#          data1 <- array(rnorm(prod(dim1)), dim1)
#          dim2 <- c(7,9,60)
#          data2 <- array(rnorm(prod(dim2)), dim2)
#          rpstwo3d(data1,data2)

rpstwo3d <- function(data1,data2) {

data1[data1 == -999.9] <- NA
nlon<-dim(data1)[1]
nlat<-dim(data1)[2]
rps<-data2[,,1]
bs1<-data2[,,1]
bs2<-data2[,,1]

# Brier score for the first and second tercile category 
#source("applyfieldclimexp.r")

.Fortran("rkeepalive",i=as.integer(0),n=as.integer(6))
thresh1<-applyfieldclimexp(data2,quantil,p=1/3)$out
binobs1<-data2
.Fortran("rkeepalive",i=as.integer(1),n=as.integer(6))
thresh2<-applyfieldclimexp(data2,quantil,p=2/3)$out
binobs2<-data2
.Fortran("rkeepalive",i=as.integer(2),n=as.integer(6))


for (i in 1:dim(data2)[3]){
  binobs1[,,i]<-(data2[,,i]<=thresh1)
  binobs2[,,i]<-(data2[,,i]<=thresh2)
}
.Fortran("rkeepalive",i=as.integer(3),n=as.integer(6))

binfcst1<-data1
binfcst2<-data1

for (i in 1:dim(data2)[3]){
     for(j in 1:dim(data1)[4]){
         binfcst1[,,i,j]<-(data1[,,i,j]<=thresh1)
         binfcst2[,,i,j]<-(data1[,,i,j]<=thresh2)
     }
}
.Fortran("rkeepalive",i=as.integer(4),n=as.integer(6))

pf1<-apply(binfcst1,c(1,2,3),mean,na.rm=TRUE)
pf2<-apply(binfcst2,c(1,2,3),mean,na.rm=TRUE)
.Fortran("rkeepalive",i=as.integer(5),n=as.integer(6))

for (i in 1:nlon){
      for(j in 1:nlat){
              bs1[i,j]<- mean((pf1[i,j,]-binobs1[i,j,])^2,na.rm = TRUE)
              bs2[i,j]<- mean((pf2[i,j,]-binobs2[i,j,])^2,na.rm = TRUE)
      }
}
.Fortran("rkeepalive",i=as.integer(6),n=as.integer(6))

rps<-(bs1+bs2)/2
rps[is.na(rps)] <- -999.99

list(rps=rps)

}
