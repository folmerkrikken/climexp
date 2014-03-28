#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./getargs.cgi
WMO=$FORM_WMO
TYPE=$FORM_TYPE
NPERYEAR=$FORM_NPERYEAR
STATION=$FORM_STATION
NAME=$FORM_NAME
FORM_dgt=${FORM_dgt}%
[ -z "$FORM_assume" ] && FORM_assume=shift

# check email address
. ./checkemail.cgi

lwrite=false
if [ $EMAIL = oldenbor@knmi.nl ]; then
	lwrite=false # true
fi

if [ $TYPE = set ]; then
	CLIM="stations"
else
	CLIM=`echo "$FORM_NAME"  | tr '[:upper:]' '[:lower:]'`
fi
station=`echo $FORM_STATION | tr '_' ' '`
# common options
if [ -z "$FORM_hist" ]; then
	FORM_hist=none
fi
if [ $TYPE = set ]; then
	corrargs="file $WMO $NAME"
	WMO=`basename $WMO .txt`
else
	corrargs="$DIR/data/$TYPE$WMO.dat"
fi
if [ -z "$FORM_timeseries" ]; then
    . ./myvinkhead.cgi "Trends in return times of extremes" "Error" "noindex,nofollow"
    echo "Please select a time series on the previous page"
    . ./myvinkfoot.cgi
    exit
fi

case "$FORM_fit" in
gauss)  FORM_plot=sqrtlog;;
gumbel) FORM_plot=gumbel;;
gev)    FORM_plot=gumbel;;
gpd)    FORM_plot=log;;
*)      echo "FORM_fit should be gauss, gumbel, gev, or gpd, not $FORM_fit"
        . ./myvinkfoot.cgi
        exit
esac

case $FORM_timeseries in
nino12)    covstation="NINO12";sfile="$DIR/NCEPData/nino2.dat";;
nino3)     covstation="NINO3";sfile="$DIR/NCEPData/nino3.dat";;
nino34)    covstation="NINO3.4";sfile="$DIR/NCEPData/nino5.dat";;
nino4)     covstation="NINO4";sfile="$DIR/NCEPData/nino4.dat";;
soi)       covstation="SOI";sfile="$DIR/CRUData/soi.dat";;
nao)       covstation="NAO-Gibraltar";sfile="$DIR/CRUData/nao.dat";;
sunspots)  covstation="sunspots";sfile="$DIR/SIDCData/sunspots.dat";;
time)      covstation="time";sfile="$DIR/KNMIData/time$NPERYEAR.dat";;
*)         covstation=`head -2 $FORM_timeseries | tail -1 | tr '_' ' '`
           sfile=$DIR/`head -1 $FORM_timeseries | tr '\`#;' '?'`
           ;;
esac
probfile=data/attribute_prob_$$.txt
corrargs="$corrargs $sfile $FORM_fit assume $FORM_assume plot $probfile"
n=0
. $DIR/getopts.cgi

if [ $EMAIL != someone@somewhere ]; then
	. ./save_commonoptions.cgi
	case $FORM_fit in
	    gev|gumbel) FORM_plot=gumbel;;
	    gpd|gauss) FORM_plot=sqrtlog;;
	esac
	cat > ./prefs/$EMAIL.histogramoptions <<EOF
FORM_plot=$FORM_plot;
FORM_nbin=$FORM_nbin;
FORM_changesign=$FORM_changesign;
FORM_restrain=$FORM_restrain;
FORM_assume=$FORM_assume;
FORM_year=$FORM_year;
FORM_begin2=$FORM_begin2;
FORM_decor=$FORM_decor;
FORM_fit=$FORM_fit;
FORM_xlo=$FORM_xlo;
FORM_xhi=$FORM_xhi;
FORM_ylo=$FORM_ylo;
FORM_yhi=$FORM_yhi;
EOF
fi

. ./myvinkhead.cgi "Trends in return times of extremes" "$CLIM $station" "noindex,nofollow"

if [ ! \( -s $sfile -a -f $sfile \) ]; then
    echo "Error: cannot locate covariate series $sfile"
    . .myvinkfoot.cgi
    exit
fi

cat <<EOF
<font color=#ff2222>Test version under development, may or may not give correct answers
today. Use with extreme caution and please report problems.</font><p>
EOF

if [ "$FORM_fit" = gumbel -o "$FORM_fit" = gev -o "$FORM_fit" = gpd ]; then
	echo "Using sub-optimal algorithms to compute the error estimates.  This may take a while.<p>"
fi

