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
NPERYEAR="$FORM_NPERYEAR"
if [ $EMAIL = oldenborgh@knmi.nl ]; then
    lwrite=true
fi

TYPE="$FORM_TYPE"
WMO="$FORM_WMO"
STATION="$FORM_STATION"
station=`echo "$STATION" | tr '_' ' '`
NAME="$FORM_NAME"
name=`echo "$NAME" | tr '_' ' '`
if [ ! -s ./data/$TYPE$WMO.dat ]; then
    . ./myvinkhead.cgi "Error" "Cannot find file"
    echo "Cannot find file $TYPE$WMO"
    . ./myvinkfoot.cgi
    exit
fi

. ./nosearchengine.cgi
. ./nperyear2timescale.cgi
. ./myvinkhead.cgi "$last$nday ${month}s of $station $name" "" "noindex,nofollow"

# arguments trump remembered values
nday="$FORM_nday"
yr=$FORM_yr
mo=$FORM_mo
dy=$FORM_dy
cdf=$FORM_cdf
anom=$FORM_anom
climyear1=$FORM_climyear1
climyear2=$FORM_climyear2
if [ "$lwrite" = true ]; then
    echo "After argument processing nday=$nday<br>"
fi

if [ $EMAIL != someone@somewhere ]; then
    def=prefs/$EMAIL.plotdaily.$NPERYEAR
    if [ -f $def ]; then
        eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.%]*;$' $def`
    fi
fi

[ -z "$nday" ] && nday="$FORM_nday"
[ -z "$yr" ] && yr=$FORM_yr
[ -z "$mo" ] && mo=$FORM_mo
[ -z "$dy" ] && dy=$FORM_dy
[ -z "$cdf" ] && cdf=$FORM_cdf
[ -z "$anom" ] && anom=$FORM_anom
[ -z "$climyear1" ] && climyear1=$FORM_climyear1
[ -z "$climyear2" ] && climyear2=$FORM_climyear2
if [ "$lwrite" = true ]; then
    echo "After remembering last time nday=$nday<br>"
fi

eval `./bin/getunits ./data/$TYPE$WMO.dat`
[ -z "$nday" ] && nday=$NPERYEAR
if [ -n "$mo" -a "${mo#0}" = "$mo" ]; then
    [ $mo -le 9 ] && mo=0$mo
fi
if [ -n "$dy" -a "${dy#0}" = "$dy" ]; then
    [ $dy -le 9 ] && dy=0$dy
fi
enddate="$yr$mo$dy"
if [ -z "$enddate" ]; then
    enddate=last
    last="Last "
else
    ending=" ending at $enddate"
fi


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
root=data/plot${nday}last$TYPE$WMO$KIND${FORM_climyear1}${FORM_climyear2}_$enddate
if [ $anom = zero ]; then
    anomarg=anom
fi
if [ -z "$cdf" ]; then
    if [ "$NEWUNITS" = "mm/day" -o "$TYPE" = p ]; then
        cdf=on
    else
        cdf=off
    fi
fi
if [ $cdf = on ]; then
    cdfarg=cdf
else
    cdfarg=""
fi

echo `date` "$EMAIL ($REMOTE_ADDR) plotdaily ./data/$TYPE$WMO.dat $nday $enddate $cdfarg $beginend $anomarg" >> log/log
(./bin/plotdaily ./data/$TYPE$WMO.dat $nday $enddate $cdfarg $beginend $anomarg > $root.txt) 2>&1
lastdate=`grep '[0-9]' $root.txt | tail -n 1 | cut -b 1-8`
[ -z "$yr" ] && yr=`echo "$lastdate" | cut -b 1-4`
[ -z "$mo" ] && mo=`echo "$lastdate" | cut -b 5-6`
[ -z "$dy" ] && dy=`echo "$lastdate" | cut -b 7-8`
lastdate=$((lastdate+1))
firstdate=`fgrep -v '#' $root.txt | grep '[0-9]' | head -n 1 | cut -b 1-8`
###echo firstdate,lastdate = $firstdate,$lastdate
if [ $anom != zero ]; then
    with="with climatology $computed"
fi
echo "<div class=\"bijschrift\">$last$nday ${month}s of $name observations at $station$ending $with"
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

if [ "$cdf" = on ]; then
    cdf_checked=checked
else
    cdf_unchecked=checked
fi
if [ "$anom" = zero ]; then
    zero_checked=checked
else
    range_checked=checked
fi

if [ $EMAIL != someone@somewhere ]; then
    cat > $def <<EOF
FORM_nday=$nday;
FORM_yr=$yr;
FORM_mo=$mo;
FORM_dy=$dy;
FORM_cdf=$cdf;
FORM_anom=$anom;
FORM_climyear1=$climyear1;
FORM_climyear2=$climyear2;
EOF
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
<input type="$number" min="1" max="2400" step=1 name="yr" $textsize4 value="$yr">
EOF
if [ ${NPERYEAR:-12} -gt 1 ]; then
    echo "<input type="$number" min="1" max="12" step=1 name="mo" $textsize2 value="$mo">"
fi
if [ ${NPERYEAR:-12} -gt 12 ]; then
    echo "<input type="$number" min="1" max="31" step=1 name="dy" $textsize2 value="$dy">"
fi
cat <<EOF
<tr><td>Plot:
<td>
<input type=radio class=formradio name="cdf" value="off" $cdf_unchecked>observations
<input type=radio class=formradio name="cdf" value="on" $cdf_checked>cumulatives
<tr><td>Compare with:
<td>
<input type=radio class=formradio name="anom" value="range" $range_checked>climatology
<input type="$number" min="1" max="2400" step=1 name="climyear1" $textsize4 value="$climyear1">-<input type="$number" min="1" max="2400" step=1 name="climyear2" $textsize4 value="$climyear2">
<br>
<input type=radio class=formradio name="anom" value="zero" $zero_checked>zero, data are already anomalies
<tr><td>
<input type="submit" class="formbutton" value="plot">
</table>
</form>
</div>
EOF

. ./myvinkfoot.cgi
