#!/bin/sh
. ./httpheaders_nocache.cgi
. ./init.cgi
. ./getargs.cgi
TYPE="$FORM_TYPE"
WMO="$FORM_WMO"
STATION="$FORM_STATION"
station=`echo "$STATION" | tr '_%' ' +'`
NAME="$FORM_NAME"
NPERYEAR="$FORM_NPERYEAR"

. ./nosearchengine.cgi

DIR=`pwd`
c1=`echo "$WMO" | fgrep -c '%%'`
c2=`echo "$WMO" | fgrep -c '++'`
if [ $c1 -gt 0 -o $c2 -gt 0 ]; then
  ENSEMBLE=true
fi

. ./myvinkhead.cgi "Spectrum or autocorrelation" "$station $NAME" "noindex,nofollow"

if [ $EMAIL != someone@somewhere ]; then
  if [ -f ./prefs/$EMAIL.period ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.:]*;$' ./prefs/$EMAIL.period`
  fi

  case ${FORM_which:-period} in
  autocor) autocor_checked=checked;;
  *)       period_checked=checked;;
  esac

  case ${FORM_normplot:-height} in
  area) area_checked=checked;;
  *)    height_checked=checked;;
  esac

fi

cat <<EOF
<form action="period.cgi" method="post">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="CLIMATE" value="$NAME">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$station">
<input type="hidden" name="NAME" value="$NAME">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<div class="formheader">Compute a spectrum or the autocorrelation of the time series</div>
<div class="formbody">
<table width="100%">
<tr><td>Compute:<td><input type="radio" name="which" value="period" $period_checked>spectrum
averaging <input type="$number" min=1 step=1 class="forminput" name="ave" value="$FORM_ave" size="2">bins of the periodogram
<br><input type="radio" name="which" value="autocor" $autocor_checked>
autocorrelation function
<tr>
EOF
intable=true
ONLYONE=true
NAME="time series"
. ./commonoptions.cgi
cat <<EOF
<tr><td>Normalise:<td><input type="radio" name="normplot" value="height" $height_checked>height or <input type="radio" name="normplot" value="area" $area_checked>area of peaks in spectrum
<tr><td colspan=2><input type="submit" class="formbutton" value="do it">
</table>
</form>
EOF

. ./myvinkfoot.cgi
