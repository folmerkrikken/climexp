#CORRELATION

##########################################################################
##########################################################################
# function that computes correlation for two given fields (observations
# and forecasts)
#
# Usage cortwo3d(data1,data2)
#
# Inputs:
#
# data1: 4d array of ensemble forecasts with 
#        first dimension nlon (number of longitude points)
#        second dimension nlat (number of latitude points)
#        third dimension n (number of time slices) and
#        fourth dimension m (number of members of the ensemble)
#        (the fourth dimesnion is optional)
#
# data2: 3d array with the observed values with
#        first dimension nlon (number of longitude points)
#        second dimension nlat (number of latitude points) and
#        third dimension n (number of time slices) and
#
# output:
#
# correlation: correlation map with
#              first dimension nlon (number of longitude points) and
#              second dimension nlat (number of latitude points) 
#
# Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>
#
# Example: dim1 <- c(7,9,60,3)
#          data1 <- array(rnorm(prod(dim1)), dim1)
#          dim2 <- c(7,9,60)
#          data2 <- array(rnorm(prod(dim2)), dim2)
#          cortwo3d(data1,data2)

cortwo3d <- function(data1,data2) {

obs<- data2
if ( length(dim(data1)) == 3 )
  ensmean <- data1
else
  ensmean <- apply( data1, c(1,2,3), mean, na.rm=TRUE)

nlon<-dim(data2)[1]
nlat<-dim(data2)[2]
correlation<-data2[,,1]
for (i in 1:nlon){
.Fortran("rkeepalive",i=as.integer(i),n=as.integer(nlon))
      for(j in 1:nlat){
	      correlation[i,j]<-cor(ensmean[i,j,],obs[i,j,],use="pairwise.complete.obs")
      }
}
correlation[is.na(correlation)] <- -999.99
list(correlation=correlation)
}



#cortwo3d.new <- function(data1,data2) {
#	obs<- data2
#	ensmean<- apply( data1, c(1,2,3), mean)
#	data <- array(NA, c(dim(obs), 2))
#	data[,,, 1] <- ensmean
#	data[,,, 2] <- obs
#	mycor <- function(x) cor(x[, 1], x[, 2],use="complete.obs")
#	list(correlation = apply(data, c(1, 2), mycor))
#}
