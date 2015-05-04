#!/bin/sh
# for pretty colours in emacs...

if [ -z "$NPERYEAR" ]; then
  NPERYEAR=12 # I hope
fi
if [ $NPERYEAR = 1 ]; then
  period=year
elif [ $NPERYEAR = 4 ]; then
  period="season"
elif [ $NPERYEAR = 12 ]; then
  period="month"
elif [ $NPERYEAR = 360 -o $NPERYEAR -eq 365 -o $NPERYEAR -eq 366 ]; then
  period="day"
else
  period="period"
fi
echo "<input type=\"hidden\" name=\"NPERYEAR\" value=\"$NPERYEAR\">"
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
# read defaults if they exist
  if [ -f ./prefs/$EMAIL.commonoptions.$NPERYEAR ]; then
	eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.:]*;$' ./prefs/$EMAIL.commonoptions.$NPERYEAR`
  fi
fi

case ${FORM_whichvar:-corr} in
	regr) regr_checked=checked;;
	*)	  corr_checked=checked;;
esac

case ${FORM_fix:-fix1} in
fix2) fix2_selected="selected";;
*)	  fix1_selected="selected";;
esac

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

case ${FORM_operation:-averaging} in
selecting)	 selecting_selected="selected";;
*)			 averaging_selected="selected";;
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
13) sum_13_selected="selected";;
14) sum_14_selected="selected";;
15) sum_15_selected="selected";;
20) sum_20_selected="selected";;
25) sum_25_selected="selected";;
30) sum_30_selected="selected";;
40) sum_40_selected="selected";;
45) sum_45_selected="selected";;
60) sum_60_selected="selected";;
*) sum_1_selected="selected";;
esac

case ${FORM_sel:-1} in
2) sel_2_selected="selected";;
3) sel_3_selected="selected";;
4) sel_4_selected="selected";;
5) sel_5_selected="selected";;
6) sel_6_selected="selected";;
7) sel_7_selected="selected";;
8) sel_8_selected="selected";;
9) sel_9_selected="selected";;
10) sel_10_selected="selected";;
11) sel_11_selected="selected";;
12) sel_12_selected="selected";;
15) sel_15_selected="selected";;
20) sel_20_selected="selected";;
25) sel_25_selected="selected";;
30) sel_30_selected="selected";;
40) sel_40_selected="selected";;
45) sel_45_selected="selected";;
60) sel_60_selected="selected";;
*) sel_1_selected="selected";;
esac

case ${FORM_sum2:-same} in
1) sum2_1_selected="selected";;
2) sum2_2_selected="selected";;
3) sum2_3_selected="selected";;
4) sum2_4_selected="selected";;
5) sum2_5_selected="selected";;
6) sum2_6_selected="selected";;
7) sum2_7_selected="selected";;
8) sum2_8_selected="selected";;
9) sum2_9_selected="selected";;
10) sum2_10_selected="selected";;
11) sum2_11_selected="selected";;
12) sum2_12_selected="selected";;
15) sum2_15_selected="selected";;
20) sum2_20_selected="selected";;
25) sum2_25_selected="selected";;
30) sum2_30_selected="selected";;
40) sum2_40_selected="selected";;
45) sum2_45_selected="selected";;
60) sum2_60_selected="selected";;
*) sum2_same_selected="selected";;
esac

