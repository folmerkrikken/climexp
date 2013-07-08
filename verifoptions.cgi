#!/bin/sh
# for pretty colours in emacs...

if [ -z "$NPERYEAR" ]; then
  NPERYEAR=12 # I hope
fi

if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
# read defaults if they exist
  if [ -f ./prefs/$EMAIL.verifoptions.$NPERYEAR ]; then
    eval `egrep '^FORM_[a-z0-9]*=[-+a-zA-Z0-9.: "]*;$' ./prefs/$EMAIL.verifoptions.$NPERYEAR`
  fi
fi

case ${FORM_month:--1} in
1) month_1_selected="selected";;
2) month_2_selected="selected";;
3) month_3_selected="selected";;
4) month_4_selected="selected";;
5) month_5_selected="selected";;
6) month_6_selected="selected";;
7) month_7_selected="selected";;
8) month_8_selected="selected";;
9) month_9_selected="selected";;
10) month_10_selected="selected";;
11) month_11_selected="selected";;
12) month_12_selected="selected";;
1:$NPERYEAR) month_all_selected="selected";;
0) month_0_selected="selected";;
*) month_m1_selected="selected";;
esac

case ${FORM_sum:-1} in
2) sum_2_selected="selected";;
3) sum_3_selected="selected";;
4) sum_4_selected="selected";;
5) sum_5_selected="selected";;
6) sum_6_selected="selected";;
7) sum_7_selected="selected";;
8) sum_8_selected="selected";;
9) sum_9_selected="selected";;
10) sum_10_selected="selected";;
11) sum_11_selected="selected";;
12) sum_12_selected="selected";;
24) sum_24_selected="selected";;
36) sum_36_selected="selected";;
48) sum_48_selected="selected";;
60) sum_60_selected="selected";;
120) sum_120_selected="selected";;
*) sum_1_selected="selected";;
esac

if [ -n "$FORM_detrend" ]; then
  detrend_checked="checked"
fi

case ${FORM_debias:-mean} in
none) debias_none=checked;;
var)  debias_var=checked;;
all)  debias_all=checked;;
*)    debias_mean=checked;;
esac

# too dangerous to leave off...
###if [ -n "$FORM_makeensfull" -o -z "$FORM_month" ]; then
  makeensfull_checked="checked"
###fi

if [ -z "$FORM_fcstname" -o "$FORM_fcstnameorg" != "$CLIM$kindname $station$climfield" ]; then
  FORM_fcstname="$CLIM$kindname $station$climfield"
fi

echo "<p><div class=\"formheader\">Options</div>"
echo "<div class=\"formbody\">"
if [ "$NPERYEAR" != 1 ]; then
  echo "<ul><li>"
  echo "Starting month"
  echo "<select class="forminput" name=\"month\">"
  if [ -z "$justonemonth" ]; then
    echo "<option value=\"1:12\" $month_all_selected>all"
  else
    echo "<option value=\"0\" $month_0_selected>together"
    echo "<option value=\"-1\" $month_m1_selected>anomalies"
  fi
  echo "<option value=\"1\" $month_1_selected>Jan"
  echo "<option value=\"2\" $month_2_selected>Feb"
  echo "<option value=\"3\" $month_3_selected>Mar"
  echo "<option value=\"4\" $month_4_selected>Apr"
  echo "<option value=\"5\" $month_5_selected>May"
  echo "<option value=\"6\" $month_6_selected>Jun"
  echo "<option value=\"7\" $month_7_selected>Jul"
  echo "<option value=\"8\" $month_8_selected>Aug"
  echo "<option value=\"9\" $month_9_selected>Sep"
  echo "<option value=\"10\" $month_10_selected>Oct"
  echo "<option value=\"11\" $month_11_selected>Nov"
  echo "<option value=\"12\" $month_12_selected>Dec"
  if [ -z "$justonemonth" ]; then
    echo "<option value=\"0\">together:"
    echo "<option value=\"0\" $month_0_selected>with seasons"
    echo "<option value=\"-1\" $month_m1_selected>anomalies"
  fi
  echo "</select>,"
echo "summing over"
echo "<select class="forminput" name=\"sum\">"
  echo "<option $sum_1_selected>1"
  echo "<option $sum_2_selected>2"
  echo "<option $sum_3_selected>3"
  echo "<option $sum_4_selected>4"
  echo "<option $sum_5_selected>5"
  echo "<option $sum_6_selected>6"
  echo "<option $sum_7_selected>7"
  echo "<option $sum_8_selected>8"
  echo "<option $sum_9_selected>9"
  echo "<option $sum_10_selected>10"
  echo "<option $sum_11_selected>11"
  echo "<option $sum_12_selected>12"
  echo "<option $sum_24_selected>24"
  echo "<option $sum_36_selected>36"
  echo "<option $sum_48_selected>48"
  echo "<option $sum_60_selected>60"
  echo "<option $sum_120_selected>120"
  echo "</select>months"
fi
cat <<EOF
<li>Begin year: <input type="$number" class="textinput" name="begin" $textsize4 value="$FORM_begin">
End year: <input type="$number" class="textinput" name="end" $textsize4 value="$FORM_end">
<li><input type="checkbox" class="formcheck" name="detrend" $detrend_checked>Detrend, 

<li>Remove bias in
<input type="radio" class="formradio" name="debias" value="none" $debias_none>nothing,
<input type="radio" class="formradio" name="debias" value="mean" $debias_mean>mean,
<input type="radio" class="formradio" name="debias" value="var" $debias_var>mean and variance,
<input type="radio" class="formradio" name="debias" value="all" $debias_all>whole PDF.

EOF


if [ -n "$ENSEMBLE" ]; then
cat <<EOF
<li>Ensemble members 
<input type="$number" name="nens1" $textsize2 value="$FORM_nens1">
to
<input type="$number" name="nens2" $textsize2 value="$FORM_nens2">
<li><input type="checkbox" class="formcheck" name="makeensfull" $makeensfull_checked>Replicate ensemble members to get the same number for each time step
EOF
fi
cat <<EOF 
<li>Name on plots
<input type="text" size="40" name="fcstname" value="$FORM_fcstname">
<input type="hidden" name="fcstnameorg" value="$CLIM$kindname $station$climfield">
</ul>
<input type="submit" class="formbutton" value="Verify">
</div>
</form>
EOF
