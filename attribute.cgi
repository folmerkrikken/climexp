#!/bin/sh
. ./init.cgi
export DIR=`pwd`
. ./getargs.cgi
echo 'Content-Type: text/html'
echo
echo

WMO=$FORM_WMO
listname=$WMO
TYPE=$FORM_TYPE
NPERYEAR=$FORM_NPERYEAR
STATION=$FORM_STATION
NAME=$FORM_NAME
prog=$NAME
FORM_dgt=${FORM_dgt%%%}
FORM_dgt=${FORM_dgt}%
[ -z "$FORM_assume" ] && FORM_assume=shift
[ -z "$FORM_pmin" ] && FORM_pmin=0.01 # compute how much area has rt2* > 100 year
extraargs=$FORM_extraargs
if [ -n "$extraargs" ]; then
  NPERYEAR=`echo "$extraargs" | cut -f 1 -d '_'`
  extraname=`echo "$extraargs " | cut -f 2- -d '_' | tr '_' ' '`
fi

# check email address
. ./checkemail.cgi

lwrite=false
if [ $EMAIL = ec8907341dfc63c526d08e36d06b7ed8 ]; then
	lwrite=fale # true
fi

if [ -n "$FORM_field" ]; then
    . ./queryfield.cgi
    CLIM="field"
    station="$kindname $climfield"
    if [ "$TYPE" = gridpoints ]; then
        station="gridpoints $station"
    else
        TYPE=field
    fi
elif [ "$TYPE" = set ]; then
	CLIM="stations"
    station=`echo $FORM_STATION | tr '_' ' '`
else
	CLIM=`echo "$FORM_NAME"  | tr '[:upper:]' '[:lower:]'`
    station=`echo $FORM_STATION | tr '_%' ' +'`
fi
# common options
if [ -z "$FORM_hist" ]; then
	FORM_hist=none
fi
if [ "$TYPE" = gridpoints ]; then
    corrargs="gridpoints $file"
elif [ "$TYPE" = field ]; then
    corrargs=$file
elif [ "$TYPE" = set ]; then
    if [ -n "$extraargs" ]; then
    	corrargs="file $WMO ${NAME}_${extraargs}"
    else
    	corrargs="file $WMO $NAME"
	fi
	WMO=`basename $WMO .txt`
elif [ "$TYPE" = setmap ]; then
    corrargs="" # the filename will be filled in by stationlist
else
	corrargs="./data/$TYPE$WMO.dat"
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
nino12)    covstation="NINO12";sfile="NCDCData/ersst_nino12a.dat";;
nino3)     covstation="NINO3";sfile="NCDCData/ersst_nino3a.dat";;
nino34)    covstation="NINO3.4";sfile="NCDCData/ersst_nino3.4a.dat";;
nino4)     covstation="NINO4";sfile="NCDCData/ersst_nino4a.dat";;
soi)       covstation="SOI";sfile="CRUData/soi.dat";;
nao)       covstation="NAO-Gibraltar";sfile="CRUData/nao.dat";;
sunspots)  covstation="sunspots";sfile="SIDCData/sunspots.dat";;
co2)       covstation="CO2 concentration";sfile="CDIACData/co2_annual.dat";;
gmst)      covstation="Global mean surface temperature (smoothed)"
            sfile="NASAData/giss_al_gl_a_4yrlo.dat";;
time)      covstation="time";sfile="$DIR/KNMIData/time$NPERYEAR.dat";;
none)      covstation="none";sfile="none";;
*)         covstation=`head -2 $FORM_timeseries | tail -1 | tr '_' ' '`
           sfile=$DIR/`head -1 $FORM_timeseries | tr '\`#;' '?'`
           ;;
esac
root=`echo data/h${TYPE}${WMO}_$$ | tr -d \\\\`
[ "$lwrite" = true ] && echo "root=$root<be>"
probfile=${root}_prob.txt
obsplotfile=${root}_obsplot.txt
corrargs="$corrargs $sfile $FORM_fit assume $FORM_assume"
if [ "$TYPE" != field -a "$TYPE" != setmap ]; then
    corrargs="$corrargs dump $probfile obsplot $obsplotfile"