case ${FORM_lag:-0} in
"-240:240") lag_m240t240_selected="selected";;
"-240:0") lag_m240t0_selected="selected";;
"-240") lag_m240_selected="selected";;
"-156") lag_m156_selected="selected";;
"-120:120") lag_m120t120_selected="selected";;
"-120:0") lag_m120t0_selected="selected";;
"-120") lag_m120_selected="selected";;
"-84") lag_m84_selected="selected";;
"-60:60") lag_m60t60_selected="selected";;
"-60:0") lag_m60t0_selected="selected";;
"-60") lag_m60_selected="selected";;
"-48") lag_m48_selected="selected";;
"-36") lag_m36_selected="selected";;
"-24:0") lag_m24t0_selected="selected";;
"-24:24") lag_m24t24_selected="selected";;
"-24") lag_m24_selected="selected";;
"-18") lag_m18_selected="selected";;
"-12:0") lag_m12t0_selected="selected";;
"-12:12") lag_m12t12_selected="selected";;
"-12") lag_m12_selected="selected";;
"-11") lag_m11_selected="selected";;
"-10") lag_m10_selected="selected";;
"-9") lag_m9_selected="selected";;
"-8") lag_m8_selected="selected";;
"-7") lag_m7_selected="selected";;
"-6") lag_m6_selected="selected";;
"-6:6") lag_m6t6_selected="selected";;
"-5") lag_m5_selected="selected";;
"-4") lag_m4_selected="selected";;
"-3") lag_m3_selected="selected";;
"-2") lag_m2_selected="selected";;
"-1") lag_m1_selected="selected";;
"1") lag_1_selected="selected";;
"2") lag_2_selected="selected";;
"3") lag_3_selected="selected";;
"4") lag_4_selected="selected";;
"5") lag_5_selected="selected";;
"6") lag_6_selected="selected";;
"7") lag_7_selected="selected";;
"8") lag_8_selected="selected";;
"9") lag_9_selected="selected";;
"10") lag_10_selected="selected";;
"11") lag_11_selected="selected";;
"12") lag_12_selected="selected";;
"0:12") lag_0t12_selected="selected";;
"18") lag_18_selected="selected";;
"24") lag_24_selected="selected";;
"0:24") lag_0t24_selected="selected";;
"36") lag_36_selected="selected";;
"48") lag_48_selected="selected";;
"60") lag_60_selected="selected";;
"0:60") lag_0t60_selected="selected";;
"-60:60") lag_m60t60_selected="selected";;
"72") lag_72_selected="selected";;
"84") lag_84_selected="selected";;
"96") lag_96_selected="selected";;
"108") lag_108_selected="selected";;
"120") lag_120_selected="selected";;
"0:120") lag_0t120_selected="selected";;
"-120:120") lag_m120t120_selected="selected";;
"132") lag_132_selected="selected";;
"144") lag_144_selected="selected";;
*) lag_0_selected="selected";;
esac

if [ -n "$FORM_anomal" ]; then
  anomal_checked="checked"
fi

if [ -n "$FORM_log" ]; then
  log_checked="checked"
fi
if [ -n "$FORM_sqrt" ]; then
  sqrt_checked="checked"
fi
if [ -n "$FORM_square" ]; then
  square_checked="checked"
fi
if [ -n "$FORM_twothird" ]; then
  twothird_checked="checked"
fi
if [ -n "$FORM_rank" ]; then
  rank_checked="checked"
fi
if [ -n "$FORM_conting" ]; then
  conting_checked="checked"
fi
if [ -n "$FORM_detrend" ]; then
  detrend_checked="checked"
fi
if [ -n "$FORM_diff" ]; then
  diff_checked="checked"
fi
if [ -n "$FORM_nooverlap" ]; then
  nooverlap_checked="checked"
fi

case $FORM_subsum in
-1) subsum_m="selected";;
*)	subsum_p="selected";;
esac

if [ -n "$FORM_runcorr" ]; then
  runcorr_checked="checked"
fi

case ${FORM_runvar:-correlation} in
regression) runvar_regression_selected="selected";;
*)			runvar_correlation_selected="selected";;
esac

case ${FORM_random:-series} in
index) random_index_selected="selected";;
*)	   random_series_selected="selected";;
esac

case ${FORM_noisetype:-white} in
red) red_selected="selected";;
*)	 white_selected="selected";;
esac

case ${FORM_fitfunc:-linear} in
quadratic) quadratic_checked="checked";;
cubic) cubic_checked="checked";;
fittime) fittime_checked="checked";;
fittime_quadratic) fittime_quadratic="checked";;
phase) phase_checked="checked";;
*) linear_checked="checked";;
esac

if [ -n "$FORM_ensanom" ]; then
  ensanom_checked="checked"
fi
if [ -n "$FORM_makeensfull" ]; then
  makeensfull_checked="checked"
fi

if [ -z "$ONLYONE" ]; then
	echo "<p><div class=\"formheader\">Options</div>"
	echo "<div class=\"formbody\">"
	echo "<table style='width:451px' border='0' cellpadding='0' cellspacing='0'>"