[ -n "$FORM_year" ] && corrargs="$corrargs end2 $FORM_year"
echo `date` "$EMAIL ($REMOTE_ADDR) attribute $corrargs" >> log/log
startstop="/tmp/startstop$$.txt"
corrargs="$corrargs startstop $startstop"
root=data/h${TYPE}${WMO}_$$

[ "$lwrite" = true ] && echo bin/attribute $corrargs
($DIR/bin/attribute $corrargs > $root.txt) 2>&1 && true
grep 'bootstrap' $root.txt | sed -e 's/#//'
echo '<table class="realtable" width=451 border=0 cellpadding=0 cellspacing=0>'
if [ $TYPE = set ]; then
	eval `./bin/getunits ./data/${NAME}*.dat`
elif [ $NPERYEAR -gt 12 ]; then
	eval `./bin/getunits.sh ./data/$TYPE$WMO.dat`
else
	eval `./bin/getunits ./data/$TYPE$WMO.dat`
fi
. ./month2string.cgi
. ./setyaxis.cgi
echo "<tr><th colspan="4">$seriesmonth $STATION $VAR [$UNITS] dependent on $covstation</th></tr>"
tail -n +2 "$root.txt" | grep '<tr>' | sed -e 's/#//'
echo '</table>'
[ "$lwrite" = true ] && wc -l $root.txt|awk '{print $1}'
c=`wc -l $root.txt|awk '{print $1}'`
[ "$lwrite" = true ] && echo "c=$c<p>"
if [ $c -lt 20 ]; then
	echo "<p>Something went wrong, c=$c"
	echo 'Please send <a href="mailto:http://www.knmi.nl/~oldenbor/">me</a> the following command and I will try to fix it.<p>'
	echo bin/attribute $corrargs
	. ./myvinkfoot.cgi
	exit
fi

ylabel_save=$ylabel
[ -n "$FORM_log" ] && ylabel="log $ylabel"
[ -n "$FORM_sqrt" ] && ylabel="sqrt $ylabel"
[ -n "$FORM_square" ] && ylabel="${ylabel}^2"

if [ -s "$startstop" ]; then
	yrstart=`head -1 $startstop`
	yrstop=`tail -1 $startstop`
	rm $startstop
fi

if [ "$FORM_plot" = "hist" ]; then
	title="$seriesmonth $CLIM $station"
	if [ -n "$yrstart" ]; then
		title="$title ${yrstart}:${yrstop}"
	elif [ -n "$FORM_end" ]; then
		if [ -n "$FORM_begin" ]; then
			title="$title ${FORM_begin}-${FORM_end}"
		else
			title="$title ending $FORM_end"
		fi
	elif [ -n "$FORM_begin" ]; then
		title="$title beginning $FORM_begin"
	fi
	if [ -n "$ndiff" ]; then
		title="$title ($ndiff-yr running mean)"
	else
		if [ -n "$FORM_diff" ]; then
			title="$title (diff)"
		fi
	fi
	if [ -n "$FORM_detrend" ]; then
		title="$title (detrend)"
	fi

	./bin/gnuplot << EOF
set size 0.7,0.7
set term png $gnuplot_png_font_hires
set output "$root.png"
set datafile missing "-999.90"
set title "$title"
set xlabel "$ylabel"
#set ylabel "number"
plot "$root.txt" u 2:3 notitle with boxes, "$root.txt" u 2:5 title "fit" with linespoints
set term postscript epsf color solid
set output "$root.eps"
replot
quit
EOF

fi

if [ $FORM_plot = "gumbel" -o $FORM_plot = "log" -o $FORM_plot = "sqrtlog" ]; then
	title="$seriesmonth $CLIM $station"
	if [ -n "$yrstart" ]; then
		title="$title ${yrstart}:${yrstop}"
	elif [ -n "$FORM_end" ]; then
		if [ -n "$FORM_begin" ]; then
			title="$title ${FORM_begin}-$FORM_end"
		else
			title="$title ending $FORM_end"
		fi
	elif [ -n "$FORM_begin" ]; then
		title="$title beginning $FORM_begin"
	fi
	if [ -n "$ndiff" ]; then
		title="$title ($ndiff-yr running mean)"
	else
		if [ -n "$FORM_diff" ]; then
			title="$title (diff)"
		fi
	fi
	if [ -n "$FORM_detrend" ]; then
		title="$title (detrend)"
	fi
	xtics=`fgrep '#@' $root.txt | sed -e 's/^#@ //'`
	if [ -n "$FORM_xlo" ]; then
		case $FORM_plot in
			gumbel)  xlo=`echo " -l(-l(1-1/$FORM_xlo))" | bc -q -l`;;
			log)     xlo=`echo " l($FORM_xlo)" | bc -q -l`;;
			sqrtlog) xlo=`echo " sqrt(l($FORM_xlo))" | bc -q -l`;;
		esac
	fi
	if [ -n "$FORM_xhi" ]; then
		case $FORM_plot in
			gumbel)  xhi=`echo " -l(-l(1-1/$FORM_xhi))" | bc -q -l`;;
			log)     xhi=`echo " l($FORM_xhi)" | bc -q -l`;;
			sqrtlog) xhi=`echo " sqrt(l($FORM_xhi))" | bc -q -l`;;
		esac
	fi
	if [ -n "$FORM_changesign" ]; then
		bottomtop=top
	else
		bottomtop=bottom
	fi
	if [ -n "$FORM_year" ]; then
		plotformyear=", \"$root.txt\" index 1 u 2:4 title \"$FORM_year\" w lines lt 1, \"$root.txt\" index 2 u 2:4 title \"$FORM_year in climate of $FORM_begin2\" w lines lt 3" 
	else
		plotformyear=""
	fi
	
	cat > /tmp/histogram$$.gnuplot << EOF
