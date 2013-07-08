#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi

# check email address
. ./checkemail.cgi
# off-limits for robots
. ./nosearchengine.cgi
echo `date` "$EMAIL ($REMOTE_ADDR) statmodel $FORM_field" >> log/log

# start real work
. ./queryfield.cgi
eval `bin/getunits.sh $file`

. ./myvinkhead.cgi "Satistical model verification" "$kindname $climfield" "noindex,nofollow"

. ./getfieldtype.cgi

echo '<form action="statmodel.cgi" method="POST">'
echo "<input type=\"hidden\" name=\"EMAIL\" value=\"$EMAIL\">"
echo "<input type=\"hidden\" name=\"field1\" value=\"$FORM_field\">"
cat <<EOF
<table class=realtable width=451 border=0 cellspacing=0 cellpadding=0>
<tr><th colspan="2">Model paramaters</th></tr>
<tr><td width=100>Forecast initial conditions:</td>
<td><select class="forminput" name="analysis">
<option value="choose" $choose_selected>choose the forecast starting date</option>
<option value="jan" $jan_selected>1 January</option>
<option value="feb" $feb_selected>1 February</option>
<option value="mar" $mar_selected>1 March</option>
<option value="apr" $apr_selected>1 April</option>
<option value="may" $may_selected>1 May</option>
<option value="jun" $jun_selected>1 June</option>
<option value="jul" $jul_selected>1 July</option>
<option value="aug" $aug_selected>1 August</option>
<option value="sep" $sep_selected>1 September</option>
<option value="oct" $oct_selected>1 October</option>
<option value="nov" $nov_selected>1 November</option>
<option value="dec" $dec_selected>1 December</option>
</select></td></tr>
<tr><td width=100>Length of predictor season:</td>
<td><select class="forminput" name="sum2">
<option $sum2_choose_selected>choose</option>
<option $sum2_1_selected>1</option>
<option $sum2_2_selected>2</option>
<option $sum2_3_selected>3</option>
<option $sum2_4_selected>4</option>
<option $sum2_5_selected>5</option>
<option $sum2_6_selected>6</option>
<option $sum2_12_selected>12</option>
<option $sum2_24_selected>24</option>
<option $sum2_36_selected>36</option>
<option $sum2_60_selected>60</option>
</td></tr>
<tr><td width=100>Persistence:</td><td><input type=checkbox class=formcheck name=persistence></td></tr>
<tr><td width=100>Climatology:</td><td><input type=$number class=forminput $textsize2 name=onc> years running mean (0: all data)</td></tr>
<tr><td width=100>Predictor time series:</td><td>
<input type=radio class=formradio name=timeseries value=none>none,,
<input type=radio class=formradio name=timeseries value=nino34>Ni&ntilde;o3.4,
<input type=radio class=formradio name=timeseries value=co2>CO2
</td></tr>
<tr><td width=100>Ensemble members:</td><td><input type=$number name=nfcstens $textsize2></td></tr>
</table>
EOF
ENSEMBLE=true
echo "<table class=realtable border=0 cellspacing=0 cellpadding=0>"
echo "<tr><th colspan="4">Verifying $field_type field</th></tr>"
fgrep "$field_type" selectfield_obs.html  | sed -e "s/EMAIL/$EMAIL/"
fgrep "$field_type" selectfield_rea1.html | sed -e "s/EMAIL/$EMAIL/"
if [ -n "$ENSEMBLE" ]; then
  echo "<tr><td>$field_type</td><td><input type=\"radio\" class=\"formradio\" name=\"field\" value=\"perfectmodel\">perfect model</td><td>&nbsp;</td><td>&nbsp;</td></tr>"
fi
echo "</table>"

. $DIR/choose_mapverification.cgi
. $DIR/choose_verification.cgi
. $DIR/choose_threshold.cgi
cat <<EOF

<p><div class="formheader">Area</div>
<div class="formbody">
<table style='width:451px' border='0' cellpadding='0' cellspacing='0'>
EOF
intable=true
. ./plotoptions.cgi
if [ -n "$LSMASK" ]; then
  echo "<tr><td>Land-sea mask:<td>one day I\'ll implement a land-sea mask"
else
  echo "<tr><td>Land-sea mask:<td>Land/sea mask not yet available"
fi
echo '</table></div>'

timeseries="forecast"
index="observations"
justonemonth="T"
. $DIR/verifoptions.cgi

. ./myvinkfoot.cgi
