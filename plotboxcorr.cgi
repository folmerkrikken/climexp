#!/bin/sh

echo "Content-Type:text/html"
echo
echo

export DIR=`pwd`
. ./init.cgi
. ./getargs.cgi
# printenv
email="$EMAIL"
. ./nosearchengine.cgi
climate="$FORM_climate"
prog="$FORM_prog"
listname="$FORM_listname"
NPERYEAR="$FORM_nperyear"
extraargs="$FORM_extraargs"
if [ -n "$extraargs" ]; then
  NPERYEAR=`echo "$extraargs" | cut -f 1 -d '_'`
  extraname=`echo "$extraargs " | cut -f 2- -d '_' | tr '_' ' '`
fi
. ./nperyear2timescale.cgi

# check email address
. ./checkemail.cgi

if [ -z "$AUTOCOR" ]; then
. ./myvinkhead.cgi "Plot correlations" "$timescale $extraname$climate stations" "noindex,nofollow"
else
. ./myvinkhead.cgi "Plot autocorrelations" "$timescale $extraname$climate stations" "noindex,nofollow"
fi

echo '<form action="correlatebox.cgi" method="POST">'
echo "<input type=\"hidden\" name=\"email\" value=\"$email\">"
echo "<input type=\"hidden\" name=\"climate\" value=\"$timescale $extraname$climate\">"
echo "<input type=\"hidden\" name=\"shortclimate\" value=\"$climate\">"
echo "<input type=\"hidden\" name=\"prog\" value=\"$prog\">"
echo "<input type=\"hidden\" name=\"extraargs\" value=\"$extraargs\">"
echo "<input type=\"hidden\" name=\"listname\" value=\"$listname\">"
if [ -z "$AUTOCOR" ]; then
  if [ $EMAIL != someone@somewhere ]; then
    if [ -f ./prefs/$EMAIL.series.$NPERYEAR ]; then
      series=`head -1 ./prefs/$EMAIL.series.$NPERYEAR`
    fi
  fi
  . ./selecttimeseries.cgi | sed \
  -e 's;name="'$series'";name="'$series'" checked;' \
  -e 's/checkbox\" class=\"formcheck\" name/radio\" class=\"formradio\" name=\"timeseries\" value/' \
  -e 's/value=\"myindex[0-9]*\"//'
fi

. ./stationplotform.cgi

timeseries="timeseries"
index="index"
justonemonth="true"
NAME=$climate
station="stations"
. ./commonoptions.cgi

. ./myvinkfoot.cgi
