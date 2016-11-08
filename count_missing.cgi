#!/bin/sh
# to be sourced from other scripts
if [ $EMAIL = oldenborgh@knmi.nl ]; then
    lwrite=false # true
fi
if [ ${NPERYEAR:-12} -gt 12 ]; then
    base=./data/$TYPE$WMO
    if [ ! -s ${base}_missing.txt -o ${base}_missing.plt -ot $base.dat ]; then
        [ "$lwrite" = true ] && echo "./bin/count_missing .$base.dat"
		( ./bin/count_missing $base.dat > ${base}_missing.txt ) 2>&1
    fi
    c=`cat ${base}_missing.txt | wc -l`
    if [ $c -le 2 ]; then
        echo "No missing data<br>"
    else
        if [ ! -s ./${base}_missing.plt -o ./${base}_missing.plt -ot ./${base}_missing.txt ]; then
            ( ./bin/plotdat ${base}_missing.txt > ./${base}_missing.plt ) 2>&1
        fi
        if [ ! -s ${base}_missing.png -o ${base}_missing.png -ot ${base}_missing.plt ]; then
            ./bin/gnuplot << EOF
$gnuplot_init
set size .7057,.4
set ylabel "fraction missing [1]"
set term postscript epsf color solid
set zeroaxis
set output "${base}_missing.eps"
plot "./${base}_missing.plt" title "$NAME $station" with steps
set term png $gnuplot_png_font_hires
set out "./${base}_missing.png"
replot
quit
EOF
        fi
        pngfile=${base}_missing.png
        getpngwidth
        datafile=`echo ${base}_missing.txt | tr '+' '%'`
        cat << EOF 
<div class="bijschrift">Fraction missing data
(<a href="${base}_missing.eps">eps</a>, <a href="ps2pdf.cgi?file=${base}_missing.eps">pdf</a>,
<a href="${base}_missing.txt">raw data</a>, 
<a href="dat2nc.cgi?datafile=${base}_missing.txt&type=i&station=missing_$STATION&id=$EMAIL">netcdf</a>)</div>
<center>
<img src="${base}_missing.png" alt="fraction missing data" width="$halfwidth" border=0 class="realimage" hspace=0 vspace=0>
</center>
EOF
    fi
fi