fi
n=0
c1=`echo ./data/$TYPE$WMO.dat $file | fgrep -c '%%'`
c2=`echo ./data/$TYPE$WMO.dat $file | fgrep -c '++'`
if [ $c1 != 0 -o $c2 != 0 ]; then
  ENSEMBLE=true
fi
. ./getopts.cgi

if [ $EMAIL != someone@somewhere ]; then
	. ./save_commonoptions.cgi
    . ./save_histogramoptions.cgi
fi

if [ -n "$FORM_year" ]; then
    corrargs="$corrargs end2 $FORM_year"
else
    if [ -n "$FORM_xyear" ]; then
        . ./myvinkhead.cgi "Trends in return times of extremes" "$CLIM $station" "noindex,nofollow"
        echo "Error: the year for which to evaluate the value"
        . ./myvinkfoot.cgi
        exit
    fi
fi

if [ "$FORM_TYPE" = "setmap" ]; then
    # send the arguments via the environment, 
    # much more convenient than a 4-letter variable
    export attribute_args=$corrargs
    FORM_type=attribute
    . ./correlatebox.cgi
    exit
fi

if [ "$FORM_TYPE" = "field" ]; then
    . ./attributefield.cgi
    exit
fi

. ./myvinkhead.cgi "Trends in return times of extremes" "$CLIM $station" "noindex,nofollow"
[ "$TYPE" != "set" -a "$TYPE" != "setmap" ] && listname="" && FORM_listname="" # otherwise we get the wrong menu

if [ ! \( -s $sfile -a -f $sfile -o $sfile = none \) ]; then
    echo "Error: cannot locate $covstation series $sfile"
    . .myvinkfoot.cgi
    exit
fi

if [ "$FORM_assume" != 'both' ]; then
    if [ "$FORM_fit" = "gpd" -a $NPERYEAR -gt 12 ]; then
        echo '<font color=#ff2222>I think it works now, please report problems.</font><p>'
    fi
else
    echo '<font color=#ff2222>Fitting position and scale independently is unfinished and untested. Use at own risk.</font><p>'
fi

echo `date` "$EMAIL ($REMOTE_ADDR) attribute $corrargs" >> log/log
startstop="/tmp/startstop$$.txt"
corrargs="$corrargs startstop $startstop"

if [ "$FORM_fit" = gumbel -o "$FORM_fit" = gev -o "$FORM_fit" = gpd ]; then
	echo "Using sub-optimal algorithms to compute the error estimates.  This may take a while.<p>"
    echo "<small>If it takes too long you can abort the job <a href=\"killit.cgi?id=$EMAIL&pid=$$\" target=\"_new\">here</a> (using the [back] button of the browser does <it>not</it> kill the job)</small><p>"
    cat | sed -e "s:$DIR::g" > pid/$$.$EMAIL <<EOF
$REMOTE_ADDR
attribute $corrargs
@
EOF
    export SCRIPTPID=$$
    export FORM_EMAIL=$EMAIL
fi

[ "$lwrite" = true ] && echo bin/attribute $corrargs | sed -e 's@ data/@ /tmp/@g'
(./bin/attribute $corrargs > $root.txt) 2>&1
grep 'bootstrap' $root.txt | sed -e 's/#//'
echo '<table class="realtable" width="100%" border=0 cellpadding=0 cellspacing=0>'
if [ "$TYPE" = gridpoints -o $TYPE = field ]; then
    f=$file
elif [ "$TYPE" = set ]; then
    i=0
    while [ -z "$f" -a $i -lt 100 ]; do
        i=$((i+1))
        if [ -z "$FORM_extraargs" ]; then
            # watch out, two extraarg names end with an "n" also...
            f=`ls -t ./data/${NAME}*[0-9ni].dat | egrep -v '_mean|_min' | head -1`
        else
            f=`ls -t ./data/${NAME}*_$FORM_extraargs.dat | head -1`
        fi
        if [ ! -s $f ]; then
            rm -f $f ${f%.dat}.nc
            f=""
        fi
    done
