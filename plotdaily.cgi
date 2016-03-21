#!/bin/sh
#
# plot the last N days of a dailytime series, inspired by the CPC/NCEP graphs at 
# http://www.cpc.ncep.noaa.gov/products/global_monitoring/temperature/global_temp_accum.shtml
#
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

. ./getargs.cgi
TYPE="$FORM_TYPE"
WMO="$FORM_WMO"
STATION="$FORM_STATION"
station=`echo "$STATION" | tr '_' ' '`
NAME="$FORM_NAME"
name=`echo "$NAME" | tr '_' ' '`
nday="$FORM_nday"
NPERYEAR="$FORM_NPERYEAR"
if [ -n "$FORM_mo" -a "${FORM_mo#0}" = "$FORM_mo" ]; then
    [ $FORM_mo -le 9 ] && FORM_mo=0$FORM_mo
fi
if [ -n "$FORM_dy" -a "${FORM_dy#0}" = "$FORM_dy" ]; then
    [ $FORM_dy -le 9 ] && FORM_dy=0$FORM_dy
fi
enddate="$FORM_yr$FORM_mo$FORM_dy"
if [ -z "$enddate" ]; then
    enddate=last
    last="Last "
else
    ending=" ending at $enddate"
fi

. ./nosearchengine.cgi
. ./nperyear2timescale.cgi
. ./myvinkhead.cgi "$last$nday ${month}s of $station $name" "" "noindex,nofollow"

if [ -n "$FORM_climyear1" -a -z "$FORM_climyear2" ]; then
    echo "Error: provide begin and end year of reference period"
    . ./myvinkfoot.cgi
    exit
fi
if [ -z "$FORM_climyear1" -a -n "$FORM_climyear2" ]; then
    echo "Error: provide begin and end year of reference period"
    . ./myvinkfoot.cgi
    exit
fi
if [ -z "$FORM_climyear1" -a -z "$FORM_climyear2" ]; then
    computed="computed with all data available"
    period=""
    beginend=""
else
    computed="computed over the period ${FORM_climyear1}:${FORM_climyear2}"
    period=" (${FORM_climyear1}:${FORM_climyear2})"
    beginend="begin ${FORM_climyear1} end ${FORM_climyear2}"
fi

eval `./bin/getunits ./data/$TYPE$WMO.dat`
###echo "./bin/getunits ./data/$TYPE$WMO.dat<br>"
###echo "NEWUNITS=$NEWUNITS<br>"
root=data/plot${nday}last$TYPE$WMO$KIND${FORM_climyear1}${FORM_climyear2}_$enddate
if [ $FORM_anom = zero ]; then
    anom=anom
fi
if [ -z "$FORM_cdf" ]; then
    if [ "$NEWUNITS" = "mm/day" -o "$TYPE" = p ]; then
        FORM_cdf=on
    else
        FORM_cdf=off
    fi
fi
if [ $FORM_cdf = on ]; then
    cdf=cdf
else
    cdf=""
fi

echo `date` "$EMAIL ($REMOTE_ADDR) plotdaily ./data/$TYPE$WMO.dat $nday $enddate $beginend $anom" >> log/log
(./bin/plotdaily ./data/$TYPE$WMO.dat $nday $enddate $cdf $beginend $anom > $root.txt) 2>&1
lastdate=`tail -n 1 $root.txt | cut -b 1-8`
[ -z "$FORM_yr" ] && FORM_yr=`echo "$lastdate" | cut -b 1-4`
[ -z "$FORM_mo" ] && FORM_mo=`echo "$lastdate" | cut -b 5-6`
[ -z "$FORM_dy" ] && FORM_dy=`echo "$lastdate" | cut -b 7-8`
lastdate=$((lastdate+1))
firstdate=`fgrep -v '#' $root.txt | head -n 1 | cut -b 1-8`
###echo firstdate,lastdate = $firstdate,$lastdate

