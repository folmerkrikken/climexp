#
# Extracts data longitude vector, latitude vector and 
# data array from a netCDF file.
#
# Description:
#
#      Returns a vector of longitudes, a vector of latitudes and an
#      array of data from a netCDF file.
# Usage:
#
#      netcdfread(file,lonname,latname,dataname)
#
# Arguments:
#
#   file:     String containing the full path and netCDF file name
#   lonname:  String containing the name of the longitude variable. 
#             If any provided, default name is "longitude".
#   latname:  String containing the name of the latitude variable
#             If any provided, default name is "latitude".
#   dataname: String containing the name of the data variable
#
# Output:
#
#   $lonncfile:  Vector of longitudes
#   $latncfile:  Vector of latitudes
#   $datancfile: Array of data
#
# Author:
#
#      Chris Ferro <c.a.t.ferro@reading.ac.uk> 9 June 2005
#      Dag Johan Steinskog <dag.johan.steinskog@nersc.no> 
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 
#
# Examples:
#
#      # First run the line below to extract the data structure/information
#      # so that you are able to know the names of variables 
#      netcdfinfo("netCDF_file_name.nc")
#
#      netcdfread("netCDF_file_name.nc","lon_name","lat_name","data_name")
#      netcdfread("/home/username/netCDF_file_name.nc","lon_name","lat_name","data_name")
#
#      Note: The user should use a netCDF file to be able to run these examples

netcdfreadclimexp <- function(file,lonname='longitude',latname='latitude',dataname) {
 
# open a netcdf file
ncfile <- open.nc(file)

# get lat and lon
lonncfileaux <- var.get.nc(ncfile, lonname)
latncfileaux <- var.get.nc(ncfile, latname)

# get data
datancfile <- var.get.nc(ncfile, dataname)

# sort lat and lon in ascending order
lonncfile <- sort(lonncfileaux)
latncfile <- sort(latncfileaux)

# rearange data 
datancfile<-datancfile[order(lonncfileaux),order(latncfileaux),,]

invisible(list(lonncfile=lonncfile,latncfile=latncfile,datancfile=datancfile))

}
