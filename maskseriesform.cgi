#!/bin/bash
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

. ./myvinkhead.cgi "Mask out parts of time series" "$station $NAME" "noindex,nofollow"
cat <<EOF
<form action="maskseries.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="CLIMATE" value="$NAME">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<div class="formheader">Select the other time series</div>
<div class="formbody"><table border=0 cellspacing=0 cellpadding=0><tr><td>
EOF

if [ $EMAIL != someone@somewhere ]; then
  if [ -f ./prefs/$EMAIL.series.$NPERYEAR ]; then
    series=`tail -1 ./prefs/$EMAIL.series.$NPERYEAR`
  fi
fi
. ./selecttimeseries.cgi | sed -e '1,/User-defined/d' \
  -e 's;="'$series'";="'$series'" checked;'

cat <<EOF
</div>
<p>
<div class="formheader">Masking</div>
<div class="formbody">
Select only the values when 
<input type="$number" step=any name="gt" $textsize4> &lt; other time series &lt; 
<input type="$number" step=any name="lt" $textsize4>
<br>
<input type="submit" class="formbutton" value="Select">
</div>
</form>
EOF

. ./myvinkfoot.cgi
