#!/bin/sh
# form with options for daily2longer.cgi

if [ "$EMAIL" != someone@somewhere ]; then
  if [ -n "$DIR" ]; then
    def=$DIR/prefs/$EMAIL.daily2longeroptions.$NPERYEAR
  else
    def=prefs/$EMAIL.daily2longeroptions.$NPERYEAR
  fi
  if [ -s $def ]; then
    eval `egrep '^FORM_[a-z0-9]*=[-a-zA-Z_]*[-+_0-9.]*;$' $def`
  fi
fi

if [ -n "$FORM_nperyearnew" ]; then
  case "$FORM_nperyearnew" in
  "-1") sel_annual_shifted="selected";;
  1) sel_annual="selected";;
  4) sel_seasonal="selected";;
  12) sel_monthly="selected";;
  36) sel_10daily="selected";;
  72) sel_5daily="selected";;
  360|365|366) sel_daily="selected";;
  esac
else
  if [ "$NPERYEAR:-12" = 12 ]; then
    sel_annual="selected"
  elif [ "$NPERYEAR" = 366 -o "$NPERYEAR" = 365 -o "$NPERYEAR" = 360 ]; then
    sel_monthly="selected"
  fi
fi
if [ "$sel_annual_shifted" = selected -a "$sel_annual" = selected ]; then
    ###echo "Something went wrong"
    sel_annual=""
fi

case ${FORM_oper:-mean} in
sd)     oper_sd="selected";;
sum)    oper_sum="selected";;
number) oper_number="selected";;
above)  oper_above="selected";;
below)  oper_below="selected";;
min)    oper_min="selected";;
max)    oper_max="selected";;
mintime) oper_mintime="selected";;
maxtime) oper_maxtime="selected";;
firsttime) oper_firsttime="selected";;
lasttime) oper_lasttime="selected";;
*)      oper_mean="selected";;
esac

case ${FORM_lgt:-none} in
lt)  lgt_lt="selected";;
gt)  lgt_gt="selected";;
*) lgt_none="selected";;
esac

case ${FORM_typecut:-val} in
p) typecut_p="selected";;
n) typecut_n="selected";;
*) typecut_v="selected";;
esac

case ${FORM_addoption:-add_anom} in
    add_clim) add_clim="checked";;
    add_trend) add_trend="checked";;
    add_persist) add_persist="checked";;
    add_damp) add_damp="checked";;
    *) add_anom="checked";;
esac    

if [ -z "$FORM_field" ]; then
  other="time series"
else
  other="field"
fi

station=`echo $STATION | tr '_' ' '`
cat <<EOF
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NAME" value="$NAME">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<tr><td>New time scale:</td><td>
<select class="forminput" name="nperyearnew">
<option value="-1" $sel_annual_shifted>annual (Jul-Jun)</option>
<option value="1" $sel_annual>annual (Jan-Dec)</option>
<option value="4" $sel_seasonal>seasonal</option>
<option value="12" $sel_monthly>monthly</option>
<option value="36" $sel_10daily>10-daily</option>
<option value="73" $sel_5daily>5-daily</option>
<option value="$NPERYEAR" $sel_daily>daily</option>
</select>
</td></tr><tr><td>
New variable:
</td><td>
<select class="forminput" name="oper">
<option $oper_mean>mean
<option $oper_sd>sd
<option $oper_sum>sum
<option value="above" $oper_above>sum above
<option value="below" $oper_below>sum below
<option $oper_number>number
<option $oper_min>min
<option $oper_mintime value="mintime">time of min
<option $oper_max>max
<option $oper_maxtime value="maxtime">time of max
<option $oper_firsttime value="firsttime">first time
<option $oper_lasttime value="lasttime">last time
</select>
of $station ${climfield:-$VAR}
</td></tr><tr><td>
Threshold:
</td><td>
<select class="forminput" name="lgt">
<option value=" " $lgt_none>no cut
<option value="lt" $lgt_lt>less than
<option value="gt" $lgt_gt>greater than 
</select>
<input type="$number" step=any class="forminput" name="cut" size="4" style="width: 5em;" value="$FORM_cut">
<select class="forminput" name="typecut">
<option value=" " $typecut_v>${UNITS:-absolute value}
<option value="p" $typecut_p>percentile
<option value="n" $typecut_n>normal 1971-2000
</select>
</td></tr><tr><td>Minimum:</td><td><input  type="$number" step=any min=0 max=100 step=1 class="forminput" name="minfac" size="3" style="width: 4em;" value="$FORM_minfac">% valid data
</td></tr><tr><td>First apply:</td><td><input  type="$number" min=1 max=100 step=1 class="forminput" name="sum" size="3" style="width: 4em;" value="${FORM_sum:-1}">-$month running mean
</td></tr><tr><td>Missing data:</td><td>
<input  type="radio" class="formradio" name="addoption" value="add_anom" $add_anom>ignore, 
<input  type="radio" class="formradio" name="addoption" value="add_clim" $add_clim>climatology,
<input  type="radio" class="formradio" name="addoption" value="add_trend" $add_trend>trend, 
<input  type="radio" class="formradio" name="addoption" value="add_persist" $add_persist>persistence<!--, 
<input  type="radio" class="formradio" name="addoption" value="add_damp" $add_damp>damped persistence-->.

</td></tr><tr><td colspan="2">
EOF