fi
if [ "$whichvar" = true ]; then
	echo "<tr><td>Variable:<td>"
	echo "<input type="radio" class="formradio" name="whichvar" value="corr" $corr_checked>correlation coefficient, "
	echo "<input type="radio" class="formradio" name="whichvar" value="regr" $regr_checked>regression"
fi
echo "<tr><td>"
if [ $NPERYEAR = 1 ]; then
  echo "<input type=hidden name=month value=1>"
elif [ $NPERYEAR = 2 ]; then
  echo "Starting season: <td>"
  echo "<select class="forminput" name=\"month\">"
  if [ -z "$justonemonth" ]; then
	echo "<option value=\"1:$NPERYEAR\" $month_all_selected>all"
  fi
  echo "<option value=\"1\" $month_1_selected>Oct-Mar"
  echo "<option value=\"2\" $month_2_selected>Apr-Sep"
  echo "<option value=\"0\" $month_0_selected>together"
  echo "</select>"
  if [ -z "$ONLYONE" ]; then
	  echo "of <select class=\"forminput\" name=\"fix\">"
	  echo "<option value=\"fix1\" $fix1_selected>$timeseries"
	  echo "<option value=\"fix2\" $fix2_selected>$index selected above"
  fi
  echo "</select><td><a href=\"javascript:pop_page('help/selectseason2.shtml',568,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
  echo "<tr><td>Season:<td><select class=\"forminput\" name=\"operation\"><option $averaging_selected>averaging<option $selecting_selected>selecting</select> over"
  echo "<select class=\"forminput\" name=\"sum\">"
  echo "<option $sum_1_selected>1"
  echo "<option $sum_2_selected>2"
  echo "</select>half years"
  [ -z "$ONLYONE" ] && echo " of the $timeseries"
elif [ $NPERYEAR = 4 ]; then
  echo "Starting season: <td>"
  echo "<select class="forminput" name=\"month\">"
  if [ -z "$justonemonth" ]; then
	echo "<option value=\"1:$NPERYEAR\" $month_all_selected>all"
  fi
  echo "<option value=\"1\" $month_1_selected>DJF"
  echo "<option value=\"2\" $month_2_selected>MAM"
  echo "<option value=\"3\" $month_3_selected>JJA"
  echo "<option value=\"4\" $month_4_selected>SON"
  echo "<option value=\"0\" $month_0_selected>together"
  echo "</select>"
  if [ -z "$ONLYONE" ]; then
	  echo "of <select class=\"forminput\" name=\"fix\">"
	  echo "<option value=\"fix1\" $fix1_selected>$timeseries"
	  echo "<option value=\"fix2\" $fix2_selected>$index selected above"
  fi
  echo "</select><td><a href=\"javascript:pop_page('help/selectseason4.shtml',568,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
  echo "<tr><td>Season:<td><select class=\"forminput\" name=\"operation\"><option $averaging_selected>averaging<option $selecting_selected>selecting</select> over"
  echo "<select class=\"forminput\" name=\"sum\">"
  echo "<option $sum_1_selected>1"
  echo "<option $sum_2_selected>2"
  echo "<option $sum_3_selected>3"
  echo "<option $sum_4_selected>4"
  echo "</select>seasons"
  [ -z "$ONLYONE" ] && echo " of the $timeseries"
