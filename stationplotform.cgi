#!/bin/sh

if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
# read defaults if they exist, they are in the commonoptions file
  if [ -f ./prefs/$EMAIL.commonoptions.$NPERYEAR ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.:]*;$' ./prefs/$EMAIL.commonoptions.$NPERYEAR`
  fi
fi

case "$FORM_var" in
     regr) regr_selected=checked;;
     nregr) nregr_selected=checked;;
     zdiff) zdiff_selected=checked;;
     *) corr_selected=checked;;
esac

case $FORM_random in
     index) index_selected=selected;;
     *) series_selected=selected;;
esac

case $FORM_noisetype in
     red) red_selected=selected;;
     *) white_selected=selected;;
esac

cat <<EOF
<p><div class="formheader">Plot</div>
<div class="formbody">
<input type="radio" name="var" value="corr" $corr_selected>correlation<br>
<input type="radio" name="var" value="regr" $regr_selected>regression<br>
<input type="radio" name="var" value="nregr" $nregr_selected>regression/mean<br>
or
<input type="radio" name="var" value="zdif" $zdiff_selected>running
<select name="runvar">
<option>correlation</option>
<option>regression</option>
</select>
with window <input type="text" name="runwindow" size="2" value="${FORM_runwindow:-30}">years, for significance test replace
<select name="random">
<option value="series" $series_selected>$extraname$climate
<option value="index" $index_selected>timeseries selected above
</select> with
<select name="noisetype">
<option $white_selected>white</option>
<option $red_selected>red</option>
</select>
gaussian noise
(running correlations/regressions are <strong>very</strong> slow, approx 6s/station, 30s/station with detrending)
<br>Only show stations with at least
<input type="text" name="minnum" size="3" value="$FORM_minnum"> valid years/months
</div>
EOF