else
    f=./data/$TYPE$WMO.dat
fi
if [ "$lwrite" = true ]; then
    echo "NPERYEAR2=$NPERYEAR<br>"
    echo "./data/${NAME}[^_]*[0-9ni].dat<br>"
    echo "f=$f<br>"
    ./bin/getunits $f
fi
if [ $NPERYEAR -gt 12 ]; then
	eval `./bin/getunits.sh $f`
else
	eval `./bin/getunits $f`
fi
. ./month2string.cgi
. ./setyaxis.cgi

echo "<tr><th colspan="4">$seriesmonth $station $VAR [$UNITS] dependent on $covstation</th></tr>"
tail -n +2 "$root.txt" | grep '<tr>' | sed -e 's/# //'
echo '</table>'
[ "$lwrite" = true ] && wc -l $root.txt|awk '{print $1}'
c=`wc -l $root.txt|awk '{print $1}'`
[ "$lwrite" = true ] && echo "c=$c<p>"
if [ $c -lt 20 ]; then
	echo "<p>Something went wrong, c=$c"
	echo 'Please send <a href="mailto:mailto:oldenborgh@knmi.nl">me</a> the following command and I will try to fix it.<p>'
	echo bin/attribute $corrargs | sed -e 's@data/attribute@/tmp/attribute@g'
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
	title=`echo "$title" | tr '_' ' '`

	cat <<EOF > $root.gnuplot
$gnuplot_init
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
	./bin/gnuplot < $root.gnuplot
fi

if [ $FORM_plot = "gumbel" -o $FORM_plot = "log" -o $FORM_plot = "sqrtlog" ]; then
    if [ -n "$FORM_normsd" -a \( -n "$ENSEMBLE" -o "$TYPE" = set \) ]; then
	    title="$seriesmonth $CLIM normalised $station"
    else
	    title="$seriesmonth $CLIM $station"
	fi
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
	title=`echo "$title" | tr '_' ' '`

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
		plus="-"
	else
		bottomtop=bottom
		plus="+"
	fi
	if [ -n "$FORM_year" ]; then
	    if [ $FORM_timeseries != none ]; then
    		plotformyear=", \"$root.txt\" index 2 u 2:4 title \"observed $FORM_year\" w lines lt 4" 
        else
    		plotformyear=", \"$root.txt\" index 1 u 2:4 title \"observed $FORM_year\" w lines lt 4" 
    	fi
	else
		plotformyear=""
	fi
	fittext=$FORM_fit
	if [ $FORM_fit = gpd ]; then
	    fittext="$fittext >${FORM_dgt}"
	fi
	
	if [ -s $obsplotfile -a "$FORM_timeseries" != 'none' ]; then
	    if [ "$covstation" = "time" ]; then
	        covstation="year"
	        x="(\$1+2000)"
	    else
	        x=1
	    fi
    	cat > ${root}_obsplot.gnuplot << EOF
