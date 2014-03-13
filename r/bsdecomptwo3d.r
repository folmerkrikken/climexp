#BRIER SCORE DECOMPOSITION

##########################################################################
##########################################################################
#Brier score decomposition for 3d fields
# function that computes Brier score decomposition for two given fields (observations
# and forecasts)
#
# Usage: bsdecomptwo3d(data1,data2,u,threshold)
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
#    bs: Brier score map with
#        first dimension nlon (number of longitude points) and
#        second dimension nlat (number of latitude points) 
#
#   rel: Map of reliability component of the Brier score
#
#   res: Map of resolution component of the Brier score
#
#   unc: Map of uncertainty component of the Brier score
#
# Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>
#
# Example: dim1 <- c(7,9,60,3)
#          data1 <- array(rnorm(prod(dim1)), dim1)
#          dim2 <- c(7,9,60)
#          data2 <- array(rnorm(prod(dim2)), dim2)
#          bsdecomptwo3d(data1,data2,0)
#          bsdecomptwo3d(data1,data2,u=50,threshold=FALSE)


bsdecomptwo3d <- function(data1,data2,u,threshold=TRUE) {
data1[data1 == -999.9] <- NA
nlon<-dim(data1)[1]
nlat<-dim(data1)[2]
bs<-data2[,,1]
rel<-data2[,,1]
res<-data2[,,1]
unc<-data2[,,1]
bsnew<-data2[,,1]

if(threshold) {

binobs<- (data2<= u)
pf <- apply( data1<= u, c(1,2,3), mean,na.rm=TRUE)
} # end of if

else{

#source("applyfieldclimexp.r")
thresh<-applyfieldclimexp(data2,quantil,p=u/100)$out
.Fortran("rkeepalive",i=as.integer(1),n=as.integer(2))
binobs<-data2
for (i in 1:dim(data2)[3]){
  binobs[,,i]<-(data2[,,i]<=thresh)
}

.Fortran("rkeepalive",i=as.integer(2),n=as.integer(2))

binfcst<-data1
for (i in 1:dim(data2)[3]){
     for(j in 1:dim(data1)[4]){
         binfcst[,,i,j]<-(data1[,,i,j]<=thresh)
     }
}

pf<-apply(binfcst,c(1,2,3),mean,na.rm=TRUE)

} #end of else

for (i in 1:nlon){
.Fortran("rkeepalive",i=as.integer(i),n=as.integer(nlon))
      for(j in 1:nlat){
              bs[i,j]<- mean((pf[i,j,]-binobs[i,j,])^2,na.rm = TRUE)

              index <- !(is.na(pf[i,j,]) | is.na(binobs[i,j,]))
              
	      probfcsts <- pf[i,j,index]
	      binobsaux <- binobs[i,j,index]
	      
              obar <- mean(binobsaux)
              n<-length(probfcsts)                                            
              h<-hist(probfcsts,breaks=seq(0,1,0.1),plot=F)$counts
              g<-hist(probfcsts[binobsaux==1],breaks=seq(0,1,0.1),plot=F)$counts 
              obari <- g/h                                                   
              obari[is.na(obari)]<-0
              # Computes reliability,resolution and uncertainty components
              # of the Brier score 
              yi <- seq(0.05,0.95,0.1)
              rel[i,j] <- sum(h*((yi-obari)^2),na.rm = TRUE)/n
              res[i,j] <- sum(h*((obari-obar)^2),na.rm = TRUE)/n
              unc[i,j]<-obar*(1-obar)
              bsnew[i,j]<-rel[i,j]-res[i,j]+unc[i,j]
      }
}
bs[is.na(bs)] <- -999.99
bsnew[is.na(bsnew)] <- -999.99
rel[is.na(rel)] <- -999.99
res[is.na(res)] <- -999.99
unc[is.na(unc)] <- -999.99
list(bs=bs,bsnew=bsnew,rel=rel,res=res,unc=unc)


}
