#!/bin/bash
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi
TYPE="$FORM_TYPE"
WMO="$FORM_WMO"
wmo=`echo "$WMO" | tr '_' ' '`
STATION="$FORM_STATION"
station=`echo "$STATION" | tr '_' ' '`
NAME="$FORM_NAME"
name=`echo "$NAME" | tr '_' ' '`
KIND="$FORM_KIND"
case $KIND in
    yr) kind="year";;
    yr0) kind="year (Jan-Dec)";;
    yr1) kind="year (Jul-Jun)";;
    half) kind="half year";;
    *) kind="$KIND"
esac

. ./nosearchengine.cgi

. ./myvinkhead.cgi "Time series plots per $kind" "$station $name" "noindex,nofollow"

eval `./bin/getunits ./data/$TYPE$WMO.dat`
if [ "$NPERYEAR" = 1 ]; then
    WMO_new=${WMO}_ave12
    yearly2shorter ./data/$TYPE$WMO.dat 12 > ./data/$TYPE$WMO_new.dat
else
    WMO_new=$WMO
fi
(./bin/series ./data/$TYPE$WMO_new.dat plot ./data/ts$TYPE$WMO.plt > ./data/ts$TYPE$WMO.txt) 2>&1
echo "<div class=\"bijschrift\">Time series plots of $station $name per $kind. The thick line is a 10-year running average "
echo "(<a href=\"data/ts$TYPE$WMO$KIND.eps.gz\">eps</a>, <a href="ps2pdf.cgi?file=data/ts$TYPE$WMO$KIND.eps.gz">pdf</a>, <a href=\"data/ts$TYPE$WMO.txt\">raw data</a>)</div>"

. ./setyaxis.cgi
var=`echo "$VAR" | tr '_' ' '`

for ext in eps png
do
    if [ $ext = eps ]; then
        term="postscript epsf color solid"
        mosize="4.5,12.5"
    elif [ $ext = png ]; then
        term="png $gnuplot_png_font_hires"
        mosize="900,2500"
    else
        term=weetikniet
    fi
    
    case $KIND in
        month)
        version=`./bin/gnuplot -V | cut -d ' ' -f 2 | tr -d '.'`
        if [ $version -le 40 ]; then # this works in old gnuplot
            ./bin/gnuplot << EOF
set size 0.7,2.4
set origin 0,0
set datafile missing "-999.900"
set zero 1e-40
set xzeroaxis
set term $term
set output "./data/ts$TYPE$WMO$KIND.$ext"
set format y "%8.2f"
set title
set multiplot
set size 0.70,0.225
set origin 0,2.2
set ylabel 'Jan'
plot "./data/ts$TYPE$WMO.plt" u 1:22 notitle with lines lt 2 lw 5,\
     "./data/ts$TYPE$WMO.plt" u 1:2  notitle with steps lt 1
set origin 0,2.0
set ylabel 'Feb'
plot "./data/ts$TYPE$WMO.plt" u 1:23 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:3  notitle with steps lt 1
set origin 0,1.8
set ylabel 'Mar'
plot "./data/ts$TYPE$WMO.plt" u 1:24 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:4  notitle with steps lt 1
set origin 0,1.6
set ylabel 'Apr'
plot "./data/ts$TYPE$WMO.plt" u 1:25 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:5  notitle with steps lt 1
set origin 0,1.4
set ylabel 'May'
plot "./data/ts$TYPE$WMO.plt" u 1:26 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:6  notitle with steps lt 1
set origin 0,1.2
set ylabel 'Jun'
plot "./data/ts$TYPE$WMO.plt" u 1:27 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:7  notitle with steps lt 1
set origin 0,1.0
set ylabel 'Jul'
plot "./data/ts$TYPE$WMO.plt" u 1:28 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:8  notitle with steps lt 1
set origin 0,0.8
set ylabel 'Aug'
plot "./data/ts$TYPE$WMO.plt" u 1:29 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:9  notitle with steps lt 1
set origin 0,0.6
set ylabel 'Sep'
plot "./data/ts$TYPE$WMO.plt" u 1:30 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:10 notitle with steps lt 1
set origin 0,0.4
set ylabel 'Oct'
plot "./data/ts$TYPE$WMO.plt" u 1:31 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:11 notitle with steps lt 1
set origin 0,0.2
set ylabel 'Nov'
plot "./data/ts$TYPE$WMO.plt" u 1:32 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:12 notitle with steps lt 1
set origin 0,0.0
set ylabel 'Dec'
plot "./data/ts$TYPE$WMO.plt" u 1:33 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:13 notitle with steps lt 1
set nomultiplot
quit
EOF
        else # more modern version of gnuplot
            ./bin/gnuplot << EOF
$gnuplot_init
set origin 0,0
set datafile missing "-999.900"
set zero 1e-40
$setxzeroaxis
set term $term size $mosize
set output "./data/ts$TYPE$WMO$KIND.$ext"
set format y "%8.2f"
set title
set multiplot
set size 1,0.091
set origin 0,0.88
set ylabel 'Jan'
plot "./data/ts$TYPE$WMO.plt" u 1:22 notitle with lines lt 2 lw 5,\
     "./data/ts$TYPE$WMO.plt" u 1:2  notitle with steps lt 1
