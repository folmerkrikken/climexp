#!/bin/sh
if [ $EMAIL != someone@somewhere ]; then
  if [ -f ./prefs/$EMAIL.commonoptions.$NPERYEAR ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.:]*;$' ./prefs/$EMAIL.commonoptions.$NPERYEAR`
  fi

  case ${FORM_month:-0} in
  0)  month_0="selected";;
  1)  month_1="selected";;
  2)  month_2="selected";;
  3)  month_3="selected";;
  4)  month_4="selected";;
  5)  month_5="selected";;
  6)  month_6="selected";;
  7)  month_7="selected";;
  8)  month_8="selected";;
  9)  month_9="selected";;
  10) month_10="selected";;
  11) month_11="selected";;
  12) month_12="selected";;
  *)  month_a="selected";;
  esac

  case ${FORM_sum:-1} in
  2)  sum_2="selected";;
  3)  sum_3="selected";;
  4)  sum_4="selected";;
  5)  sum_5="selected";;
  6)  sum_6="selected";;
  7)  sum_7="selected";;
  8)  sum_8="selected";;
  9)  sum_9="selected";;
  10) sum_10="selected";;
  11) sum_11="selected";;
  12) sum_12="selected";;
  *)  sum_1="selected";;
  esac

  [ -n "$FORM_anomal" ]  && anomal_checked="checked"
  [ -n "$FORM_ensanom" ]  && ensanom_checked="checked"
  [ -n "$FORM_log" ]     && log_checked="checked"
  [ -n "$FORM_sqrt" ]    && sqrt_checked="checked"
  [ -n "$FORM_square" ]  && square_checked="checked"
  [ -n "$FORM_diff" ]    && diff_checked="checked"
  [ -n "$FORM_detrend" ] && detrend_checked="checked"

  case ${FORM_subsum:-1} in
  -1) subsum_m="selected";;
  *)  subsum_p="selected";;
  esac

fi

if [ -n "$FORM_field" ]; then
  seriesfield=field
else
  seriesfield=series
fi

if [ ${NPERYEAR:-12} -ge 12 ]; then
cat << EOF
<tr><td>Starting month: <td><select class=forminput name="month">
<option value="0" $month_0>together
EOF
if [ -z "$justonemonth" ]; then
  echo "<option value=\"1:12\" $month_a>all"
fi
cat <<EOF
<option value="1" $month_1>Jan
<option value="2" $month_2>Feb
<option value="3" $month_3>Mar
<option value="4" $month_4>Apr
<option value="5" $month_5>May
<option value="6" $month_6>Jun
<option value="7" $month_7>Jul
<option value="8" $month_8>Aug
<option value="9" $month_9>Sep
<option value="10" $month_10>Oct
<option value="11" $month_11>Nov
<option value="12" $month_12>Dec
</select>,
<select class=forminput name="operation">
<option>averaging
<option>selecting
</select> over
EOF
if [ ${NPERYEAR:-12} -eq 12 ]; then
cat <<EOF
<select class=forminput name="sum">
<option $sum_1>1
<option $sum_2>2
<option $sum_3>3
<option $sum_4>4
<option $sum_5>5
<option $sum_6>6
<option $sum_7>7
<option $sum_8>8
<option $sum_9>9
<option $sum_10>10
<option $sum_11>11
<option $sum_12>12
</select>month(s),
EOF
timeunit="month(s)"
elif [ $NPERYEAR -ge 360 -a $NPERYEAR -le 366 ]; then
echo "<input type=$number name=sum value=\"${FORM_sum:-1}\" $textsize4>days"
timeunit="days(s)"
else
echo "<input type=$number name=sum value=\"${FORM_sum:-1}\" $textsize4>periods"
timeunit="periods"
fi
fi
if [ "$NPERYEAR" = 4 ]; then
cat <<EOF
<tr><td>Starting month: <td><select class=forminput name="month">
<option value="0" $month_0>together
<option value="1" $month_1>DJF
<option value="2" $month_2>MAM
<option value="3" $month_3>JJA
<option value="4" $month_4>SON
</select>,
<select class=forminput name="operation"><option>averaging<option>selecting</select> over
<select class=forminput name="sum">
<option $sum_1>1
<option $sum_2>2
<option $sum_3>3
<option $sum_4>4
</select>seasons(s),
EOF
timunit="season(s)"
fi
cat <<EOF
<tr><td>Anomalies: <td><input type="checkbox" class="formcheck" name="anomal" $anomal_checked>
<tr><td>Begin year: <td><input type="$number" name="begin" $textsize4 value="$FORM_begin">
End year: <input type="$number" name="end" $textsize4 value="$FORM_end">
<tr><td>Only for: <td><input type="$number" step=any name="gt" $textsize4 value="$FORM_gt"> &lt; $seriesfield &lt; 
<input type="$number" step=any name="lt" $textsize4 value="$FORM_lt">
<tr><td>Apply: <td><input type="checkbox" class="formcheck" name="log" $log_checked>log, 
<input type="checkbox" class="formcheck" name="sqrt" $sqrt_checked>sqrt,
<input type="checkbox" class="formcheck" name="square" $square_checked>square,
<input type="checkbox" class="formcheck" name="diff" $diff_checked>year-on-year difference
<tr><td>
Filter: <td><select class=forminput name="subsum">
<option value="1" $subsum_p>subtract mean of
<option value="-1" $subsum_m>average with
</select>
<input type="$number" name="ndiff" $textsize3 value="$FORM_ndiff"> previous years on all data
<tr><td>Detrend: <td><input type="checkbox" class="formcheck" name="detrend" $detrend_checked>
EOF
if [ -n "$ENSEMBLE" ]; then
cat <<EOF
<tr><td>Ensemble members:<td> 
<input type="$number" class="forminput" name="nens1" value="$FORM_nens1" $textsize2>
to
<input type="$number" class="forminput" name="nens2" value="$FORM_nens2" $textsize2>
<tr><td>Anomalies relative to the ensemble mean:<td><input type="checkbox" class="formcheck" name="ensanom" $ensanom_checked>
EOF
fi
