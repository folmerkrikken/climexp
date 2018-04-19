#!/bin/sh
# to be sourced from other scripts
###echo "<div class=\"alineakop\">Annual cycle and anomalies</div>"
if [ -z "$EMAIL" ]; then
	EMAIL=FORM_EMAIL
fi
if [ $EMAIL = ec8907341dfc63c526d08e36d06b7ed8 ]; then
    lwrite=false # true
fi
if [ "$EMAIL" != someone@somewhere ]; then
	def=./prefs/$EMAIL.plot_anomalies
	if [ -s $def ]; then
		eval `egrep '^FORM_[a-z0-9]*=[a-zA-Z]*[-+0-9.]*;$' $def`
	fi
fi

base=data/$TYPE${WMO}_$FORM_climyear1$FORM_climyear2
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
name_=`echo $name | tr "_" " "`
station_=`echo $station | tr "_" " "`

[ -z "$firstfile" ] && firstfile=./data/$TYPE$WMO.dat
if [ ${NPERYEAR:-12} -gt 1 ]; then
	startstop=./data/$TYPE${WMO}_${FORM_climyear1}_${FORM_climyear2}.startstop
    if [ ! -s $startstop -o ! -s ${base}_yr.plt -o ${base}_yr.plt -ot $firstfile ]; then
        [ "$lwrite" = true ] && echo "./bin/climatology ./data/$TYPE$WMO.dat $beginend startstop $startstop"
		( ./bin/climatology ./data/$TYPE$WMO.dat $beginend startstop $startstop > ${base}_yr.plt ) 2>&1
    fi
    if [ ! -s ${base}_yr.txt -o ${base}_yr.txt -ot ${base}_yr.plt ]; then
		sort ${base}_yr.plt | egrep -v '^200[12]' > ${base}_yr.txt
    fi
    yrstart=`head -1 $startstop`
    yrstop=`tail -1 $startstop`
    if [ "$yrstart" = '9999' -o "$yrstart" = "$yrstop" ]; then
    	echo "Not enough data in requested interval ${FORM_climyear1}:${FORM_climyear2}, using all data for climatology"
		###echo "./bin/climatology ./data/$TYPE$WMO.dat startstop $startstop"
		(./bin/climatology ./data/$TYPE$WMO.dat startstop $startstop > ${base}_yr.plt) 2>&1
		sort ${base}_yr.plt | egrep -v '^200[12]' > ${base}_yr.txt
	    yrstart=`head -1 $startstop`
    	yrstop=`tail -1 $startstop`
	    computed="computed with all data available"
    	period=""
    	FORM_climyear1=""
    	FORM_climyear2=""
	elif [ -n "$FORM_climyear1" -o -n "$FORM_climyear2" ]; then
    	computed="computed over the period ${yrstart}:${yrstop}"
    	period=" (${yrstart}:${yrstop})"
	fi
    echo "<div class=\"bijschrift\">Annual cycles, $computed"
    computed_=`echo "$computed" | tr ' ' '_'`
    base_=`echo "$base" | tr '+' '%'`
    for type in 1 -1; do
        if [ $type = -1 ]; then
            suffix=yrm1
            setxrange='set xrange ["20000701":"20010630"]
set xtics ("" "20000801" 1, "" "20000901" 1, "" "20001001" 1, "" "20001101" 1, "" "20001201" 1, "" "20010101" 1, "" "20010201" 1, "" "20010301" 1, "" "20010401" 1, "" "20010501" 1, "" "20010601" 1) 
set xtics add ("Jul" "20000715", "Aug" "20000815", "Sep" "20000915", "Oct" "20001015", "Nov" "20001115", "Dec" "20001215", "Jan" "20010115", "Feb" "20010214", "Mar" "20010315", "Apr" "20010415", "May" "20010515", "Jun" "20010615")'
            bijschriftbegin="Jul-Jun: "
            bijschrifteind=")"
        else
            suffix=yr1
            setxrange='set xrange ["20000101":"20001231"]
set xtics ("" "20000201" 1, "" "20000301" 1, "" "20000401" 1, "" "20000501" 1, "" "20000601" 1, "" "20000701" 1, "" "20000801" 1, "" "20000901" 1, "" "20001001" 1, "" "20001101" 1, "" "20001201" 1)
set xtics add ("Jan" "20000115", "Feb" "20000214", "Mar" "20000315", "Apr" "20000415", "May" "20000515", "Jun" "20000615", "Jul" "20000715", "Aug" "20000815", "Sep" "20000915", "Oct" "20001015", "Nov" "20001115", "Dec" "20001215")'
            bijschriftbegin="(Jan-Dec: "
            bijschrifteind=","
        fi
        echo "$bijschriftbegin<a href=\"${base}_$suffix.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${base}_$suffix.eps.gz\">pdf</a>, 
