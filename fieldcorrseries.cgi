#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi

# no robots
. ./nosearchengine.cgi
# check email address
. ./checkemail.cgi
echo `date` "$EMAIL ($REMOTE_ADDR) $FORM_field" >> log/log

# start real work
. ./queryfield.cgi

. ./myvinkhead.cgi "Correlate with a time series" "$kindname $climfield" "noindex,nofollow"

eval `./bin/getunits.sh $file`

echo '<form action="correlate1.cgi" method="POST">'
echo "<input type=\"hidden\" name=\"EMAIL\" value=\"$EMAIL\">"
echo "<input type=\"hidden\" name=\"field1\" value=\"$FORM_field\">"

if [ $EMAIL != someone@somewhere ]; then
  if [ -f ./prefs/$EMAIL.series.$NPERYEAR ]; then
    series=`tail -1 ./prefs/$EMAIL.series.$NPERYEAR`
  fi
fi
. ./selecttimeseries.cgi | sed \
-e 's;="'$series'";="'$series'" checked;' \
-e 's/checkbox\" class=\"formcheck\" name/radio\" class=\"formradio\" name=\"timeseries\" value/' \
-e 's/value=\"myindex[0-9]*\"//' \
#-e '/sunlength/d'

echo "<p><div class=\"formheader\">Plot options</div>"
echo "<div class=\"formbody\">"
echo "<table style='width:451px' border='0' cellpadding='0' cellspacing='0'>"
echo "<tr><td>Variable<td>"
. ./choosevariable.cgi
echo "<tr><td>Demand at least<td><input type=\"$number\" name=\"minfac\" value=\"$FORM_minfac\" $textsize2>% valid points"
intable=true
probmask=true
lsmask=yes
. ./plotoptions.cgi
echo "</table>"
echo "</div>"
NAME="field"
station="$kindname $climfield"
timeseries="selected field"
index="time series"
echo '<p>'
. ./commonoptions.cgi

. ./myvinkfoot.cgi
