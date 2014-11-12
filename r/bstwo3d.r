##########################################################################
##########################################################################
#Brier score for 3d fields
# function that computes Brier score for two given fields (observations
# and forecasts)
#
# Usage: bstwo3d(data1,data2,nbins,u,threshold)
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
# nbins: number of bins used to compute the Brier score
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
# Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>
#
# Example: dim1 <- c(7,9,60,3)
#          data1 <- array(rnorm(prod(dim1)), dim1)
#          dim2 <- c(7,9,60)
#          data2 <- array(rnorm(prod(dim2)), dim2)
#          bstwo3d(data1,data2,nbins=10,u=0)
#          bstwo3d(data1,data2,nbins=10,u=50,threshold=FALSE)

bstwo3d <- function(data1,data2,nbins,u,threshold=TRUE) {
    data1[data1 == -999.9] <- NA
    data2[data2 == -999.9] <- NA

    if (threshold)
        thresh <- u
    else # The threshold depends on the lon and lat indexes
        thresh <- applyfieldclimexp(data2,quantil,p=u/100.0)$out

    p       <- data1
    y       <- data2
    ntime   <- dim(data1)[3]
    nmember <- dim(data1)[4]
    for(i in 1:ntime){
        for (j in 1:nmember) p[,,i,j] <- ( data1[,,i,j] <= thresh )
        y[,,i] <- ( data2[,,i] <= thresh )
    }
    p <- apply(p,1:3,mean,na.rm=TRUE)

    bs   <- data2[,,1]
    rel  <- data2[,,1]
    res  <- data2[,,1]
    unc  <- data2[,,1]

    nlon <- dim(data1)[1]
    nlat <- dim(data1)[2]
    for (i in 1:nlon) {
        .Fortran("rkeepalive",i=as.integer(i),n=as.integer(nlon))
        for (j in 1:nlat) {
            terms <- SpecsVerification::BrierScoreDecomposition(
                p=p[i,j,],y=y[i,j,],calibration=list(method="bin",bins=((0:nbins)/nbins)) )
            bs [i,j] <- sum(terms)
            rel[i,j] <- terms[1]
            res[i,j] <- terms[2]
            unc[i,j] <- terms[3]
        }
    }

    bs [is.na(bs )] <- -999.99
    rel[is.na(rel)] <- -999.99
    res[is.na(res)] <- -999.99
    unc[is.na(unc)] <- -999.99

    list(bs=bs,rel=rel,res=res,unc=unc)
}
