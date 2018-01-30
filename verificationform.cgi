#!/bin/sh
. ./init.cgi
. ./httpheaders_nocache.cgi

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
c1=`echo "$WMO" | fgrep -c '%'`
c2=`echo "$WMO" | fgrep -c '++'`
if [ $c1 -gt 0 -o $c2 -gt 0 ]; then
  ENSEMBLE=true
fi
eval `./bin/getunits $DIR/data/$TYPE$WMO.dat`
if [ -z "$NEWUNITS" ]; then
  NEWUNITS=$UNITS
fi

. ./myvinkhead.cgi "Verify time series hindcasts" "$station $NAME"

cat <<EOF
Verification is under active development and may still contain bugs.  Please report problems back to <a href="mailto:oldenborgh@knmi.nl">me</a>.
EOF
if [ "$NEWUNITS" != "$UNITS" ]; then
  echo "Converting $VAR from $UNITS to $NEWUNITS"
fi
cat <<EOF
<form action="verification.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="CLIMATE" value="$NAME">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
EOF

. ./selectveriftimeseries.cgi
. ./choose_verification.cgi
. ./choose_threshold.cgi

cat <<EOF
<p><div class="formheader">Options</div>
<div class="formbody">
<table style='width:100%' border='0' cellpadding='0' cellspacing='0'>
EOF
timeseries="forecast"
index="observations"
justonemonth="T"
ONLYONE=true
VERIF=true
NAME="both obs and fcst"
. ./commonoptions.cgi
. $DIR/verifoptions2.cgi
echo '</table></div></form>'

###timeseries="timeseries"
###index="index"
###justonemonth="T"
###. $DIR/verifoptions.cgi

. ./myvinkfoot.cgi
