#!/bin/sh
. ./httpheaders_nochache.cgi
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

. ./myvinkhead.cgi "Extend time series" "$station $NAME" "noindex,nofollow"
cat <<EOF
<form action="patchseries.cgi" method="POST">
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
  
if [ $EMAIL != someone@somewhere ]; then
  if [ -f ./prefs/$EMAIL.patchseries ]; then
    eval `egrep '^FORM_[a-z0-9]*=[-+a-zA-Z0-9.: "]*;$' ./prefs/$EMAIL.patchseries`
  fi
fi
case $FORM_extend_method in
    none) none_checked=checked;;
    regr) regr_checked=checked;;
    *) bias_checked=checked;;
esac

cat <<EOF
</div>
<p>
<div class="formheader">Method</div>
<div class="formbody">
<input type="radio" class="formradio" name="extend_method" value="none" $none_checked>just add values from second series,<br>
<input type="radio" class="formradio" name="extend_method" value="bias" $bias_checked>first do a (seasonally dependent) bias correction,<br>
<input type="radio" class="formradio" name="extend_method" value="regr" $regr_checked>also correct the amplitude with a  linear regression.<br>
<br>
<input type="submit" class="formbutton" value="Extend">
</div>
</form>
EOF

. ./myvinkfoot.cgi