elif [ $NPERYEAR -ge 12 ]; then
  echo "Starting month: <td>"
  echo "<select class=\"forminput\" name=\"month\">"
  if [ -z "$justonemonth" ]; then
	echo "<option value=\"1:12\" $month_all_selected>all"
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
  echo "<option value=\"0\" $month_0_selected>together"
  echo "</select>"
  if [ -z "$ONLYONE" ]; then
	  echo "of <select class=\"forminput\" name=\"fix\">"
	  echo "<option value=\"fix1\" $fix1_selected>$timeseries"
	  echo "<option value=\"fix2\" $fix2_selected>$index selected above</select>"
  fi
  if [ "$NPERYEAR" = 12 ]; then
	echo "<td><a href=\"javascript:pop_page('help/selectseason12.shtml',568,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
  elif [ "$NPERYEAR" = 360 -o "$NPERYEAR" = 365 -o "$NPERYEAR" = 366 ]; then
	echo "<td><a href=\"javascript:pop_page('help/selectseason365.shtml',568,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
  else
	echo "</select><td><a href=\"javascript:pop_page('help/selectseason.shtml',568,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"

  fi
  echo "<tr><td>Season:<td>"
  if [ "$NPERYEAR" != 12 ]; then
	echo "selecting <select class=\"forminput\" name=\"sel\">"
	echo "<option $sel_1_selected>1"
	echo "<option $sel_2_selected>2"
	echo "<option $sel_3_selected>3"
	echo "<option $sel_4_selected>4"
	echo "<option $sel_5_selected>5"
	echo "<option $sel_6_selected>6"
	echo "<option $sel_7_selected>7"
	echo "<option $sel_8_selected>8"
	echo "<option $sel_9_selected>9"
	echo "<option $sel_10_selected>10"
	echo "<option $sel_11_selected>11"
	echo "<option $sel_12_selected>12"
  else
	echo "<select class=\"forminput\" name=\"operation\"><option $averaging_selected>averaging<option $selecting_selected>selecting</select> over"
	echo "<select class=\"forminput\" name=\"sum\">"
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
	if [ $EMAIL = oldenbor@knmi.nl ]; then
	    echo "<option $sum_13_selected>13"
	    echo "<option $sum_14_selected>14"
	fi
  #echo "<option>13"
  #echo "<option>18"
  #echo "<option>24"
  #echo "<option>36"
  #echo "<option>48"
  #echo "<option>60"
  #echo "<option>120"
  fi
  echo "</select>month(s)"
  [ -z "$ONLYONE" ] && echo " of the $timeseries"
fi
if [ $NPERYEAR = 12 ]; then
	if [ -z "$ONLYONE" ]; then
		echo "<select class="forminput" name=\"sum2\">"
		echo "<option $sum2_same_selected value=\"\">same"
		echo "<option $sum2_1_selected>1"
		echo "<option $sum2_2_selected>2"
		echo "<option $sum2_3_selected>3"
		echo "<option $sum2_4_selected>4"
		echo "<option $sum2_5_selected>5"
		echo "<option $sum2_6_selected>6"
		echo "<option $sum2_7_selected>7"
		echo "<option $sum2_8_selected>8"
		echo "<option $sum2_9_selected>9"
		echo "<option $sum2_10_selected>10"
		echo "<option $sum2_11_selected>11"
		echo "<option $sum2_12_selected>12"
#echo "<option>13"
#echo "<option>18"
#echo "<option>24"
#echo "<option>36"
#echo "<option>48"
#echo "<option>60"
#echo "<option>120"
		echo "</select>month(s) of the $index,"
	fi
else
	echo "<tr><td>Running mean:<td>"
	echo "<select class=\"forminput\" name=\"sum\">"
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
	echo "<option $sum_15_selected>15"
	echo "<option $sum_20_selected>20"
	echo "<option $sum_25_selected>25"
	echo "<option $sum_30_selected>30"
	echo "<option $sum_40_selected>40"
	echo "<option $sum_45_selected>45"
	echo "<option $sum_60_selected>60"
	echo "</select>$period(s)"
	if [ -z "$ONLYONE" ]; then
		echo " of the $timeseries,<br>"
		echo "<select class=\"forminput\" name=\"sum2\">"
		echo "<option $sum2_same_selected value=\"\">same"
		echo "<option $sum2_1_selected>1"
		echo "<option $sum2_2_selected>2"
		echo "<option $sum2_3_selected>3"
		echo "<option $sum2_4_selected>4"
		echo "<option $sum2_5_selected>5"
		echo "<option $sum2_6_selected>6"
		echo "<option $sum2_7_selected>7"
		echo "<option $sum2_8_selected>8"
		echo "<option $sum2_9_selected>9"
		echo "<option $sum2_10_selected>10"
		echo "<option $sum2_15_selected>15"
		echo "<option $sum2_20_selected>20"
		echo "<option $sum2_25_selected>25"
		echo "<option $sum2_30_selected>30"
		echo "<option $sum2_40_selected>40"
		echo "<option $sum2_45_selected>45"
		echo "<option $sum2_60_selected>60"
		echo "</select>$period(s) of the $index selected above"
	fi
	echo "<td><a href=\"javascript:pop_page('help/runningmean.shtml',284,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
