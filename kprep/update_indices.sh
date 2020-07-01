#!/bin/sh

# Script to run empirical seasonal prediction system for TAS, PREC and PSL.
# User to specify predictand variable names
# F. Krikken, KNMI, 2017.12.07
# ---------------------------
res=$1

# Copy grid description file to correct place
cp griddes${res}.txt ~/climexp_data/KPREPData/targetgrid/
# Change working directory to where to store data / files / plots / etc.
cd ~/climexp_data/KPREPData
# First get resolution..

# First get TMAX at 1 degree resolution for the MDC forecast

#wget -N https://climexp.knmi.nl/ERA5/era5_tmax.nc -P inputdata/
#cdo remapbil,targetgrid/griddes10.txt inputdata/era5_tmax.nc inputdata/era5_tmax_r10.nc

wget -N http://climexp.knmi.nl/BerkeleyData/land_mask.nc -P inputdata/land_mask_TMAX_LatLong1.nc
wget -N http://climexp.knmi.nl/BerkeleyData/TMAX_LatLong1.nc -P inputdata/
cdo remapbil,targetgrid/griddes10.txt inputdata/land_mask_TMAX_LatLong1.nc inputdata/land_mask_TMAX_LatLong1_r10.nc
cdo remapbil,targetgrid/griddes10.txt inputdata/TMAX_LatLong1.nc inputdata/TMAX_LatLong1_r10.nc




# Now for the other forecast

# Download ERSSTV5 from climexp
wget -N http://climexp.knmi.nl/NCDCData/ersstv5.nc -P inputdata/
# Download GHCN_CAMS from NCEP
# Upgrade to 1 degree, download 0.5 degrees
wget -N ftp://ftp.cdc.noaa.gov/Datasets/ghcncams/air.mon.mean.nc -P inputdata/
#wget -N ftp://ftp.cpc.ncep.noaa.gov/wd51yf/GHCN_CAMS/ghcn_cams_1948_cur_2.5.grb -P inputdata/
#wget -N ftp://ftp.cpc.ncep.noaa.gov/wd51yf/GHCN_CAMS/ghcn_cams_1979_2006.clim.grb -P inputdata/
# Merge ersstv4 and ghcn_cams and fill missing data through interpolation
# TODO, check if inputdata is actually updated..
#cdo -f nc copy inputdata/ghcn_cams_1948_cur_2.5.grb inputdata/ghcn_cams_1948_cur_25.nc
#cdo -f nc copy inputdata/ghcn_cams_1976_2006.clim.grb inputdata/ghcn_cams_1979_2006.clim.nc

# Remap ghcn_cams and ersstv5
#cdo remapbil,targetgrid/griddes${res}.txt inputdata/ghcn_cams_1948_cur_25.nc inputdata/ghcn_cams_1948_cur_r25.nc
#cdo remapbil,targetgrid/griddes${res}.txt inputdata/air_mon_mean.nc inputdata/ghcn_cams_1948_r${res}.nc
#cdo remapbil,targetgrid/griddes${res}.txt inputdata/ersstv5.nc inputdata/ersstv5_r${res}.nc
 
# Old method
#cdo settunits,days -fillmiss -mergegrid -addc,273.15 -selyear,1948/2030 -remapbil,targetgrid/griddes${res}.txt -setmissval,-999 inputdata/ersstv5.nc -remapbil,targetgrid/griddes${res}.txt -setmissval,-999 inputdata/ghcn_cams_1948_cur_25.nc inputdata/gcecom_r${res}.nc
cdo settunits,days -fillmiss -mergegrid -addc,273.15 -selyear,1948/2030 -remapbil,targetgrid/griddes${res}.txt -setmissval,-999 inputdata/ersstv5.nc -remapbil,targetgrid/griddes${res}.txt -setmissval,-999 inputdata/air_mon_mean.nc.nc inputdata/gcecom_r${res}.nc

# Download Hadley4 with kriging
wget -N http://www-users.york.ac.uk/~kdc3/papers/coverage2013/had4_krig_v2_0_0.nc.gz -P inputdata/
gunzip -f inputdata/had4_krig_v2_0_0.nc.gz
cdo -remapbil,targetgrid/griddes${res}.txt -selyear,1901/2010 inputdata/had4_krig_v2_0_0.nc inputdata/had4_krig_v2_0_0_r${res}.nc


# Download SLP data from climate explorer
wget -N http://climexp.knmi.nl/20C/prmsl.mon.mean.nc -P inputdata/          # Data from 1851 to 2011
wget -N http://climexp.knmi.nl/NCEPNCAR40/slp.mon.mean.nc -P inputdata/     # Data from 1948 to current

# Use prmsl.mon.mean.nc for 1901 to 1948 and slp.mon.mean.nc for 1948 to current
rm -f inputdata/slp_mon_mean_1901-current_r${res}.nc
cdo mergetime -selyear,1901/1947 -remapbil,targetgrid/griddes${res}.txt -selvar,prmsl -divc,100 inputdata/prmsl.mon.mean.nc -remapbil,targetgrid/griddes${res}.txt inputdata/slp.mon.mean.nc inputdata/slp_mon_mean_1901-current_r${res}.nc

# Download precipitation data from 
wget -N http://climexp.knmi.nl/GPCCData/gpcc_10_combined.nc -P inputdata/
cdo muldpm inputdata/gpcc_10_combined.nc inputdata/gpcc_10_combined_mon.nc

cdo remapbil,targetgrid/griddes10.txt inputdata/gpcc_10_combined_mon.nc inputdata/gpcc_10_combined_mon_r10.nc
cdo remapbil,targetgrid/griddes${res}.txt inputdata/gpcc_10_combined_mon.nc inputdata/gpcc_10_combined_r${res}.nc

# Download the climate indices from climate explorer
wget -N http://climexp.knmi.nl/CDIACData/RCP45_CO2EQ_mo.dat -P inputdata/
wget -N http://climexp.knmi.nl/NCDCData/ersst_nino3.4a.dat -P inputdata/
#wget -N http://climexp.knmi.nl/NCDCData/qbo_30.dat -P inputdata/
wget -N http://climexp.knmi.nl/NCDCData/dmi_ersst.dat -P inputdata/
wget -N http://climexp.knmi.nl/UWData/pdo_ersst.dat -P inputdata/
wget -N http://climexp.knmi.nl/NCDCData/amo_ersst_ts.dat -P inputdata/
#wget -N http://climexp.knmi.nl/NCDCData/amo_ersst_ts.dat -P inputdata/





