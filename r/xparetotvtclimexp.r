xparetotvtclimexp <- function(lon,lat,array3d,p=0.9,upper=T,nonmissing=0.5) {

# Fit Generalized Pareto distribution with time-varying threshold at each grid 
# point for a given three-dimensional array of montly data with first two space 
# dimensions (e.g. longitude and latitude) and third time dimension. 
#
# Description:
#
#      Returns maps of fitted parameters (constant scale and
#      constant shape), the time varying threshold, the mean
#      of excesses above the time varying threshold, the median
#      of excesses above the time varying threshold, the st. dev
#      of excesses above the time varying threshold.
#      
# Usage:
#
#      xparetotvtclimexp(lon,lat,array3d,p,upper,nonmissing)
#
# Input:
#
#       lon: vector with p longitude values
#
#       lat: vector with q latitude values 
# 
#   array3d: a three-dimensional array of monthly data with p longitude points
#            and q latitude points as the first two dimensions and n as the
#            third time dimension 
#
#         p: a value between 0 and 1 that informs the percentage of point
#            that will be left below the time-varying threshold 
#
#nonmissing: Only grid points with fraction given by 'nonmissing' 
#            (between 0 and 1) of non-missing values are used to estimate the
#            Generalized Pareto distribution parameters. Default is 0.5.
#
# Output:
#
#     $output: 2 x p x q array with scale (first level of the array) and
#              shape (second level of the array) parameters
# 
#         $th: p x q x n' array containing the time varying threshold, where
#              n' is the number of months considered when computing the
#              time-varying threshold
#
#$meanexcesses: p x q matrix with mean of excesses above the time varying threshold
#
#$medianexcesses: p x q matrix with median of excesses above the time varying threshold
#
#$stdevexcesses: p x q matrix with st. dev of excesses above the time varying threshold
#
#
# Authors:
#
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 28 Feb 2006
#      Chris Ferro <c.a.t.ferro@reading.ac.uk>


# reshape three-dimensional array into a data matrix with
# time as first dimension and space as sencond dimension
data <- reshapefield(lon,lat,array3d)$out

# compute percentage of non-missing values at each grid point
aux <- apply(data,2,function(x)sum(!is.na(x))/(length(x)))

# identify grid points with less than 50% missing values
indexgrid <- (1:length(aux))[aux >= nonmissing]

out1 <- rep(NA,dim(data)[2])
out2 <- rep(NA,dim(data)[2])
mthresh <- matrix(nrow=dim(data)[1],ncol=dim(data)[2])


year<-10
nyears <- dim(data)[1]

if(upper) {
# Estimate Generalized Pareto distribution parameters (scale and shape) for
# exceedances above the threshold p
estim.par <- function(y,p) {

threshold<-tvtclimexp(y,span=year/nyears,1-p)$threshold

params<-gpd.fit(y[!is.na(y)], threshold[!is.na(y)], show=FALSE)$mle

list(params=params,threshold=threshold)

}

out<-apply(data[,indexgrid],2,estim.par,p)

} # end if upper

else {
# Estimate Generalized Pareto distribution parameters (scale and shape) for
# exceedances below the threshold p
estim.par <- function(y,p) {

threshold<-tvtclimexp(-y,span=year/nyears,p)$threshold

params<-gpd.fit(-y[!is.na(-y)], threshold[!is.na(-y)], show=FALSE)$mle

list(params=params,threshold=threshold)

}

out<-apply(data[,indexgrid],2,estim.par,p)


} # end else

for (i in 1:length(indexgrid)){
#scale parameter
out1[indexgrid[i]]<-out[[i]]$params[1]

mthresh[,indexgrid[i]]<-out[[i]]$threshold


#shape parameter
out2[indexgrid[i]]<-out[[i]]$params[2]

}

if(upper){
th<-reshapefield(lon,lat,mthresh)$out
excesses<-array3d-th
excesses[excesses<0]<-NA
}
else{
th<-reshapefield(lon,lat,-mthresh)$out
excesses<-array3d-th
excesses[excesses>0]<-NA
}

output<-array(NA,c(2,dim(array3d)[1],dim(array3d)[2]))
output[1,,]<-reshapefield(lon,lat,t(as.matrix(out1)))$out
output[2,,]<-reshapefield(lon,lat,t(as.matrix(out2)))$out


#excesses<-array3d-th
#excesses[excesses<0]<-NA

# Mean of excesses
meanexcesses<-apply(excesses,c(1,2),mean,na.rm=T)
meanexcesses[is.na(meanexcesses)]<--999.99

# Median of excesses
medianexcesses<-apply(excesses,c(1,2),median,na.rm=T)
medianexcesses[is.na(medianexcesses)]<--999.99

# St. dev of excesses
stdevexcesses<-sqrt(apply(excesses,c(1,2),var,na.rm=T))
stdevexcesses[is.na(stdevexcesses)]<--999.99


output[is.na(output)]<--999.99
th[is.na(th)]<--999.99

invisible(list(output=output,th=th,meanexcesses=meanexcesses,medianexcesses=medianexcesses,stdevexcesses=stdevexcesses))

}
