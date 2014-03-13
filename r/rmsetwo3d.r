#RMSE

##########################################################################
##########################################################################
# function that computes root mean squared error for two given  fields (observations
# and forecasts)
#
# Usage rmsetwo3d(data1,data2)
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
# Output:
#
#  rmse: RMSE map with
#        first dimension nlon (number of longitude points) and
#        second dimension nlat (number of latitude points) 
#
# Author: Caio Coelho <c.a.d.s.coelho@reading.ac.uk>
#
# Example: dim1 <- c(7,9,60,3)
#          data1 <- array(rnorm(prod(dim1)), dim1)
#          dim2 <- c(7,9,60)
#          data2 <- array(rnorm(prod(dim2)), dim2)
#          rmsetwo3d(data1,data2)


rmsetwo3d <- function(data1,data2) {

obs<- data2
if ( length(dim(data1)) == 3 )
  ensmean <- data1
else
  ensmean <- apply( data1, c(1,2,3), mean,na.rm = TRUE)

nlon<-dim(data2)[1]
nlat<-dim(data2)[2]

rmse<-data2[,,1]

for (i in 1:nlon){
      for(j in 1:nlat){
              rmse[i,j]<- sqrt(mean((ensmean[i,j,]-obs[i,j,])^2,na.rm = TRUE))
      }
}
rmse[is.na(rmse)] <- -999.99
list(rmse=rmse)
}
