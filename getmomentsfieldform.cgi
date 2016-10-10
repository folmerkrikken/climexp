#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi
# check email address
. ./checkemail.cgi
# no robots
. ./nosearchengine.cgi

echo `date` "$EMAIL ($REMOTE_ADDR) $FORM_field" >> log/log

# start real work
. ./queryfield.cgi
eval `./bin/getunits.sh $file`

# values filled out last time - there must be an easier way...
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
# read defaults if they exist
  if [ -f ./prefs/$EMAIL.momentsfield.$NPERYEAR ]; then
    eval `egrep '^FORM_[a-z0-9_]*=[a-zA-Z_]*[-+0-9.:]*;$' ./prefs/$EMAIL.momentsfield.$NPERYEAR`
  fi
fi

case "$FORM_var" in
sd)         sd_checked="checked";;
norm_rt)    norm_rt_checked="checked";;
norm_z)     norm_z_checked="checked";;
sdm)        sdm_checked="checked";;
skew)       skew_checked="checked";;
kurt)       kurt_checked="checked";;
perc)       perc_checked="checked";;
max)        max_checked="checked";;
min)        min_checked="checked";;
pot_mean)   pot_mean_checked="checked";;
pot_median) pot_median_checked="checked";;
pot_sd)     pot_sd_checked="checked";;
pot_scale)  pot_scale_checked="checked";;
pot_shape)  pot_shape_checked="checked";;
pot_return) pot_return_checked="checked";;
pot_return_diff) pot_return_diff_checked="checked";;
pot_rt)     pot_rt_checked=checked;;
gev_pos)    gev_pos_checked="checked";;
gev_scale)  gev_scale_checked="checked";;
gev_shape)  gev_shape_checked="checked";;
gev_return) gev_return_checked="checked";;
gev_return_diff) gev_return_diff_checked="checked";;
gev_rt)     gev_rt_checked=checked;;
rank)       rank_checked=checked;;
time)       time_checked=checked;;
*)          mean_checked="checked";;
esac

case ${FORM_pot_return:-10} in
20) t20_selected="selected";;
50) t50_selected="selected";;
100) t100_selected="selected";;
200) t200_selected="selected";;
500) t500_selected="selected";;
1000) t1000_selected="selected";;
2000) t2000_selected="selected";;
5000) t5000_selected="selected";;
10000) t10000_selected="selected";;
*)  t10_selected="selected";;
esac
case ${FORM_gev_return:-10} in
20) gev_t20_selected="selected";;
50) gev_t50_selected="selected";;
100) gev_t100_selected="selected";;
200) gev_t200_selected="selected";;
500) gev_t500_selected="selected";;
1000) gev_t1000_selected="selected";;
2000) gev_t2000_selected="selected";;
5000) gev_t5000_selected="selected";;
10000) gev_t10000_selected="selected";;
*)  gev_t10_selected="selected";;
esac

if [ "$FORM_changesign" = "both" ]; then
  both_checked="checked"
elif [ -n "$FORM_changesign" ]; then
  lower_checked="checked"
else
  upper_checked="checked"
fi

case ${FORM_restrain:-0} in
0.2) select02=selected;;
0.3) select03=selected;;
0.4) select04=selected;;
0.5) select05=selected;;
*)   select00=selected;;
esac

if [ -n "$FORM_tv" ]; then
  tv_checked="checked"
fi
if [ -n "$FORM_ensanom" ]; then
  ensanom_checked="checked"
fi

# GO
. ./myvinkhead.cgi "Compute mean, s.d., or extremes" "$kindname $climfield" "noindex,nofollow"

if [ "$lwrite" = true ]; then
    echo '<pre>'
    ./bin/getunits.sh $file
    echo '</pre>'
    echo "UNITS,NEWUNITS=$UNITS,$NEWUNITS<br>"
