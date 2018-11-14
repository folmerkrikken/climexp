#!/bin/sh
. ./init.cgi
echo 'Content-Type: text/html'
echo
echo

export DIR=`pwd`
. ./init.cgi
. ./getargs.cgi
WMO=$FORM_WMO
listname=$WMO
TYPE=$FORM_TYPE
NPERYEAR=$FORM_NPERYEAR
STATION=$FORM_STATION
NAME=$FORM_NAME
prog=$NAME
FORM_dgt=${FORM_dgt%%%}
FORM_dgt=${FORM_dgt}%
extraargs="$FORM_extraargs"
if [ -n "$extraargs" ]; then
  NPERYEAR=`echo "$extraargs" | cut -f 1 -d '_'`
  extraname=`echo "$extraargs " | cut -f 2- -d '_' | tr '_' ' '`
fi
. ./nperyear2timescale.cgi

# check email address
. ./checkemail.cgi

lwrite=false
if [ $EMAIL = oldenborgh@knmi.nl ]; then
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
    if [ -n "$extraargs" ]; then
    	corrargs="file $WMO ${NAME}_${extraargs}"
    else
    	corrargs="file $WMO $NAME"
	fi
	WMO=`basename $WMO .txt`
elif [ $TYPE = setmap ]; then
    corrargs="" # the filename will be filled in by stationlist
else
	corrargs="./data/$TYPE$WMO.dat"
fi
corrargs="$corrargs $FORM_nbin fit $FORM_fit hist $FORM_plot"
n=0
if [ -n "$FORM_lowerlimitzero" ]; then
    FORM_assume=scale
    corrargs="$corrargs assume scale"
fi
. ./getopts.cgi

if [ $EMAIL != someone@somewhere ]; then
	. ./save_commonoptions.cgi
    . ./save_histogramoptions.cgi
fi

if [ $FORM_plot = "qq" ]; then
	. ./myvinkhead.cgi "Quantile-quantile plot" "$timescale $extraname$FORM_CLIM $station" "noindex,nofollow"
elif [ $FORM_plot = "gumbel" ]; then
	. ./myvinkhead.cgi "Gumbel plot" "$timescale $extraname$FORM_CLIM $station" "noindex,nofollow"
else
	. ./myvinkhead.cgi "Histogram" "$timescale $extraname$FORM_CLIM $station" "noindex,nofollow"
fi
[ $TYPE != "set" -a $TYPE != "setmap" ] && listname="" # otherwise we get the wrong menu

if [ "$FORM_fit" = poisson -o  "$FORM_fit" = gamma -o "$FORM_fit" = gumbel -o "$FORM_fit" = gev -o "$FORM_fit" = gpd ]; then
	echo "Using sub-optimal algorithms to compute the error estimates.  This may take a while.<p>"
    echo "<small>If it takes too long you can abort the job <a href=\"killit.cgi?id=$EMAIL&pid=$$\" target=\"_new\">here</a> (using the [back] button of the browser does <it>not</it> kill the histogram job)</small><p>"
    cat | sed -e "s:$DIR::g" > pid/$$.$EMAIL <<EOF
$REMOTE_ADDR
histogram $corrargs
@
EOF
    export SCRIPTPID=$$
    export FORM_EMAIL=$EMAIL
fi

if [ -n "$FORM_year" ]; then
    if [ -n "$FORM_xyear" ]; then
        echo "Warning: ignoring the year for which to evaluate the return time, $FORM_year<p>"
        FORM_year=""
    else
        corrargs="$corrargs end2 $FORM_year"
    fi
fi
echo `date` "$EMAIL ($REMOTE_ADDR) histogram $corrargs" >> log/log
startstop="/tmp/startstop$$.txt"
corrargs="$corrargs startstop $startstop"
root=data/h${TYPE}${WMO}_$$