echo "<div class=\"bijschrift\">$last$nday ${month}s of $name observations at $station$ending with climatology $computed"
echo "(<a href=\"$root.eps\">eps</a>, <a href="ps2pdf.cgi?file=$root.eps">pdf</a>, <a href=\"$root.txt\">raw data</a>)</div>"
if [ "$NPERYEAR" -ge 360 ]; then
    timefmt="'%Y%m%d'"
else
    timefmt="'%Y%m'"
fi
if [ "$NEWUNITS" = "mm/day" -o "$VAR" = "soilw" ]; then
    above=3
    below=1
else
    above=1
    below=3
fi

wmo_=`echo "$WMO" | tr '_' ' '`
./bin/gnuplot << EOF
$gnuplot_init
set size 0.8,0.6
set datafile missing "-999.900"
set zero 1e-40
set xzeroaxis
set term png $gnuplot_png_font_hires
set output "./$root.png"
set xdata time
set timefmt $timefmt
set format x $timefmt
set xrange ["$firstdate":"$lastdate"]
set ylabel "$VAR [$UNITS]"
set title "$name $station ($wmo_)"
plot "./$root.txt" using 1:2:3 notitle with filledcurves above lt $above, \
     "./$root.txt" using 1:2:3 notitle with filledcurves below lt $below, \
     "./$root.txt" using 1:2 notitle with lines lt -1, \
     "./$root.txt" using 1:3 notitle with lines lt -1

set term postscript epsf color solid
set output "./$root.eps"
replot
quit
EOF

pngfile="./$root.png"
getpngwidth
echo "<center><img src=\"$pngfile\" alt=\"last $nday ${months}s of $name at $station\" width="$halfwidth" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

if [ $FORM_cdf = on ]; then
    cdf_checked=checked
else
    cdf_unchecked=checked
fi
if [ $FORM_anom = zero ]; then
    zero_checked=checked
else
    range_checked=checked
fi

cat <<EOF
<div class="formbody">
<form action="plotdaily.cgi" method="POST">
<input type="hidden" name="EMAIL" value="$EMAIL">
<input type="hidden" name="TYPE" value="$TYPE">
<input type="hidden" name="WMO" value="$WMO">
<input type="hidden" name="STATION" value="$STATION">
<input type="hidden" name="NAME" value="$NAME">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<table style='width:100%' border='0' cellpadding='0' cellspacing='0'>
<tr><td>Replot: 
<td><input type="$number" min="1" max="1000" step=1 name="nday" $textsize3 value="$nday">
${month}s with end date
<input type="$number" min="1" max="2400" step=1 name="yr" $textsize4 value="$FORM_yr">
EOF
if [ ${NPERYEAR:-12} -gt 1 ]; then
    echo "<input type="$number" min="1" max="12" step=1 name="mo" $textsize2 value="$FORM_mo">"
fi
if [ ${NPERYEAR:-12} -gt 12 ]; then
    echo "<input type="$number" min="1" max="31" step=1 name="dy" $textsize2 value="$FORM_dy">"
fi
cat <<EOF
<tr><td>Plot:
<td>
<input type=radio class=formradio name="cdf" value="off" $cdf_unchecked>observations
<input type=radio class=formradio name="cdf" value="on" $cdf_checked>cumulatives
<tr><td>Compare with:
<td>
<input type=radio class=formradio name="anom" value="range" $range_checked>climatology
<input type="$number" min="1" max="2400" step=1 name="climyear1" $textsize4 value="$FORM_climyear1">-<input type="$number" min="1" max="2400" step=1 name="climyear2" $textsize4 value="$FORM_climyear2">
<br>
<input type=radio class=formradio name="anom" value="zero" $zero_checked>zero, data are already anomalies
<tr><td>
<input type="submit" class="formbutton" value="plot">
</table>
</form>
</div>
EOF

. ./myvinkfoot.cgi
