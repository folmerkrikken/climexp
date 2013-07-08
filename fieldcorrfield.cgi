#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi

# off limits for search engines
. ./nosearchengine.cgi
# check email address
. ./checkemail.cgi
echo `date` "$EMAIL ($REMOTE_ADDR) $FORM_field" >> log/log

# start real work
. ./queryfield.cgi
if [ -z "$NPERYEAR" ]; then
  NPERYEAR=12
fi

NO_CSM=
myname=`basename $0 .cgi`
if [ "$myname" = "fieldcorrfield_obs" ]; then
  NO_REA=true
  NO_SEA=true
  NO_CO2=true
  NO_CSM=true
  NO_USE=true
  anotherfield="an observation field"
elif [ "$myname" = "fieldcorrfield_rea" ]; then
  NO_OBS=true
  NO_SEA=true
  NO_CO2=true
  NO_CSM=true
  NO_USE=true
  anotherfield="a reanalysis field"
elif [ "$myname" = "fieldcorrfield_sea" ]; then
  NO_OBS=true
  NO_REA=true
  NO_CO2=true
  NO_CSM=true
  NO_USE=true
  anotherfield="a seasonal forecast field"
elif [ "$myname" = "fieldcorrfield_co2" ]; then
  NO_OBS=true
  NO_REA=true
  NO_SEA=true
  NO_USE=true
  anotherfield="a scenario run field"
elif [ "$myname" = "fieldcorrfield_use" ]; then
  NO_OBS=true
  NO_REA=true
  NO_SEA=true
  NO_CO2=true
  NO_CSM=true
  anotherfield="a user-defined field"
else
  anotherfield="another field"
  NO_SEA=true
  NO_CO2=true
  NO_CSM=true
fi

. ./myvinkhead.cgi "Pointwise correlations with $anotherfield" "$kindname $climfield" "noindex,nofollow"

cat << EOF
<form action="correlate1.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="field1" value="$FORM_field">
EOF

if [ -z "$NO_OBS" ]; then
  echo '<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="4">Observations</th></tr>'
  sed -e "s/EMAIL/$EMAIL/" selectfield_obs.html 
  echo '</table>'
fi
hiddenstyle_erainterim="style=\"display: none;\""
hiddenstyle_era40="style=\"display: none;\""
hiddenstyle_ncepncar="style=\"display: none;\""
hiddenstyle_ncepdoe="style=\"display: none;\""
hiddenstyle_20c="style=\"display: none;\""

if [ -z "$NO_REA" ]; then
  echo '<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="8">Reanalyses</th></tr>'
  sed -e "s/hiddenstyle_erainterim/$hiddenstyle_erainterim/" \
    -e "s/hiddenstyle_era40/$hiddenstyle_era40/" \
    -e "s/hiddenstyle_ncepncar/$hiddenstyle_ncepncar/" \
    -e "s/hiddenstyle_ncepdoe/$hiddenstyle_ncepdoe/" \
    -e "s/hiddenstyle_20c/$hiddenstyle_20c/" \
    ./selectfield_rea.html
  echo '</table>'
fi
if [ -z "$NO_SEA" ]; then
  echo '<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="13">Seasonal forecasts ensemble means</th></tr>'
  cat $DIR/selectfield_sea.html
  echo '</table>'
fi
if [ -z "$NO_CSM" ]; then
  echo '<table class="realtable" width=451 border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="15">Scenario runs</th></tr>'
  fgrep -v getindices $DIR/selectfield_ipcc.html
  echo '</table>'
fi
if [ -z "$NO_USE" ]; then 
 . $DIR/selectuserfield.cgi
fi
echo '<div class="formheader">Plot options</div>'
echo '<div class="formbody">'
echo "<table style='width:451px' border='0' cellpadding='0' cellspacing='0'>"
echo "<tr valign="baseline"><td>Variable<td>"
. ./choosevariable.cgi
echo "<tr><td>Demand at least<td><input type=\"$number\" name=\"minfac\" value=\"$FORM_minfac\" $textsize2>% valid points"
intable=true
interpolate=true
probmask=true
. ./plotoptions.cgi
echo "</table>"
echo '</div>'

NAME="field"
station="$kindname $climfield"
timeseries="selected field"
index="second field"
. ./commonoptions.cgi

. ./myvinkfoot.cgi
