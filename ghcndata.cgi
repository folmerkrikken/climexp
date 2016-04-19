#!/bin/sh

. ./getargs.cgi

WMO="$FORM_WMO"
STATION="$FORM_STATION"
PROG=`basename $SCRIPT_FILENAME .cgi`
NPERYEAR=12

case $PROG in
    getprcp) TYPE=p; NAME="GHCN v2 precipitation";;
    getprcpall) TYPE=pa; NAME="GHCN v2 precipitation (all)";;
    getslp) TYPE=s; NAME="GHCN v2 sealevel pressure";;
    gettemp) TYPE=t; NAME="GHCN v3 mean temperature";;
    gettempall) TYPE=ta; NAME="GHCN v3 mean temperature (all)";;
    getmin) TYPE=m; NAME="GHCN v3 minimum temperature";;
    getminall) TYPE=ma; NAME="GHCN v3 minimum temperature (all)";;
    getmax) TYPE=x; NAME="GHCN v3 maximum temperature";;
    getmaxall) TYPE=xa; NAME="GHCN v3 maximum temperature (all)";;
    *) echo "Content-Type: text/html"; echo; . ./myvinkhead.cgi "Error" "Unknown GHCN data type" ""; . ./myvinkfoot.cgi; exit;;
esac

export DIR=`pwd`
FROM="from <a href="wipefoot.cgi?https://www.ncdc.noaa.gov/ghcnm/" target="_new">GHCN-M v2/v3 (adjusted) database</a>"
[ -z "$extraargs" ] && makenetcdf=true

. $DIR/getdata.cgi