[ "$lwrite" = true ] && echo bin/histogram $corrargs
(./bin/histogram $corrargs > $root.txt) 2>&1
[ -f pid/$$.$EMAIL ] && rm pid/$$.$EMAIL
grep 'bootstrap' $root.txt | sed -e 's/#//'
echo '<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>'
ok=false
n=1
while [ $ok != true ]; do # sometimes the most recent series does not have data...
    if [ $TYPE = set ]; then
        f=`ls -t ./data/${NAME}*$FORM_extraargs.dat|head -n $n | tail -n 1`
    else
        f=./data/$TYPE$WMO.dat
    fi
    if [ -z "$f" -o ! -s "$f" ]; then
        echo "Can not find any valid data, giving up."
        . ./myvinkfoot.cgi
        exit
    fi
    if [ $NPERYEAR -gt 12 ]; then
        eval `./bin/getunits.sh $f`
    else
        eval `./bin/getunits $f`
    fi
    if [ $NPERYEAR = 0 ]; then
        n=$((n+1))
    else
        ok=true
    fi
done
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
	echo 'Please send <a href="mailto:mailto:oldenborgh@knmi.nl">me</a> the following command and I will try to fix it.<p>'
	echo bin/histogram $corrargs
	. ./myvinkfoot.cgi
	exit
fi

ylabel_save=$ylabel
ylo_save=$FORM_ylo
yhi_save=$FORM_yhi
ylo=$FORM_ylo
yhi=$FORM_yhi
if [ -n "$FORM_log" ]; then
    ylabel="log $ylabel"
    [ -n "$FORM_ylo" -a "$FORM_ylo" != "0" ] && ylo=`echo "l($ylo)/l(10)" | bc -l`
    [ -n "$FORM_yhi" -a "$FORM_yhi" != "0" ] && yhi=`echo "l($yhi)/l(10)" | bc -l`
fi
if [ -n "$FORM_sqrt" ]; then
    ylabel="sqrt $ylabel"
    [ -n "$FORM_ylo" ] && ylo=`echo "sqrt($ylo)" | bc -l`
    [ -n "$FORM_yhi" ] && yhi=`echo "sqrt($yhi)" | bc -l`
fi
if [ -n "$FORM_square" ]; then
    ylabel="${ylabel}^2"
    [ -n "$FORM_ylo" ] && ylo=`echo "$ylo * $ylo" | bc -l`
    [ -n "$FORM_yhi" ] && yhi=`echo "$yhi * $yhi" | bc -l`
fi
if [ -n "$FORM_cube" ]; then
    ylabel="${ylabel}^3"
    [ -n "$FORM_ylo" ] && ylo=`echo "$ylo * $ylo * $ylo" | bc -l`
    [ -n "$FORM_yhi" ] && yhi=`echo "$yhi * $yhi * $yhi" | bc -l`
fi
if [ -n "$FORM_twothird" ]; then
    ylabel="${ylabel}^(2/3)"
    [ -n "$FORM_ylo" ] && ylo=`echo "exp(2/3*l($ylo)" | bc -l`
    [ -n "$FORM_yhi" ] && yhi=`echo "exp(2/3*l($yhi)" | bc -l`
fi
if [ "$ylabel" != "$ylabel_save" ]; then
    sety2label="set y2label \"$ylabel_save\""
fi

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
    title=`echo $title | tr '_' ' '`

	cat > $root.gnuplot << EOF
$gnuplot_init
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
	./bin/gnuplot $root.gnuplot

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
    title=`echo $title | tr '_' ' '`

	cat > $root.gnuplot << EOF
$gnuplot_init
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
	./bin/gnuplot $root.gnuplot

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
	title="$title (${FORM_ci}% CI)"
    title=`echo $title | tr '_' ' '`

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
	elif [ -n "$FORM_xyear" ]; then
		plotformyear=", \"$root.txt\" index 1 u 2:4 title \"$FORM_xyear\" w lines"
	else
		plotformyear=""
	fi
	fit=$FORM_fit
	if [ $fit = "gpd" ]; then
	    fit="${FORM_dgt} $fit"
	fi
	
	cat > $root.gnuplot << EOF
