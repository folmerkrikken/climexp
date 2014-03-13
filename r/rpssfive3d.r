##########################################################################
##########################################################################
#Ranked probability skill score for 3d fields (for five categories)
# function that computes Ranked probability score for two given fields 
# (observations and forecasts) with respect to climatology
#
# Usage: rpssfive3d(data1,data2)
#
# Inputs:
#
# data1: 4d array of ensemble forecasts with 
#        first dimension nlon (number of longitude points)
#        second dimension nlat (number of latitude points)
#        third dimension n (number of time slices) and
#        fourth dimension m (number of members of the ensemble)
#
# data2: 3d array with the observed values with
#        first dimension nlon (number of longitude points)
#        second dimension nlat (number of latitude points) and
#        third dimension n (number of time slices) and
#
#  Output:
#
#   rpss: Ranked probability skill score map with
#        first dimension nlon (number of longitude points) and
#        second dimension nlat (number of latitude points) 
#
# Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>
#
# Example: dim1 <- c(7,9,60,3)
#          data1 <- array(rnorm(prod(dim1)), dim1)
#          dim2 <- c(7,9,60)
#          data2 <- array(rnorm(prod(dim2)), dim2)
#          rpssfive3d(data1,data2)

rpssfive3d <- function(data1,data2) {

nlon<-dim(data1)[1]
nlat<-dim(data1)[2]
rps<-data2[,,1]
rpss<-data2[,,1]
bs1<-data2[,,1]
bs2<-data2[,,1]
bs3<-data2[,,1]
bs4<-data2[,,1]
bsclim1<-data2[,,1]
bsclim2<-data2[,,1]
bsclim3<-data2[,,1]
bsclim4<-data2[,,1]

# Brier score for the first to fourth category 
#source("applyfieldclimexp.r")

.Fortran("rkeepalive",i=as.integer(0),n=as.integer(11))
thresh1<-applyfieldclimexp(data2,quantil,p=1/5)$out
binobs1<-data2
.Fortran("rkeepalive",i=as.integer(1),n=as.integer(11))
thresh2<-applyfieldclimexp(data2,quantil,p=2/5)$out
binobs2<-data2
.Fortran("rkeepalive",i=as.integer(2),n=as.integer(11))
thresh3<-applyfieldclimexp(data2,quantil,p=3/5)$out
binobs3<-data2
.Fortran("rkeepalive",i=as.integer(3),n=as.integer(11))
thresh4<-applyfieldclimexp(data2,quantil,p=4/5)$out
binobs4<-data2
.Fortran("rkeepalive",i=as.integer(4),n=as.integer(11))

#threshobs == thresholds defined from observations

# Brier score for the first to fourth category 
#source("applyfieldclimexp.r")


for (i in 1:dim(data2)[3]){
    binobs1[,,i]<-(data2[,,i]<=thresh1)
    binobs2[,,i]<-(data2[,,i]<=thresh2)
    binobs3[,,i]<-(data2[,,i]<=thresh3)
    binobs4[,,i]<-(data2[,,i]<=thresh4)

}

.Fortran("rkeepalive",i=as.integer(5),n=as.integer(11))
binfcst1<-data1
.Fortran("rkeepalive",i=as.integer(5),n=as.integer(11))
binfcst2<-data1
.Fortran("rkeepalive",i=as.integer(5),n=as.integer(11))
binfcst3<-data1
.Fortran("rkeepalive",i=as.integer(5),n=as.integer(11))
binfcst4<-data1


for (i in 1:dim(data2)[3]){
.Fortran("rkeepalive",i=as.integer(i),n=as.integer(dim(data2)[3]))
     for(j in 1:dim(data1)[4]){
         binfcst1[,,i,j]<-(data1[,,i,j] <=thresh1)
         binfcst2[,,i,j]<-(data1[,,i,j] <=thresh2)
	 binfcst3[,,i,j]<-(data1[,,i,j] <=thresh3)
	 binfcst4[,,i,j]<-(data1[,,i,j] <=thresh4)
     }
}

.Fortran("rkeepalive",i=as.integer(6),n=as.integer(11))
pf1<-apply(binfcst1,c(1,2,3),mean,na.rm=TRUE)
.Fortran("rkeepalive",i=as.integer(7),n=as.integer(11))
pf2<-apply(binfcst2,c(1,2,3),mean,na.rm=TRUE)
.Fortran("rkeepalive",i=as.integer(8),n=as.integer(11))
pf3<-apply(binfcst3,c(1,2,3),mean,na.rm=TRUE)
.Fortran("rkeepalive",i=as.integer(9),n=as.integer(11))
pf4<-apply(binfcst4,c(1,2,3),mean,na.rm=TRUE)


.Fortran("rkeepalive",i=as.integer(10),n=as.integer(11))

for (i in 1:nlon){
.Fortran("rkeepalive",i=as.integer(i),n=as.integer(nlon))
      for(j in 1:nlat){
              bs1[i,j]<- mean((pf1[i,j,]-binobs1[i,j,])^2,na.rm = TRUE)
              bs2[i,j]<- mean((pf2[i,j,]-binobs2[i,j,])^2,na.rm = TRUE)
	      bs3[i,j]<- mean((pf3[i,j,]-binobs3[i,j,])^2,na.rm = TRUE)
	      bs4[i,j]<- mean((pf4[i,j,]-binobs4[i,j,])^2,na.rm = TRUE)
              bsclim1[i,j]<- mean(((1/5)-binobs1[i,j,])^2,na.rm = TRUE)
              bsclim2[i,j]<- mean(((2/5)-binobs2[i,j,])^2,na.rm = TRUE)
	      bsclim3[i,j]<- mean(((3/5)-binobs3[i,j,])^2,na.rm = TRUE)
	      bsclim4[i,j]<- mean(((4/5)-binobs4[i,j,])^2,na.rm = TRUE)

      }
}
.Fortran("rkeepalive",i=as.integer(11),n=as.integer(11))

rps<-bs1+bs2+bs3+bs4
rpsclim<-bsclim1+bsclim2+bsclim3+bsclim4

# bias correction from Andraes Weigel's paper
M <- dim(data1)[4]
k <- 5
d <- (k*k - 1)/(6*k)/M

rpss <- 1- rps/(rpsclim+d)
rpss[rpss<=-1] <- -999.99
rpss[rpss>=1]  <- 1
rpss[is.na(rpss)] <- -999.99

list(rpss=rpss)

}
