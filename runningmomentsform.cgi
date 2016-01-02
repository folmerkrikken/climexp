#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

DIR=`pwd`
. ./getargs.cgi
TYPE="$FORM_TYPE"
WMO="$FORM_WMO"
STATION="$FORM_STATION"
station=` echo "$STATION" | tr '_' ' '`
NAME="$FORM_NAME"
NPERYEAR="$FORM_NPERYEAR"

. ./nosearchengine.cgi

c1=`echo "$WMO" | fgrep -c '%%'`
c2=`echo "$WMO" | fgrep -c '++'`
if [ $c1 -gt 0 -o $c2 -gt 0 ]; then
  ENSEMBLE=true
fi

. ./myvinkhead.cgi "Running moments" "$station $NAME" "noindex,nofollow"

if [ -z "$NPERYEAR" ]; then
  NPERYEAR=12 # I hope
fi
if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
# read defaults if they exist
  if [ -f ./prefs/$EMAIL.runningmoments.$NPERYEAR ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z.]*[-+0-9.:]*;$' ./prefs/$EMAIL.runningmoments.$NPERYEAR`
  fi
fi

case ${FORM_moment:-mean} in
"s.d.") sd_selected=selected;;
skew) skew_selected=selected;;
curtosis) curtosis_selected=selected;;
all)  all_selected=selected;;
*)    mean_selected=selected;;
esac

if [ -n "$FORM_separate" ]; then
  separate_checked="checked"
fi

cat <<EOF
<form action="runningmoments.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="hidden" name="CLIMATE" value="$NAME">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="NAME" value="$NAME">
<input type="hidden" name="STATION" value="$STATION">
<div class="formheader">Compute running mean, standard deviation, skewness, ...</div>
<div class="formbody">
<table style='width:100%' border='0' cellpadding='0' cellspacing='0'>
<tr><td>Running: <td> 
<select name="moment">
<option $mean_selected>mean
<option $sd_selected>s.d.
<option $skew_selected>skew
<option $curtosis_selected>curtosis
<option $all_selected>all
</select>
<tr><td>Window: <td>
<input type="hidden" name="runvar" value="corr">
<input type="$number" min=1 step=1 name="runwindow" size="3" style="width: 4em;" value="${FORM_runwindow:-15}"> years, with at least
<input type="$number" min=1 step=1 name="minnum" size="3" style="width: 4em;" value="$FORM_minnum"> years with data
EOF
justonemonth=true
ONLYONE=true
DECOR=true
. ./commonoptions.cgi

if [ -n "$ENSEMBLE" ]; then
cat <<EOF
<tr><td>&nbsp;<td><input type="checkbox" class="formcheck" name="separate" $separate_checked>keep separate
EOF
fi
echo "<tr><td><input type=\"submit\" class=\"formbutton\" value=\"Compute\">"
echo "</table></div></form>"

. ./myvinkfoot.cgi
