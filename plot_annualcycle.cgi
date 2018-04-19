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

if [ $FORM_type = -1 ]; then
    suffix=yrm1
    setxrange='set xrange ["20000701":"20010630"]
set xtics ("Jul" "20000715", "Aug" "20000815", "Sep" "20000915", "Oct" "20001015", "Nov" "20001115", "Dec" "20001215", "Jan" "20010115", "Feb" "20010214", "Mar" "20010315", "Apr" "20010415", "May" "20010515", "Jun" "20010615")'    
else
    suffix=yr1
    setxrange='set xrange ["20000101":"20001231"]
set xtics ("Jan" "20000115", "Feb" "20000214", "Mar" "20000315", "Apr" "20000415", "May" "20000515", "Jun" "20000615", "Jul" "20000715", "Aug" "20000815", "Sep" "20000915", "Oct" "20001015", "Nov" "20001115", "Dec" "20001215")'
fi
if [ -n "$period" ]; then
    suffix=${suffix}_`echo "$period" | tr -d -c '[0-9]'`
fi

echo 'Content-Type: text/html'
echo
. ./myvinkhead.cgi "Annual cycle of $VAR" "$station" 

###echo "base=\"$base\"<br>"
name_=`echo $name | tr "_" " "`
station_=`echo $station | tr "_" " "`

echo "<div class=\"bijschrift\">Annual cycle, $computed_"
echo "(<a href=\"${base}_$suffix.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${base}_$suffix.eps.gz\">pdf</a>, 
<a href=\"${base}_yr.txt\">raw data</a>)."
ylabel=`echo "$VAR $plotunits" | tr '_' ' '`
if [ \( ! -s ${base}_$suffix.png \) -o ${base}_$suffix.png -ot ${base}_yr.plt ]; then
	./bin/gnuplot << EOF
$gnuplot_init
###set title "$title"
set datafile missing "0.300000E+34"
set size 0.5,.4
set zeroaxis
set xdata time
set timefmt "%Y%m%d"
set xtics nomirror
set xtics scale 0.
$setxrange
$setyrange
$setformaty
set ylabel "$ylabel"
set term postscript epsf color solid
set output "./${base}_$suffix.eps"
plot \
 "./${base}_yr.plt" using 1:3 title "2.5%,17%,83%,97.5% percentiles" with steps lt 2 lw 2,\
 "./${base}_yr.plt" using 1:4 notitle with steps lt 2 lw 2,\
 "./${base}_yr.plt" using 1:6 notitle with steps lt 2 lw 2,\
 "./${base}_yr.plt" using 1:7 notitle with steps lt 2 lw 2,\
"./${base}_yr.plt" using 1:2 title "mean $name_ $station_ $period" w steps lt 1 lw 4
set term png $gnuplot_png_font_hires
set out "./${base}_$suffix.png"
replot
quit
EOF
    gzip -f ./${base}_$suffix.eps
fi
pngfile=${base}_$suffix.png
getpngwidth
echo "<center><img src=\"${base}_$suffix.png\" alt=\"annual cycle\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

. ./myvinkfoot.cgi
exit
