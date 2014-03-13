# Extracts data structure, names of variables and dimention information 
# form netCDF file
#
# Description:
#
#      Returns a summary of the data structure, a list of dimentions, 
#      a list of variables and the lenghts (size) of each dimention.
#
# Usage:
#
#      netcdfinfo(file)
#
# Arguments:
#
#   file: String containing the full path and netCDF file name.
#
# Output:
#
#   $dims: Dimention names
#   $vars: Variable names
#   $lenghts: Dimention lenghts (size)
#
#
# Author:
#
#      Chris Ferro <c.a.t.ferro@reading.ac.uk> 9 June 2005
#      Dag Johan Steinskog <dag.johan.steinskog@nersc.no> 
#      Caio Coelho <c.a.d.s.coelho@reading.ac.uk> 
#
# Examples:
#
#      netcdfinfo("netCDF_file_name.nc")
#      netcdfinfo("/home/username/netCDF_file_name.nc")
#
#      Note: The user should use a netCDF file to be able to run these examples

netcdfinfo <- function(file) {
 
# open a netcdf file
ncfile <- open.nc(file)

# print details
print.nc(ncfile)

# store dimension names
dims <- character(file.inq.nc(ncfile)$ndims)
for(i in 1:length(dims))
  dims[i] <- dim.inq.nc(ncfile, i - 1)$name

# store variables names
vars <- character(file.inq.nc(ncfile)$nvars)
for(i in 1:length(vars))
  vars[i] <- var.inq.nc(ncfile, i - 1)$name


# store lenghts of each dimention
lenghts <- as.vector(seq(1:file.inq.nc(ncfile)$ndims))
for(i in 1:length(dims))
  lenghts[i] <- dim.inq.nc(ncfile, i - 1)$length

list(dims=dims,vars=vars,lenghts=lenghts)

}