set origin 0,0.80
set ylabel 'Feb'
plot "./data/ts$TYPE$WMO.plt" u 1:23 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:3  notitle with steps lt 1
set origin 0,0.72
set ylabel 'Mar'
plot "./data/ts$TYPE$WMO.plt" u 1:24 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:4  notitle with steps lt 1
set origin 0,0.64
set ylabel 'Apr'
plot "./data/ts$TYPE$WMO.plt" u 1:25 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:5  notitle with steps lt 1
set origin 0,0.56
set ylabel 'May'
plot "./data/ts$TYPE$WMO.plt" u 1:26 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:6  notitle with steps lt 1
set origin 0,0.48
set ylabel 'Jun'
plot "./data/ts$TYPE$WMO.plt" u 1:27 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:7  notitle with steps lt 1
set origin 0,0.40
set ylabel 'Jul'
plot "./data/ts$TYPE$WMO.plt" u 1:28 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:8  notitle with steps lt 1
set origin 0,0.32
set ylabel 'Aug'
plot "./data/ts$TYPE$WMO.plt" u 1:29 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:9  notitle with steps lt 1
set origin 0,0.24
set ylabel 'Sep'
plot "./data/ts$TYPE$WMO.plt" u 1:30 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:10 notitle with steps lt 1
set origin 0,0.16
set ylabel 'Oct'
plot "./data/ts$TYPE$WMO.plt" u 1:31 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:11 notitle with steps lt 1
set origin 0,0.08
set ylabel 'Nov'
plot "./data/ts$TYPE$WMO.plt" u 1:32 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:12 notitle with steps lt 1
set origin 0,0
set ylabel 'Dec'
plot "./data/ts$TYPE$WMO.plt" u 1:33 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:13 notitle with steps lt 1
set nomultiplot
quit
EOF
        fi
            ;;
        season)
            ./bin/gnuplot << EOF
$gnuplot_init
set size 0.7,1
set origin 0,0
set datafile missing "-999.900"
set zero 1e-40
$setxzeroaxis
set term $term
set output "./data/ts$TYPE$WMO$KIND.$ext"
set format y "%8.2f"
set title
set multiplot
set size 0.7,0.275
set origin 0,0.75
set ylabel 'Dec-Feb'
###set yrange [-4:7]
plot "./data/ts$TYPE$WMO.plt" u 1:34 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:14 notitle with steps lt 1 
set origin 0,0.5
set ylabel 'Mar-May'
###set yrange [0:300]
plot "./data/ts$TYPE$WMO.plt" u 1:35 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:15 notitle with steps lt 1
set origin 0,0.25
set ylabel 'Jun-Aug'
###set yrange [11:22]
plot "./data/ts$TYPE$WMO.plt" u 1:36 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:16 notitle with steps lt 1
set origin 0.,0
set ylabel 'Sep-Nov'
###set yrange [5:16]
plot "./data/ts$TYPE$WMO.plt" u 1:37 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:17 notitle with steps lt 1
set nomultiplot
quit
EOF
            ;;
        half)
            ./bin/gnuplot << EOF
$gnuplot_init
set size 0.7,1
set datafile missing "-999.900"
set zero 1e-40
$setxzeroaxis
set term $term
set output "./data/ts$TYPE$WMO$KIND.$ext"
set format y "%8.2f"
set ylabel "$var [$UNITS]"
set multiplot
set size 0.7,0.5
set origin 0,0.5
set title "Oct-Mar $name $station ($wmo)"
plot "./data/ts$TYPE$WMO.plt" u 1:38 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:18 notitle with steps lt 1
set origin 0,0
set title "Apr-Sep $name $station ($wmo)"
plot "./data/ts$TYPE$WMO.plt" u 1:39 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:19 notitle with steps lt 1
set nomultiplot
quit
EOF
            ;;
        yr)
            ./bin/gnuplot << EOF
$gnuplot_init
set datafile missing "-999.900"
set zero 1e-40
set xzeroaxis
set size 0.7,0.5
set term $term
set title "$name $station ($wmo)"
set ylabel "$var [$UNITS]"
set output "./data/ts$TYPE$WMO$KIND.$ext"
plot "./data/ts$TYPE$WMO.plt" u 1:40 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:20 notitle with steps lt 1
quit
EOF
            ;;
        yr0)
            ./bin/gnuplot << EOF
$gnuplot_init
set datafile missing "-999.900"
set zero 1e-40
set xzeroaxis
set size 0.7,0.5
set term $term
set title "Jan-Dec $name $station ($wmo)"
set ylabel "$var [$UNITS]"
set output "./data/ts$TYPE$WMO$KIND.$ext"
plot "./data/ts$TYPE$WMO.plt" u 1:40 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:20 notitle with steps lt 1
quit
EOF
            ;;
        yr1)
            ./bin/gnuplot << EOF
$gnuplot_init
set datafile missing "-999.900"
set zero 1e-40
set xzeroaxis
set size 0.7,0.5
set term $term
set title "Jul-Jun $name $station ($wmo)"
set ylabel "$var [$UNITS]"
set output "./data/ts$TYPE$WMO$KIND.$ext"
plot "./data/ts$TYPE$WMO.plt" u 1:41 notitle with lines lt 2 lw 5, \
     "./data/ts$TYPE$WMO.plt" u 1:21 notitle with steps lt 1
quit
EOF
            ;;
        *) echo "Cannot handle KIND=$KIND yet";exit;;
    esac
done
###rm data/ts$TYPE$WMO$KIND.plt
gzip -f ./data/ts$TYPE$WMO$KIND.eps
pngfile=data/ts$TYPE$WMO$KIND.png
getpngwidth
echo "<center><img src=\"data/ts$TYPE$WMO$KIND.png\" alt=\"time series per $kind\" width=\"$halfwidth\" border=0 class="realimage" hspace=0 vspace=0></center>"

. ./myvinkfoot.cgi
