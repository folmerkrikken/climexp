#!/bin/sh

. ./getargs.cgi
TYPE="$FORM_TYPE"

# set up the information that getstations.cgi expects

FORM_EMAIL="$EMAIL"
FORM_email="$EMAIL"

case "$TYPE" in
dd) FORM_climate="prevailing_wind_direction";;
fg) FORM_climate="daily_mean_windspeed";;
fh) FORM_climate="maximum_hourly_windspeed";;
fn) FORM_climate="minimum_hourly_windspeed";;
fx) FORM_climate="maximum_wind_gust";;
tg) FORM_climate="mean_temperature";;
tn) FORM_climate="min_temperature";;
tx) FORM_climate="max_temperature";;
t1) FORM_climate="min_surface_temperature";;
td) FORM_climate="max_dew_point_temperature";;
ng) FORM_climate="cloud_cpver";;
qq) FORM_climate="global_radiation";;
sq) FORM_climate="sunshine_duration";;
sp) FORM_climate="sunshine_fraction";;
dr) FORM_climate="precipitation_duration";;
rd) FORM_climate="precipitation";;
rh) FORM_climate="precipitation";;
rr) FORM_climate="precipitation";;
ev) FORM_climate="Makking_evaporation";;
pg) FORM_climate="mean_surface_pressure";;
pn) FORM_climate="minimum_surface_pressure";;
px) FORM_climate="maximum_surface_pressure";;
vn) FORM_climate="minimum_visibility";;
vx) FORM_climate="maximum_visibility";;
dx) FORM_climate="zonal_wind_direction";;
dy) FORM_climate="meridional_wind_direction";;
ug) FORM_climate="mean_relative_humidity";;
un) FORM_climate="minimum_relative_humidity";;
ux) FORM_climate="maximum_relative_humidity";;
sc) FORM_climate="precipitation";;
sw) FORM_climate="global shortwave radiation";;
si) FORM_climate="circulation-independent_global_shortwave_radiation";;
sr) FORM_climate="circulation-dependent_global_shortwave_radiation";;
temp_hom) FORM_climate="homogenised_temperature";;
precipraw1910-2009) FORM_climate="raw precipitation";;
preciphom1910) FORM_climate="homogenised precipitation";;
precipraw1951-2009) FORM_climate="raw precipitation";;
preciphom1951) FORM_climate="homogenised precipitation";;
rx) FORM_climate="max hourly precipitation";;
esac

listname=KNMIData/list_${TYPE}.txt
prog="getdutch$TYPE"
type=$TYPE
NPERYEAR=366
if [ "$TYPE" = sw -o "$TYPE" = si -o "$TYPE" = sr -o "$TYPE" = temp_hom ]; then
  NPERYEAR=12
fi
format=new

. ./getstations.cgi
