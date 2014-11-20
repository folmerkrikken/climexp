#!/bin/sh
if [ "$VAR" = "temp" -a "$kindname" = "SODA  " ]; then
  VAR=sst
fi
myvar=${VAR#min_}
myvar=${myvar#max_}
case ${myvar:-unknown} in 
prcp|prec|tp|prate|rr|pr|pre|precip*|prlr) field_type="Precipitation";;
T|tmp|tmp2m|t2m|t2msst|t2x|t2n|TMP2m|TMAX2m|tasmax|TMIN2m|tasmin|max2t|temp|tmin|tmax|tg|tn|tx|tmx|tmn|p2m_t|tas|temp2|air2m|no2Tsfc|p2t|NT2M|T2M|air_temperature1|tempanomaly|temperature_anomaly|air|TMP_2maboveground) field_type="Temperature";;
sst|ts|stemp|st_stl1|tsf|tsfc|TMPsfc|tsw|SSTa|SST|tos|TOS) field_type="SST";;
mslp|msl|MSL*|slp|SLP|psl|PRESsfc|aps|prmsl) field_type="Pressure";;
z|z200|z300|z500|z700|z850|zg|g|geopoth|hgt) field_type="Geopotential";;
u|u200|u300|u500|u700|u850|ugrd|uwnd) field_type="Wind";;
v|v200|v300|v500|v700|v850|vgrd|vwnd) field_type="Wind";;
p10m_u|u10|u10m|p10m_v|v10|v10m|ustr|vstr|ugeo|vgeo) field_type="Wind";;
dssr|ssd|aclcov|rsds|cld) field_type="Solar";;
snd|sd) field_type="Snow";;
psiuwe|PSIUWE) field_type="Streamfunction";;
heat|HEAT750) field_type='Heat content';;
rhum|shum) field_type="Humidity";;
snow) field_type="Snow";;
time*) field_type="Time";;
fd*) field_type="frost days";;
*) echo "getfieldtype: please ask <a href=\"http://www.knmi.nl/~oldenbor/\">me</a> to add \"$VAR\" to the lists in getfieldtype";field_type="$VAR";;
esac
