#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi
TYPE="$FORM_TYPE"
WMO="$FORM_WMO"
STATION="$FORM_STATION"
NAME="$FORM_NAME"
KIND="$FORM_KIND"

. ./nosearchengine.cgi

. ./myvinkhead.cgi "Time series plots per ${KIND}" "$STATION $NAME" "noindex,nofollow"

eval `./bin/getunits $DIR/data/$TYPE$WMO.dat`
($DIR/bin/series $DIR/data/$TYPE$WMO.dat plot $DIR/data/ts$TYPE$WMO.plt > $DIR/data/ts$TYPE$WMO.txt) 2>&1
echo "<div class=\"bijschrift\">The thick line is a 10-year running average "
echo "(<a href=\"data/ts$TYPE$WMO$KIND.eps.gz\">eps</a>, <a href="ps2pdf.cgi?file=data/ts$TYPE$WMO$KIND.eps.gz">pdf</a>, <a href=\"data/ts$TYPE$WMO.txt\">raw data</a>)</div>"

. ./setyaxis.cgi

for ext in eps png
do
    if [ $ext = eps ];then
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
set output "$DIR/data/ts$TYPE$WMO$KIND.$ext"
set format y "%8.2f"
set title
set multiplot
set size 0.70,0.225
set origin 0,2.2
set ylabel 'Jan'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:22 notitle with lines lt 2 lw 5,\
     "$DIR/data/ts$TYPE$WMO.plt" u 1:2  notitle with steps lt 1
set origin 0,2.0
set ylabel 'Feb'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:23 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:3  notitle with steps lt 1
set origin 0,1.8
set ylabel 'Mar'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:24 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:4  notitle with steps lt 1
set origin 0,1.6
set ylabel 'Apr'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:25 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:5  notitle with steps lt 1
set origin 0,1.4
set ylabel 'May'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:26 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:6  notitle with steps lt 1
set origin 0,1.2
set ylabel 'Jun'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:27 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:7  notitle with steps lt 1
set origin 0,1.0
set ylabel 'Jul'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:28 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:8  notitle with steps lt 1
set origin 0,0.8
set ylabel 'Aug'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:29 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:9  notitle with steps lt 1
set origin 0,0.6
set ylabel 'Sep'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:30 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:10 notitle with steps lt 1
set origin 0,0.4
set ylabel 'Oct'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:31 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:11 notitle with steps lt 1
set origin 0,0.2
set ylabel 'Nov'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:32 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:12 notitle with steps lt 1
set origin 0,0.0
set ylabel 'Dec'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:33 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:13 notitle with steps lt 1
set nomultiplot
quit
EOF
        else # more modern version of gnuplot
            ./bin/gnuplot << EOF
set origin 0,0
set datafile missing "-999.900"
set zero 1e-40
set xzeroaxis
set term $term size $mosize
set output "$DIR/data/ts$TYPE$WMO$KIND.$ext"
set format y "%8.2f"
set title
set multiplot
set size 1,0.091
set origin 0,0.88
set ylabel 'Jan'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:22 notitle with lines lt 2 lw 5,\
     "$DIR/data/ts$TYPE$WMO.plt" u 1:2  notitle with steps lt 1
set origin 0,0.80
set ylabel 'Feb'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:23 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:3  notitle with steps lt 1
set origin 0,0.72
set ylabel 'Mar'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:24 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:4  notitle with steps lt 1
set origin 0,0.64
set ylabel 'Apr'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:25 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:5  notitle with steps lt 1
set origin 0,0.56
set ylabel 'May'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:26 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:6  notitle with steps lt 1
set origin 0,0.48
set ylabel 'Jun'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:27 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:7  notitle with steps lt 1
set origin 0,0.40
set ylabel 'Jul'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:28 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:8  notitle with steps lt 1
set origin 0,0.32
set ylabel 'Aug'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:29 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:9  notitle with steps lt 1
set origin 0,0.24
set ylabel 'Sep'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:30 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:10 notitle with steps lt 1
set origin 0,0.16
set ylabel 'Oct'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:31 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:11 notitle with steps lt 1
set origin 0,0.08
set ylabel 'Nov'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:32 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:12 notitle with steps lt 1
set origin 0,0
set ylabel 'Dec'
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:33 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:13 notitle with steps lt 1
set nomultiplot
quit
EOF
        fi
            ;;
        season)
            $DIR/bin/gnuplot << EOF
set size 0.7,1
set origin 0,0
set datafile missing "-999.900"
set zero 1e-40
set xzeroaxis
set term $term
set output "$DIR/data/ts$TYPE$WMO$KIND.$ext"
set format y "%8.2f"
set title
set multiplot
set size 0.7,0.275
set origin 0,0.75
set ylabel 'Dec-Feb'
###set yrange [-4:7]
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:34 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:14 notitle with steps lt 1 
set origin 0,0.5
set ylabel 'Mar-May'
###set yrange [0:300]
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:35 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:15 notitle with steps lt 1
set origin 0,0.25
set ylabel 'Jun-Aug'
###set yrange [11:22]
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:36 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:16 notitle with steps lt 1
set origin 0.,0
set ylabel 'Sep-Nov'
###set yrange [5:16]
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:37 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:17 notitle with steps lt 1
set nomultiplot
quit
EOF
            ;;
        half)
            $DIR/bin/gnuplot << EOF
set size 0.7,1
set datafile missing "-999.900"
set zero 1e-40
set xzeroaxis
set term $term
set output "$DIR/data/ts$TYPE$WMO$KIND.$ext"
set format y "%8.2f"
set ylabel "$VAR [$UNITS]"
set multiplot
set size 0.7,0.5
set origin 0,0.5
set title "Oct-Mar $NAME $STATION ($WMO)"
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:38 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:18 notitle with steps lt 1
set origin 0,0
set title "Apr-Sep $NAME $STATION ($WMO)"
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:39 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:19 notitle with steps lt 1
set nomultiplot
quit
EOF
            ;;
        yr0)
            $DIR/bin/gnuplot << EOF
set datafile missing "-999.900"
set zero 1e-40
set xzeroaxis
set size 0.7,0.5
set term $term
set title "Jan-Dec $NAME $STATION ($WMO)"
set ylabel "$VAR [$UNITS]"
set output "$DIR/data/ts$TYPE$WMO$KIND.$ext"
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:40 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:20 notitle with steps lt 1
quit
EOF
            ;;
        yr1)
            $DIR/bin/gnuplot << EOF
set datafile missing "-999.900"
set zero 1e-40
set xzeroaxis
set size 0.7,0.5
set term $term
set title "Jul-Jun $NAME $STATION ($WMO)"
set ylabel "$VAR [$UNITS]"
set output "$DIR/data/ts$TYPE$WMO$KIND.$ext"
plot "$DIR/data/ts$TYPE$WMO.plt" u 1:41 notitle with lines lt 2 lw 5, \
     "$DIR/data/ts$TYPE$WMO.plt" u 1:21 notitle with steps lt 1
quit
EOF
            ;;
        *) echo "Cannot handle KIND=$KIND yet";exit;;
    esac
done
###rm data/ts$TYPE$WMO$KIND.plt
gzip -f $DIR/data/ts$TYPE$WMO$KIND.eps
pngfile=data/ts$TYPE$WMO$KIND.png
getpngwidth
echo "<center><img src=\"data/ts$TYPE$WMO$KIND.png\" alt=\"time series per $KIND\" width=\"$halfwidth\" border=0 class="realimage" hspace=0 vspace=0></center>"

. ./myvinkfoot.cgi
