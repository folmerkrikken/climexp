#!/bin/bash
ncatted -O \
-a long_name,lon,a,c,"Longitude" \
-a units,lon,a,c,"degrees_east" \
-a axis,lon,a,c,"X" \
-a long_name,lat,a,c,"Latitude" \
-a units,lat,a,c,"degrees_north" \
-a axis,lat,a,c,"Y" \
$ncfile
ncrename -v data,$FORM_var $ncfile
