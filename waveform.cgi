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

DIR=`pwd`
c1=`echo "$WMO" | fgrep -c '%%'`
c2=`echo "$WMO" | fgrep -c '++'`
if [ $c1 -gt 0 -o $c2 -gt 0 ]; then
  ENSEMBLE=true
fi

. ./myvinkhead.cgi "Wavelet analysis" "$station $NAME" "noindex,nofollow"

if [ -n "$EMAIL" -a "$EMAIL" != someone@somewhere ]; then
# read defaults if they exist
  if [ -f ./prefs/$EMAIL.waveoptions.$NPERYEAR ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.:]*;$' ./prefs/$EMAIL.waveoptions.$NPERYEAR`
  fi
fi

case "$FORM_type" in
    paul) paul_selected=selected;;
    dog)  dog_selected=selected;;
    *)    morlet_selected=selected;;
esac

case "$FORM_var" in
    prob) prob_checked=checked;;
    *)    power_checked=checked;;
esac

case "$FORM_logplot" in
    linear) linear_selected=selected;;
    inverse) inverse_selected=selected;;
    *) logarithmic_selected=selected;;
esac

if [ -n "$FORM_nocbar" ]; then
    nocbar_checked=checked
fi

case "$FORM_shadingtype" in
    shaded) shaded_checked=checked;;
    contour) contour_checked=checked;;
    grfill) grfill_checked=checked;;
    *) shadedcontour_checked=checked;;
esac

cat <<EOF
<div class="formheader">Compute wavelet transform</div>
<div class="formbody">
<form action="wave.cgi" method="post">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="CLIMATE" value="$NAME">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$station">
<input type="hidden" name="NAME" value="$NAME">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<table width=451 cellspacing=0 cellpadding=0 border=0>
<tr>
<td>Order, type:
<td><input type="$number" min=1 step=1 class="forminput" name="param" size="2" style="width: 4em;" value="${FORM_number:-6}">
<select class="forminput" name="type">
<option value="morlet" $morlet_selected>Morlet (sin*gauss)
<option value="paul"   $paul_selected  >Paul   (1+is)^(-m-1)
<option value="dog"    $dog_selected   >DOG    (derivative of Gauss)
</select>
wavelet transform
<tr>
<td>Plot:
<td><input type="radio" class="formradio" name="var" value="power" $power_checked>power
<input type="radio" class="formradio" name="var" value="prob" $prob_checked>p-value
<select class=forminput name=maskout><option value=mask $mask_selected>mask out<option value=light $light_selected>make light</select>: p&gt;<input type="$number" step=any class="forminput" name="pmin" value="${FORM_pmin:-10}" $textsize3>%
EOF
justonemonth=true
ONLYONE=true
. ./commonoptions.cgi
cat <<EOF
<tr>
<td>Scale:
<td> <select class="forminput" name="logplot"><option $inverse_selected>inverse<option $logarithmic_selected>logarithmic<option $linear_selected>linear</select> scale
<tr>
<td>Periods:
<td><input type="$number" step=any class="forminput" name="period1" value="$FORM_period1" $textsize4>-<input type="$number" step=any class="forminput" name="period2" value="$FORM_period2" $textsize4> years
<tr>
<td>Contours:
<td><input type="$number" step=any class="forminput" name="cmin" $textsize6 value="$FORM_cmin">-<input type="$number" step=any class="forminput" name="cmax" $textsize6 value="$FORM_cmax">
<tr>
<input type="hidden" name="colourscale" value="3">
<tr>
<td>Shading: 
<td><input type="radio" class="formradio" name="shadingtype" value="shadedcontour" $shadedcontour_checked>shading and contours
<input type="radio" class="formradio" name="shadingtype" value="shaded" $shaded_checked>shading
<input type="radio" class="formradio" name="shadingtype" value="contour" $contour_checked>contours
<input type="radio" class="formradio" name="shadingtype" value="grfill" $grfill_checked>grid boxes
<tr>
<td>Colour bar:
<td><input type="checkbox" class="formcheck" name="nocbar" $nocbar_checked>no colour bar
EOF
cat <<EOF
<tr>
<td colspan=2><input type="submit" class="formbutton" value="Make waves">
<td>&nbsp;
</table>
</form>
</div>
EOF

. ./myvinkfoot.cgi
