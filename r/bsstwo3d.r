##########################################################################
##########################################################################
#Brier score for 3d fields
# function that computes Brier skill score for two given fields (observations
# and forecasts) with respect to climatology
#
# Usage: bsstwo3d(data1,data2,u,threshold)
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
#     u: threshold for which the Brier score will be computed     
#
#    threshold: Logical. If TRUE (Default) uses the value u as threshold, if
#               FALSE u should have the value of the quantile to be computed
#               (e.g. 50 for the median, 90 for the 90th quantile, etc...)
#
#  Output:
#
#    bss: Brier skill score map with
#        first dimension nlon (number of longitude points) and
#        second dimension nlat (number of latitude points) 
#
# Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>
#
# Example: dim1 <- c(7,9,60,3)
#          data1 <- array(rnorm(prod(dim1)), dim1)
#          dim2 <- c(7,9,60)
#          data2 <- array(rnorm(prod(dim2)), dim2)
#          bsstwo3d(data1,data2,u=50,threshold=FALSE)

bsstwo3d <- function(data1,data2,u,threshold=TRUE) {
data1[data1 == -999.9] <- NA
nlon<-dim(data1)[1]
nlat<-dim(data1)[2]
bs<-data2[,,1]
bsclim<-data2[,,1]

if(threshold) {
u<- u
binobs<- (data2<= u)
pf <- apply( data1<= u, c(1,2,3), mean,na.rm = TRUE)
} #end if

else{

#source("applyfieldclimexp.r")
thresh<-applyfieldclimexp(data2,quantil,p=u/100)$out
.Fortran("rkeepalive",i=as.integer(0),n=as.integer(3))

binobs<-data2
for (i in 1:dim(data2)[3]){
  binobs[,,i]<-(data2[,,i]<=thresh)
}

.Fortran("rkeepalive",i=as.integer(1),n=as.integer(3))

binfcst<-data1
for (i in 1:dim(data2)[3]){
     for(j in 1:dim(data1)[4]){
         binfcst[,,i,j]<-(data1[,,i,j]<=thresh)
     }
}

.Fortran("rkeepalive",i=as.integer(2),n=as.integer(3))

pf<-apply(binfcst,c(1,2,3),mean,na.rm=TRUE)

} #end else

climfreq<-apply(binobs,c(1,2),mean,na.rm=T)

for (i in 1:nlon){
      for(j in 1:nlat){
              bs[i,j]<- mean((pf[i,j,]-binobs[i,j,])^2,na.rm = TRUE)
              bsclim[i,j]<- mean((climfreq[i,j]-binobs[i,j,])^2,na.rm = TRUE)
      }
}
.Fortran("rkeepalive",i=as.integer(3),n=as.integer(3))

# bias correction term as in Weigel et al (MWR, 2006) or Chris Ferror's paper
if ( threshold ) {
# absolute threshold
  p = apply(binobs, 3, mean,na.rm = TRUE)
} else {
# percentile threshold - easy
  p = u/100
}
M <- dim(data1)[4]
d <- p*(1-p)/M

# compute BSS
bss <- 1 - bs/(bsclim+d)
bss[bss<=-1]<--1
bss[bss>=1]<-1
bss[is.na(bss)] <- -999.99

list(bss=bss)

}
