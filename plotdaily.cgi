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

. ./nosearchengine.cgi

. ./myvinkhead.cgi "Time series of the last $nday days of $station $name" "" "noindex,nofollow"

if [ -n "$FORM_climyear1" -a -z "$FORM_climyear2" ]; then
        echo "Error: provide begin and end year of reference period"
        exit
fi
if [ -z "$FORM_climyear1" -a -n "$FORM_climyear2" ]; then
    echo "Error: provide begin and end year of reference period"
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
root=data/plot${nday}daily$TYPE$WMO$KIND

echo `date` "$EMAIL ($REMOTE_ADDR) plotdaily ./data/$TYPE$WMO.dat $nday $beginend" >> log/log
(./bin/plotdaily ./data/$TYPE$WMO.dat $nday $beginend > $root.txt) 2>&1
lastdate=`tail -n 1 $root.txt | cut -b 1-8`

echo "<div class=\"bijschrift\"> Last $nday days of $name observations at $station with climatology $computed"
echo "(<a href=\"$root.eps\">eps</a>, <a href="ps2pdf.cgi?file=$root.eps">pdf</a>, <a href=\"$root.txt\">raw data</a>)</div>"

./bin/gnuplot << EOF
set size 0.8,0.6
set datafile missing "-999.900"
set zero 1e-40
set xzeroaxis
set term png $gnuplot_png_font_hires
set output "./$root.png"
set xdata time
set timefmt "%Y%m%d"
set format x '%Y%m%d'
set xrange [:"$lastdate"]
set ylabel "$VAR [$UNITS]"
set title "$name $station ($WMO)"
plot "./$root.txt" using 1:2:3 notitle with filledcurves above lt 1, \
     "./$root.txt" using 1:2:3 notitle with filledcurves below lt 3, \
     "./$root.txt" using 1:2 notitle with lines lt -1, \
     "./$root.txt" using 1:3 notitle with lines lt -1

set term postscript epsf color solid
set output "./$root.eps"
replot
quit
EOF

pngfile="./$root.png"
getpngwidth
echo "<center><img src=\"$pngfile\" alt=\"last $nday days of $name at $station\" width="$halfwidth" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

. ./myvinkfoot.cgi
