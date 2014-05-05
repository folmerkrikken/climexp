#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi
TYPE="$FORM_TYPE"
WMO="$FORM_WMO"
STATION="$FORM_STATION"
station=` echo "$STATION" | tr '_' ' '`
NAME="$FORM_NAME"
NPERYEAR="$FORM_NPERYEAR"

. ./nosearchengine.cgi

if [ $TYPE = set ]; then
  . ./myvinkhead.cgi "Cannot handle set of stations" "$station stations" "noindex,nofollow"
  . ./myvinkfoot.cgi
  exit
else
  . ./myvinkhead.cgi "Trends in return times of extremes" "$station $NAME ($WMO)" "noindex,nofollow"
fi

cat <<EOF
Compute the return times of an extreme in the distribution of the other values and in the 
counterfactual world of another year, assuming that the PDF or scales shifts with the covariate.

<font color=#ff2222>Test version under development, may or may not give correct answers
today. Use with extreme caution and please report problems.</font><p>
EOF

DIR=`pwd`
c1=`echo "$WMO" | fgrep -c '%%'`
c2=`echo "$WMO" | fgrep -c '++'`
if [ $c1 -gt 0 -o $c2 -gt 0 ]; then
  ENSEMBLE=true
fi

if [ "$EMAIL" != somene@somewhere ]; then
  if [ -n "$DIR" ]; then
    def=$DIR/prefs/$EMAIL.histogramoptions
  else
    def=prefs/$EMAIL.histogramoptions
  fi
  if [ -s $def ]; then
    eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.%]*;$' $def`
  fi
fi

case ${FORM_fit:-none} in
poisson) fit_poisson="checked";;
gauss)   fit_gauss="checked";;
gamma)   fit_gamma="checked";;
gumbel)  fit_gumbel="checked";;
gev)     fit_gev="checked";;
gpd)     fit_gpd="checked";;
*)       fit_none="checked";;
esac

case $FORM_assume in
scale) assume_scale=checked;;
both)  assume_both=checked;;
*)     assume_shift=checked;;
esac

if [ -n "$FORM_changesign" ]; then
  changesign_checked="checked"
fi

case ${FORM_restrain:-0} in
0.5) select05=selected;;
0.4) select04=selected;;
0.3) select03=selected;;
0.2) select02=selected;;
*)   select00=selected;;
esac

cat <<EOF
<form action="attribute.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="NAME" value="$NAME">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="hidden" name="nbin" value="$FORM_nbin">
<div class="formheader">Covariate series</div>
EOF

# we can handle time series at all time scales...
if [ $NPERYEAR -ge 360 ]; then
    nperyears="1 12 $NPERYEAR"
elif [ $NPERYEAR -ge 12 ]; then
    nperyears="1 12"
elif [ $NPERYEAR -ge 4 ]; then
    nperyears="1 4"
else
    nperyears="1"
fi

if [ "$EMAIL" != "someone@somewhere" -a -f ./prefs/$EMAIL.series ]; then
    series=`cat ./prefs/$EMAIL.series | head -1`
fi
save_nperyear=$NPERYEAR
for NPERYEAR in $nperyears
do
    . ./selecttimeseries.cgi | sed \
    -e 's;="'$series'";="'$series'" checked;' \
    -e 's/checkbox\" class=\"formcheck\" name/radio\" class=\"formradio\" name=\"timeseries\" value/' \
    -e 's/value=\"myindex[0-9]*\"//'
done
NPERYEAR=$save_nperyear

cat <<EOF
<div class="formheader">Plot</div>
<div class="formbody">
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
EOF

justonemonth=true
ONLYONE=true
NAME=series
###DECOR=true
INCLUDE_SQUARE=true
NORANGE=true
NOFILTERS=true
. ./commonoptions.cgi

cat <<EOF
<tr><td>Demand at least<td><input type="$number" step=any name="minfac" value="$FORM_minfac" $textsize2>% valid points
<tr><td>Change sign:
<td><input type="checkbox" class="formcheck" name="changesign" $changesign_checked>study the low extremes<td><a href="javascript:pop_page('help/changesign.shtml',284,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>

<tr><td valign=top>Use:<td>
<input type="radio" class="formradio" name="fit" value="gauss" $fit_gauss>Average and fit normal distribution<br>
<input type="radio" class="formradio" name="fit" value="gumbel" $fit_gumbel>Block maxima and fit Gumbel distribution<br>
<input type="radio" class="formradio" name="fit" value="gev" $fit_gev>Block maxima and fit GEV<br>
<input type="radio" class="formradio" name="fit" value="gpd" $fit_gpd>Peak over threshold
<input type="$number" class="forminput" name="dgt" value="${FORM_dgt:-80}" $textsize3>% and fit GPD
<select class="forminput" name="restrain">
<option value="0" $select00>do not constrain shape
<option value="0.5" $select05>constrain shape to &plusmn;0.5
<option value="0.4" $select04>constrain shape to &plusmn;0.4
<option value="0.3" $select03>constrain shape to &plusmn;0.3
<option value="0.2" $select02>constrain shape to &plusmn;0.2
</select> of GEV and GPD
<tr><td>Assume:<td>The PDF <input type="radio" class="formradio" name="assume" value="shift" $assume_shift>shifts, <input type="radio" class="formradio" name="assume" value="scale" $assume_scale>scales or <input type="radio" class="formradio" name="assume" value="both" $assume_both>both with the covariate<td><a href="javascript:pop_page('help/assume.shtml',284,450)"><img align="right" src="images/info-i.gif" alt="help" border="0"></a>
<tr><td>Compare:<td>return time in the counterfactual world of year <input type="$number" min=1 max=2500 step=1 class="forminput" name="begin2" $textsize4 value="$FORM_begin2">
<tr><td>Leave out:<td>year <input type="$number" min=1 max=2500 step=1 class="forminput" name="year" $textsize4 value="$FORM_year"> and compute return time
EOF

if [ -n "$ENSEMBLE" ]; then
cat <<EOF
<tr><td>Ensemble members:
<td><input type="$number" min=0 step=1 class="forminput" name="nens1" $textsize2 value="$FORM_nens1">to
<input type="$number" min=0 step=1 class="forminput" name="nens2" $textsize2 value="$FORM_nens2">
EOF
fi
cat <<EOF
<tr><td>Plot range:<td>X <input type="$number" step=any class="forminput" name="xlo" size="4" style="width: 5em;" value="$FORM_xlo">:<input type="$number" step=any class="forminput" name="xhi" size="4" style="width: 5em;" value="$FORM_xhi">,
Y <input type="$number" step=any class="forminput" name="ylo" size="4" style="width: 5em;" value="$FORM_ylo">:<input type="$number" step=any class="forminput" name="yhi" size="4" style="width: 5em;" value="$FORM_yhi">
<tr><td colspan="2"><input type="submit" class="formbutton" value="Compute">
</table>
</div>
</form>
EOF

. ./myvinkfoot.cgi