fi
#if [ "$NPERYEAR" = 360 -o "$NPERYEAR" = 365 -o "$NPERYEAR" = 366 ]; then
#	 echo "<tr><td>Averaging:<td><input type=\"$number\" step=1 class=\"forminput\" name=\"ave\" size=\"3\" style=\"width: 5em;\" value=\"$FORM_ave\">days"
#elif [ "$NPERYEAR" != 12 ]; then
#	 echo "<tr><td>Averaging:<td><input type=\"$number\" step=1 class=\"forminput\" name=\"ave\" size=\"3\" style=\"width: 5em;\" value=\"$FORM_ave\">periods"
#fi
echo "<tr><td>Anomalies: <td><input type=\"checkbox\" class=\"formcheck\" name=\"anomal\" $anomal_checked>subtract seasonal cycle<td><a href=\"javascript:pop_page('help/anomalies.shtml',284,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
if [ -z "$ONLYONE" ]; then
	echo "<tr><td>Lag: <td><select class=\"forminput\" name=\"lag\">"
	echo "<option $lag_m240t240_selected>-240:240"
	echo "<option $lag_m240t0_selected>-240:0"
	echo "<option $lag_m240_selected>-240"
	echo "<option $lag_m156_selected>-156"
	echo "<option $lag_m120t120_selected>-120:120"
	echo "<option $lag_m120t0_selected>-120:0"
	echo "<option $lag_m120_selected>-120"
	echo "<option $lag_m84_selected>-84"
	echo "<option $lag_m60t60_selected>-60:60"
	echo "<option $lag_m60t0_selected>-60:0"
	echo "<option $lag_m60_selected>-60"
	echo "<option $lag_m48_selected>-48"
	echo "<option $lag_m36_selected>-36"
	echo "<option $lag_m24t0_selected>-24:0"
	echo "<option $lag_m24t24_selected>-24:24"
	echo "<option $lag_m24_selected>-24"
	echo "<option $lag_m18_selected>-18"
	echo "<option $lag_m12t0_selected>-12:0"
	echo "<option $lag_m12t12_selected>-12:12"
	echo "<option $lag_m12_selected>-12"
	echo "<option $lag_m11_selected>-11"
	echo "<option $lag_m10_selected>-10"
	echo "<option $lag_m9_selected>-9"
	echo "<option $lag_m8_selected>-8"
	echo "<option $lag_m7_selected>-7"
	echo "<option $lag_m6_selected>-6"
	echo "<option $lag_m6t6_selected>-6:6"
	echo "<option $lag_m5_selected>-5"
	echo "<option $lag_m4_selected>-4"
	echo "<option $lag_m3_selected>-3"
	echo "<option $lag_m2_selected>-2"
	echo "<option $lag_m1_selected>-1"
	echo "<option $lag_0_selected>0"
	echo "<option $lag_1_selected>1"
	echo "<option $lag_2_selected>2"
	echo "<option $lag_3_selected>3"
	echo "<option $lag_4_selected>4"
	echo "<option $lag_5_selected>5"
	echo "<option $lag_6_selected>6"
	echo "<option $lag_7_selected>7"
	echo "<option $lag_8_selected>8"
	echo "<option $lag_9_selected>9"
	echo "<option $lag_10_selected>10"
	echo "<option $lag_11_selected>11"
	echo "<option $lag_12_selected>12"
	echo "<option $lag_0t12_selected>0:12"
	echo "<option $lag_18_selected>18"
	echo "<option $lag_24_selected>24"
	echo "<option $lag_0t24_selected>0:24"
	echo "<option $lag_36_selected>36"
	echo "<option $lag_48_selected>48"
	echo "<option $lag_60_selected>60"
	echo "<option $lag_0t60_selected>0:60"
	echo "<option $lag_m60t60_selected>-60:60"
	echo "<option $lag_72_selected>72"
	echo "<option $lag_84_selected>84"
	echo "<option $lag_96_selected>96"
	echo "<option $lag_108_selected>108"
	echo "<option $lag_120_selected>120"
	echo "<option $lag_0t120_selected>0:120"
	echo "<option $lag_m120t120_selected>-120:120"
	echo "<option $lag_132_selected>132"
	echo "<option $lag_144_selected>144"
	if [ $NPERYEAR = 366 ]; then
		echo "</select>days"
	elif [ $NPERYEAR = 12 ]; then
		echo "</select>months"
	else
		echo "</select>periods"
	fi
	echo "<tr><td>&nbsp;<td>(lag positive: $NAME $station lagging $index)"
	echo "<td><a href=\"javascript:pop_page('help/lag.shtml',284,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