$gnuplot_init
set size 0.7,0.7
set title "$title"
set xlabel "return period [yr]"
set ylabel "$ylabel"
$sety2label
set datafile missing '-999.900'
set key $bottomtop
$xtics
set xrange [${xlo}:${xhi}]
set yrange [${ylo}:${yhi}]
set term unknown
plot "$root.txt" index 0 u 2:3 notitle with points, "$root.txt" index 0 u 2:4 title "$fit fit" with line$plotformyear
set yrange [GPVAL_Y_MIN:GPVAL_Y_MAX]
set y2range [GPVAL_Y_MIN:GPVAL_Y_MAX]
set term png $gnuplot_png_font_hires
set output "${root}.png"
plot "$root.txt" index 0 u 2:3 notitle with points, "$root.txt" index 0 u 2:4 title "$fit fit" with line$plotformyear
set term postscript epsf color solid
set output "${root}.eps"
replot
quit
EOF
	if [ "$lwrite" = true ]; then
		echo '<pre>'
		cat $root.gnuplot
		echo '</pre>'
	fi
	./bin/gnuplot < $root.gnuplot 2>&1
	if [ ! -s ${root}.png ]; then
		echo "Something went wrong while making the plot."
		echo "The plot command are <a href=\"$root.gnuplot\">here</a>."
		. ./myvinkfoot.cgi
		exit
	fi
fi

gzip -f $root.eps
pngfile=${root}.png
getpngwidth
echo "<div class=\"bijschrift\">$title (<a href=\"${root}.eps.gz\">eps</a>,  <a href=\"ps2pdf.cgi?file=${root}.eps.gz\">pdf</a>, <a href=\"$root.txt\">raw data</a>, <a href=\"$root.gnuplot\">plot script</a>)</div>"
echo "<center><img src=\"${root}.png\" alt=\"$FORM_which\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

if [ -n "$FORM_log" -o -n "$FORM_sqrt" -o -n "$FORM_square" ]; then
	./bin/untransform ${FORM_log:-false} ${FORM_sqrt:-false} ${FORM_square:-false} < $root.txt > ${root}un.txt
	root=${root}un
	if [ -n "$FORM_year" ]; then
		plotformyear=", \"$root.txt\" index 1 u 2:4 title \"$FORM_year\" w lines"
	elif [ -n "$FORM_xyear" ]; then
		plotformyear=", \"$root.txt\" index 1 u 2:4 title \"$FORM_xyear\" w lines"
	else
		plotformyear=""
	fi
	if [ $FORM_plot = "gumbel" -o $FORM_plot = "log" ]; then
		ylabel=$ylabel_save
		ylo=$ylo_save
		yhi=$yhi_save
		cat > $root.gnuplot << EOF
$gnuplot_init
set size 0.7,0.7
set title "$title"
set xlabel "return period [yr]"
set ylabel "$ylabel"
set datafile missing '-999.900'
set key $bottomtop
$xtics
set xrange [${xlo}:${xhi}]
set yrange [${ylo}:${yhi}]
set term png $gnuplot_png_font_hires
set output "${root}.png"
plot "$root.txt" index 0 u 2:3 notitle with points, "$root.txt" index 0 u 2:4 title "$fit fit" with line$plotformyear
set term postscript epsf color solid
set output "${root}.eps"
replot
quit
EOF
		if [ "$lwrite" = true ]; then
			echo '<pre>'
			cat $root.gnuplot
			echo '</pre>'
		fi
		./bin/gnuplot < $root.gnuplot 2>&1
		if [ ! -s ${root}.png ]; then
			echo "Something went wrong while making the plot."
			echo "The plot command are <a href=\"$root.gnuplot\">here</a>."
			. ./myvinkfoot.cgi
			exit
		fi
	else
    	echo "Not yet ready for plot = $FORM_plot, only gumbel or log"  
	fi
	gzip -f $root.eps
	pngfile=${root}.png
	getpngwidth
	echo "<div class=\"bijschrift\">$title (<a href=\"${root}.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${root}.eps.gz\">pdf</a>, <a href=\"$root.txt\">raw data</a>, <a href=\"$root.gnuplot\">plot script</a>)</div>"
	echo "<center><img src=\"${root}.png\" alt=\"$FORM_which\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"
fi

. ./myvinkfoot.cgi
