#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./init.cgi
. ./getargs.cgi

TYPE="$FORM_TYPE"
WMO="$FORM_WMO"
STATION="$FORM_STATION"
station=` echo "$STATION" | tr '_%' ' +'`
NAME="$FORM_NAME"
NPERYEAR="$FORM_NPERYEAR"
if [ -z "$NPERYEAR" ]; then
  NPERYEAR=12
fi

. ./nosearchengine.cgi

DIR=`pwd`
c1=`echo "$WMO" | fgrep -c '%%'`
c2=`echo "$WMO" | fgrep -c '++'`
if [ $c1 -gt 0 -o $c2 -gt 0 ]; then
  ENSEMBLE=true
fi

. ./myvinkhead.cgi "Correlate with another time series" "$station $NAME" "noindex,nofollow"
cat <<EOF
<form action="correlate.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="CLIMATE" value="$NAME">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NAME" value="$NAME">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
EOF

selecttimeseries=`. ./selecttimeseries.cgi`
if [ $EMAIL != someone@somewhere ]; then
  if [ -f ./prefs/$EMAIL.series.$NPERYEAR ]; then
    for series in `cat ./prefs/$EMAIL.series.$NPERYEAR`
    do
      selecttimeseries=`echo $selecttimeseries | sed \
	  -e 's;="'$series'";="'$series'" checked;'`
    done
  fi
fi
echo $selecttimeseries

timeseries="timeseries"
index="index"
XYplot=true
DECOR=true
whichvar=true
. ./commonoptions.cgi

. ./myvinkfoot.cgi