fi
echo "<tr><td>Years: <td><input type=\"$number\" min="1" max="2400" step=1 name=\"begin\" $textsize4 value=\"$FORM_begin\">"
echo "&ndash;<input type=\"$number\" name=\"end\" min="1" max="2400" step=1 $textsize4 value=\"$FORM_end\"><td><a href=\"javascript:pop_page('help/beginendyear.shtml',284,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
if [ -z "$NORANGE" ]; then
    if [ -z "$ONLYONE" ]; then
	    echo "<tr><td>Only for: <td><input type=\"$number\" step=any name=\"gt\" $textsize4 value=\"$FORM_gt\"> &lt; $index selected above "
    	echo " &lt; <input type=\"$number\" step=any name=\"lt\" $textsize4 value=\"$FORM_lt\">"
	    echo "<tr><td>&nbsp;<td>"
    	echo "<input type=\"$number\" step=any name=\"dgt\" $textsize4 value=\"$FORM_dgt\"> &lt; "
	    if [ -z "$FORM_field" ]; then
		    echo "$NAME $station"
	else
    		echo "field"
	    fi
    	echo "&lt; <input type=\"$number\" step=any name=\"dlt\" $textsize4 value=\"$FORM_dlt\">"
    elif [ -z "$VERIF" ]; then
	    echo "<tr><td>Only for: <td><input type=\"$number\" step=any name=\"gt\" $textsize4 value=\"$FORM_gt\"> &lt; ${NAME:-time series} "
    	echo " &lt; <input type=\"$number\" step=any name=\"lt\" $textsize4 value=\"$FORM_lt\">"
    fi
    if [ -z "$VERIF" ]; then
        echo "<td><a href=\"javascript:pop_page('help/restrictrange.shtml',426,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
    fi
fi
echo "<tr><td>Apply: <td><input type=\"checkbox\" class=\"formcheck\" name=\"log\" $log_checked>logarithm, "
printf "<input type=\"checkbox\" name=\"sqrt\" class=\"formcheck\" $sqrt_checked>sqrt"
[ -n "$INCLUDE_SQUARE" ] && echo ", <input type=\"checkbox\" name=\"square\" class=\"formcheck\" $square_checked>square"
[ -n "$INCLUDE_TWOTHIRD" ] && echo ", <input type=\"checkbox\" name=\"twothird\" class=\"formcheck\" $twothird_checked>power 2/3"
echo " to $NAME $station"
echo "<td><a href=\"javascript:pop_page('help/logsqrt.shtml',286,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
if [ -z "$ONLYONE" -a -z "$norun" ]; then
	echo "<tr><td>Output: <td><input type=\"checkbox\" class=\"formcheck\" name=\"rank\" $rank_checked>rank correlation"
	if [ -n "$XYplot" ]; then
		echo "or <input type=\"checkbox\" class=\"formcheck\" name=\"conting\" $conting_checked>contingency tables."
	fi
	echo "<td><a href=\"javascript:pop_page('help/rank.shtml',284,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
fi
cat <<EOF
<tr><td>Detrend:<td><input type="checkbox" class="formcheck" name="detrend" $detrend_checked>detrend everything<td><a href="javascript:pop_page('help/detrend.shtml',286,450)"><img align="right" src="images/info-i.gif" alt="help" border=\"0\"></a>
EOF
if [ -z "$NOFILTERS" ]; then
    cat <<EOF
<tr><td>Filters: <td><input type="checkbox" class="formcheck" name="diff" $diff_checked>take year-on-year differences
<tr><td>&nbsp;<td>
<select class=forminput name="subsum">
<option value="1" $subsum_p>subtract mean of
<option value="-1" $subsum_m>average with
</select><input type="$number" min=0 step=1 class="forminput" name="ndiff" size="3" style="width: 4em;" value="$FORM_ndiff"> previous years
EOF
    if [ -n "$VERIF" -o -n "$XYplot" ]; then
	    echo "<input type=checkbox class=formcheck name=nooverlap $nooverlap_checked>no overlap"
    fi
    echo "<td><a href=\"javascript:pop_page('help/difference.shtml',426,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