fi
cat <<EOF
<form action="getmomentsfield.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="field" value="$FORM_field">
<div class="formheader">Make a map of the mean, s.d., percentile or extreme property</div>
<div class="formbody">
<table style='width:100%' border='0' cellpadding='0' cellspacing='0'>
<tr><td>Property:<td>
<input type="radio" class="formradio" name="var" value="mean" $mean_checked>mean
,<input type="radio" class="formradio" name="var" value="sd" $sd_checked>standard deviation
(<input type="radio" class="formradio" name="var" value="sdm" $sdm_checked>/mean)
<tr><td><td>
<input type="radio" class="formradio" name="var" value="norm_rt" $norm_rt_checked>return time of year <input type="$number" min=1 max=2500 step=1 class="forminput" $textsize4 name="normyear" value="${FORM_year}"> in the context of the other years assuming a normal distribution, <input type="radio" class="formradio" name="var" value="norm_z" $norm_z_checked>z-value
<tr><td><td>
<input type="radio" class="formradio" name="var" value="skew" $skew_checked>skewness
<input type="radio" class="formradio" name="var" value="kurt" $kurt_checked>kurtosis or
<tr><td><td>
<input type="radio" class="formradio" name="var" value="perc" $perc_checked>percentile at 
<input type="$number" step=any class="forminput" $textsize2 name="perc" value="${FORM_perc:-50}">% of $climfield
<tr><td><td>
<input type="radio" class="formradio" name="var" value="min" $min_checked>minimum value
<input type="radio" class="formradio" name="var" value="max" $max_checked>maximum value
<tr><td><td>&nbsp;
<tr><td><td>Extreme value fits: <input type="radio" class="formradio" name="changesign" value="" $upper_checked>upper <input type="radio" class="formradio" name="changesign" value="on" $lower_checked>lower tail, or <input type="radio" class="formradio" name="changesign" value="both" $both_checked>both,
<select class="forminput" name="restrain">
<option value="0" $select00>do not constrain shape
<option value="0.5" $select05>constrain shape to &plusmn;0.5
<option value="0.4" $select04>constrain shape to &plusmn;0.4
<option value="0.3" $select03>constrain shape to &plusmn;0.3
<option value="0.2" $select02>constrain shape to &plusmn;0.2
</select>
<tr><td><td>&nbsp;
<tr><td><td>
Peak over threshold 
<input type="$number" step=any class="forminput" name="threshold" $textsize2 value="${FORM_threshold:-90}">%
<tr><td><td>
<!--
<input type="radio" class="formradio" name="var" value="pot_median" $pot_median_checked>median, 
<input type="radio" class="formradio" name="var" value="pot_mean" $pot_mean_checked>mean, 
<input type="radio" class="formradio" name="var" value="pot_sd" $pot_sd_checked>s.d. of excesses
above threshold<tr><td><td>
-->
<input type="radio" class="formradio" name="var" value="pot_scale" $pot_scale_checked>scale &sigma;, 
<input type="radio" class="formradio" name="var" value="pot_shape" $pot_shape_checked>shape &xi; of
GPD
<tr><td><td>
<input type="radio" class="formradio" name="var" value="pot_return" $pot_return_checked>value for return time 
<!--
<input type="$number" class="forminput" $textsize4 name="pot_return" value="${FORM_pot_return:-100}">years/months
-->
<select class="forminput" name="pot_return">
<option $t10_selected>10
<option $t20_selected>20
<option $t50_selected>50
<option $t100_selected>100
<option $t200_selected>200
<option $t500_selected>500
<option $t1000_selected>1000
<option $t2000_selected>2000
<option $t5000_selected>5000
<option $t10000_selected>10000
</select>years/months
<tr><td><td>
<input type="radio" class="formradio" name="var" value="pot_rt" $pot_rt_checked>return time of year <input type="$number" min=1 max=2500 step=1 class="forminput" $textsize4 name="potyear" value="${FORM_year}"> in the context of the other years
<!--
<tr><td><td>
<input type="radio" class="formradio" name="var" value="pot_return_diff" $pot_return_diff_checked>return time for values in a pattern (<a href="javascript:hidden_info_switch('hidden_info');">show list</a>)<br>
<div id="hidden_info" style="display: none;">
-->
<tr><td><td>&nbsp;
<tr><td><td>
Block maxima (it is assumed these have already been computed).
EOF
if [ $NPERYEAR -ge 12 ]; then
    . ./nperyear2timescale.cgi
    echo "Are you sure these $timescale data are block maxima?"
fi
cat <<EOF
<tr><td><td>
<input type="radio" class="formradio" name="var" value="gev_pos" $gev_pos_checked>position &mu;, 
<input type="radio" class="formradio" name="var" value="gev_scale" $gev_scale_checked>scale &sigma;, 
<input type="radio" class="formradio" name="var" value="gev_shape" $gev_shape_checked>shape &xi; of
GEV
<tr><td><td>
<input type="radio" class="formradio" name="var" value="gev_return" $gev_return_checked>value for return time 
<select class="forminput" name="gev_return">
<option $gev_t10_selected>10
<option $gev_t20_selected>20
<option $gev_t50_selected>50
<option $gev_t100_selected>100
<option $gev_t200_selected>200
<option $gev_t500_selected>500
<option $gev_t1000_selected>1000
<option $gev_t2000_selected>2000
<option $gev_t5000_selected>5000
<option $gev_t10000_selected>10000
</select>years/months
<tr><td><td>
<input type="radio" class="formradio" name="var" value="gev_rt" $gev_rt_checked>return time of year <input type="$number" min=1 max=2500 step=1 class="forminput" $textsize4 name="gevyear" value="${FORM_year}"> in the context of the other years
<tr><td><td>&nbsp;
<tr><td><td><input type="radio" class="formradio" name="var" value="rank" $rank_checked>Rank of year <input type="$number" min=1 max=2500 step=1 class="forminput" $textsize4 name="rankyear" value="${FORM_year}"> in the context of the other years
<tr><td><td><input type="radio" class="formradio" name="var" value="timex" $time_checked>Year of highest/lowest value
<tr><td><td>&nbsp;
<tr><td>
Demand: <td>at least <input type="$number" step=any class="forminput" name="minfac" $textsize2 value="$FORM_minfac">% valid points
EOF
echo '<tr><td>&nbsp;'
intable=true
lsmask=yes
. ./plotoptions.cgi
echo '<tr><td>&nbsp;'
ONLYONE=true
NAME=field
INCLUDE_TWOTHIRD=true
. ./commonoptions.cgi

echo "<tr><td>"
echo "<input type=\"submit\" class=\"formbutton\" value=\"Plot\">"
echo "</table></div></form>"

. ./myvinkfoot.cgi
