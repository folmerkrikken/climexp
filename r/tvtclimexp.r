tvtclimexp<-function(y,span,prob){

# Compute time-varying threshold for a given monthly time series
#
#  Description:
#
#       Returns smooth long term mean, time-varying threshold and fitted values
#       given by long term mean plus mean monthly or seasonal value
#
# Usage: tvtclimexp(y,span,prob)
#
# Input:
#
#       y: vector containing a monthly time series of data
#
#    span: fraction of the total number of points of 'y' to be used to compute
#          the long term mean
#
#    prob: a value between 0 and 1 that informs the percentage of point
#          that will be left above the time-varying threshold 
#
# Outputs
#
#    $mfit: fitted data (i.e. long term mean + mean annual cycle)
#
#     $ltm: long term mean
#
#$theshold: time-varying threshold
#
# Authors:
#
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 28 Feb 2006
#      Chris Ferro <c.a.t.ferro@reading.ac.uk>


x<-1:length(y)
lo<-loess(y~x,span=span)

resid<-rep(NA,length(y))
resid[!is.na(y)]<-lo$residuals

meanresid<-mean(resid,na.rm=T)


fitted<-rep(NA,length(y))
fitted[!is.na(y)]<-lo$fitted

mfit<-fitted+meanresid


step <- sort(y- mfit)
step <- unique(step[step > 0])
th <- mfit
p <- mean(y > th, na.rm = TRUE)
k <- 0
while(p > prob) {
  k <- k + 1
  th <- mfit + step[k]
  p <- mean(y > th, na.rm = TRUE)
}

list(threshold=th,ltm=fitted,mfit=mfit)
}
