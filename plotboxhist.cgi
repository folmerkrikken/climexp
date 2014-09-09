#!/bin/sh

echo "Content-Type:text/html"
echo
echo

export DIR=`pwd`
. ./getargs.cgi
# printenv
email="$EMAIL"
. ./nosearchengine.cgi
climate="$FORM_climate"
prog="$FORM_prog"
listname="$FORM_listname"
NPERYEAR="$FORM_nperyear"
extraargs="$FORM_extraargs"
if [ -n "$extraargs" ]; then
  NPERYEAR=`echo "$extraargs" | cut -f 1 -d '_'`
  extraname=`echo "$extraargs " | cut -f 2- -d '_' | tr '_' ' '`
fi
. ./nperyear2timescale.cgi

# check email address
. ./checkemail.cgi

. ./myvinkhead.cgi "Plot statistical properties" "$timescale $extraname$climate stations" "noindex,nofollow"

if [ $EMAIL != someone@somewhere ]; then
    def=prefs/$EMAIL.statistical.$NPERYEAR
    if [ -s $def ]; then
        eval `egrep '^FORM_[a-z]*=[0-9a-zA-Z]*;$' $def`
    fi
fi

case ${FORM_var:-mean} in
    hime) hime=checked;;
    hisd) hisd=checked;;
    hisk) hisk=checked;;
    higa) higa=checked;;
    higr) higr=checked;;
    higR) higR=checked;;
    hipr) hipr=checked;;
    hipR) hipR=checked;;
    hivr) hivr=checked;;
    hivR) hivR=checked;;
esac

if [ -n "$FORM_changesign" ]; then
    lower_checked=checked
else
    upper_checked=checked
fi

case ${FORM_restrain:-0} in
    0.5) select05=selected;;
    0.4) select04=selected;;
    0.3) select03=selected;;
    0.2) select02=selected;;
    *)   select00=selected;;
esac

cat <<EOF
<form action="correlatebox.cgi" method="POST">
<input type="hidden" name="email" value="$email">
<input type="hidden" name="climate" value="$timescale $extraname$climate">
<input type="hidden" name="prog" value="$prog">
<input type="hidden" name="extraargs" value="$extraargs">
<input type="hidden" name="listname" value="$listname">
<input type="hidden" name="type" value="histogram">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">

<div class="formheader">Plot options</div>
<div class="formbody">
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
<tr><td>Variable:
<td><input type="radio" name="var" value="hime" $hime>mean
<tr><td>&nbsp;
<td><input type="radio" name="var" value="hisd" $hisd>standard deviation
<tr><td>&nbsp;
<td><input type="radio" name="var" value="hisk" $hisk>skewness
<tr><td>Fit:
<td><input type="radio" name="var" value="higa" $higa>Gaussian and plot &chi;<sup>2</sup> 
<tr><td>Return time:
<td>year <input type="text" class="forminput" name="year" size="4" value="$FORM_year">, <input type="radio" class="formradio" name="changesign" value="" $upper_checked>upper <input type="radio" class="formradio" name="changesign" value="on" $lower_checked>lower tail
<tr><td>&nbsp;
<td><input type="radio" name="var" value="higr" $higr>Gaussian fit, plot best fit
<tr><td>&nbsp;
<td><input type="radio" name="var" value="higR" $higR>same, plot lower limit of 95% CI
<tr><td>&nbsp;
<td><input type="radio" name="var" value="hipr" $hipr>GPD fit with threshold <input type="text" class="forminput" name="dgt" size="4" value="${FORM_dgt:-80}">%, plot best fit
<tr><td>&nbsp;
<td><input type="radio" name="var" value="hipR" $hipR>same, plot lower limit of 95% CI
<tr><td>&nbsp;
<td><input type="radio" name="var" value="hivr" $hivr>GEV fit, plot best fit
<tr><td>&nbsp;
<td><input type="radio" name="var" value="hivR" $hivR>same, plot lower limit of 95% CI
<tr><td>GPD, GEV:
<td><select class="forminput" name="restrain">
<option value="0" $select00>do not constrain shape
<option value="0.5" $select05>constrain shape to &plusmn;0.5
<option value="0.4" $select04>constrain shape to &plusmn;0.4
<option value="0.3" $select03>constrain shape to &plusmn;0.3
<option value="0.2" $select02>constrain shape to &plusmn;0.2
</select>
<tr><td>Minimum length:
<td>require at least
<input type="text" name="minnum" size="3" value="$FORM_minnum"> valid years/months
</table>
</div>
<p><div class="formheader">Common options</div>
<div class="formbody">
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
EOF

justonemonth=true
ONLYONE=true
NAME=series
. ./commonoptions.cgi

cat << EOF
<tr><td colspan="2"><input type="submit" class="formbutton" value="Compute">
</table>
</div>
EOF

. ./myvinkfoot.cgi
