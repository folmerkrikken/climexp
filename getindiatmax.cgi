#!/bin/sh

. ./getargs.cgi
WMO="$FORM_WMO"
STATION="$FORM_STATION"
TYPE=x
NAME="Tmax"
NPERYEAR=12
export DIR=`pwd`
PROG=getindiatmax
FROM="from <a href=\"http://www.tropmet.res.in/\" target=\"_new\">IITM</a>"

. $DIR/getdata.cgi
