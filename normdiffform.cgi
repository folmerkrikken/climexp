#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

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
DIR=`pwd`
. ./nosearchengine.cgi

. ./myvinkhead.cgi "Subtract another time series" "$station $NAME"  "noindex,nofollow"

cat <<EOF
Many indices of weather are constructed by subtracting two time
series, e.g., SOI from the pressure at Darwin and Tahiti, NAO from
Iceland and Azores.  This form allows you to subtract two time series,
after optionally normalizing them to unit standard deviation (either
yearly or monthly).  The result can again be normalized.

<form action="normdiff.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="CLIMATE" value="$NAME">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<div class="formheader">Select the other time series</div>
<div class="formbody"><table border=0 cellspacing=0 cellpadding=0>
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

<p><div class="formheader">Normalization</div>
<div class="formbody">
First apply <select name="my1" class="forminput"><option selected>no<option>monthly<option>yearly</select> normalization to the time
series,<br>
next apply <select name="my2" class="forminput"><option selected>no<option>monthly<option>yearly</select> normalization to the difference

<p><input type="submit" class="formbutton" value="Subtract">
</div>
</form>
EOF

. ./myvinkfoot.cgi
