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
corrargs="$corrargs $FORM_nbin fit $FORM_fit hist $FORM_plot"
n=0
. $DIR/getopts.cgi

if [ $EMAIL != someone@somewhere ]; then
	. ./save_commonoptions.cgi
	cat > ./prefs/$EMAIL.histogramoptions <<EOF
FORM_plot=$FORM_plot;
FORM_nbin=$FORM_nbin;
FORM_changesign=$FORM_changesign;
FORM_restrain=$FORM_restrain;
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

if [ $FORM_plot = "qq" ]; then
	. ./myvinkhead.cgi "Quantile-quantile plot" "$FORM_CLIM $station" "noindex,nofollow"
elif [ $FORM_plot = "gumbel" ]; then
	. ./myvinkhead.cgi "Gumbel plot" "$FORM_CLIM $station" "noindex,nofollow"
else
	. ./myvinkhead.cgi "Histogram" "$FORM_CLIM $station" "noindex,nofollow"
fi

if [ "$FORM_fit" = gumbel -o "$FORM_fit" = gev -o "$FORM_fit" = gpd ]; then
	echo "Using sub-optimal algorithms to compute the error estimates.  This may take a while.<p>"
fi

[ -n "$FORM_year" ] && corrargs="$corrargs end2 $FORM_year"
echo `date` "$EMAIL ($REMOTE_ADDR) histogram $corrargs" >> log/log
startstop="/tmp/startstop$$.txt"
corrargs="$corrargs startstop $startstop"
root=data/h${TYPE}${WMO}_$$

[ "$lwrite" = true ] && echo bin/histogram $corrargs
($DIR/bin/histogram $corrargs > $root.txt) 2>&1 && true
grep 'bootstrap' $root.txt | sed -e 's/#//'
echo '<table class="realtable" width=451 border=0 cellpadding=0 cellspacing=0>'
if [ $TYPE = set ]; then
	eval `./bin/getunits ./data/${NAME}*.dat`
else
	eval `./bin/getunits ./data/$TYPE$WMO.dat`
fi
. ./month2string.cgi
. ./setyaxis.cgi
echo "<tr><th colspan="3">$seriesmonth $station $VAR [$UNITS]</th></tr>"
tail -n +2 "$root.txt" | grep '<tr>' | sed -e 's/#//'
echo '</table>'
[ "$lwrite" = true ] && wc -l $root.txt|awk '{print $1}'
c=`wc -l $root.txt|awk '{print $1}'`
[ "$lwrite" = true ] && echo "c=$c<p>"
if [ $c -lt 20 ]; then
	echo "<p>Something went wrong, c=$c"
	echo 'Please send <a href="mailto:http://www.knmi.nl/~oldenbor/">me</a> the following command and I will try to fix it.<p>'
	echo bin/histogram $corrargs
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
set xrange [${FORM_xlo}:${FORM_xhi}]
set yrange [${FORM_ylo}:${FORM_yhi}]
#set ylabel "number"
plot "$root.txt" u 2:3 notitle with boxes, "$root.txt" u 2:5 title "fit" with linespoints
set term postscript epsf color solid
set output "$root.eps"
replot
quit
EOF

fi

if [ $FORM_plot = "qq" ]; then
	if [ "$FORM_fit" = "none" ]; then
		echo "I can only make a QQ plot after fitting to something"
		. ./myvinkfoot.cgi
		exit
	fi
	title="Quantile-quantile plot of $seriesmonth $CLIM $station vs fit"
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

	./bin/gnuplot << EOF
set size 0.7,0.7
set term png $gnuplot_png_font_hires
set output "${root}.png"
set title "$title"
set xlabel "fitted $ylabel"
set ylabel "observed $ylabel"
plot "$root.txt" u 3:2 notitle with points, x notitle with line
set term postscript epsf color solid
set output "${root}.eps"
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
		plotformyear=", \"$root.txt\" index 1 u 2:4 title \"$FORM_year\" w lines"
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
plot "$root.txt" index 0 u 2:3 notitle with points, "$root.txt" index 0 u 2:4 title "$FORM_fit fit" with line$plotformyear
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
echo "<div class=\"bijschrift\">$title (<a href=\"${root}.eps.gz\">eps</a>,  <a href=\"ps2pdf.cgi?file=${root}.eps.gz\">pdf</a>, <a href=\"$root.txt\">raw data</a>)</div>"
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
plot "$root.txt" index 0 u 2:3 notitle with points, "$root.txt" index 0 u 2:4 title "$FORM_fit fit" with line$plotformyear
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
	else
    	echo "Not yet ready"  
	fi
	gzip -f $root.eps
	pngfile=${root}.png
	getpngwidth
	echo "<div class=\"bijschrift\">$title (<a href=\"${root}.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${root}.eps.gz\">pdf</a>, <a href=\"$root.txt\">raw data</a>)</div>"
	echo "<center><img src=\"${root}.png\" alt=\"$FORM_which\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"
fi

. ./myvinkfoot.cgi