<a href=\"${base}_yr.txt\">raw data</a>$bijschrifteind."
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
set xtics scale 0.,1.
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
        fi # does plot already exist?
    done # Jan-Dec and Jul-JUn
    echo "<center>"
    for type in 1 -1; do
        if [ $type = -1 ]; then
            suffix=yrm1
            range="Jan-Dec"
        else
            suffix=yr1
            range="Jul-Jun"
        fi
    	pngfile=${base}_$suffix.png
	    getpngwidth
        echo "<img src=\"${base}_$suffix.png\" alt=\"$range annual cycle of $name_ $station_ $period\" width=\"48%\" border=0 class=\"realimage\" hspace=0 vspace=0>"
    done
    echo "</center>"
fi # NPERYEAR > 1

if [ "${WMO#corr}" = "$WMO" -a "${WMO#sign}" = "$WMO" ]; then
    if [ ! -s ./${base}a.eps.gz -o ! -s ./${base}a.png -o ! -s ./${base}a.plt -o ./${base}a.plt -ot $firstfile ]; then
        ###echo ./bin/plotdat anomal $FORM_climyear1 $FORM_climyear2 ./data/$TYPE$WMO.dat
        if [ ! -s ./${base}a.plt -o ./${base}a.plt -ot $firstfile ]; then
            ( ./bin/plotdat anomal $FORM_climyear1 $FORM_climyear2 ./data/$TYPE$WMO.dat | fgrep -v 'disregarding' > ./${base}a.plt ) 2>&1
        fi
        if [ ! -s ./${base}a.txt -o ./${base}a.txt -ot ./${base}a.plt ]; then
            fgrep -v "# repeat last"  ./${base}a.plt > ./${base}a.txt
        fi
	    ###title="anomalies of $station $NAME$period"
        ./bin/gnuplot << EOF
$gnuplot_init
set size .7057,.4
###set title "$title"
set ylabel "$ylabel"
set term postscript epsf color solid
set zeroaxis
set output "./${base}a.eps"
plot "./${base}a.plt" title "$name_ $station_ anomalies$period" with steps
set term png $gnuplot_png_font_hires
set out "./${base}a.png"
replot
quit
EOF
###gs -q -r100 -dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dNOPAUSE -sDEVICE=ppmraw -sOutputFile=./${base}a.ppm ./${base}a.eps -c quit
###(pnmcrop ./${base}a.ppm | pnmtopng > ./${base}a.png) > /dev/null 2>&1
###rm ./${base}a.ppm
        gzip -f ./${base}a.eps
    fi
    if [ ${NPERYEAR:-12} -gt 1 ]; then
		wrt="with respect to the above annual cycle"
    else
		wrt=
    fi
    pngfile=${base}a.png
    getpngwidth
    datafile=`echo ${base}a.txt | tr '+' '%'`
    cat << EOF 
<div class="bijschrift">Anomalies $wrt $period
(<a href="${base}a.eps.gz">eps</a>, <a href="ps2pdf.cgi?file=${base}a.eps.gz">pdf</a>,
<a href="${base}a.txt">raw data</a>, 
<a href="dat2nc.cgi?datafile=${datafile}&type=$TYPE&station=$STATION&id=$EMAIL">netcdf</a>,
<a href="analyse_anomaly.cgi?datafile=$datafile&STATION=${STATION}_anomalies&TYPE=$TYPE&NPERYEAR=$NPERYEAR&id=$EMAIL">analyse this time series</a>)</div>
<center>
<img src="${base}a.png" alt="anomalies" width="$halfwidth" border=0 class="realimage" hspace=0 vspace=0>
</center>
<p><form action="new_anomalies.cgi" method="post">
Redisplay the anomalies using the years
<input type="hidden" name="wmo"     value="$WMO">
<input type="hidden" name="station" value="$STATION">
<input type="hidden" name="email"   value="$EMAIL">
<input type="hidden" name="type"    value="$TYPE">
<input type="hidden" name="name"    value="$NAME">
<input type="hidden" name="NPERYEAR" value="$NPERYEAR">
<input type="$number" min=1 max=2500 step=1 name="climyear1" size="4"  style="width: 5em;" value="${FORM_climyear1:-1981}">-<input type="$number" min=1 max=2500 step=1 name="climyear2" size="4" style="width: 5em;" value="${FORM_climyear2:-2010}">
<input type="submit" value="select">
</form>
EOF
fi
