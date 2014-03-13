#DISCRIMINATION

##########################################################################
##########################################################################
# function that computes the discrimination score  for two given fields
# (observations and forecasts)
#
# Usage discrim(data1,data2)
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
# discrimination: discrimination map  with
#              first dimension nlon (number of longitude points) and
#              second dimension nlat (number of latitude points) 
#
# Author: Andreas Weigel <andreas.weigel@meteoswiss.ch>
#         Based on the routine cortwo3d by Caio Coelho
#
# Example: dim1 <- c(7,9,60,3)
#          data1 <- array(rnorm(prod(dim1)), dim1)
#          dim2 <- c(7,9,60)
#          data2 <- array(rnorm(prod(dim2)), dim2)
#          discrim(data1,data2)

# Andreas: changed function name to discrim
discrim <- function(data1,data2) {

obs<- data2
if ( length(dim(data1)) == 3 )
  ensmean <- data1
else
  ensmean <- apply( data1, c(1,2,3), mean, na.rm=TRUE)

nlon<-dim(data2)[1]
nlat<-dim(data2)[2]

#Andreas: Changed varname "correlation" to "discrimination"
#Andreas: Changed Pearson correlation to Kendall correlation

discrimination<-data2[,,1]
for (i in 1:nlon){
.Fortran("rkeepalive",i=as.integer(i),n=as.integer(nlon))
      for(j in 1:nlat){
	   discrimination[i,j]<-cor(ensmean[i,j,],obs[i,j,],
                                    use="pairwise.complete.obs",method="kendall")
      }
}

#Andreas: Calculate discrimination score from Kendall-Correlation
discrimination = 0.5*(discrimination+1)
discrimination[is.na(discrimination)] <- -999.99
list(discrimination=discrimination)
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
