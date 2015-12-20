#!/bin/sh
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi
TYPE="$FORM_TYPE"
WMO="$FORM_WMO"
listname=$WMO
STATION="$FORM_STATION"
station=` echo "$STATION" | tr '_' ' '`
NAME="$FORM_NAME"
prog=$NAME
NPERYEAR="$FORM_NPERYEAR"

. ./nosearchengine.cgi

if [ $TYPE = set ]; then
  . ./myvinkhead.cgi "Make and fit a histogram" "$station stations" "noindex,nofollow"
else
  . ./myvinkhead.cgi "Make and fit a histogram" "$station $NAME ($WMO)" "noindex,nofollow"
fi

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

case ${FORM_plot:-hist} in
qq) plot_qq="checked";;
gumbel) plot_gumbel="checked";;
log) plot_log="checked";;
sqrtlog) sqrtplot_log="checked";;
*) plot_hist="checked";;
esac

case ${FORM_fit:-none} in
poisson) fit_poisson="checked";;
gauss)   fit_gauss="checked";;
gamma)   fit_gamma="checked";;
gumbel)  fit_gumbel="checked";;
gev)     fit_gev="checked";;
gpd)     fit_gpd="checked";;
*)       fit_none="checked";;
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
<form action="histogram.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="NAME" value="$NAME">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="hidden" name="extraargs" value="$FORM_extraargs">
<input type="hidden" name="begin2" value="$FORM_begin2">
<input type="hidden" name="assume" value="$FORM_assume">

<div class="formheader">Plot</div>
<div class="formbody">
<table style='width:443px' border='0' cellpadding='0' cellspacing='0'>
<tr><td>Type of plot:<td>
<input type="radio" class="formradio" name="plot" value="hist" $plot_hist>histogram with <input type="$number" min=2 step=1 class="forminput" name="nbin" size="4" style="width: 5em;" value="${FORM_nbin:-20}">bins<br>
<input type="radio" class="formradio" name="plot" value="qq" $plot_qq>quantile-quantile plot<br>
<input type="radio" class="formradio" name="plot" value="gumbel" $plot_gumbel>Gumbel plot<br>
<input type="radio" class="formradio" name="plot" value="log" $plot_log>logarithmic plot<br>
<input type="radio" class="formradio" name="plot" value="sqrtlog" $sqrtplot_log>sqrt-logarithmic plot
EOF

justonemonth=true
ONLYONE=true
save_name=$NAME
NAME=series
DECOR=true
INCLUDE_SQUARE=true
INCLUDE_CUBE=true
INCLUDE_TWOTHIRD=true
. ./commonoptions.cgi
NAME=$save_name

echo "<tr><td>Change sign:"
echo "<td><input type=\"checkbox\" class=\"formcheck\" name=\"changesign\" $changesign_checked>study the low extremes<td><a href=\"javascript:pop_page('help/changesign.shtml',284,450)\"><img align=\"right\" src=\"images/info-i.gif\" alt=\"help\" border=\"0\"></a>"

echo "<tr><td>Fit:<td>"
echo "<input type=\"radio\" class=\"formradio\" name=\"fit\" value=\"none\" $fit_none>nothing"
echo "<input type=\"radio\" class=\"formradio\" name=\"fit\" value=\"poisson\" $fit_poisson>Poisson"
echo "<input type=\"radio\" class=\"formradio\" name=\"fit\" value=\"gauss\" $fit_gauss>Gauss"
echo "<input type=\"radio\" class=\"formradio\" name=\"fit\" value=\"gamma\" $fit_gamma>Gamma"
echo "<input type=\"radio\" class=\"formradio\" name=\"fit\" value=\"gumbel\" $fit_gumbel>Gumbel"
echo "<input type=\"radio\" class=\"formradio\" name=\"fit\" value=\"gev\" $fit_gev>GEV<br>"
echo "<input type=\"radio\" class=\"formradio\" name=\"fit\" value=\"gpd\" $fit_gpd>GPD, threshold"
echo "<input type=\"$number\" class=\"forminput\" name=\"dgt\" value=\"${FORM_dgt:-80}\" $textsize6>%"
echo "<select class=\"forminput\" name=\"restrain\">"
echo "<option value=\"0\" $select00>do not constrain shape"
echo "<option value=\"0.5\" $select05>constrain shape to &plusmn;0.5"
echo "<option value=\"0.4\" $select04>constrain shape to &plusmn;0.4"
echo "<option value=\"0.3\" $select03>constrain shape to &plusmn;0.3"
echo "<option value=\"0.2\" $select02>constrain shape to &plusmn;0.2"
echo "</select>"
echo "<tr><td>Return time:<td>year <input type=\"$number\" min=1 max=2500 step=1 class=\"forminput\" name=\"year\" $textsize4 value=\"$FORM_year\"> or value <input type=\"text\" class=\"forminput\" name=\"xyear\" $textsize6 value=\"$FORM_xyear\">"
if [ -n "$ENSEMBLE" ]; then
cat <<EOF
<tr><td>Ensemble members:
<td><input type="$number" min=0 step=1 class="forminput" name="nens1" $textsize2 value="$FORM_nens1">to
<input type="$number" min=0 step=1 class="forminput" name="nens2" $textsize2 value="$FORM_nens2">
EOF
fi
cat <<EOF
<tr><td>Plot range:<td>X <input type="$number" step=any class="forminput" name="xlo" $textsize4 value="$FORM_xlo">:<input type="$number" step=any class="forminput" name="xhi" $textsize4 value="$FORM_xhi">,
Y <input type="$number" step=any class="forminput" name="ylo" $textsize4 value="$FORM_ylo">:<input type="$number" step=any class="forminput" name="yhi" $textsize4 value="$FORM_yhi">
<tr><td>Confidence interval:<td><input type="$number" step=any class="forminput" name="ci" $textsize4 value="${FORM_ci:-95}">%
<tr><td colspan="2"><input type="submit" class="formbutton" value="Compute">
</table>
</div>
</form>
EOF

. ./myvinkfoot.cgi