$gnuplot_init
set size 0.7,0.5
set term png $gnuplot_png_font_hires
set output "${root}_obsplot.png"
set title "$title"
set xlabel "$covstation"
set ylabel "$ylabel"
set datafile missing '-999.900'
set yrange [${FORM_ylo}:${FORM_yhi}]
plot \
"$obsplotfile" index 0 using $x:2 notitle with points lt 3,\\
"$obsplotfile" index 1 using $x:2 notitle with points lt 4,\\
"$obsplotfile" index 2 using $x:2 notitle with line lt 1 lw 3,\\
"$obsplotfile" index 3 using $x:2:3:4 notitle with errorbars lt 1 lw 3,\\
"$obsplotfile" index 2 using $x:(\$2+\$3) notitle with line lt 1,\\
"$obsplotfile" index 2 using $x:(\$2+2*\$3) notitle with line lt 1
set term postscript epsf color solid
set output "${root}_obsplot.eps"
replot
quit
EOF
        [ "$covstation" = year ] && covstation=time
	    if [ "$lwrite" = true ]; then
		    echo '<pre>'
		    cat ${root}_obsplot.gnuplot
		    echo '</pre>'
	    fi
    	./bin/gnuplot < ${root}_obsplot.gnuplot 2>&1
	    if [ ! -s ${root}_obsplot.png ]; then
		    echo "Something went wrong while making the plot, cannot find ${root}_obsplot.png."
		    echo "The plot command are <a href=\"${root}_obsplot.gnuplot\">here</a>."
		    . ./myvinkfoot.cgi
		    exit
	    fi
        gzip -f ${root}_obsplot.eps
        pngfile=${root}_obsplot.png
        getpngwidth
        if [ $FORM_fit = gpd ]; then
            plotvariable=threshold
        elif [ $FORM_fit = gauss ]; then
            plotvariable="mean"
        else
            plotvariable="position parameter"
        fi
        echo "<div class=\"bijschrift\">Fitted points, value in $FORM_year,  $plotvariable &mu;, &mu;${plus}&sigma; and &mu;${plus}2&sigma;"
        echo "(<a href=\"${root}_obsplot.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${root}_obsplot.eps.gz\">pdf</a>, <a href=\"${obsplotfile}\">raw data</a>, <a href=\"${root}_obsplot.gnuplot\">plot script</a>)</div>"
        echo "<center><img src=\"${root}_obsplot.png\" alt=\"$FORM_which\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"
    fi

    if [ $FORM_timeseries != none ]; then
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
set yrange [${FORM_ylo}:${FORM_yhi}]
set term unknown
plot \\
"$root.txt" index 0 u 2:3 notitle with points lt 3,\\
"$root.txt" index 0 u 2:4 title "$fittext $FORM_assume fit $FORM_begin2" with line lt 3,\\
"$root.txt" index 1 u 2:3 notitle with points lt 1,\\
"$root.txt" index 1 u 2:4 title "$fittext $FORM_assume fit $FORM_year" with line lt 1$plotformyear
set yrange [GPVAL_Y_MIN:GPVAL_Y_MAX]
set y2range [GPVAL_Y_MIN:GPVAL_Y_MAX]
set term png $gnuplot_png_font_hires
set output "${root}.png"
plot \\
"$root.txt" index 0 u 2:3 notitle with points lt 3,\\
"$root.txt" index 0 u 2:4 title "$fittext $FORM_assume fit $FORM_begin2" with line lt 3,\\
"$root.txt" index 1 u 2:3 notitle with points lt 1,\\
"$root.txt" index 1 u 2:4 title "$fittext $FORM_assume fit $FORM_year" with line lt 1$plotformyear
set term postscript epsf color solid
set output "${root}.eps"
replot
quit
EOF
    else
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
set yrange [${FORM_ylo}:${FORM_yhi}]
set term unknown
plot \\
"$root.txt" index 0 u 2:3 notitle with points lt 1,\\
"$root.txt" index 0 u 2:4 title "$fittext fit" with line lt 1
set yrange [GPVAL_Y_MIN:GPVAL_Y_MAX]
set y2range [GPVAL_Y_MIN:GPVAL_Y_MAX]
set term png $gnuplot_png_font_hires
set output "${root}.png"
plot \\
"$root.txt" index 0 u 2:3 notitle with points lt 1,\\
"$root.txt" index 0 u 2:4 title "$fittext fit" with line lt 1$plotformyear
set term postscript epsf color solid
set output "${root}.eps"
replot
quit
EOF
    fi # none
	if [ "$lwrite" = true ]; then
		echo '<pre>'
		cat $root.gnuplot
		echo '</pre>'
	fi
	./bin/gnuplot < $root.gnuplot 2>&1 | fgrep -v "'unknown' terminal" | fgrep -v 'select a terminal' 
	# the filtering is necessary since gnuplot 5, I could not yet find another way 
	# to plot nowhere
	if [ ! -s ${root}.png ]; then
		echo "Something went wrong while making the plot."
		echo "The plot commands are <a href=\"$root.gnuplot\">here</a>."
		. ./myvinkfoot.cgi
		exit
	fi
