#!/bin/sh

. ./getargs.cgi
WMO="$FORM_WMO"
STATION="$FORM_STATON"
TYPE=x
NAME="Tmax"
NPERYEAR=12
export DIR=`pwd`
PROG=getindiatmax
FROM="from <a href="wipefeet.cgi?http://www.tropmet.res.in/" target="_new">IITM</a>"

. $DIR/getdata.cgi
