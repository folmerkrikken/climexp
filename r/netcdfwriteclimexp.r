# Write three-dimentional array of data, longitude vector, latitude vector and
# time vector into a netcdf file.
#
# Description:
#
#      Returns a netcdf file that contains a three-dimentional array of data
#      a longitude vector, a latitude vector and a time vector
#
# Usage:
#
#      netcdfwrite(lon,lat,array3d,time,filename)
#
# Arguments:
#
#   	 array3d:  an three-dimentional array containing the data (fields)
#	 lon:	   a vector containing the longitudes of array3d
#        lat:      a vector containing the latitudes of array3d
#	 time:	   a vector containing the times of array3d
#	 filename: string with the name of the netcdf file to be created.
#                  Default is "data.nc".
#
# Output:
#
#	 netcdf-file containing the data 
#
# Author:
#
#     Dag Johan Steinskog <dag.johan.steinskog@nersc.no>  27 October 2005
#     Caio Coelho <c.a.d.s.coelho@reading.ac.uk>
#
# Example:
#
#     x <- seq(-20, 20, 5)
#     y <- seq(30, 60, 5)
#     dims <- c(length(x), length(y), 100)
#     data <- array(rnorm(prod(dims)), dims)
#     time <- 1:100
#     netcdfwrite(x,y,data,time,filename="data.nc")


netcdfwriteclimexp <- function(lon,lat,data,filename="data.nc",time=1) {

#create netcdf file
#ncfile <- create.nc(filename,clobber)
ncfile <- create.nc(filename)


#give dimentions to variables
dim.def.nc(ncfile,"lon",length(lon))
dim.def.nc(ncfile,"lat",length(lat))
#dim.def.nc(ncfile,"time",length(time))


# create variables
var.def.nc(ncfile,"lon","NC_DOUBLE","lon")
var.def.nc(ncfile,"lat","NC_DOUBLE","lat")
#var.def.nc(ncfile,"time","NC_DOUBLE","time")
#var.def.nc(ncfile,"data","NC_DOUBLE",c("lon","lat","time"))
var.def.nc(ncfile,"data","NC_DOUBLE",c("lon","lat"))


# add data to variables
var.put.nc(ncfile,"lat",lat)
var.put.nc(ncfile,"lon",lon)
#var.put.nc(ncfile,"time",time)
var.put.nc(ncfile,"data",data)

att.put.nc(ncfile,"data","missing_value","NC_DOUBLE",-999.99)

att.put.nc(ncfile,"lon","long_name","NC_DOUBLE","Longitude")
att.put.nc(ncfile,"lon","units","NC_DOUBLE","degrees_east")
att.put.nc(ncfile,"lon","axis","NC_DOUBLE","X")

att.put.nc(ncfile,"lat","long_name","NC_DOUBLE","Latitude")
att.put.nc(ncfile,"lat","units","NC_DOUBLE","degrees_north")
att.put.nc(ncfile,"lat","axis","NC_DOUBLE","Y")

# syncronize and close the netcdf file    
sync.nc(ncfile)
close.nc(ncfile)
}