fi

gzip -f $root.eps
pngfile=${root}.png
getpngwidth
echo "<div class=\"bijschrift\">$title"
if [ $FORM_timeseries != none ]; then
    times=times
    if [ $FORM_assume = 'shift' ]; then
        echo "with the effects of $covstation linearly subtracted from the position parameter &mu;,"
    elif [ $FORM_assume = 'scale' ]; then
        echo "with the effects of $covstation scaling the position and scale parameters parameter &mu;,&sigma;, "
    elif [ $FORM_assume = 'both' ]; then
        echo "with the effects of $covstation linearly subtracted from the position parameter &mu; and independently from the scale parameter &sigma;,"
    else
        echo "using an unknown assumption,"
    fi
    if [ $FORM_assume = 'scale' -a -n "$FORM_anomal" ]; then
        echo "It does not make sense to assume that he distribution scales with $covstation when taking anomalies"
        . ./myvinkfoot.cgi
        exit
    fi
    echo "referenced at $FORM_begin2 and $FORM_year"
else
    times=time
fi
echo "(<a href=\"${root}.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${root}.eps.gz\">pdf</a>, <a href=\"$root.txt\">raw data</a>, <a href=\"$root.gnuplot\">plot script</a>)</div>"
echo "<center><img src=\"${root}.png\" alt=\"$FORM_which\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

cat > ${root}_cdf.gnuplot << EOF
$gnuplot_init
set size 0.7,0.4
set term png $gnuplot_png_font_hires
set output "${root}_cdf.png"
set title "CDF of return $times"
set xlabel "return period [yr]"
set ylabel "CDF"
set datafile missing '-999.900'
set key $bottomtop
$xtics
set xrange [${xlo}:${xhi}]
set yrange [0:1]
set ytics (0,0.1,0.25,0.5,0.75,0.9,1)
EOF
if [ $FORM_timeseries != none ]; then
    cat >> ${root}_cdf.gnuplot << EOF
plot "$probfile" u 5:1 title "in climate $FORM_begin2" with lines lt 3, "$probfile" index 0 u 6:1 title "in climate $FORM_year" with lines lt 1
EOF
else
    cat >> ${root}_cdf.gnuplot << EOF
plot "$probfile" index 0 u 6:1 notitle with lines lt 1
EOF
fi
cat >> ${root}_cdf.gnuplot << EOF
set term postscript epsf color solid
set output "${root}_cdf.eps"
replot
quit
EOF
if [ "$lwrite" = true ]; then
    echo '<pre>'
    cat ${root}_cdf.gnuplot
    echo '</pre>'
fi
./bin/gnuplot < ${root}_cdf.gnuplot 2>&1
if [ ! -s ${root}_cdf.png ]; then
    echo "Something went wrong while making the plot."
    echo "The plot commands are <a href=\"${root}_cdf.gnuplot\">here</a>."
    . ./myvinkfoot.cgi
    exit
fi
gzip -f ${root}_cdf.eps
pngfile=${root}_cdf.png
getpngwidth
echo "<div class=\"bijschrift\">CDF of the return time"
if [ $FORM_timeseries != none ]; then
    echo "of $FORM_year $title in the climates of $FORM_year and of $FORM_begin2"
fi
echo "(<a href=\"${root}_cdf.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${root}_cdf.eps.gz\">pdf</a>, <a href=\"$probfile\">raw data</a>, <a href=\"${root}_cdf.gnuplot\">plot script</a>)</div>"
echo "<center><img src=\"${root}_cdf.png\" alt=\"CDF of the return time of $FORM_year\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