set size 0.7,0.7
set term png $gnuplot_png_font_hires
set output "${root}.png"
set title "$title"
set xlabel "return period [yr]"
set ylabel "$ylabel"
set datafile missing '-999.900'
set key $bottomtop
$xtics
set xrange [${xlo}:${xhi}]
set yrange [${FORM_ylo}:${FORM_yhi}]
plot "$root.txt" index 0 u 2:3 notitle with points, "$root.txt" index 0 u 2:4 title "$FORM_fit $FORM_assume fit" with line$plotformyear
set term postscript epsf color solid
set output "${root}.eps"
replot
quit
EOF
	if [ "$lwrite" = true ]; then
		echo '<pre>'
		cat /tmp/histogram$$.gnuplot
		echo '</pre>'
	fi
	./bin/gnuplot < /tmp/histogram$$.gnuplot 2>&1
	if [ ! -s ${root}.png ]; then
		cp /tmp/histogram$$.gnuplot data/
		echo "Something went wrong while making the plot."
		echo "The plot command are <a href=\"data/histogram$$.gnuplot\">here</a>."
		. ./myvinkfoot.cgi
		exit
	fi
	rm /tmp/histogram$$.gnuplot
fi

gzip -f $root.eps
pngfile=${root}.png
getpngwidth
echo "<div class=\"bijschrift\">$title"
if [ $FORM_assume = 'shift' ]; then
    echo "with the effects of $station linearly subtracted from the position parameter a,"
elif [ $FORM_assume = 'scale' ]; then
    echo "with the effects of $station scaling the position and scale parameters parameter a,b, "
elif [ $FORM_assume = 'both' ]; then
    echo "with the effects of $station linearly subtracted from the position parameter a and independently from the scale parameter b,"
else
    echo "using an unknown assumption,"
fi
echo "referenced at $FORM_year (<a href=\"${root}.eps.gz\">eps</a>,  <a href=\"ps2pdf.cgi?file=${root}.eps.gz\">pdf</a>, <a href=\"$root.txt\">raw data</a>)</div>"
echo "<center><img src=\"${root}.png\" alt=\"$FORM_which\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

if [ -n "$FORM_log" -o -n "$FORM_sqrt" -o -n "$FORM_square" ]; then
	./bin/untransform ${FORM_log:-false} ${FORM_sqrt:-false} ${FORM_square:-false} < $root.txt > ${root}un.txt
	root=${root}un
	if [ $FORM_plot = "gumbel" -o $FORM_plot = "log" ]; then
		ylabel=$ylabel_save
		cat > /tmp/histogram$$.gnuplot << EOF
set size 0.7,0.7
set term png $gnuplot_png_font_hires
set output "${root}.png"
set title "$title"
set xlabel "return period [yr]"
set ylabel "$ylabel"
set datafile missing '-999.900'
set key $bottomtop
$xtics
set xrange [${xlo}:${xhi}]
set yrange [${FORM_ylo}:${FORM_yhi}]
plot "$root.txt" index 0 u 2:3 notitle with points, "$root.txt" index 0 u 2:4 title "$FORM_fit $FORM_assume fit" with line$plotformyear
set term postscript epsf color solid
set output "${root}.eps"
replot
quit
EOF
		if [ "$lwrite" = true ]; then
			echo '<pre>'
			cat /tmp/histogram$$.gnuplot
			echo '</pre>'
		fi
		./bin/gnuplot < /tmp/histogram$$.gnuplot 2>&1
		if [ ! -s ${root}.png ]; then
			cp /tmp/histogram$$.gnuplot data/
			echo "Something went wrong while making the plot."
			echo "The plot commands are <a href=\"data/histogram$$.gnuplot\">here</a>."
			. ./myvinkfoot.cgi
			exit
		fi
		rm /tmp/histogram$$.gnuplot
	else
    	echo "Not yet ready"  
	fi
	gzip -f $root.eps
	pngfile=${root}.png
	getpngwidth
	echo "<div class=\"bijschrift\">$title (<a href=\"${root}.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${root}.eps.gz\">pdf</a>, <a href=\"$root.txt\">raw data</a>)</div>"
	echo "<center><img src=\"${root}.png\" alt=\"$FORM_which\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"
