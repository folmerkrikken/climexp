#!/bin/sh

export DIR=`pwd`
. ./getargs.cgi

WMO="$FORM_WMO"
TYPE=`basename $0 .cgi`
TYPE=${TYPE#getdutchprecip_}
STATION="$FORM_STATION"
NPERYEAR=366
extraargs="$FORM_extraargs"

case $TYPE in
hom*) NAME="homogenised precipitation";;
raw*) NAME="observed precipitation";;
*) echo "Content-Type: text/html"; echo; . ./myvinkhead.cgi "Error" "$TYPE";. ./myvinkfoot.cgi; exit -1
esac
file="KNMIData/precip${WMO}_${TYPE}.dat.gz"
PROG="mygunzip.sh $file "
###FROM="from <a href=\"http://www.knmi.nl/klimatologie/daggegevens/download.html\" target=\"_new\">KNMI climatological service</a>"
LASTMODIFIED=`stat $file | fgrep Modify | cut -b 8-27`
LASTMODIFIED=`date -R -d "$LASTMODIFIED"`

. $DIR/getdata.cgi
