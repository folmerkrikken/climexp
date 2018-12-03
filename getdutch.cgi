#!/bin/bash

export DIR=`pwd`
. ./init.cgi
. ./getargs.cgi

WMO="$FORM_WMO"
TYPE="$FORM_TYPE"
if [ -z "$TYPE" ]; then
    scriptname=`basename $0 .cgi`
    scriptname=${scriptname%.cgi} 
    TYPE=${scriptname#getdutch}
fi
STATION="$FORM_STATION"
NPERYEAR=366
extraargs="$FORM_extraargs"

case $TYPE in
dd) NAME="prevailing wind direction";;
fg) NAME="daily mean windspeed";;
fh) NAME="maximum hourly windspeed";;
upx) NAME="maximum hourly potential windspeed";;
fn) NAME="minimum hourly windspeed";;
fx) NAME="maximum wind gust";;
tg) NAME="mean temperature";;
tn) NAME="min temperature";;
tx) NAME="max temperature";;
tw) NAME="max wet bulb temperature";;
t1) NAME="min surface temperature";;
td) NAME="max dew point temperature";;
ng) NAME="cloud cover";;
qq) NAME="global radiation";;
sq) NAME="sunshine duration";;
sp) NAME="sunshine fraction";;
dr) NAME="precipitation duration";;
rh) NAME="precipitation";;
rr) NAME="precipitation";;
rx) NAME="max hourly precipitation";;
rd) NAME="precipitation";;
pg) NAME="mean surface pressure";;
px) NAME="maximum surface pressure";;
pn) NAME="minimum surface pressure";;
vn) NAME="minimum visibility";;
vx) NAME="maximum visibility";;
dx) NAME="zonal wind direction";;
dy) NAME="meridional wind direction";;
ug) NAME="mean relative humidity";;
un) NAME="minimum relative humidity";;
ux) NAME="maximum relative humidity";;
sc) NAME="precipitation";;
sd) NAME="snow depth";;
sdhom) NAME="hom snow depth";;
sw) NAME="global shortwave radiation";NPERYEAR=12;;
si) NAME="circulation-independent global shortwave radiation";NPERYEAR=12;;
sr) NAME="cicrulation-dependent global shortwave radiation";NPERYEAR=12;;

esac
WMO="KNMIData/$TYPE$WMO"
PROG="gunzip -c"
FROM="from <a href=\"http://www.knmi.nl/klimatologie/daggegevens/download.html\" target=\"_new\">KNMI climatological service</a>"
LASTMODIFIED=`stat $WMO.dat | fgrep Modify | cut -b 8-27`
LASTMODIFIED=`date -R -d "$LASTMODIFIED"`

. $DIR/getdata.cgi
