#!/bin/sh
. ./init.cgi
. ./getargs.cgi

base=`echo $FORM_base | tr '%' '+'`
computed_=`echo "$FORM_computed" | tr '_' ' '`
station=$FORM_station
name=$FORM_name
period=$FORM_period
VAR=$FORM_VAR
plotunits=$FORM_plotunits

echo 'Content-Type: text/html'
echo
. ./myvinkhead.cgi "Annual cycle of $VAR" "$station" 

###echo "base=\"$base\"<br>"
name_=`echo $name | tr "_" " "`
station_=`echo $station | tr "_" " "`

echo "<div class=\"bijschrift\">Annual cycle, $computed_"
echo "(<a href=\"${base}_yr1.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${base}_yr1.eps.gz\">pdf</a>, 
<a href=\"${base}_yr1.txt\">raw data</a>)."
ylabel=`echo "$VAR $plotunits" | tr '_' ' '`
# when plotting pressure, subtract 1000
if [ \( ! -s ${base}_yr1.png \) -o ${base}_yr1.png -ot ${base}_yr.plt ]; then
	./bin/gnuplot << EOF
$gnuplot_init
###set title "$title"
set datafile missing "0.300000E+34"
set size 0.5,.4
set zeroaxis
set xdata time
set timefmt "%Y%m%d"
set xrange ["20000101":"20001231"]
set xtics nomirror
set xtics scale 0.
set xtics ("Jan" "20000115", "Feb" "20000214", "Mar" "20000315", "Apr" "20000415", "May" "20000515", "Jun" "20000615", "Jul" "20000715", "Aug" "20000815", "Sep" "20000915", "Oct" "20001015", "Nov" "20001115", "Dec" "20001215")
$setyrange
$setformaty
set ylabel "$ylabel"
set term postscript epsf color solid
set output "./${base}_yr1.eps"
plot \
 "./${base}_yr.plt" using 1:3 title "2.5%,17%,83%,97.5% percentiles" with steps lt 2 lw 2,\
 "./${base}_yr.plt" using 1:4 notitle with steps lt 2 lw 2,\
 "./${base}_yr.plt" using 1:6 notitle with steps lt 2 lw 2,\
 "./${base}_yr.plt" using 1:7 notitle with steps lt 2 lw 2,\
"./${base}_yr.plt" using 1:2 title "mean $name_ $station_$period" w steps lt 1 lw 4
set term png $gnuplot_png_font_hires
set out "./${base}_yr1.png"
replot
quit
EOF
    gzip -f ./${base}_yr1.eps
fi
pngfile=${base}_yr1.png
getpngwidth
echo "<center><img src=\"${base}_yr1.png\" alt=\"annual cycle\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

. ./myvinkfoot.cgi
exit
