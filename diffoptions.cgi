#!/bin/sh
# for pretty colours in emacs...

if [ -z "$NPERYEAR" ]; then
  NPERYEAR=12 # I hope
fi

if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
    # read defaults if they exist
    def=./prefs/$EMAIL.diffoptions.$NPERYEAR
    if [ -f $def ]; then
        eval `egrep '^FORM_[a-z0-9]*=[-+a-zA-Z0-9.: "]*;$' $def`
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

case ${FORM_var:-diff} in
reldiff) reldiff_checked=checked;;
*)       diff_checked=checked;;
esac

cat <<EOF
<p><div class="formheader">Difference options</div>
<div class="formbody">
<table width=451>
<tr><td>Difference:</td><td><input type="radio" class="formradio" name="var" value="diff" $diff_checked>absolute
<input type="radio" class="formradio" name="var" value="reldiff" $reldiff_checked>relative</td></tr>
<tr>
EOF
if [ "$NPERYEAR" = 1 ]; then
  echo "<!-- no seasons -->"
elif [ $NPERYEAR = 2 ]; then
  echo "<td>Starting half year:</td>"
  echo "<td><select class="forminput" name=\"month\">"
  if [ -z "$justonemonth" ]; then
    echo "<option value=\"1:2\" $month_all_selected>all"
  else
    echo "<option value=\"0\" $month_0_selected>together"
  fi
  echo "<option value=\"1\" $month_1_selected>October-March"
  echo "<option value=\"2\" $month_2_selected>April-September"
  if [ -z "$justonemonth" ]; then
    echo "<option value=\"0\">together"
  fi
  echo "</select>,"
  if [ $field_type = Precipitation ]; then
    echo "summing over"
  else
    echo "averaging"
  fi
  echo "<select class="forminput" name=\"sum\">"
  echo "<option $sum_1_selected>1"
  echo "<option $sum_2_selected>2"
  echo "</select>half years</td></tr>"
elif [ $NPERYEAR = 4 ]; then
  echo "<td>Starting season:</td>"
  echo "<td><select class="forminput" name=\"month\">"
  if [ -z "$justonemonth" ]; then
    echo "<option value=\"1:12\" $month_all_selected>all"
  else
    echo "<option value=\"0\" $month_0_selected>together"
  fi
  echo "<option value=\"1\" $month_1_selected>DJF"
  echo "<option value=\"2\" $month_2_selected>MAM"
  echo "<option value=\"3\" $month_3_selected>JJA"
  echo "<option value=\"4\" $month_4_selected>SON"
  if [ -z "$justonemonth" ]; then
    echo "<option value=\"0\">together:"
    echo "<option value=\"0\" $month_0_selected>with seasons"
    echo "<option value=\"-1\" $month_m1_selected>anomalies"
  fi
  echo "</select>,"
  if [ $field_type = Precipitation ]; then
    echo "summing over"
  else
    echo "averaging"
  fi
  echo "<select class="forminput" name=\"sum\">"
  echo "<option $sum_1_selected>1"
  echo "<option $sum_2_selected>2"
  echo "<option $sum_3_selected>3"
  echo "<option $sum_4_selected>4"
  echo "</select>seasons</td></tr>"
else
  echo "<td>Starting month:</td>"
  echo "<td><select class="forminput" name=\"month\">"
  if [ -z "$justonemonth" ]; then
    echo "<option value=\"1:12\" $month_all_selected>all"
  else
    echo "<option value=\"0\" $month_0_selected>together"
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
  if [ $field_type = Precipitation ]; then
    echo "summing over"
  else
    echo "averaging"
  fi
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
  echo "</select>months</td></tr>"
fi
cat <<EOF
<tr><td>First field:</td><td>years <input type="$number" min=1 max=2500 step=1 name="begin" $textsize4 value="$FORM_begin">-<input type="$number" min=1 max=2500 step=1 name="end" $textsize4 value="$FORM_end"> ($kindname $climfield)</td></tr>
<tr><td>Second field:</td><td>years <input type="$number" min=1 max=2500 step=1 name="begin2" $textsize4 value="$FORM_begin2">-<input type="$number" min=1 max=2500 step=1 name="end2" $textsize4 value="$FORM_end2"> (default: same)</td></tr>
<tr><td colspan="2"><input type="submit" class="formbutton" value="Plot difference"></td></tr>
</table>
</div>
</form>
EOF
