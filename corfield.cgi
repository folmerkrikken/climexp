#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

. ./init.cgi
. ./getargs.cgi

TYPE="$FORM_TYPE"
WMO="$FORM_WMO"
STATION="$FORM_STATION"
station=`echo "$STATION" | tr '_%' ' +'`
NAME="$FORM_NAME"
NPERYEAR="$FORM_NPERYEAR"
[ -z "$NPERYEAR" ] && NPERYEAR=12
DIR=`pwd`

. ./nosearchengine.cgi

c=`echo $WMO | egrep -c '\+\+|%%'`
if [ "$c" != 0 ]; then
   ENSEMBLE=true
fi

myname=`basename $0 .cgi`
if [ "$myname" = "corfield_obs" ]; then
  NO_REA=true
  NO_SEA=true
  NO_CO2=true
  NO_AR5=true
  NO_USE=true
  anotherfield="an observation field"
elif [ "$myname" = "corfield_rea" ]; then
  NO_OBS=true
  NO_SEA=true
  NO_CO2=true
  NO_AR5=true
  NO_USE=true
  anotherfield="a reanalysis field"
elif [ "$myname" = "corfield_sea" ]; then
  NO_OBS=true
  NO_REA=true
  NO_CO2=true
  NO_AR5=true
  NO_USE=true
  anotherfield="a seasonal forecast field"
elif [ "$myname" = "corfield_co2" ]; then
  NO_OBS=true
  NO_REA=true
  NO_AR5=true
  NO_SEA=true
  NO_USE=true
  anotherfield="a scenario run"
elif [ "$myname" = "corfield_cmip5" ]; then
  NO_OBS=true
  NO_REA=true
  NO_CO2=true
  NO_SEA=true
  NO_USE=true
  anotherfield="a scenario run"
elif [ "$myname" = "corfield_use" ]; then
  NO_OBS=true
  NO_REA=true
  NO_AR5=true
  NO_SEA=true
  NO_CO2=true
  anotherfield="a user-defined field"
else
  NO_SEA=true
  NO_CO2=true
  NO_AR5=true
  anotherfield="a field"
fi

. ./myvinkhead.cgi "Correlate time series with $anotherfield" "$station $NAME" "noindex,nofollow"

cat <<EOF
<form action="correlate.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="CLIMATE" value="$NAME">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NAME" value="$NAME">
EOF

. ./selectfieldform.cgi

cat <<EOF
<div class="formheader">Plot options</div>
<div class="formbody">
<table style='width:100%' border='0' cellpadding='0' cellspacing='0'>
<tr valign="baseline"><td>Variable:<td>
EOF
. ./choosevariable.cgi
echo "<tr><td>Demand at least<td><input type=\"$number\" step=any name=\"minfac\" value=\"$FORM_minfac\" $textsize2>% valid points"
probmask=true
NX=100
NY=100
intable=true
. ./plotoptions.cgi
echo "</table>"
echo '</div>'

timeseries="timeseries"
index="field"
. ./commonoptions.cgi

. ./myvinkfoot.cgi
