#!/bin/sh

. ./getargs.cgi
WMO="$FORM_WMO"
STATION="$FORM_STATON"
TYPE=n
NAME="Tmin"
NPERYEAR=12
export DIR=`pwd`
PROG=getindiatmin
FROM="from <a href="wipefeet.cgi?http://www.tropmet.res.in/" target="_new">IITM</a>"

. $DIR/getdata.cgi
