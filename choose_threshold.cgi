#!/bin/sh
#if [ "$ENSEMBLE" = true ]; then
case $FORM_threshold_type in
FALSE) checked_threshold_type_false="selected";;
TRUE) checked_threshold_type_true="selected";;
esac

cat <<EOF
<p><div class="formheader">Threshold</div>
<div class="formbody">
For measures that require a threshold, use <input type="$number" step=any $textsize4 name="threshold" value="${FORM_threshold:-50}">
<select name="threshold_type">
<option value="FALSE" $checked_threshold_type_false>%</option>
<option value="TRUE" $checked_threshold_type_true>${NEWUNITS:-absolute}</option>
</select>
<br>Use <input type="$number" min=2 step=1 $textsize4 name="nbins" value="${FORM_nbins:-10}">
bins <input type="checkbox" name="debug">show R logfile
</div>
EOF
#fi