fi
# only for timeseries and not (yet) for sets of stations
if [ "$station" != "stations" -a -z "$ONLYONE" -a -z "$norun" ]; then
    if [ -z "$runcorr_checked" ]; then
        hiddenstyle="style=\"display: none;\""
    else
        hiddenstyle=""
    fi
    cat <<EOF
<tr><td>Running correlation:<td><div class="kalelink"><a href="javascript:hidden_info_switch('hidden_info');">show/hide running correlation options</a></div>
<tr><td><td>
<div id="hidden_info" $hiddenstyle>
<input type="checkbox" class="formcheck" name="runcorr" $runcorr_checked>running <select class="forminput" name="runvar">
<option $runvar_correlation_selected>correlation</option>
<option $runvar_regression_selected>regression</option>
</select>
analysis<br>
<input type="$number" min=1 step=1 class="forminput" name="runwindow" size="3" style="width: 5em;" value="$FORM_runwindow"> years window<br>
<input type="$number" min=1 step=1 class="forminput" name="minnum" size="3" style="width: 5em;" value="$FORM_minnum"> minimum number of years with data
<br>
significance test:<br>
replace <select class="forminput" name="random">
<option value="series" $random_series_selected>$timeseries
<option value="index" $random_index_selected>$index selected above
</select> with
<select class="forminput" name="noisetype">
<option $white_selected>white</option>
<option $red_selected>red</option>
</select>
gaussian noise
</div>
<tr><td>Fit: <td><input type="radio" class="formradio" name="fitfunc" value="linear" $linear_checked>straight line, 
<input type="radio" class="formradio" name="fitfunc" value="quadratic" $quadratic_checked>parabola, 
EOF
    if [ -n "$XYplot" ]; then
        cat <<EOF
<input type="radio" class="formradio" name="fitfunc" value="cubic" $cubic_checked>cubic, 
<input type="radio" class="formradio" name="fitfunc" value="fittime" $fittime_checked>straight line 
<!-- or <input type="radio" class="formradio" name="fitfunc" value="fittimequadratic" $fittime_quadratic>parabola-->
 + a
<input type="$number" min=2 step=1 class="forminput" name="nfittime" size="2" style="width: 4em;" value="$FORM_nfittime">month time derivative, 
<input type="radio" class="formradio" name="fitfunc" value="phase" $phase_checked>phase diagram, ...
EOF
    fi
    echo "<td><a href=\"javascript:pop_page('help/fitfunction.shtml',426,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"
    if [ -n "$XYplot" ]; then
        cat <<EOF
<tr><td>Plot range: <td>X <input type="$number" step=any class="forminput" name="xlo" size="4" value="$FORM_xlo">:<input type="$number" step=any class="forminput" name="xhi" size="4" value="$FORM_xhi">,
Y <input type="$number" step=any class="forminput" name="ylo" size="4" value="$FORM_ylo">:<input type="$number" step=any class="forminput" name="yhi" size="4" value="$FORM_yhi">
EOF
    fi
fi
if [ -n "$DECOR" ]; then
	echo "<tr><td>Decorrelation scale:"
	echo "<td><input type=\"$number\" class=\"forminput\" name=\"decor\" value=\"${FORM_decor:-0}\" $textsize2> ${period}s"
fi
if [ -n "$ENSEMBLE" ]; then
	cat <<EOF
<tr><td>Ensemble members: <td>
<input type="$number" min=0 step=1 class="forminput" name="nens1" $textsize2 value="$FORM_nens1">
to
<input type="$number" min=0 step=1 class="forminput" name="nens2" $textsize2 value="$FORM_nens2">
<tr><td>&nbsp;<td>
<input type="checkbox" class="formcheck" name="makeensfull" $makeensfull_checked>replicate ensemble members to get the same number for each time step
EOF
	if [ -z "$VERIF" ]; then
		cat <<EOF
<br><input type="checkbox" class="formcheck" name="ensanom" $ensanom_checked>take anomalies relative to the ensemble mean
EOF
	fi
fi
if [ -z "$ONLYONE" ]; then
	cat <<EOF 
<tr><td colspan="2"><input type="submit" class="formbutton" value="${SUBMIT:-Correlate}">
</table>
</div>
</form>
EOF
fi
