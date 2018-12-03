#!/bin/bash
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./init.cgi
. ./getargs.cgi

# check email address
. ./checkemail.cgi
# off limits for search engines
. ./nosearchengine.cgi
echo `date` "$EMAIL ($REMOTE_ADDR) fieldcorrelate $FORM_field" >> log/log

# start real work
. ./queryfield.cgi

myname=`basename $0 .cgi`
if [ "$myname" = "fieldcorrfield1_obs" ]; then
  NO_REA=true
  NO_SEA=true
  NO_CO2=true
  NO_USE=true
  anotherfield="an observation field"
elif [ "$myname" = "fieldcorrfield1_rea" ]; then
  NO_OBS=true
  NO_SEA=true
  NO_CO2=true
  NO_USE=true
  anotherfield="a reanalysis field"
elif [ "$myname" = "fieldcorrfield1_sea" ]; then
  NO_OBS=true
  NO_REA=true
  NO_CO2=true
  NO_USE=true
  anotherfield="a seasonal forecast field"
elif [ "$myname" = "fieldcorrfield1_co2" ]; then
  NO_OBS=true
  NO_REA=true
  NO_SEA=true
  NO_USE=true
  anotherfield="a seasonal forecast field"
elif [ "$myname" = "fieldcorrfield1_use" ]; then
  NO_OBS=true
  NO_REA=true
  NO_SEA=true
  NO_CO2=true
  anotherfield="a user-defined field"
else
  anotherfield="another field"
fi

. ./myvinkhead.cgi "Spatial correlations with $anotherfield" "$kindname $climfield"

echo '<form action="fieldcorrelate.cgi" method="POST">'
echo "<input type=\"hidden\" name=\"EMAIL\" value=\"$EMAIL\">"
echo "<input type=\"hidden\" name=\"field1\" value=\"$FORM_field\">"

if [ -z "$NO_OBS" ]; then
  echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="2">Observations</th></tr>'
  sed -e "s/EMAIL/$EMAIL/" selectfield_obs.html 
  echo '</table>'
fi
if [ -z "$NO_REA" ]; then
  echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="8">Reanalyses</th></tr>'
  cat $DIR/selectfield_rea.html
  echo '</table>'
fi
if [ -z "$NO_SEA" ]; then
  echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="13">Seasonal forecasts ensemble means</th></tr>'
  cat $DIR/selectfield_sea.html
  echo '</table>'
fi
if [ -z "$NO_CO2" ]; then
  echo '<table class="realtable" width="100%" border=0 cellspacing=0 cellpadding=0>'
  echo '<tr><th colspan="15">Scenario runs</th></tr>'
  fgrep -v getindices $DIR/selectfield_ipcc.html
  echo '</table>'
fi
if [ -z "$NO_USE" ]; then 
 . $DIR/selectuserfield.cgi
fi
cat <<EOF
<p><div class="formheader">Output options</div>
<div class="formbody">Give
EOF
. ./choosevariable.cgi
cat <<EOF
<br>
with at least <input type="$number" name="minfac" $default $textsize2>% valid points
</div>
<p><div class="formheader">Options</div>
<div class="formbody">Only consider the area
<input type="$number" step=any name="lat1" $textsize4>&deg;N to <input type="$number" step=any name="lat2" $textsize4>&deg;N, <input type="$number" step=any name="lon1" $textsize4>&deg;E to <input type="$number" step=any name="lon2" $textsize4>&deg;E.<br>
Interpolate to <select name="intertype">
<option value="high">finest
<option value="low">coarsest
<option value="1">first
<option value="2">second
</select> grid<br>
EOF
echo "Average over"
echo "<select name=\"sum\">"
echo "<option selected>1"
echo "<option>2"
echo "<option>3"
echo "<option>4"
echo "<option>5"
echo "<option>6"
echo "<option>7"
echo "<option>8"
echo "<option>9"
echo "<option>10"
echo "<option>11"
echo "<option>12"
echo "<option>13"
#echo "<option>18"
#echo "<option>24"
#echo "<option>36"
#echo "<option>48"
#echo "<option>60"
#echo "<option>120"
echo "</select>month(s) of the first field, "
echo "<select name=\"sum2\">"
echo "<option selected value=\"\">same"
echo "<option>1"
echo "<option>2"
echo "<option>3"
echo "<option>4"
echo "<option>5"
echo "<option>6"
echo "<option>7"
echo "<option>8"
echo "<option>9"
echo "<option>10"
echo "<option>11"
echo "<option>12"
echo "<option>13"
#echo "<option>18"
#echo "<option>24"
#echo "<option>36"
#echo "<option>48"
#echo "<option>60"
#echo "<option>120"
echo "</select>month(s) of the second one,<br>"
echo "lag: <select name=\"lag\">"
echo "<option>-120:0"
echo "<option>-120"
echo "<option>-84"
echo "<option>-60:0"
echo "<option>-60"
echo "<option>-48"
echo "<option>-36"
echo "<option>-24:0"
echo "<option>-24:24"
echo "<option>-24"
echo "<option>-18"
echo "<option>-12:0"
echo "<option>-12:12"
echo "<option>-12"
echo "<option>-11"
echo "<option>-10"
echo "<option>-9"
echo "<option>-8"
echo "<option>-7"
echo "<option>-6"
echo "<option>-6:6"
echo "<option>-5"
echo "<option>-4"
echo "<option>-3"
echo "<option>-2"
echo "<option>-1"
echo "<option selected>0"
echo "<option>1"
echo "<option>2"
echo "<option>3"
echo "<option>4"
echo "<option>5"
echo "<option>6"
echo "<option>7"
echo "<option>8"
echo "<option>9"
echo "<option>10"
echo "<option>11"
echo "<option>12"
echo "<option>0:12"
echo "<option>18"
echo "<option>24"
echo "<option>0:24"
echo "<option>36"
echo "<option>48"
echo "<option>60"
echo "<option>0:60"
echo "<option>-60:60"
echo "<option>72"
echo "<option>84"
echo "<option>96"
echo "<option>108"
echo "<option>120"
echo "<option>0:120"
echo "<option>-120:120"
echo "<option>132"
echo "<option>144"
echo "</select>months"
echo "(lag positive: first field lagging second one)<br>"
echo "<input type=\"checkbox\" name=\"anomal\" checked>Take anomaliesi ww.r.t the seasonal cycle first"
echo "<p>"
echo "<input type=\"submit\" class=\"formbutton\" value=\"Correlate\">"
echo "</div>"
echo "</form>"

. ./myvinkfoot.cgi