if [ "$FORM_timeseries" = none ]; then
    . ./myvinkfoot.cgi
    exit
fi

###xtics=`fgrep '#@' $probfile | sed -e 's/^#@ //'`
cat > ${root}_cdfdiff.gnuplot << EOF
$gnuplot_init
set size 0.7,0.4
set term png $gnuplot_png_font_hires
set output "${root}_cdfdiff.png"
set title "ratio of return times in climates of $FORM_begin2 and $FORM_year"
set xlabel "ratio [1]"
set ylabel "CDF"
set datafile missing '-999.900'
set key $bottomtop
set logscale x
set xrange [0.001:1000]
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
./bin/gnuplot < ${root}_cdfdiff.gnuplot 2>&1
if [ ! -s ${root}_cdfdiff.png ]; then
    echo "Something went wrong while making the plot."
    echo "The plot commands are <a href=\"${root}_cdfdiff.gnuplot\">here</a>."
    . ./myvinkfoot.cgi
    exit
fi
gzip -f ${root}_cdfdiff.eps
pngfile=${root}_cdfdiff.png
getpngwidth
echo "<div class=\"bijschrift\">CDF of the ratio of the return times of $FORM_year $title in the climates of $FORM_year and of $FORM_begin2 (<a href=\"${root}_cdfdiff.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${root}_cdfdiff.eps.gz\">pdf</a>, <a href=\"$probfile\">raw data</a>, <a href=\"${root}_cdfdiff.gnuplot\">plot script</a>)</div>"
echo "<center><img src=\"${root}_cdfdiff.png\" alt=\"CDF of the difference in return times of $FORM_year and $FORM_begin2\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

# FAR plot

cat > ${root}_far.gnuplot << EOF
$gnuplot_init
set size 0.7,0.4
set term png $gnuplot_png_font_hires
set output "${root}_far.png"
set title "FAR due to the trend from $FORM_begin2 to $FORM_year"
set xlabel "FAR"
set ylabel "CDF"
set datafile missing '-999.900'
set key $bottomtop
set xrange [-0.5:1]
set yrange [0:1]
set ytics (0,0.1,0.25,0.5,0.75,0.9,1)
plot "$probfile" u (1-1/\$4):1 notitle with lines lt 1
set term postscript epsf color solid
set output "${root}_far.eps"
replot
quit
EOF
if [ "$lwrite" = true ]; then
    echo '<pre>'
    cat /tmp/far$$.gnuplot
    echo '</pre>'
fi
./bin/gnuplot < ${root}_far.gnuplot 2>&1
if [ ! -s ${root}_far.png ]; then
    echo "Something went wrong while making the plot."
    echo "The plot commands are <a href=\"${root}_far.gnuplot\">here</a>."
    . ./myvinkfoot.cgi
    exit
fi
gzip -f ${root}_far.eps
pngfile=${root}_far.png
getpngwidth
echo "<div class=\"bijschrift\">Fraction of Attributable Risk (FAR) of $FORM_year $title in the climate of $FORM_year due to the trend from $FORM_begin2 (<a href=\"${root}_far.eps.gz\">eps</a>, <a href=\"ps2pdf.cgi?file=${root}_far.eps.gz\">pdf</a>, <a href=\"$probfile\">raw data</a>, <a href=\"${root}_far.gnuplot\">plot script</a>)</div>"
echo "<center><img src=\"${root}_far.png\" alt=\"FAR due to the trend from $FORM_begin2 to $FORM_year\" width=\"$halfwidth\" border=0 class=\"realimage\" hspace=0 vspace=0></center>"

echo "<p>This is the Fraction of Attributable Risk (FAR) due to the trend. In order to interpret it as the FAR due to climate change a quantitative argument has to be added that connects the trend to anthropogenic factors, via a climate model or a scaling argument to a temperature trend that already has been attributed. The uncertainty estimate does not include the structural uncertainty in the statistical model due to the assumptions made on the previous page, so the true uncertainty is larger."

. ./myvinkfoot.cgi
