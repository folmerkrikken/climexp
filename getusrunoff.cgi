#!/bin/sh

. ./getargs.cgi
WMO="$FORM_WMO"
STATION="$FORM_STATION"
TYPE=r
NAME="streamflow"
NPERYEAR=12
export DIR=`pwd`
PROG=getusrunoff
FROM="from <a href="wipefeet.cgi?http://water.usgs.gov/pubs/wri/wri934076/1st_page.html" target="_new">HCDN database</a>"

. $DIR/getdata.cgi
