#!/bin/bash
. ./init.cgi
. ./getargs.cgi
WMO="$FORM_WMO"
STATION="$FORM_STATION"
TYPE=p
NAME="Precipitation"
NPERYEAR=12
export DIR=`pwd`
PROG=getindiaprcp
FROM="from <a href=\"http://www.tropmet.res.in/\" target="_new">IITM</a>"
LASTMODIFIED=`stat IITMData/ALLIN.dat | fgrep Modify | cut -b 8-27`
LASTMODIFIED=`date -R -d "$LASTMODIFIED"`

. $DIR/getdata.cgi
