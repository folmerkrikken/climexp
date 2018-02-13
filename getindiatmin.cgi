#!/bin/sh
. ./init.cgi
. ./getargs.cgi
WMO="$FORM_WMO"
STATION="$FORM_STATION"
TYPE=n
NAME="Tmin"
NPERYEAR=12
export DIR=`pwd`
PROG=getindiatmin
FROM="from <a href="http://www.tropmet.res.in/" target="_new">IITM</a>"

. $DIR/getdata.cgi