fi

cat > /tmp/cdf$$.gnuplot << EOF
set size 0.7,0.4
set term png $gnuplot_png_font_hires
set output "${root}_cdf.png"
set title "CDF of return times"
set xlabel "return period [yr]"
set ylabel "CDF"
set datafile missing '-999.900'
set key $bottomtop
$xtics
set xrange [${xlo}:${xhi}]
set yrange [0:1]
set ytics (0,0.1,0.25,0.5,0.75,0.9,1)
plot "$probfile" u 5:1 title "in climate $FORM_begin2" with lines lt 3, "$probfile" index 0 u 6:1 title "in climate $FORM_year" with lines lt 1
set term postscript epsf color solid
set output "${root}_cdf.eps"
replot
quit
EOF
if [ "$lwrite" = true ]; then
    echo '<pre>'
    cat /tmp/cdf$$.gnuplot
    echo '</pre>'
fi
./bin/gnuplot < /tmp/cdf$$.gnuplot 2>&1
if [ ! -s ${root}_cdf.png ]; then
    cp /tmp/cdf$$.gnuplot data/
    echo "Something went wrong while making the plot."
    echo "The plot commands are <a href=\"data/cdf$$.gnuplot\">here</a>."
    . ./myvinkfoot.cgi
    exit
fi
rm /tmp/cdf$$.gnuplot
gzip -f ${root}_cdf.eps
pngfile=${root}_cdf.png
getpngwidth
echo "<div class=\"bijschrift\">CDF of the return time of $FORM_year $title in the climates of $FORM_year and of $FORM_begin2 (<a href=\"${root}_cdf.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${root}_cdf.eps.gz\">pdf</a>, <a href=\"$probfile\">raw data</a>)</div>"
echo "<center><img src=\"${root}_cdf.png\" alt=\"CDF of the return time of $FORM_year\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

###xtics=`fgrep '#@' $probfile | sed -e 's/^#@ //'`
cat > /tmp/cdfdiff$$.gnuplot << EOF
set size 0.7,0.4
set term png $gnuplot_png_font_hires
set output "${root}_cdfdiff.png"
set title "ratio of return times in climates of $FORM_year and $FORM_begin2"
set xlabel "ratio [1]"
set ylabel "CDF"
set datafile missing '-999.900'
set key $bottomtop
set logscale x
set xrange [0.01:100]
set yrange [0:1]
set ytics (0,0.1,0.25,0.5,0.75,0.9,1)
plot "$probfile" u 4:1 notitle with lines lt 1
set term postscript epsf color solid
set output "${root}_cdfdiff.eps"
replot
quit
EOF
if [ "$lwrite" = true ]; then
    echo '<pre>'
    cat /tmp/cdfdiff$$.gnuplot
    echo '</pre>'
fi
./bin/gnuplot < /tmp/cdfdiff$$.gnuplot 2>&1
if [ ! -s ${root}_cdfdiff.png ]; then
    cp /tmp/cdfdiff$$.gnuplot data/
    echo "Something went wrong while making the plot."
    echo "The plot commands are <a href=\"data/cdfdiff$$.gnuplot\">here</a>."
    . ./myvinkfoot.cgi
    exit
fi
rm /tmp/cddiff$$.gnuplot
gzip -f ${root}_cdfdiff.eps
pngfile=${root}_cdfdiff.png
getpngwidth
echo "<div class=\"bijschrift\">CDF of the ratio of the return times of $FORM_year $title in the climates of $FORM_year and of $FORM_begin2 (<a href=\"${root}_cdfdiff.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${root}_cdfdiff.eps.gz\">pdf</a>, <a href=\"$probfile\">raw data</a>)</div>"
echo "<center><img src=\"${root}_cdfdiff.png\" alt=\"CDF of the difference in return times of $FORM_year and $FORM_begin2\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

. ./myvinkfoot.cgi
